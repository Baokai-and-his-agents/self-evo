"""Signal layer: Donchian breakout, ATR stop, position-independent trade events.

Requirements:
- No lookahead: only use past bars
- Clear execution rules at next available price
- Generate immutable trade events (entry, exit, stop) independent of position sizing
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from enum import Enum

from .data import OHLCBar


class SignalType(Enum):
    """Trade signal types."""
    ENTRY_LONG = "entry_long"
    EXIT = "exit"
    STOP = "stop"


@dataclass(frozen=True)
class TradeEvent:
    """Position-independent trade event.

    Immutable record of when and why a trade action occurred.
    Sizing policies (A/B/E/G) consume the same event stream.

    For E policy confirmation support:
    - confirmation_timestamp: when confirmation signal occurred (if any)
    - confirmation_price: market price at confirmation
    - If confirmation exists, E must treat this as two phases:
      Phase 1: entry -> confirmation (probe sizing)
      Phase 2: confirmation -> exit (amplified sizing)
    """
    event_id: int
    timestamp: datetime
    signal_type: SignalType
    entry_price: float
    exit_price: Optional[float] = None
    stop_price: Optional[float] = None
    raw_r: Optional[float] = None  # Exit price / entry price - 1, before sizing
    hit_stop: bool = False
    bars_held: int = 0
    confirmation_timestamp: Optional[datetime] = None
    confirmation_price: Optional[float] = None

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "event_id": self.event_id,
            "timestamp": self.timestamp.isoformat(),
            "signal_type": self.signal_type.value,
            "entry_price": self.entry_price,
            "exit_price": self.exit_price,
            "stop_price": self.stop_price,
            "raw_r": self.raw_r,
            "hit_stop": self.hit_stop,
            "bars_held": self.bars_held,
            "confirmation_timestamp": self.confirmation_timestamp.isoformat() if self.confirmation_timestamp else None,
            "confirmation_price": self.confirmation_price
        }

    def has_confirmation(self) -> bool:
        """Check if this event has confirmation data for E policy."""
        return self.confirmation_timestamp is not None and self.confirmation_price is not None


class DonchianATRSignal:
    """Donchian breakout with ATR-based stop.

    Pre-registered parameters (not optimized):
    - Entry: 20-day high breakout
    - Exit: 10-day low
    - Stop: 2.0 * ATR(14)
    """

    def __init__(
        self,
        entry_period: int = 20,
        exit_period: int = 10,
        atr_period: int = 14,
        atr_stop_multiplier: float = 2.0
    ):
        """Initialize signal parameters.

        Args:
            entry_period: Donchian channel period for entry
            exit_period: Donchian channel period for exit
            atr_period: ATR calculation period
            atr_stop_multiplier: Stop distance in ATR multiples
        """
        self.entry_period = entry_period
        self.exit_period = exit_period
        self.atr_period = atr_period
        self.atr_stop_multiplier = atr_stop_multiplier

    def compute_donchian_high(self, bars: List[OHLCBar], index: int, period: int) -> Optional[float]:
        """Compute Donchian high using ONLY past bars.

        Args:
            bars: Full bar list
            index: Current bar index
            period: Lookback period

        Returns:
            Highest high in past 'period' bars, or None if insufficient data
        """
        if index < period:
            return None

        # Use bars [index - period : index], NOT including current bar
        past_bars = bars[index - period:index]
        return max(bar.high for bar in past_bars)

    def compute_donchian_low(self, bars: List[OHLCBar], index: int, period: int) -> Optional[float]:
        """Compute Donchian low using ONLY past bars."""
        if index < period:
            return None

        past_bars = bars[index - period:index]
        return min(bar.low for bar in past_bars)

    def compute_atr(self, bars: List[OHLCBar], index: int) -> Optional[float]:
        """Compute ATR using ONLY past bars.

        Uses simple moving average of True Range.
        """
        if index < self.atr_period + 1:
            return None

        true_ranges = []
        for i in range(index - self.atr_period, index):
            prev_close = bars[i - 1].close if i > 0 else None
            tr = bars[i].true_range(prev_close)
            true_ranges.append(tr)

        return sum(true_ranges) / len(true_ranges)

    def generate_trade_events(self, bars: List[OHLCBar], detect_confirmation: bool = True, confirmation_r_threshold: float = 3.0) -> List[TradeEvent]:
        """Generate position-independent trade events from OHLC data.

        Execution rules:
        - Entry signal on day N triggers entry at day N+1 open
        - Exit signal on day N triggers exit at day N+1 open
        - Stop checked intrabar: if low <= stop, exit at stop price (same bar)

        Confirmation detection (for E policy):
        - If during the trade, high reaches entry_price * (1 + confirmation_r_threshold * stop_distance / entry_price)
        - Record confirmation_timestamp and confirmation_price
        - This is independent of stop_count sequence

        Args:
            bars: OHLC bar data
            detect_confirmation: Whether to detect confirmation signals (default True)
            confirmation_r_threshold: R-multiple threshold for confirmation (default 3.0)

        Returns:
            List of complete trade events (entry + exit pairs)
        """
        events = []
        in_position = False
        entry_bar_index = -1
        entry_price = 0.0
        stop_price = 0.0
        event_id = 0
        confirmation_timestamp = None
        confirmation_price = None

        for i in range(len(bars)):
            bar = bars[i]

            # Skip until we have enough data for all indicators
            if i < max(self.entry_period, self.exit_period, self.atr_period + 1):
                continue

            if not in_position:
                # Check for entry signal
                donchian_high = self.compute_donchian_high(bars, i, self.entry_period)

                if donchian_high is None:
                    continue

                # Entry signal: current close breaks above Donchian high
                if bar.close > donchian_high:
                    # Entry at next bar open
                    if i + 1 < len(bars):
                        in_position = True
                        entry_bar_index = i + 1
                        entry_price = bars[i + 1].open
                        confirmation_timestamp = None
                        confirmation_price = None

                        # Compute stop: entry - ATR_multiplier * ATR
                        atr = self.compute_atr(bars, i + 1)
                        if atr is None:
                            # Fallback if ATR not available
                            atr = (bar.high - bar.low) * 0.5

                        stop_price = entry_price - self.atr_stop_multiplier * atr

            else:
                # In position: check for confirmation, exit or stop
                bars_held = i - entry_bar_index

                # Check stop first (intrabar priority)
                if bar.low <= stop_price:
                    # Hit stop - exit immediately, do not record confirmation for this bar
                    exit_price = stop_price
                    raw_r = (exit_price / entry_price) - 1.0

                    event = TradeEvent(
                        event_id=event_id,
                        timestamp=bars[entry_bar_index].timestamp,
                        signal_type=SignalType.ENTRY_LONG,
                        entry_price=entry_price,
                        exit_price=exit_price,
                        stop_price=stop_price,
                        raw_r=raw_r,
                        hit_stop=True,
                        bars_held=bars_held,
                        confirmation_timestamp=confirmation_timestamp,  # Keep existing confirmation if any
                        confirmation_price=confirmation_price
                    )
                    events.append(event)
                    event_id += 1

                    in_position = False
                    continue

                # Only check for confirmation if stop was not hit
                if detect_confirmation and confirmation_timestamp is None:
                    stop_distance = entry_price - stop_price
                    confirmation_target = entry_price + confirmation_r_threshold * stop_distance

                    if bar.high >= confirmation_target:
                        confirmation_timestamp = bar.timestamp
                        confirmation_price = confirmation_target  # Use target price as confirmation price

                # Check exit signal
                donchian_low = self.compute_donchian_low(bars, i, self.exit_period)

                if donchian_low is not None and bar.close < donchian_low:
                    # Exit signal at next bar open
                    if i + 1 < len(bars):
                        exit_price = bars[i + 1].open
                        raw_r = (exit_price / entry_price) - 1.0

                        event = TradeEvent(
                            event_id=event_id,
                            timestamp=bars[entry_bar_index].timestamp,
                            signal_type=SignalType.ENTRY_LONG,
                            entry_price=entry_price,
                            exit_price=exit_price,
                            stop_price=stop_price,
                            raw_r=raw_r,
                            hit_stop=False,
                            bars_held=bars_held + 1,
                            confirmation_timestamp=confirmation_timestamp,
                            confirmation_price=confirmation_price
                        )
                        events.append(event)
                        event_id += 1

                        in_position = False

        # Close any open position at last bar
        if in_position and len(bars) > 0:
            exit_price = bars[-1].close
            raw_r = (exit_price / entry_price) - 1.0
            bars_held = len(bars) - 1 - entry_bar_index

            event = TradeEvent(
                event_id=event_id,
                timestamp=bars[entry_bar_index].timestamp,
                signal_type=SignalType.ENTRY_LONG,
                entry_price=entry_price,
                exit_price=exit_price,
                stop_price=stop_price,
                raw_r=raw_r,
                hit_stop=False,
                bars_held=bars_held,
                confirmation_timestamp=confirmation_timestamp,
                confirmation_price=confirmation_price
            )
            events.append(event)

        return events


def compute_atr_for_bar(bars: List[OHLCBar], index: int, period: int = 14) -> Optional[float]:
    """Standalone ATR computation for position sizing.

    Args:
        bars: Full bar list
        index: Current bar index
        period: ATR period

    Returns:
        ATR value or None if insufficient data
    """
    if index < period + 1:
        return None

    true_ranges = []
    for i in range(index - period, index):
        prev_close = bars[i - 1].close if i > 0 else None
        tr = bars[i].true_range(prev_close)
        true_ranges.append(tr)

    return sum(true_ranges) / len(true_ranges)

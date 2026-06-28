"""Deterministic trade event fixtures for testing.

These fixtures provide hand-crafted trade events with known outcomes
to verify business logic correctness.
"""

from datetime import datetime, timedelta
from typing import List
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from fx_backtest.signals import TradeEvent, SignalType


def create_fixture_consecutive_losses(num_losses: int, start_date: datetime = None) -> List[TradeEvent]:
    """Create fixture with consecutive stop losses.

    Args:
        num_losses: Number of consecutive losses (0..K range)
        start_date: Starting date for events

    Returns:
        List of trade events, all hitting stops
    """
    if start_date is None:
        start_date = datetime(2020, 1, 1)

    events = []
    entry_price = 1.1000
    stop_distance = 0.0020  # 20 pips

    for i in range(num_losses):
        event = TradeEvent(
            event_id=i,
            timestamp=start_date + timedelta(days=i),
            signal_type=SignalType.ENTRY_LONG,
            entry_price=entry_price,
            exit_price=entry_price - stop_distance,  # Hit stop
            stop_price=entry_price - stop_distance,
            raw_r=-stop_distance / entry_price,
            hit_stop=True,
            bars_held=1
        )
        events.append(event)

    return events


def create_fixture_cycle_failure_and_continue(K: int = 5) -> List[TradeEvent]:
    """Create fixture demonstrating cycle failure followed by continuation.

    Sequence:
    - K consecutive losses (triggers reset)
    - 1 win (confirms continuation after reset)
    - 2 more losses
    - 1 win

    Args:
        K: Max stop count before reset

    Returns:
        List of trade events
    """
    events = []
    start_date = datetime(2020, 1, 1)
    entry_price = 1.1000
    stop_distance = 0.0020

    event_id = 0

    # K consecutive losses
    for i in range(K):
        event = TradeEvent(
            event_id=event_id,
            timestamp=start_date + timedelta(days=event_id),
            signal_type=SignalType.ENTRY_LONG,
            entry_price=entry_price,
            exit_price=entry_price - stop_distance,
            stop_price=entry_price - stop_distance,
            raw_r=-stop_distance / entry_price,
            hit_stop=True,
            bars_held=1
        )
        events.append(event)
        event_id += 1

    # Win after reset
    win_event = TradeEvent(
        event_id=event_id,
        timestamp=start_date + timedelta(days=event_id),
        signal_type=SignalType.ENTRY_LONG,
        entry_price=entry_price,
        exit_price=entry_price + stop_distance * 2,  # 2R win
        stop_price=entry_price - stop_distance,
        raw_r=(stop_distance * 2) / entry_price,
        hit_stop=False,
        bars_held=3
    )
    events.append(win_event)
    event_id += 1

    # 2 more losses
    for i in range(2):
        event = TradeEvent(
            event_id=event_id,
            timestamp=start_date + timedelta(days=event_id),
            signal_type=SignalType.ENTRY_LONG,
            entry_price=entry_price,
            exit_price=entry_price - stop_distance,
            stop_price=entry_price - stop_distance,
            raw_r=-stop_distance / entry_price,
            hit_stop=True,
            bars_held=1
        )
        events.append(event)
        event_id += 1

    # Final win
    final_win = TradeEvent(
        event_id=event_id,
        timestamp=start_date + timedelta(days=event_id),
        signal_type=SignalType.ENTRY_LONG,
        entry_price=entry_price,
        exit_price=entry_price + stop_distance * 3,  # 3R win
        stop_price=entry_price - stop_distance,
        raw_r=(stop_distance * 3) / entry_price,
        hit_stop=False,
        bars_held=5
    )
    events.append(final_win)
    event_id += 1

    # A third cycle creates repeated stop-count states across the event stream.
    for _ in range(3):
        events.append(TradeEvent(
            event_id=event_id,
            timestamp=start_date + timedelta(days=event_id),
            signal_type=SignalType.ENTRY_LONG,
            entry_price=entry_price,
            exit_price=entry_price - stop_distance,
            stop_price=entry_price - stop_distance,
            raw_r=-stop_distance / entry_price,
            hit_stop=True,
            bars_held=1
        ))
        event_id += 1

    events.append(TradeEvent(
        event_id=event_id,
        timestamp=start_date + timedelta(days=event_id),
        signal_type=SignalType.ENTRY_LONG,
        entry_price=entry_price,
        exit_price=entry_price + stop_distance * 2,
        stop_price=entry_price - stop_distance,
        raw_r=(stop_distance * 2) / entry_price,
        hit_stop=False,
        bars_held=4
    ))

    return events


def create_fixture_e_confirmation() -> List[TradeEvent]:
    """Create fixture with E policy confirmation event.

    Sequence:
    - Event without confirmation (probe only)
    - Event WITH confirmation at 3R (probe -> amplified)
    - Event without confirmation

    Returns:
        List of trade events
    """
    events = []
    start_date = datetime(2020, 1, 1)
    entry_price = 1.1000
    stop_distance = 0.0020

    # Trade 1: No confirmation, small win
    events.append(TradeEvent(
        event_id=0,
        timestamp=start_date,
        signal_type=SignalType.ENTRY_LONG,
        entry_price=entry_price,
        exit_price=entry_price + stop_distance * 1.5,  # 1.5R (below confirmation threshold)
        stop_price=entry_price - stop_distance,
        raw_r=(stop_distance * 1.5) / entry_price,
        hit_stop=False,
        bars_held=2,
        confirmation_timestamp=None,
        confirmation_price=None
    ))

    # Trade 2: WITH confirmation at 3R target
    confirmation_price = entry_price + stop_distance * 3.0
    events.append(TradeEvent(
        event_id=1,
        timestamp=start_date + timedelta(days=1),
        signal_type=SignalType.ENTRY_LONG,
        entry_price=entry_price,
        exit_price=entry_price + stop_distance * 5.0,  # Final exit at 5R
        stop_price=entry_price - stop_distance,
        raw_r=(stop_distance * 5.0) / entry_price,
        hit_stop=False,
        bars_held=10,
        confirmation_timestamp=start_date + timedelta(days=1, hours=6),
        confirmation_price=confirmation_price
    ))

    # Trade 3: No confirmation, loss
    events.append(TradeEvent(
        event_id=2,
        timestamp=start_date + timedelta(days=2),
        signal_type=SignalType.ENTRY_LONG,
        entry_price=entry_price,
        exit_price=entry_price - stop_distance,
        stop_price=entry_price - stop_distance,
        raw_r=-stop_distance / entry_price,
        hit_stop=True,
        bars_held=1,
        confirmation_timestamp=None,
        confirmation_price=None
    ))

    return events


def create_fixture_gap_beyond_stop() -> List[TradeEvent]:
    """Create fixture with gap that exceeds stop distance.

    Returns:
        List with one event where exit is worse than stop due to gap
    """
    entry_price = 1.1000
    stop_distance = 0.0020
    gap_slippage = 0.0010  # Additional 10 pips beyond stop

    event = TradeEvent(
        event_id=0,
        timestamp=datetime(2020, 1, 1),
        signal_type=SignalType.ENTRY_LONG,
        entry_price=entry_price,
        exit_price=entry_price - stop_distance - gap_slippage,  # Worse than stop
        stop_price=entry_price - stop_distance,
        raw_r=-(stop_distance + gap_slippage) / entry_price,
        hit_stop=True,
        bars_held=1
    )

    return [event]


def create_fixture_zero_and_nonzero_cost() -> List[TradeEvent]:
    """Create simple fixture for cost model testing.

    Two trades with known parameters suitable for hand calculation:
    - 1R loss
    - 2R win

    Returns:
        List of trade events
    """
    entry_price = 1.1000
    stop_distance = 0.0020

    events = [
        TradeEvent(
            event_id=0,
            timestamp=datetime(2020, 1, 1),
            signal_type=SignalType.ENTRY_LONG,
            entry_price=entry_price,
            exit_price=entry_price - stop_distance,
            stop_price=entry_price - stop_distance,
            raw_r=-stop_distance / entry_price,
            hit_stop=True,
            bars_held=1
        ),
        TradeEvent(
            event_id=1,
            timestamp=datetime(2020, 1, 2),
            signal_type=SignalType.ENTRY_LONG,
            entry_price=entry_price,
            exit_price=entry_price + stop_distance * 2,
            stop_price=entry_price - stop_distance,
            raw_r=(stop_distance * 2) / entry_price,
            hit_stop=False,
            bars_held=3
        )
    ]

    return events

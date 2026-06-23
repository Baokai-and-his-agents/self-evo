"""Tests for signal layer: Donchian, ATR, lookahead prevention."""

import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from fx_backtest.data import OHLCBar, SyntheticDataGenerator
from fx_backtest.signals import DonchianATRSignal, compute_atr_for_bar


def test_donchian_no_lookahead():
    """Test that Donchian only uses past bars."""
    print("Testing Donchian no lookahead...")

    bars = SyntheticDataGenerator.generate_trend_and_consolidation(
        start_date=datetime(2020, 1, 1),
        num_days=50,
        seed=42
    )

    signal = DonchianATRSignal(entry_period=20, exit_period=10, atr_period=14)

    # At index 25, compute Donchian high
    donchian_high = signal.compute_donchian_high(bars, 25, 20)

    # Should use bars [5:25], NOT including bar 25
    expected_high = max(bar.high for bar in bars[5:25])
    assert donchian_high == expected_high

    # Should NOT include current bar
    assert donchian_high <= bars[25].high or donchian_high == bars[25].high

    print("[PASS] Donchian no lookahead tests passed")


def test_atr_no_lookahead():
    """Test that ATR only uses past bars."""
    print("Testing ATR no lookahead...")

    bars = SyntheticDataGenerator.generate_trend_and_consolidation(
        start_date=datetime(2020, 1, 1),
        num_days=50,
        seed=42
    )

    signal = DonchianATRSignal(atr_period=14)

    # At index 20, compute ATR
    atr = signal.compute_atr(bars, 20)

    # Should use bars [6:20], NOT including bar 20
    assert atr is not None

    # Manual calculation
    true_ranges = []
    for i in range(6, 20):
        prev_close = bars[i-1].close
        tr = bars[i].true_range(prev_close)
        true_ranges.append(tr)

    expected_atr = sum(true_ranges) / len(true_ranges)
    assert abs(atr - expected_atr) < 1e-6

    print("[PASS] ATR no lookahead tests passed")


def test_trade_event_generation():
    """Test trade event generation."""
    print("Testing trade event generation...")

    bars = SyntheticDataGenerator.generate_trend_and_consolidation(
        start_date=datetime(2020, 1, 1),
        num_days=300,
        seed=42
    )

    signal = DonchianATRSignal(entry_period=20, exit_period=10, atr_period=14)
    events = signal.generate_trade_events(bars)

    assert len(events) > 0, "Should generate at least one event"

    # Check event properties
    for event in events:
        assert event.entry_price > 0
        assert event.exit_price > 0
        assert event.stop_price > 0
        assert event.stop_price < event.entry_price  # Long trades
        assert event.raw_r is not None
        assert event.bars_held >= 0

    print(f"[PASS] Generated {len(events)} trade events")


def test_event_immutability():
    """Test that events are independent of sizing."""
    print("Testing event immutability...")

    bars = SyntheticDataGenerator.generate_trend_and_consolidation(
        start_date=datetime(2020, 1, 1),
        num_days=200,
        seed=42
    )

    signal = DonchianATRSignal()
    events1 = signal.generate_trade_events(bars)

    # Generate again
    signal2 = DonchianATRSignal()
    events2 = signal2.generate_trade_events(bars)

    # Should be identical
    assert len(events1) == len(events2)

    for e1, e2 in zip(events1, events2):
        assert e1.entry_price == e2.entry_price
        assert e1.exit_price == e2.exit_price
        assert e1.stop_price == e2.stop_price
        assert e1.raw_r == e2.raw_r
        assert e1.hit_stop == e2.hit_stop

    print("[PASS] Event immutability tests passed")


def test_stop_execution():
    """Test that stops execute at stop price, not worse."""
    print("Testing stop execution...")

    bars = SyntheticDataGenerator.generate_trend_and_consolidation(
        start_date=datetime(2020, 1, 1),
        num_days=300,
        seed=42
    )

    signal = DonchianATRSignal()
    events = signal.generate_trade_events(bars)

    stop_events = [e for e in events if e.hit_stop]

    if stop_events:
        for event in stop_events:
            # Exit should be at stop price (simplified model)
            assert event.exit_price == event.stop_price
            # Should be a loss
            assert event.raw_r < 0

        print(f"[PASS] Verified {len(stop_events)} stop executions")
    else:
        print("  Note: No stop events in this dataset")


if __name__ == '__main__':
    test_donchian_no_lookahead()
    test_atr_no_lookahead()
    test_trade_event_generation()
    test_event_immutability()
    test_stop_execution()
    print("\n[PASS] All signal layer tests passed")

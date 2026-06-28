"""Tests for data layer: OHLC validation, CSV loading, synthetic generation."""

import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from fx_backtest.data import OHLCBar, OHLCDataLoader, SyntheticDataGenerator


def test_ohlc_validation():
    """Test OHLC bar validation."""
    print("Testing OHLC validation...")

    # Valid bar
    bar = OHLCBar(
        timestamp=datetime(2020, 1, 1),
        open=1.1000,
        high=1.1050,
        low=1.0950,
        close=1.1020
    )
    assert bar.low <= bar.open <= bar.high
    assert bar.low <= bar.close <= bar.high

    # Invalid: open outside range
    try:
        invalid = OHLCBar(
            timestamp=datetime(2020, 1, 1),
            open=1.1100,  # > high
            high=1.1050,
            low=1.0950,
            close=1.1020
        )
        assert False, "Should have raised ValueError"
    except ValueError:
        pass

    # Invalid: low > high
    try:
        invalid = OHLCBar(
            timestamp=datetime(2020, 1, 1),
            open=1.1000,
            high=1.0950,
            low=1.1050,  # > high
            close=1.1020
        )
        assert False, "Should have raised ValueError"
    except ValueError:
        pass

    print("[PASS] OHLC validation tests passed")


def test_true_range():
    """Test True Range calculation."""
    print("Testing True Range...")

    bar1 = OHLCBar(
        timestamp=datetime(2020, 1, 1),
        open=1.1000,
        high=1.1050,
        low=1.0950,
        close=1.1020
    )

    # Without previous close
    tr1 = bar1.true_range()
    assert tr1 == 1.1050 - 1.0950

    # With previous close
    prev_close = 1.0980
    tr2 = bar1.true_range(prev_close)
    # max(high-low, high-prev_close, prev_close-low)
    # = max(0.01, 0.007, 0.003) = 0.01
    assert abs(tr2 - 0.01) < 1e-6

    print("[PASS] True Range tests passed")


def test_synthetic_generation():
    """Test synthetic data generation."""
    print("Testing synthetic generation...")

    bars = SyntheticDataGenerator.generate_trend_and_consolidation(
        start_date=datetime(2020, 1, 1),
        num_days=100,
        initial_price=1.1000,
        seed=42
    )

    assert len(bars) == 100
    assert bars[0].timestamp == datetime(2020, 1, 1)
    assert bars[-1].timestamp == datetime(2020, 1, 1) + timedelta(days=99)

    # Check all bars are valid
    for bar in bars:
        assert bar.low <= bar.open <= bar.high
        assert bar.low <= bar.close <= bar.high

    # Deterministic: same seed produces same result
    bars2 = SyntheticDataGenerator.generate_trend_and_consolidation(
        start_date=datetime(2020, 1, 1),
        num_days=100,
        initial_price=1.1000,
        seed=42
    )

    assert len(bars2) == len(bars)
    for b1, b2 in zip(bars, bars2):
        assert b1.close == b2.close

    print("[PASS] Synthetic generation tests passed")


def test_csv_roundtrip():
    """Test CSV save and load."""
    print("Testing CSV roundtrip...")

    import tempfile

    bars_original = SyntheticDataGenerator.generate_trend_and_consolidation(
        start_date=datetime(2020, 1, 1),
        num_days=50,
        initial_price=1.1000,
        seed=123
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        csv_path = Path(tmpdir) / "test.csv"
        SyntheticDataGenerator.save_to_csv(bars_original, csv_path)

        bars_loaded = OHLCDataLoader.load_csv(csv_path, timestamp_format='%Y-%m-%d')

        assert len(bars_loaded) == len(bars_original)

        for orig, loaded in zip(bars_original, bars_loaded):
            assert orig.timestamp.date() == loaded.timestamp.date()
            assert abs(orig.open - loaded.open) < 1e-4
            assert abs(orig.close - loaded.close) < 1e-4

    print("[PASS] CSV roundtrip tests passed")


def test_data_validation():
    """Test data validation diagnostics."""
    print("Testing data validation...")

    bars = SyntheticDataGenerator.generate_trend_and_consolidation(
        start_date=datetime(2020, 1, 1),
        num_days=100,
        initial_price=1.1000,
        seed=42
    )

    validation = OHLCDataLoader.validate_data(bars)

    assert validation['valid'] == True
    assert validation['num_bars'] == 100
    assert 'start' in validation
    assert 'end' in validation

    # Empty data
    validation_empty = OHLCDataLoader.validate_data([])
    assert validation_empty['valid'] == False

    print("[PASS] Data validation tests passed")


if __name__ == '__main__':
    test_ohlc_validation()
    test_true_range()
    test_synthetic_generation()
    test_csv_roundtrip()
    test_data_validation()
    print("\n[PASS] All data layer tests passed")

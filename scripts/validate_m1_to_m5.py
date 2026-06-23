#!/usr/bin/env python3
"""
Aggregate HistData M1 bars to M5 and validate OHLC consistency.

Validates that M5 bars can be correctly reconstructed from M1 data:
- Open: First M1 open in 5-minute window
- High: Max of all M1 highs
- Low: Min of all M1 lows
- Close: Last M1 close

If M5 data is available from HistData, compares aggregated vs downloaded M5.

Usage:
    python scripts/validate_m1_to_m5.py state/download-cache/fx-backtest/histdata/raw/DAT_MT_EURUSD_M1_2005.csv
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime, timedelta
import csv


def parse_histdata_timestamp(date_str: str, time_str: str) -> datetime:
    """
    Parse HistData timestamp.

    Format: Date=YYYY.MM.DD, Time=HH:MM
    Timezone: EST (UTC-5) without DST
    """
    return datetime.strptime(f"{date_str} {time_str}", "%Y.%m.%d %H:%M")


def aggregate_m1_to_m5(m1_csv_path: Path):
    """
    Aggregate M1 bars to M5.

    Returns:
        List of M5 bars: [(timestamp, open, high, low, close), ...]
    """
    print(f"Reading M1 data from: {m1_csv_path}")

    m5_bars = []
    current_window = []
    window_start = None

    with open(m1_csv_path, 'r') as f:
        reader = csv.DictReader(f)

        for i, row in enumerate(reader):
            timestamp = parse_histdata_timestamp(row['Date'], row['Time'])

            # Determine M5 window start (floor to 5-minute boundary)
            m5_start = timestamp.replace(minute=(timestamp.minute // 5) * 5, second=0, microsecond=0)

            if window_start is None:
                window_start = m5_start

            # New M5 window?
            if m5_start != window_start:
                # Aggregate previous window
                if current_window:
                    m5_bar = aggregate_window(window_start, current_window)
                    m5_bars.append(m5_bar)

                # Start new window
                window_start = m5_start
                current_window = []

            # Add to current window
            bar = {
                'timestamp': timestamp,
                'open': float(row['Open']),
                'high': float(row['High']),
                'low': float(row['Low']),
                'close': float(row['Close']),
            }
            current_window.append(bar)

            if (i + 1) % 50000 == 0:
                print(f"  Processed {i + 1:,} M1 bars...")

        # Aggregate final window
        if current_window:
            m5_bar = aggregate_window(window_start, current_window)
            m5_bars.append(m5_bar)

    print(f"  Total M1 bars: {i + 1:,}")
    print(f"  Total M5 bars: {len(m5_bars):,}")

    return m5_bars


def aggregate_window(window_start: datetime, bars: list) -> tuple:
    """
    Aggregate M1 bars within a 5-minute window to one M5 bar.

    Returns:
        (timestamp, open, high, low, close, bar_count)
    """
    m5_open = bars[0]['open']
    m5_high = max(bar['high'] for bar in bars)
    m5_low = min(bar['low'] for bar in bars)
    m5_close = bars[-1]['close']

    return (window_start, m5_open, m5_high, m5_low, m5_close, len(bars))


def validate_ohlc_consistency(m5_bars: list):
    """
    Validate OHLC consistency for aggregated M5 bars.

    Checks:
    - High >= Open
    - High >= Close
    - Low <= Open
    - Low <= Close
    - High >= Low
    """
    print(f"\nValidating OHLC consistency for {len(m5_bars):,} M5 bars...")

    errors = []

    for i, (timestamp, open_price, high, low, close, bar_count) in enumerate(m5_bars):
        issues = []

        if high < open_price:
            issues.append(f"High ({high}) < Open ({open_price})")
        if high < close:
            issues.append(f"High ({high}) < Close ({close})")
        if low > open_price:
            issues.append(f"Low ({low}) > Open ({open_price})")
        if low > close:
            issues.append(f"Low ({low}) > Close ({close})")
        if high < low:
            issues.append(f"High ({high}) < Low ({low})")

        if issues:
            errors.append((timestamp, bar_count, issues))

    if errors:
        print(f"  ❌ Found {len(errors)} bars with OHLC inconsistencies:\n")
        for timestamp, bar_count, issues in errors[:10]:  # Show first 10
            print(f"    {timestamp} (from {bar_count} M1 bars):")
            for issue in issues:
                print(f"      - {issue}")

        if len(errors) > 10:
            print(f"    ... and {len(errors) - 10} more")

        return False
    else:
        print(f"  ✅ All {len(m5_bars):,} M5 bars have consistent OHLC")
        return True


def analyze_bar_counts(m5_bars: list):
    """
    Analyze M1 bar counts per M5 window.

    Expected: 5 bars per M5 window (no gaps)
    Reality: Varies due to gaps in M1 data
    """
    print(f"\nAnalyzing M1 bar counts per M5 window...")

    bar_counts = [bar_count for _, _, _, _, _, bar_count in m5_bars]

    from collections import Counter
    count_distribution = Counter(bar_counts)

    print(f"  M1 bars per M5 window distribution:")
    for count in sorted(count_distribution.keys()):
        freq = count_distribution[count]
        pct = 100.0 * freq / len(m5_bars)
        bar = '█' * int(pct / 2)
        print(f"    {count} bars: {freq:6,} ({pct:5.2f}%) {bar}")

    complete_windows = count_distribution[5]
    complete_pct = 100.0 * complete_windows / len(m5_bars)
    print(f"\n  Complete M5 windows (5 M1 bars): {complete_windows:,} ({complete_pct:.1f}%)")

    if complete_pct < 95.0:
        print(f"  ⚠️  Only {complete_pct:.1f}% of M5 windows are complete")
    else:
        print(f"  ✅ {complete_pct:.1f}% of M5 windows are complete")


def compare_with_m5_file(m5_aggregated: list, m5_file_path: Path, tolerance: float = 1e-6):
    """
    Compare aggregated M5 bars with downloaded M5 file (if available).

    Args:
        tolerance: Max absolute difference for price comparison
    """
    if not m5_file_path.exists():
        print(f"\nM5 file not found: {m5_file_path}")
        print(f"  Skipping comparison (aggregation validation only)")
        return

    print(f"\nComparing with downloaded M5 file: {m5_file_path}")

    # Load M5 file
    m5_downloaded = []
    with open(m5_file_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            timestamp = parse_histdata_timestamp(row['Date'], row['Time'])
            m5_downloaded.append((
                timestamp,
                float(row['Open']),
                float(row['High']),
                float(row['Low']),
                float(row['Close']),
            ))

    print(f"  Aggregated M5: {len(m5_aggregated):,} bars")
    print(f"  Downloaded M5: {len(m5_downloaded):,} bars")

    # Compare
    mismatches = []

    agg_dict = {ts: (o, h, l, c) for ts, o, h, l, c, _ in m5_aggregated}

    for ts, o_dl, h_dl, l_dl, c_dl in m5_downloaded:
        if ts not in agg_dict:
            mismatches.append((ts, "Missing in aggregated"))
            continue

        o_agg, h_agg, l_agg, c_agg = agg_dict[ts]

        issues = []
        if abs(o_agg - o_dl) > tolerance:
            issues.append(f"Open: agg={o_agg} vs dl={o_dl}")
        if abs(h_agg - h_dl) > tolerance:
            issues.append(f"High: agg={h_agg} vs dl={h_dl}")
        if abs(l_agg - l_dl) > tolerance:
            issues.append(f"Low: agg={l_agg} vs dl={l_dl}")
        if abs(c_agg - c_dl) > tolerance:
            issues.append(f"Close: agg={c_agg} vs dl={c_dl}")

        if issues:
            mismatches.append((ts, issues))

    if mismatches:
        print(f"  ❌ Found {len(mismatches)} mismatches:\n")
        for ts, issues in mismatches[:10]:
            print(f"    {ts}:")
            if isinstance(issues, str):
                print(f"      {issues}")
            else:
                for issue in issues:
                    print(f"      - {issue}")

        if len(mismatches) > 10:
            print(f"    ... and {len(mismatches) - 10} more")

        return False
    else:
        print(f"  ✅ All {len(m5_downloaded):,} M5 bars match aggregated data")
        return True


def main():
    parser = argparse.ArgumentParser(
        description="Validate M1 to M5 aggregation for HistData"
    )
    parser.add_argument(
        'm1_csv',
        type=Path,
        help='Path to M1 CSV file (e.g., DAT_MT_EURUSD_M1_2005.csv)',
    )
    parser.add_argument(
        '--m5-csv',
        type=Path,
        help='Path to M5 CSV file for comparison (optional)',
    )

    args = parser.parse_args()

    if not args.m1_csv.exists():
        print(f"ERROR: M1 file not found: {args.m1_csv}")
        sys.exit(1)

    print(f"HistData M1 → M5 Aggregation Validator\n")
    print(f"  M1 file: {args.m1_csv}")

    # Aggregate M1 to M5
    m5_bars = aggregate_m1_to_m5(args.m1_csv)

    # Validate OHLC consistency
    ohlc_valid = validate_ohlc_consistency(m5_bars)

    # Analyze bar counts
    analyze_bar_counts(m5_bars)

    # Compare with M5 file if available
    if args.m5_csv:
        m5_match = compare_with_m5_file(m5_bars, args.m5_csv)
    else:
        # Try to find M5 file automatically
        m5_auto = args.m1_csv.parent / args.m1_csv.name.replace('_M1_', '_M5_')
        if m5_auto.exists():
            m5_match = compare_with_m5_file(m5_bars, m5_auto)
        else:
            m5_match = None

    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)
    print(f"  OHLC consistency: {'✅ PASS' if ohlc_valid else '❌ FAIL'}")
    if m5_match is not None:
        print(f"  M5 comparison: {'✅ PASS' if m5_match else '❌ FAIL'}")
    else:
        print(f"  M5 comparison: ⏭️  SKIPPED (no M5 file)")
    print()

    sys.exit(0 if ohlc_valid and (m5_match is None or m5_match) else 1)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Aggregate HistData M1 bars to Daily OHLC using FX session day boundaries.

FX Trading Day: Sunday 17:00 EST → Friday 16:59 EST
- Sunday bars 17:00-23:59 EST → Monday session
- Saturday bars → discarded (off-market quotes)
- Sunday bars 00:00-16:59 EST → discarded (off-market quotes)

Usage:
    python scripts/aggregate_m1_to_daily.py state/download-cache/fx-backtest/histdata/raw/DAT_MT_EURUSD_M1_2005.csv
    python scripts/aggregate_m1_to_daily.py DAT_MT_EURUSD_M1_2005.csv --output eurusd_daily_2005.csv
    python scripts/aggregate_m1_to_daily.py DAT_MT_EURUSD_M1_2005.csv --format parquet
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime, time, timedelta, date
import csv
from collections import defaultdict


def parse_histdata_timestamp(date_str: str, time_str: str) -> datetime:
    """
    Parse HistData timestamp.

    Format: Date=YYYY.MM.DD, Time=HH:MM
    Timezone: EST (UTC-5) without DST
    """
    return datetime.strptime(f"{date_str} {time_str}", "%Y.%m.%d %H:%M")


def get_fx_session_day(timestamp: datetime) -> date:
    """
    Map EST timestamp to FX session day.

    FX trading week: Sunday 17:00 EST → Friday 16:59 EST

    Rules:
    - If time >= 17:00: session day = calendar date
    - If time < 17:00: session day = previous calendar date
    - Saturday bars → Friday session (will be discarded as off-market)
    - Sunday 00:00-16:59 → Saturday session (will be discarded)
    - Sunday 17:00-23:59 → Monday session (valid market open)

    Returns:
        date: FX session day (Monday-Friday for valid data)
    """
    if timestamp.time() >= time(17, 0):
        session_day = timestamp.date()
    else:
        session_day = timestamp.date() - timedelta(days=1)

    return session_day


def is_valid_fx_session_day(session_day: date) -> bool:
    """
    Check if session day is a valid FX trading day (Monday-Friday).

    Returns:
        bool: True if Monday-Friday, False if Saturday/Sunday
    """
    weekday = session_day.weekday()  # 0=Monday, 6=Sunday
    return 0 <= weekday <= 4  # Monday-Friday


def aggregate_m1_to_daily(m1_csv_path: Path, discard_weekend: bool = True):
    """
    Aggregate M1 bars to daily OHLC using FX session day boundaries.

    Args:
        m1_csv_path: Path to M1 CSV file
        discard_weekend: If True, discard bars mapping to weekend session days

    Returns:
        dict: {session_day: (open, high, low, close, bar_count, first_ts, last_ts)}
    """
    print(f"Reading M1 data from: {m1_csv_path}")

    daily_bars = defaultdict(list)
    weekend_bars_discarded = 0
    total_bars = 0

    with open(m1_csv_path, 'r') as f:
        reader = csv.DictReader(f)

        for i, row in enumerate(reader):
            total_bars += 1
            timestamp = parse_histdata_timestamp(row['Date'], row['Time'])

            # Map to FX session day
            session_day = get_fx_session_day(timestamp)

            # Discard weekend session days?
            if discard_weekend and not is_valid_fx_session_day(session_day):
                weekend_bars_discarded += 1
                continue

            # Store bar
            bar = {
                'timestamp': timestamp,
                'open': float(row['Open']),
                'high': float(row['High']),
                'low': float(row['Low']),
                'close': float(row['Close']),
            }
            daily_bars[session_day].append(bar)

            if (i + 1) % 50000 == 0:
                print(f"  Processed {i + 1:,} M1 bars...")

    print(f"  Total M1 bars: {total_bars:,}")
    print(f"  Weekend bars discarded: {weekend_bars_discarded:,} ({100.0 * weekend_bars_discarded / total_bars:.2f}%)")
    print(f"  Valid bars for aggregation: {total_bars - weekend_bars_discarded:,}")
    print(f"  Unique session days: {len(daily_bars):,}")

    # Aggregate each session day
    print(f"\nAggregating to daily OHLC...")

    daily_ohlc = {}

    for session_day in sorted(daily_bars.keys()):
        bars = daily_bars[session_day]

        if not bars:
            continue

        # Sort by timestamp (should already be sorted)
        bars = sorted(bars, key=lambda b: b['timestamp'])

        daily_open = bars[0]['open']
        daily_high = max(bar['high'] for bar in bars)
        daily_low = min(bar['low'] for bar in bars)
        daily_close = bars[-1]['close']

        first_ts = bars[0]['timestamp']
        last_ts = bars[-1]['timestamp']

        daily_ohlc[session_day] = {
            'open': daily_open,
            'high': daily_high,
            'low': daily_low,
            'close': daily_close,
            'bar_count': len(bars),
            'first_timestamp': first_ts,
            'last_timestamp': last_ts,
        }

    print(f"  Daily OHLC bars: {len(daily_ohlc):,}")

    return daily_ohlc


def validate_daily_ohlc(daily_ohlc: dict):
    """
    Validate daily OHLC consistency.

    Checks:
    - High >= Open, Close
    - Low <= Open, Close
    - High >= Low
    - All days are Monday-Friday
    """
    print(f"\nValidating daily OHLC consistency...")

    errors = []

    for session_day, ohlc in sorted(daily_ohlc.items()):
        o, h, l, c = ohlc['open'], ohlc['high'], ohlc['low'], ohlc['close']

        issues = []

        if h < o:
            issues.append(f"High ({h}) < Open ({o})")
        if h < c:
            issues.append(f"High ({h}) < Close ({c})")
        if l > o:
            issues.append(f"Low ({l}) > Open ({o})")
        if l > c:
            issues.append(f"Low ({l}) > Close ({c})")
        if h < l:
            issues.append(f"High ({h}) < Low ({l})")

        # Check weekday
        weekday = session_day.weekday()
        if not (0 <= weekday <= 4):
            issues.append(f"Invalid weekday: {session_day.strftime('%A')}")

        if issues:
            errors.append((session_day, ohlc['bar_count'], issues))

    if errors:
        print(f"  ❌ Found {len(errors)} days with issues:\n")
        for session_day, bar_count, issues in errors[:10]:
            print(f"    {session_day} ({bar_count} bars):")
            for issue in issues:
                print(f"      - {issue}")

        if len(errors) > 10:
            print(f"    ... and {len(errors) - 10} more")

        return False
    else:
        print(f"  ✅ All {len(daily_ohlc):,} daily bars have consistent OHLC")
        return True


def analyze_bar_counts(daily_ohlc: dict):
    """
    Analyze M1 bar counts per trading day.

    Expected: ~1440 bars/day (24 hours × 60 minutes)
    FX reality: ~1200 bars/day (5 days/week, 24/5 market)
    """
    print(f"\nAnalyzing M1 bar counts per trading day...")

    bar_counts = [ohlc['bar_count'] for ohlc in daily_ohlc.values()]

    min_bars = min(bar_counts)
    max_bars = max(bar_counts)
    avg_bars = sum(bar_counts) / len(bar_counts)

    print(f"  Min bars/day: {min_bars}")
    print(f"  Max bars/day: {max_bars}")
    print(f"  Avg bars/day: {avg_bars:.1f}")

    # Check for thin days (< 500 bars)
    thin_days = [(day, ohlc['bar_count']) for day, ohlc in daily_ohlc.items() if ohlc['bar_count'] < 500]

    if thin_days:
        print(f"\n  ⚠️  {len(thin_days)} thin days (< 500 bars):")
        for day, count in sorted(thin_days)[:10]:
            print(f"      {day}: {count} bars")
        if len(thin_days) > 10:
            print(f"      ... and {len(thin_days) - 10} more")
    else:
        print(f"\n  ✅ No thin days (all days >= 500 bars)")


def write_csv(daily_ohlc: dict, output_path: Path):
    """Write daily OHLC to CSV file."""
    print(f"\nWriting CSV to: {output_path}")

    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Date', 'Open', 'High', 'Low', 'Close', 'BarCount', 'FirstTime', 'LastTime'])

        for session_day in sorted(daily_ohlc.keys()):
            ohlc = daily_ohlc[session_day]
            writer.writerow([
                session_day.isoformat(),
                f"{ohlc['open']:.6f}",
                f"{ohlc['high']:.6f}",
                f"{ohlc['low']:.6f}",
                f"{ohlc['close']:.6f}",
                ohlc['bar_count'],
                ohlc['first_timestamp'].strftime('%H:%M'),
                ohlc['last_timestamp'].strftime('%H:%M'),
            ])

    print(f"  ✅ Written {len(daily_ohlc):,} daily bars")


def write_parquet(daily_ohlc: dict, output_path: Path):
    """Write daily OHLC to Parquet file."""
    try:
        import pandas as pd
    except ImportError:
        print("ERROR: pandas required for Parquet output")
        print("Install with: pip install pandas pyarrow")
        sys.exit(1)

    print(f"\nWriting Parquet to: {output_path}")

    rows = []
    for session_day in sorted(daily_ohlc.keys()):
        ohlc = daily_ohlc[session_day]
        rows.append({
            'date': session_day,
            'open': ohlc['open'],
            'high': ohlc['high'],
            'low': ohlc['low'],
            'close': ohlc['close'],
            'bar_count': ohlc['bar_count'],
        })

    df = pd.DataFrame(rows)
    df.to_parquet(output_path, index=False)

    print(f"  ✅ Written {len(daily_ohlc):,} daily bars")


def main():
    parser = argparse.ArgumentParser(
        description="Aggregate HistData M1 to Daily OHLC with FX session boundaries"
    )
    parser.add_argument(
        'm1_csv',
        type=Path,
        help='Path to M1 CSV file (e.g., DAT_MT_EURUSD_M1_2005.csv)',
    )
    parser.add_argument(
        '--output',
        type=Path,
        help='Output file path (default: auto-generated)',
    )
    parser.add_argument(
        '--format',
        choices=['csv', 'parquet'],
        default='csv',
        help='Output format (default: csv)',
    )
    parser.add_argument(
        '--keep-weekend',
        action='store_true',
        help='Keep weekend session days (default: discard)',
    )

    args = parser.parse_args()

    if not args.m1_csv.exists():
        print(f"ERROR: M1 file not found: {args.m1_csv}")
        sys.exit(1)

    # Auto-generate output path
    if args.output is None:
        base_name = args.m1_csv.stem.replace('_M1_', '_DAILY_')
        ext = '.parquet' if args.format == 'parquet' else '.csv'
        args.output = args.m1_csv.parent / f"{base_name}{ext}"

    print(f"HistData M1 → Daily OHLC Aggregator")
    print(f"  Session boundaries: Sunday 17:00 EST → Friday 16:59 EST")
    print(f"  Discard weekend: {not args.keep_weekend}")
    print()

    # Aggregate
    daily_ohlc = aggregate_m1_to_daily(args.m1_csv, discard_weekend=not args.keep_weekend)

    # Validate
    ohlc_valid = validate_daily_ohlc(daily_ohlc)

    # Analyze
    analyze_bar_counts(daily_ohlc)

    # Write output
    if args.format == 'csv':
        write_csv(daily_ohlc, args.output)
    else:
        write_parquet(daily_ohlc, args.output)

    print("\n" + "=" * 60)
    print("AGGREGATION SUMMARY")
    print("=" * 60)
    print(f"  OHLC consistency: {'✅ PASS' if ohlc_valid else '❌ FAIL'}")
    print(f"  Output file: {args.output}")
    print()

    sys.exit(0 if ohlc_valid else 1)


if __name__ == '__main__':
    main()

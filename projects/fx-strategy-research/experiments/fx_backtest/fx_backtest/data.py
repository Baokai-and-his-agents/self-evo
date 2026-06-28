"""Data layer: OHLC schema, CSV loader, validation, fixtures.

Requirements:
- Unified OHLC schema
- CSV loader (source-agnostic)
- Time sorting, deduplication, basic validation
- Deterministic synthetic fixtures
- Data manifest with SHA256
"""

import csv
import hashlib
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional
import math


@dataclass
class OHLCBar:
    """Unified OHLC bar structure."""

    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float = 0.0

    def __post_init__(self):
        """Validate OHLC relationships."""
        if not (self.low <= self.open <= self.high):
            raise ValueError(f"Invalid OHLC: open {self.open} not in [{self.low}, {self.high}]")
        if not (self.low <= self.close <= self.high):
            raise ValueError(f"Invalid OHLC: close {self.close} not in [{self.low}, {self.high}]")
        if self.low > self.high:
            raise ValueError(f"Invalid OHLC: low {self.low} > high {self.high}")
        if self.volume < 0:
            raise ValueError(f"Invalid volume: {self.volume} < 0")

    def true_range(self, prev_close: Optional[float] = None) -> float:
        """Calculate True Range for ATR."""
        if prev_close is None:
            return self.high - self.low

        return max(
            self.high - self.low,
            abs(self.high - prev_close),
            abs(self.low - prev_close)
        )


@dataclass
class DataManifest:
    """Metadata for loaded data."""

    source: str
    pair: str
    timeframe: str
    start_date: datetime
    end_date: datetime
    num_bars: int
    sha256: str
    timezone: str = "UTC"
    data_type: str = "mid"  # mid, bid, ask
    notes: str = ""

    def to_dict(self) -> dict:
        return {
            "source": self.source,
            "pair": self.pair,
            "timeframe": self.timeframe,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "num_bars": self.num_bars,
            "sha256": self.sha256,
            "timezone": self.timezone,
            "data_type": self.data_type,
            "notes": self.notes
        }


class OHLCDataLoader:
    """CSV OHLC data loader with validation."""

    @staticmethod
    def load_csv(
        filepath: Path,
        timestamp_col: str = "timestamp",
        open_col: str = "open",
        high_col: str = "high",
        low_col: str = "low",
        close_col: str = "close",
        volume_col: str = "volume",
        timestamp_format: str = "%Y-%m-%d %H:%M:%S",
        skip_header: bool = True
    ) -> List[OHLCBar]:
        """Load OHLC data from CSV.

        Args:
            filepath: Path to CSV file
            timestamp_col: Column name or index for timestamp
            open_col: Column name or index for open
            high_col: Column name or index for high
            low_col: Column name or index for low
            close_col: Column name or index for close
            volume_col: Column name or index for volume
            timestamp_format: strptime format for timestamp
            skip_header: Skip first row (header)

        Returns:
            List of OHLCBar, sorted by timestamp
        """
        bars = []

        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f) if skip_header else csv.reader(f)

            for row in reader:
                try:
                    if isinstance(row, dict):
                        timestamp_str = row[timestamp_col]
                        open_price = float(row[open_col])
                        high_price = float(row[high_col])
                        low_price = float(row[low_col])
                        close_price = float(row[close_col])
                        volume = float(row.get(volume_col, 0.0))
                    else:
                        # List-based (no header)
                        timestamp_str = row[0]
                        open_price = float(row[1])
                        high_price = float(row[2])
                        low_price = float(row[3])
                        close_price = float(row[4])
                        volume = float(row[5]) if len(row) > 5 else 0.0

                    timestamp = datetime.strptime(timestamp_str, timestamp_format)

                    bar = OHLCBar(
                        timestamp=timestamp,
                        open=open_price,
                        high=high_price,
                        low=low_price,
                        close=close_price,
                        volume=volume
                    )
                    bars.append(bar)

                except (ValueError, KeyError, IndexError) as e:
                    # Skip invalid rows
                    continue

        # Sort by timestamp
        bars.sort(key=lambda b: b.timestamp)

        # Remove duplicates (keep first occurrence)
        deduplicated = []
        seen_timestamps = set()
        for bar in bars:
            if bar.timestamp not in seen_timestamps:
                deduplicated.append(bar)
                seen_timestamps.add(bar.timestamp)

        return deduplicated

    @staticmethod
    def validate_data(bars: List[OHLCBar]) -> dict:
        """Validate loaded data and return diagnostics.

        Returns:
            Dictionary with validation results
        """
        if not bars:
            return {"valid": False, "error": "No data"}

        issues = []

        # Check for gaps
        if len(bars) > 1:
            time_diffs = [(bars[i+1].timestamp - bars[i].timestamp).total_seconds()
                          for i in range(len(bars) - 1)]
            median_diff = sorted(time_diffs)[len(time_diffs) // 2]

            large_gaps = [i for i, diff in enumerate(time_diffs) if diff > median_diff * 3]
            if large_gaps:
                issues.append(f"{len(large_gaps)} gaps > 3x median time diff detected")

        # Check for zero-range bars
        zero_range = [i for i, bar in enumerate(bars) if bar.high == bar.low]
        if zero_range:
            issues.append(f"{len(zero_range)} zero-range bars (high == low)")

        # Check for extreme price movements
        if len(bars) > 1:
            price_changes = [abs(bars[i+1].close / bars[i].close - 1.0)
                             for i in range(len(bars) - 1)]
            extreme_moves = [i for i, change in enumerate(price_changes) if change > 0.10]
            if extreme_moves:
                issues.append(f"{len(extreme_moves)} bars with >10% price change")

        return {
            "valid": True,
            "num_bars": len(bars),
            "start": bars[0].timestamp,
            "end": bars[-1].timestamp,
            "issues": issues
        }

    @staticmethod
    def compute_sha256(filepath: Path) -> str:
        """Compute SHA256 hash of file."""
        sha256_hash = hashlib.sha256()
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    @staticmethod
    def create_manifest(
        bars: List[OHLCBar],
        source: str,
        pair: str,
        timeframe: str,
        filepath: Optional[Path] = None,
        **kwargs
    ) -> DataManifest:
        """Create data manifest with metadata."""
        sha256 = OHLCDataLoader.compute_sha256(filepath) if filepath else "synthetic"

        return DataManifest(
            source=source,
            pair=pair,
            timeframe=timeframe,
            start_date=bars[0].timestamp,
            end_date=bars[-1].timestamp,
            num_bars=len(bars),
            sha256=sha256,
            **kwargs
        )


class SyntheticDataGenerator:
    """Generate deterministic synthetic OHLC data for testing."""

    @staticmethod
    def generate_trend_and_consolidation(
        start_date: datetime,
        num_days: int,
        initial_price: float = 1.1000,
        seed: int = 42
    ) -> List[OHLCBar]:
        """Generate synthetic daily OHLC with trend and consolidation phases.

        Pattern:
        - Consolidation (50 days): tight range, frequent false breakouts
        - Trend up (100 days): clear upward movement
        - Consolidation (50 days): range-bound
        - Trend down (100 days): clear downward movement
        - Repeat pattern

        Args:
            start_date: Starting date
            num_days: Number of daily bars to generate
            initial_price: Starting price
            seed: Random seed for determinism

        Returns:
            List of OHLCBar
        """
        # Simple deterministic pseudo-random
        def pseudo_random(i: int, seed: int) -> float:
            """Return pseudo-random float in [0, 1) based on index."""
            x = (i * 7919 + seed * 2654435761) % 2147483647
            return (x / 2147483647.0)

        bars = []
        price = initial_price

        for day in range(num_days):
            date = start_date + timedelta(days=day)

            # Determine phase (cycle every 300 days)
            cycle_day = day % 300

            if cycle_day < 50:
                # Consolidation phase
                daily_trend = 0.0
                daily_volatility = 0.003
            elif cycle_day < 150:
                # Uptrend phase
                daily_trend = 0.002
                daily_volatility = 0.004
            elif cycle_day < 200:
                # Consolidation phase
                daily_trend = 0.0
                daily_volatility = 0.003
            else:
                # Downtrend phase
                daily_trend = -0.002
                daily_volatility = 0.004

            # Generate OHLC
            rand1 = pseudo_random(day * 4 + 0, seed)
            rand2 = pseudo_random(day * 4 + 1, seed)
            rand3 = pseudo_random(day * 4 + 2, seed)
            rand4 = pseudo_random(day * 4 + 3, seed)

            # Open with small gap
            open_price = price * (1.0 + (rand1 - 0.5) * 0.001)

            # Close with trend + noise
            close_price = open_price * (1.0 + daily_trend + (rand2 - 0.5) * daily_volatility)

            # High and low
            range_size = abs(close_price - open_price) * (1.5 + rand3)
            high_price = max(open_price, close_price) + range_size * rand4
            low_price = min(open_price, close_price) - range_size * (1.0 - rand4)

            # Ensure valid OHLC
            high_price = max(high_price, open_price, close_price)
            low_price = min(low_price, open_price, close_price)

            bar = OHLCBar(
                timestamp=date,
                open=round(open_price, 5),
                high=round(high_price, 5),
                low=round(low_price, 5),
                close=round(close_price, 5),
                volume=100000.0
            )
            bars.append(bar)

            price = close_price

        return bars

    @staticmethod
    def save_to_csv(bars: List[OHLCBar], filepath: Path):
        """Save bars to CSV file."""
        filepath.parent.mkdir(parents=True, exist_ok=True)

        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['timestamp', 'open', 'high', 'low', 'close', 'volume'])

            for bar in bars:
                writer.writerow([
                    bar.timestamp.strftime('%Y-%m-%d'),
                    bar.open,
                    bar.high,
                    bar.low,
                    bar.close,
                    bar.volume
                ])

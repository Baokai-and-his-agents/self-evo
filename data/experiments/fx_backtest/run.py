"""Main CLI entry point for FX backtest MVP.

Single-command execution of full backtest pipeline:
1. Load data (synthetic fixture or real CSV)
2. Generate trade events (position-independent)
3. Run A/B/E/G sizing policies
4. Compute conditional probabilities
5. Generate reports (JSON + Chinese markdown)
"""

import argparse
import yaml
from pathlib import Path
from datetime import datetime

from fx_backtest.data import OHLCDataLoader, SyntheticDataGenerator
from fx_backtest.signals import DonchianATRSignal
from fx_backtest.engine import BacktestEngine, CostModel
from fx_backtest.sizing import create_default_policies, create_multi_seed_placebo
from fx_backtest.analysis import compute_conditional_probabilities
from fx_backtest.report import generate_markdown_report, save_json_results


def load_config(config_path: Path) -> dict:
    """Load YAML configuration."""
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def main():
    parser = argparse.ArgumentParser(description="FX Position Sizing Backtest MVP")
    parser.add_argument('--config', type=str, required=True, help='Path to config YAML')
    parser.add_argument('--real-data', action='store_true', help='Use real data instead of fixture')
    parser.add_argument('--output-dir', type=str, default=None, help='Override output directory')

    args = parser.parse_args()

    # Load config
    config_path = Path(args.config)
    if not config_path.exists():
        print(f"Error: Config file not found: {config_path}")
        return 1

    config = load_config(config_path)
    print(f"Loaded config from {config_path}")

    # Determine output directory
    if args.output_dir:
        output_dir = Path(args.output_dir)
    else:
        output_dir = Path(config.get('output_dir', 'output'))

    output_dir.mkdir(parents=True, exist_ok=True)

    # Step 1: Load data
    print("\n=== Step 1: Loading Data ===")

    data_config = config.get('data', {})

    if args.real_data:
        data_path = Path(data_config.get('real_data_path', ''))
        if not data_path.exists():
            print(f"Error: Real data file not found: {data_path}")
            print("Falling back to synthetic fixture")
            args.real_data = False

    if not args.real_data:
        # Generate synthetic fixture
        print("Generating synthetic fixture...")
        fixture_config = data_config.get('fixture', )
        start_date = datetime.strptime(fixture_config.get('start_date', '2020-01-01'), '%Y-%m-%d')
        num_days = fixture_config.get('num_days', 750)

        bars = SyntheticDataGenerator.generate_trend_and_consolidation(
            start_date=start_date,
            num_days=num_days,
            initial_price=1.1000,
            seed=42
        )

        # Save fixture
        fixture_path = output_dir / 'fixture.csv'
        SyntheticDataGenerator.save_to_csv(bars, fixture_path)
        print(f"Saved fixture to {fixture_path}")

        manifest = OHLCDataLoader.create_manifest(
            bars=bars,
            source="synthetic",
            pair="EURUSD",
            timeframe="daily",
            notes="Synthetic fixture for testing full pipeline"
        )
    else:
        # Load real data
        print(f"Loading real data from {data_path}")
        bars = OHLCDataLoader.load_csv(
            filepath=data_path,
            timestamp_format=data_config.get('timestamp_format', '%Y-%m-%d')
        )

        validation = OHLCDataLoader.validate_data(bars)
        print(f"Validation: {validation}")

        manifest = OHLCDataLoader.create_manifest(
            bars=bars,
            source=data_config.get('source', 'unknown'),
            pair=data_config.get('pair', 'EURUSD'),
            timeframe=data_config.get('timeframe', 'daily'),
            filepath=data_path
        )

    print(f"Loaded {len(bars)} bars from {bars[0].timestamp} to {bars[-1].timestamp}")

    # Step 2: Generate trade events
    print("\n=== Step 2: Generating Trade Events ===")

    signal_config = config.get('signal', {})
    signal = DonchianATRSignal(
        entry_period=signal_config.get('entry_period', 20),
        exit_period=signal_config.get('exit_period', 10),
        atr_period=signal_config.get('atr_period', 14),
        atr_stop_multiplier=signal_config.get('atr_stop_multiplier', 2.0)
    )

    trade_events = signal.generate_trade_events(bars)
    print(f"Generated {len(trade_events)} trade events")

    if not trade_events:
        print("Error: No trade events generated. Check signal parameters or data.")
        return 1

    # Save trade events
    events_path = output_dir / 'trade_events.json'
    import json
    with open(events_path, 'w') as f:
        json.dump([e.to_dict() for e in trade_events], f, indent=2)
    print(f"Saved trade events to {events_path}")

    # Step 3: Run A/B/E/G policies
    print("\n=== Step 3: Running Sizing Policies ===")

    backtest_config = config.get('backtest', {})
    initial_equity = backtest_config.get('initial_equity', 100000.0)

    cost_config = backtest_config.get('cost', {})
    cost_model = CostModel(
        spread_pips=cost_config.get('spread_pips', 0.0),
        commission_per_lot=cost_config.get('commission_per_lot', 0.0),
        slippage_pips=cost_config.get('slippage_pips', 0.0),
        pip_value=cost_config.get('pip_value', 10.0)
    )

    engine = BacktestEngine(initial_equity=initial_equity, cost_model=cost_model)

    policies = create_default_policies()
    results = {}

    for name, policy in policies.items():
        print(f"Running policy {name} ({policy.get_name()})...")
        result = engine.run(trade_events, policy)
        results[name] = result
        print(f"  Final equity: ${result.final_equity:,.2f} ({result.total_return:+.2%})")

    # Step 4: Conditional probability analysis
    print("\n=== Step 4: Conditional Probability Analysis ===")

    # Use policy A (fixed) trades for conditional analysis (unbiased by sizing)
    conditional_stats = compute_conditional_probabilities(results['A'].trades, max_stop_count=10)

    print("P(win | stop_count=n):")
    for stat in conditional_stats[:6]:
        if stat.n > 0:
            print(f"  n={stat.n}: {stat.n} samples, P(win)={stat.p_win:.3f} [{stat.p_win_ci_low:.3f}, {stat.p_win_ci_high:.3f}]")

    # Step 5: Generate reports
    print("\n=== Step 5: Generating Reports ===")

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    # JSON report
    json_path = output_dir / f'results_{timestamp}.json'
    save_json_results(results, conditional_stats, manifest, json_path)
    print(f"Saved JSON results to {json_path}")

    # Markdown report
    markdown_path = output_dir / f'report_{timestamp}.md'
    generate_markdown_report(results, conditional_stats, manifest, cost_model, config, markdown_path)
    print(f"Saved markdown report to {markdown_path}")

    print("\n=== Backtest Complete ===")
    print(f"Output directory: {output_dir.absolute()}")

    return 0


if __name__ == '__main__':
    exit(main())

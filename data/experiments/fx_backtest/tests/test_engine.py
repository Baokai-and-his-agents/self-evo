"""Tests for backtest engine: cost model, equity tracking, cycle management."""

import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from fx_backtest.data import SyntheticDataGenerator
from fx_backtest.signals import DonchianATRSignal
from fx_backtest.engine import BacktestEngine, CostModel
from fx_backtest.sizing import FixedSizing, ArithmeticAfterLoss


def test_zero_cost_backtest():
    """Test backtest with zero costs."""
    print("Testing zero cost backtest...")

    bars = SyntheticDataGenerator.generate_trend_and_consolidation(
        start_date=datetime(2020, 1, 1),
        num_days=200,
        seed=42
    )

    signal = DonchianATRSignal()
    events = signal.generate_trade_events(bars)

    cost_model = CostModel()  # Zero cost
    engine = BacktestEngine(initial_equity=100000, cost_model=cost_model)

    policy = FixedSizing(risk_pct=0.01)
    result = engine.run(events, policy)

    assert result.initial_equity == 100000
    assert result.final_equity != result.initial_equity  # Should have some change
    assert len(result.trades) == len(events)

    # All costs should be zero
    for trade in result.trades:
        assert trade.cost == 0.0

    print(f"[PASS] Zero cost backtest: {len(result.trades)} trades, final equity ${result.final_equity:,.2f}")


def test_cost_impact():
    """Test that costs reduce returns."""
    print("Testing cost impact...")

    bars = SyntheticDataGenerator.generate_trend_and_consolidation(
        start_date=datetime(2020, 1, 1),
        num_days=200,
        seed=42
    )

    signal = DonchianATRSignal()
    events = signal.generate_trade_events(bars)

    # Zero cost
    engine_zero = BacktestEngine(initial_equity=100000, cost_model=CostModel())
    policy_zero = FixedSizing(risk_pct=0.01)
    result_zero = engine_zero.run(events, policy_zero)

    # With costs
    cost_model = CostModel(spread_pips=2.0, commission_per_lot=5.0, slippage_pips=0.0)
    engine_cost = BacktestEngine(initial_equity=100000, cost_model=cost_model)
    policy_cost = FixedSizing(risk_pct=0.01)
    result_cost = engine_cost.run(events, policy_cost)

    # Cost version should have lower final equity
    assert result_cost.final_equity < result_zero.final_equity

    # Costs should be > 0
    total_cost = sum(t.cost for t in result_cost.trades)
    assert total_cost > 0

    print(f"[PASS] Cost impact: ${result_zero.final_equity - result_cost.final_equity:,.2f} difference")


def test_policy_event_consistency():
    """Test that A/B/E/G see the same events."""
    print("Testing policy event consistency...")

    bars = SyntheticDataGenerator.generate_trend_and_consolidation(
        start_date=datetime(2020, 1, 1),
        num_days=200,
        seed=42
    )

    signal = DonchianATRSignal()
    events = signal.generate_trade_events(bars)

    engine = BacktestEngine(initial_equity=100000)

    policy_a = FixedSizing(risk_pct=0.01)
    policy_b = ArithmeticAfterLoss(r_0=0.01, d=0.005, K=5)

    result_a = engine.run(events, policy_a)
    result_b = engine.run(events, policy_b)

    # Should have same number of trades (before B hits K limit)
    # But B might stop early if it hits K
    assert result_a.num_trades > 0
    assert result_b.num_trades > 0

    # Check that event_ids match for common trades
    trades_a_dict = {t.event_id: t for t in result_a.trades}
    trades_b_dict = {t.event_id: t for t in result_b.trades}

    common_ids = set(trades_a_dict.keys()) & set(trades_b_dict.keys())
    assert len(common_ids) > 0

    for event_id in common_ids:
        ta = trades_a_dict[event_id]
        tb = trades_b_dict[event_id]

        # Same entry/exit/stop prices (before sizing)
        assert ta.entry_price == tb.entry_price
        assert ta.exit_price == tb.exit_price
        assert ta.stop_price == tb.stop_price

        # Different risk fractions (sizing differs)
        # A is always 0.01, B varies
        assert ta.risk_fraction == 0.01

    print(f"[PASS] Policy consistency: {len(common_ids)} common trades verified")


def test_stop_count_tracking():
    """Test that stop_count is tracked correctly."""
    print("Testing stop count tracking...")

    bars = SyntheticDataGenerator.generate_trend_and_consolidation(
        start_date=datetime(2020, 1, 1),
        num_days=200,
        seed=42
    )

    signal = DonchianATRSignal()
    events = signal.generate_trade_events(bars)

    engine = BacktestEngine(initial_equity=100000)
    policy = ArithmeticAfterLoss(r_0=0.01, d=0.005, K=5)

    result = engine.run(events, policy)

    # Find consecutive stops
    stop_counts = [t.stop_count_at_entry for t in result.trades]

    # After a win, stop_count should reset
    for i in range(1, len(result.trades)):
        prev_trade = result.trades[i-1]
        curr_trade = result.trades[i]

        if prev_trade.pnl > 0:
            # After a win, stop_count should reset to 0
            assert curr_trade.stop_count_at_entry == 0, f"Stop count should reset after win at trade {i}"

    print(f"[PASS] Stop count tracking verified over {len(result.trades)} trades")


def test_equity_curve():
    """Test equity curve generation."""
    print("Testing equity curve...")

    bars = SyntheticDataGenerator.generate_trend_and_consolidation(
        start_date=datetime(2020, 1, 1),
        num_days=200,
        seed=42
    )

    signal = DonchianATRSignal()
    events = signal.generate_trade_events(bars)

    engine = BacktestEngine(initial_equity=100000)
    policy = FixedSizing(risk_pct=0.01)

    result = engine.run(events, policy)

    # Equity curve should have entries
    assert len(result.equity_curve) > 0
    assert result.equity_curve[0][1] == 100000  # Initial equity

    # Last equity should match final_equity
    assert result.equity_curve[-1][1] == result.final_equity

    print(f"[PASS] Equity curve: {len(result.equity_curve)} points")


if __name__ == '__main__':
    test_zero_cost_backtest()
    test_cost_impact()
    test_policy_event_consistency()
    test_stop_count_tracking()
    test_equity_curve()
    print("\n[PASS] All backtest engine tests passed")

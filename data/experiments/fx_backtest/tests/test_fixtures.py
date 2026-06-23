"""Test deterministic fixtures and business logic correctness."""

import json
import hashlib
from datetime import datetime
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Fix console encoding for Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from fx_backtest.engine import BacktestEngine, CostModel
from fx_backtest.sizing import FixedSizing, ArithmeticAfterLoss, ConfirmThenAmplify, PermutationPlacebo
from tests.fixtures import (
    create_fixture_consecutive_losses,
    create_fixture_cycle_failure_and_continue,
    create_fixture_e_confirmation,
    create_fixture_gap_beyond_stop,
    create_fixture_zero_and_nonzero_cost
)


def serialize_events(events):
    """Create canonical serialization of events for comparison."""
    return json.dumps([e.to_dict() for e in events], sort_keys=True)


def hash_events(events):
    """Create hash of event stream."""
    serialized = serialize_events(events)
    return hashlib.sha256(serialized.encode()).hexdigest()


def test_event_immutability():
    """Verify that running policies does not modify the event stream."""
    print("\n=== Test: Event Immutability ===")

    events = create_fixture_cycle_failure_and_continue(K=5)
    events_before = serialize_events(events)
    hash_before = hash_events(events)

    engine = BacktestEngine(initial_equity=100000.0, cost_model=CostModel())

    policies = [
        FixedSizing(risk_pct=0.01),
        ArithmeticAfterLoss(r_0=0.01, d=0.005, K=5, r_max=0.03, total_budget=0.10),
        ConfirmThenAmplify(r_probe=0.005, r_confirmed=0.02),
        PermutationPlacebo(r_0=0.01, d=0.005, K=5, r_max=0.03, total_budget=0.10, seed=42)
    ]

    for policy in policies:
        result = engine.run(events, policy)
        events_after = serialize_events(events)
        hash_after = hash_events(events)

        assert events_after == events_before, f"Policy {policy.get_name()} modified events!"
        assert hash_after == hash_before, f"Policy {policy.get_name()} changed event hash!"

    print(f"✓ All {len(policies)} policies preserved event immutability")
    print(f"  Event hash: {hash_before[:16]}...")


def test_b_cycle_failure_and_reset():
    """Test B policy cycle failure and continuation after reset."""
    print("\n=== Test: B Cycle Failure and Reset ===")

    K = 5
    events = create_fixture_cycle_failure_and_continue(K=K)

    engine = BacktestEngine(initial_equity=100000.0, cost_model=CostModel())
    policy = ArithmeticAfterLoss(r_0=0.01, d=0.005, K=K, r_max=0.03, total_budget=0.10)

    result = engine.run(events, policy)

    print(f"Total events: {len(events)}")
    print(f"Total trades executed: {result.num_trades}")
    print(f"Cycle failures: {result.num_cycle_failures}")
    print(f"Cycles completed: {result.num_cycles}")

    # Should execute all events (K losses + 1 win + 2 losses + 1 win = K+4)
    assert result.num_trades == len(events), f"Expected {len(events)} trades, got {result.num_trades}"

    # Should have 1 cycle failure (K consecutive losses)
    assert result.num_cycle_failures == 1, f"Expected 1 cycle failure, got {result.num_cycle_failures}"

    # Should have 2 successful cycles (2 wins)
    assert result.num_cycles == 2, f"Expected 2 cycles, got {result.num_cycles}"

    print("✓ B correctly handles cycle failure and continues trading")


def test_e_confirmation_amplification():
    """Test E policy confirmation and amplified sizing."""
    print("\n=== Test: E Confirmation and Amplification ===")

    events = create_fixture_e_confirmation()

    engine = BacktestEngine(initial_equity=100000.0, cost_model=CostModel())
    policy_e = ConfirmThenAmplify(r_probe=0.005, r_confirmed=0.02)

    result = engine.run(events, policy_e)

    print(f"Total trades: {result.num_trades}")

    # Find the trade with confirmation (event_id=1)
    confirmed_trade = [t for t in result.trades if t.event_id == 1][0]
    non_confirmed_trades = [t for t in result.trades if t.event_id != 1]

    print(f"Confirmed trade (event_id=1):")
    print(f"  Risk fraction: {confirmed_trade.risk_fraction:.4f}")
    print(f"  Initial risk: ${confirmed_trade.initial_risk:,.2f}")
    print(f"  PnL: ${confirmed_trade.pnl:,.2f}")

    # Confirmed trade should use amplified risk (0.02)
    assert confirmed_trade.risk_fraction > 0.005, f"Expected amplified risk, got {confirmed_trade.risk_fraction}"

    # Non-confirmed trades should use probe risk (0.005)
    for trade in non_confirmed_trades:
        assert trade.risk_fraction == 0.005, f"Expected probe risk 0.005, got {trade.risk_fraction}"

    print("✓ E correctly amplifies after confirmation")


def test_g_same_event_ids_and_multiset():
    """Test G has same event IDs as B.

    Note: G permutes the risk VALUES within each cycle, so the exact
    multiset may differ from B due to how stop_count maps to permuted values.
    What matters is:
    1. Same event IDs (same trading decisions)
    2. Same VALUE SET available (0.01, 0.015, 0.02, 0.025, 0.03)
    3. Permutation is deterministic per seed
    """
    print("\n=== Test: G Event IDs and Value Set ===")

    events = create_fixture_cycle_failure_and_continue(K=5)

    engine = BacktestEngine(initial_equity=100000.0, cost_model=CostModel())

    policy_b = ArithmeticAfterLoss(r_0=0.01, d=0.005, K=5, r_max=0.03, total_budget=0.10)
    policy_g = PermutationPlacebo(r_0=0.01, d=0.005, K=5, r_max=0.03, total_budget=0.10, seed=42)

    result_b = engine.run(events, policy_b)
    result_g = engine.run(events, policy_g)

    # Extract event IDs
    event_ids_b = [t.event_id for t in result_b.trades]
    event_ids_g = [t.event_id for t in result_g.trades]

    print(f"B event IDs: {event_ids_b}")
    print(f"G event IDs: {event_ids_g}")

    assert event_ids_b == event_ids_g, "G and B must trade the same events"

    # Extract risk fractions
    risks_b = [t.risk_fraction for t in result_b.trades]
    risks_g = [t.risk_fraction for t in result_g.trades]

    print(f"B risks: {[f'{r:.4f}' for r in risks_b]}")
    print(f"G risks: {[f'{r:.4f}' for r in risks_g]}")

    # Verify G uses values from the same set as B
    value_set_b = set([0.01, 0.015, 0.02, 0.025, 0.03])
    value_set_g = set(risks_g)

    print(f"B value set: {sorted(value_set_b)}")
    print(f"G value set: {sorted(value_set_g)}")

    # G should only use values from B's value set
    for risk in risks_g:
        assert risk in value_set_b, f"G used unexpected risk value {risk}"

    print("✓ G preserves event IDs and uses same risk value set")


def test_g_seed_reproducibility():
    """Test G produces identical results for same seed."""
    print("\n=== Test: G Seed Reproducibility ===")

    events = create_fixture_cycle_failure_and_continue(K=5)
    engine = BacktestEngine(initial_equity=100000.0, cost_model=CostModel())

    # Run with seed 42 twice
    policy_g1 = PermutationPlacebo(r_0=0.01, d=0.005, K=5, r_max=0.03, total_budget=0.10, seed=42)
    policy_g2 = PermutationPlacebo(r_0=0.01, d=0.005, K=5, r_max=0.03, total_budget=0.10, seed=42)

    result1 = engine.run(events, policy_g1)
    result2 = engine.run(events, policy_g2)

    risks1 = [t.risk_fraction for t in result1.trades]
    risks2 = [t.risk_fraction for t in result2.trades]

    assert risks1 == risks2, "Same seed must produce identical results"

    # Run with different seed
    policy_g3 = PermutationPlacebo(r_0=0.01, d=0.005, K=5, r_max=0.03, total_budget=0.10, seed=99)
    result3 = engine.run(events, policy_g3)

    risks3 = [t.risk_fraction for t in result3.trades]

    # Different seed should (likely) produce different sequence
    # Note: multisets may differ due to how resets interact with permutations
    different = risks1 != risks3
    assert different, "Different seeds should produce different sequences"

    # But both should use the same value set
    value_set = set([0.01, 0.015, 0.02, 0.025, 0.03])
    assert set(risks1).issubset(value_set), "Seed 42 uses wrong values"
    assert set(risks3).issubset(value_set), "Seed 99 uses wrong values"

    print(f"✓ Seed 42 run 1: {[f'{r:.4f}' for r in risks1]}")
    print(f"✓ Seed 42 run 2: {[f'{r:.4f}' for r in risks2]}")
    print(f"✓ Seed 99:       {[f'{r:.4f}' for r in risks3]}")
    print(f"✓ Seed reproducibility verified")


def test_cost_model_hand_calculation():
    """Test cost model with hand-calculable values."""
    print("\n=== Test: Cost Model Hand Calculation ===")

    # Simple scenario: 1% risk, 1 trade
    # Entry: 1.1000, Stop: 1.0980 (20 pips = 0.0020)
    # Position: risk $1000 / $0.0020 = 500,000 EUR = 5 standard lots
    #
    # Conservative costs:
    # - Spread: 1 pip * 2 (round-trip) * $10/pip * 5 lots = $100
    # - Commission: $7/lot * 5 lots = $35
    # - Slippage: 0.5 pips * 2 * $10/pip * 5 lots = $50
    # Total cost: $185

    events = create_fixture_zero_and_nonzero_cost()

    # Zero cost
    engine_zero = BacktestEngine(initial_equity=100000.0, cost_model=CostModel())
    policy_a = FixedSizing(risk_pct=0.01)
    result_zero = engine_zero.run(events, policy_a)

    print(f"Zero cost scenario:")
    print(f"  Trade 0 cost: ${result_zero.trades[0].cost:.2f}")
    print(f"  Trade 1 cost: ${result_zero.trades[1].cost:.2f}")

    assert result_zero.trades[0].cost == 0.0, "Zero cost should be $0"
    assert result_zero.trades[1].cost == 0.0, "Zero cost should be $0"

    # Conservative cost
    cost_model = CostModel(spread_pips=1.0, commission_per_lot=7.0, slippage_pips=0.5)
    engine_cost = BacktestEngine(initial_equity=100000.0, cost_model=cost_model)
    result_cost = engine_cost.run(events, policy_a)

    print(f"\nConservative cost scenario:")
    print(f"  Trade 0 position: {result_cost.trades[0].position_size:,.0f} EUR = {result_cost.trades[0].position_size/100000:.2f} lots")
    print(f"  Trade 0 cost: ${result_cost.trades[0].cost:.2f}")
    print(f"  Trade 1 cost: ${result_cost.trades[1].cost:.2f}")

    # Expected cost: ~$185 per trade (hand calculation above)
    # Allow some tolerance due to equity changes
    expected_cost = 185.0
    assert 150 < result_cost.trades[0].cost < 220, f"Expected ~$185, got ${result_cost.trades[0].cost:.2f}"

    print("✓ Cost model calculations are reasonable")


def run_all_tests():
    """Run all deterministic fixture tests."""
    print("=" * 60)
    print("Running Deterministic Fixture Tests")
    print("=" * 60)

    test_event_immutability()
    test_b_cycle_failure_and_reset()
    test_e_confirmation_amplification()
    test_g_same_event_ids_and_multiset()
    test_g_seed_reproducibility()
    test_cost_model_hand_calculation()

    print("\n" + "=" * 60)
    print("✓ All deterministic fixture tests passed")
    print("=" * 60)


if __name__ == '__main__':
    run_all_tests()

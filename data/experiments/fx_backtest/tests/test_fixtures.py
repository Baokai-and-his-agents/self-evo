"""Deterministic business-logic tests for the backtest MVP."""

import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from fx_backtest.engine import BacktestEngine, CostModel
from fx_backtest.sizing import (
    ArithmeticAfterLoss,
    ConfirmThenAmplify,
    FixedSizing,
    ScheduledPermutationPlacebo,
)
from tests.fixtures import (
    create_fixture_cycle_failure_and_continue,
    create_fixture_e_confirmation,
    create_fixture_zero_and_nonzero_cost,
)


def serialize_events(events):
    return json.dumps([event.to_dict() for event in events], sort_keys=True)


def hash_events(events):
    return hashlib.sha256(serialize_events(events).encode()).hexdigest()


def make_b_result(events, total_budget=0.10):
    engine = BacktestEngine(initial_equity=100000.0, cost_model=CostModel())
    policy = ArithmeticAfterLoss(
        r_0=0.01,
        d=0.005,
        K=5,
        r_max=0.03,
        total_budget=total_budget,
    )
    return engine, engine.run(events, policy)


def test_event_immutability_and_complete_stream():
    events = create_fixture_cycle_failure_and_continue(K=5)
    expected_ids = [event.event_id for event in events]
    before = serialize_events(events)
    before_hash = hash_events(events)

    engine, result_b = make_b_result(events)
    b_schedule = [
        (trade.event_id, trade.risk_fraction) for trade in result_b.trades
    ]
    policies = [
        FixedSizing(risk_pct=0.01),
        ConfirmThenAmplify(r_probe=0.005, r_confirmed=0.02),
        ScheduledPermutationPlacebo(b_schedule=b_schedule, seed=42),
    ]
    results = [result_b] + [engine.run(events, policy) for policy in policies]

    for result in results:
        assert [trade.event_id for trade in result.trades] == expected_ids
        assert serialize_events(events) == before
        assert hash_events(events) == before_hash


def test_b_cycle_failure_and_budget_reset_continue():
    events = create_fixture_cycle_failure_and_continue(K=5)
    expected_ids = [event.event_id for event in events]

    _, result_k = make_b_result(events)
    assert [trade.event_id for trade in result_k.trades] == expected_ids
    assert result_k.num_cycle_failures == 1
    assert result_k.num_cycles == 3

    _, result_budget = make_b_result(events, total_budget=0.015)
    assert [trade.event_id for trade in result_budget.trades] == expected_ids
    assert result_budget.num_cycle_failures > 0


def test_e_confirmation_risk_is_measured_from_confirmation():
    events = create_fixture_e_confirmation()
    engine = BacktestEngine(initial_equity=100000.0, cost_model=CostModel())
    result = engine.run(
        events,
        ConfirmThenAmplify(r_probe=0.005, r_confirmed=0.02),
    )
    trade = next(trade for trade in result.trades if trade.event_id == 1)
    event = next(event for event in events if event.event_id == 1)

    actual_stop_loss = trade.amplified_units * (
        event.confirmation_price - event.stop_price
    )
    assert abs(actual_stop_loss - trade.amplified_risk) < 1e-8
    assert trade.probe_notional == trade.probe_units * event.entry_price
    assert trade.amplified_notional == (
        trade.amplified_units * event.confirmation_price
    )
    serialized = result.to_dict()
    serialized_trade = next(
        item for item in serialized["trades"] if item["event_id"] == 1
    )
    assert serialized_trade["probe_notional"] == trade.probe_notional
    assert serialized_trade["amplified_notional"] == trade.amplified_notional
    assert "additional_metrics" in serialized


def test_g_exact_multiset_across_seeds():
    events = create_fixture_cycle_failure_and_continue(K=5)
    expected_ids = [event.event_id for event in events]
    engine, result_b = make_b_result(events)
    b_schedule = [
        (trade.event_id, trade.risk_fraction) for trade in result_b.trades
    ]
    b_risks = [trade.risk_fraction for trade in result_b.trades]

    sequences = []
    for seed in range(42, 52):
        result_g = engine.run(
            events,
            ScheduledPermutationPlacebo(b_schedule=b_schedule, seed=seed),
        )
        risks_g = [trade.risk_fraction for trade in result_g.trades]
        assert [trade.event_id for trade in result_g.trades] == expected_ids
        assert sorted(risks_g) == sorted(b_risks)
        sequences.append(risks_g)

    assert any(sequence != b_risks for sequence in sequences)
    assert len({tuple(sequence) for sequence in sequences}) >= 2
    repeated = engine.run(
        events,
        ScheduledPermutationPlacebo(b_schedule=b_schedule, seed=42),
    )
    assert [trade.risk_fraction for trade in repeated.trades] == sequences[0]


def test_cost_model_hand_calculation():
    events = create_fixture_zero_and_nonzero_cost()
    engine_zero = BacktestEngine(initial_equity=100000.0, cost_model=CostModel())
    result_zero = engine_zero.run(events, FixedSizing(risk_pct=0.01))
    assert all(trade.cost == 0.0 for trade in result_zero.trades)

    cost_model = CostModel(
        spread_pips=1.0,
        commission_per_lot=7.0,
        slippage_pips=0.5,
    )
    engine_cost = BacktestEngine(initial_equity=100000.0, cost_model=cost_model)
    result_cost = engine_cost.run(events, FixedSizing(risk_pct=0.01))
    assert 150 < result_cost.trades[0].cost < 220


def run_all_tests():
    test_event_immutability_and_complete_stream()
    test_b_cycle_failure_and_budget_reset_continue()
    test_e_confirmation_risk_is_measured_from_confirmation()
    test_g_exact_multiset_across_seeds()
    test_cost_model_hand_calculation()
    print("[PASS] All deterministic fixture tests passed")


if __name__ == "__main__":
    run_all_tests()

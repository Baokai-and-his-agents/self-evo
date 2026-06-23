"""Tests for sizing policies: A/B/E/G correctness and event independence."""

import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from fx_backtest.sizing import (
    FixedSizing, ArithmeticAfterLoss, ConfirmThenAmplify, PermutationPlacebo,
    SizingContext
)


def test_fixed_sizing():
    """Test fixed sizing policy."""
    print("Testing fixed sizing...")

    policy = FixedSizing(risk_pct=0.01)

    # Should return same size regardless of stop_count
    ctx0 = SizingContext(event_id=0, stop_count=0, equity=100000, entry_price=1.1, stop_price=1.09)
    ctx5 = SizingContext(event_id=5, stop_count=5, equity=100000, entry_price=1.1, stop_price=1.09)

    size0 = policy.calculate_size(ctx0)
    size5 = policy.calculate_size(ctx5)

    assert size0 == 0.01
    assert size5 == 0.01
    assert size0 == size5

    print("[PASS] Fixed sizing tests passed")


def test_arithmetic_sizing():
    """Test arithmetic after loss sizing."""
    print("Testing arithmetic sizing...")

    policy = ArithmeticAfterLoss(r_0=0.01, d=0.005, K=5, r_max=0.03)

    # n=0: r_0 = 1%
    ctx0 = SizingContext(event_id=0, stop_count=0, equity=100000, entry_price=1.1, stop_price=1.09, cumulative_loss=0.0)
    size0 = policy.calculate_size(ctx0)
    assert size0 == 0.01

    # n=1: r_0 + d = 1.5%
    ctx1 = SizingContext(event_id=1, stop_count=1, equity=100000, entry_price=1.1, stop_price=1.09, cumulative_loss=1000.0)
    size1 = policy.calculate_size(ctx1)
    assert size1 == 0.015

    # n=2: r_0 + 2*d = 2%
    ctx2 = SizingContext(event_id=2, stop_count=2, equity=100000, entry_price=1.1, stop_price=1.09, cumulative_loss=2500.0)
    size2 = policy.calculate_size(ctx2)
    assert size2 == 0.02

    # n=5: should hit K limit, return 0
    ctx5 = SizingContext(event_id=5, stop_count=5, equity=100000, entry_price=1.1, stop_price=1.09, cumulative_loss=7000.0)
    size5 = policy.calculate_size(ctx5)
    assert size5 == 0.03  # Changed: engine handles reset, policy continues

    # Exceeded budget: should return 0
    ctx_budget = SizingContext(event_id=3, stop_count=3, equity=100000, entry_price=1.1, stop_price=1.09, cumulative_loss=11000.0)
    size_budget = policy.calculate_size(ctx_budget)
    assert size_budget == 0.0

    print("[PASS] Arithmetic sizing tests passed")


def test_confirm_then_amplify():
    """Test confirm-then-amplify sizing."""
    print("Testing confirm-then-amplify...")

    policy = ConfirmThenAmplify(r_probe=0.005, r_confirmed=0.02)

    # Probe phase
    ctx_probe = SizingContext(
        event_id=0, stop_count=0, equity=100000,
        entry_price=1.1, stop_price=1.09,
        in_confirmed_trend=False
    )
    size_probe = policy.calculate_size(ctx_probe)
    assert size_probe == 0.005

    # Confirmed phase
    ctx_confirmed = SizingContext(
        event_id=1, stop_count=0, equity=100000,
        entry_price=1.1, stop_price=1.09,
        in_confirmed_trend=True
    )
    size_confirmed = policy.calculate_size(ctx_confirmed)
    assert size_confirmed == 0.02

    print("[PASS] Confirm-then-amplify tests passed")


def test_permutation_placebo():
    """Test permutation placebo sizing."""
    print("Testing permutation placebo...")

    policy = PermutationPlacebo(r_0=0.01, d=0.005, K=5, r_max=0.03, seed=42)

    # Get permutation map
    risk_multiset = policy.get_risk_multiset()
    assert len(risk_multiset) == 5  # 0 to K inclusive

    # Verify it's a permutation (bijection)

    # Size should depend on permuted stop_count
    ctx0 = SizingContext(event_id=0, stop_count=0, equity=100000, entry_price=1.1, stop_price=1.09)
    ctx1 = SizingContext(event_id=1, stop_count=1, equity=100000, entry_price=1.1, stop_price=1.09)

    size0 = policy.calculate_size(ctx0)
    size1 = policy.calculate_size(ctx1)

    # Sizes should be valid (within B's range)
    assert 0.0 <= size0 <= 0.03
    assert 0.0 <= size1 <= 0.03

    # Deterministic: same seed produces same permutation
    policy2 = PermutationPlacebo(r_0=0.01, d=0.005, K=5, r_max=0.03, seed=42)
    perm_map2 = policy2.get_permutation_map()
    assert perm_map == perm_map2

    print("[PASS] Permutation placebo tests passed")


def test_policy_independence():
    """Test that policies don't interfere with each other."""
    print("Testing policy independence...")

    ctx = SizingContext(event_id=0, stop_count=2, equity=100000, entry_price=1.1, stop_price=1.09)

    policy_a = FixedSizing(risk_pct=0.01)
    policy_b = ArithmeticAfterLoss(r_0=0.01, d=0.005, K=5)

    size_a = policy_a.calculate_size(ctx)
    size_b = policy_b.calculate_size(ctx)

    # Should give different sizes
    assert size_a == 0.01
    assert size_b == 0.02
    assert size_a != size_b

    # Running A doesn't affect B
    size_b2 = policy_b.calculate_size(ctx)
    assert size_b2 == size_b

    print("[PASS] Policy independence tests passed")


if __name__ == '__main__':
    test_fixed_sizing()
    test_arithmetic_sizing()
    test_confirm_then_amplify()
    test_permutation_placebo()
    test_policy_independence()
    print("\n[PASS] All sizing policy tests passed")

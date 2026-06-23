"""Permutation test: B vs multi-seed placebo distribution."""

from typing import List, Optional
from .engine import BacktestResult


def analyze_placebo_distribution(
    b_result: BacktestResult,
    placebo_results: List[BacktestResult],
    min_placebo_seeds: int = 10
) -> dict:
    """Analyze B's position in the placebo distribution.

    Args:
        b_result: Result from B policy
        placebo_results: Results from multiple G (placebo) runs with different seeds
        min_placebo_seeds: Minimum number of placebo seeds required

    Returns:
        Dictionary with percentile, p-value, and interpretation
    """
    if not placebo_results:
        return {
            "test": "INSUFFICIENT_DATA",
            "reason": "No placebo results provided",
            "num_seeds": 0,
            "min_required": min_placebo_seeds
        }

    if len(placebo_results) < min_placebo_seeds:
        return {
            "test": "INSUFFICIENT_DATA",
            "reason": f"Only {len(placebo_results)} placebo seeds (need {min_placebo_seeds})",
            "num_seeds": len(placebo_results),
            "min_required": min_placebo_seeds
        }

    # Extract final equity from B and all G runs
    b_equity = b_result.final_equity
    placebo_equities = [r.final_equity for r in placebo_results]

    # Calculate percentile: what fraction of placebo runs did B beat?
    num_better = sum(1 for g_equity in placebo_equities if b_equity > g_equity)
    percentile = num_better / len(placebo_equities)

    # Two-tailed p-value: how extreme is B's position?
    # p-value = 2 * min(percentile, 1 - percentile)
    p_value = 2 * min(percentile, 1 - percentile)

    # Distribution statistics
    placebo_mean = sum(placebo_equities) / len(placebo_equities)
    placebo_sorted = sorted(placebo_equities)
    placebo_median = placebo_sorted[len(placebo_sorted) // 2]
    placebo_min = min(placebo_equities)
    placebo_max = max(placebo_equities)

    # Calculate where B sits relative to distribution
    if len(placebo_sorted) >= 20:
        p05 = placebo_sorted[int(len(placebo_sorted) * 0.05)]
        p95 = placebo_sorted[int(len(placebo_sorted) * 0.95)]
    else:
        p05 = placebo_min
        p95 = placebo_max

    # Interpretation
    if p_value < 0.05:
        interpretation = (
            f"B's final equity (${b_equity:,.2f}) is statistically extreme "
            f"compared to placebo distribution (p={p_value:.4f}). "
            f"This suggests the timing of size increases matters."
        )
    else:
        interpretation = (
            f"B's final equity (${b_equity:,.2f}) falls within the expected range "
            f"of the placebo distribution (p={p_value:.4f}). "
            f"No evidence that the timing of size increases (vs just the distribution) matters."
        )

    return {
        "test": "permutation",
        "num_seeds": len(placebo_results),
        "b_equity": b_equity,
        "placebo_mean": placebo_mean,
        "placebo_median": placebo_median,
        "placebo_min": placebo_min,
        "placebo_max": placebo_max,
        "placebo_p05": p05,
        "placebo_p95": p95,
        "percentile": percentile,
        "p_value": p_value,
        "interpretation": interpretation,
        "significant_at_5pct": p_value < 0.05
    }


def verify_risk_multiset_equality(b_result: BacktestResult, g_result: BacktestResult) -> dict:
    """Verify that B and G used the same multiset of risk fractions.

    Args:
        b_result: Result from B policy
        g_result: Result from G policy (single seed)

    Returns:
        Dictionary with verification result
    """
    # Extract risk fractions from trades
    b_risks = sorted([t.risk_fraction for t in b_result.trades])
    g_risks = sorted([t.risk_fraction for t in g_result.trades])

    # Check equality
    equal = b_risks == g_risks

    # Compute multiset difference if not equal
    if not equal:
        b_set = set(b_risks)
        g_set = set(g_risks)
        only_in_b = b_set - g_set
        only_in_g = g_set - b_set
    else:
        only_in_b = set()
        only_in_g = set()

    return {
        "equal": equal,
        "b_num_trades": len(b_risks),
        "g_num_trades": len(g_risks),
        "b_risk_multiset": b_risks,
        "g_risk_multiset": g_risks,
        "only_in_b": list(only_in_b),
        "only_in_g": list(only_in_g)
    }

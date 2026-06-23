"""Permutation test: B vs multi-seed placebo distribution."""

from typing import List
from .engine import BacktestResult


def analyze_placebo_distribution(
    b_result: BacktestResult,
    placebo_results: List[BacktestResult],
    min_placebo_seeds: int = 10,
    min_trades: int = 20
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

    if len(b_result.trades) < min_trades:
        return {
            "test": "INSUFFICIENT_DATA",
            "reason": (
                f"B has {len(b_result.trades)} trades "
                f"(need at least {min_trades})"
            ),
            "num_seeds": len(placebo_results),
            "min_required": min_placebo_seeds,
            "min_trades": min_trades
        }
    if any(len(result.trades) != len(b_result.trades) for result in placebo_results):
        raise ValueError("Placebo trade counts must match B")

    # Extract final equity from B and all G runs
    b_equity = b_result.final_equity
    placebo_equities = [r.final_equity for r in placebo_results]

    # Calculate percentile: what fraction of placebo runs did B beat?
    num_better = sum(1 for g_equity in placebo_equities if b_equity > g_equity)
    placebo_mean = sum(placebo_equities) / len(placebo_equities)
    lower_tail = (
        1 + sum(equity <= b_equity for equity in placebo_equities)
    ) / (len(placebo_equities) + 1)
    upper_tail = (
        1 + sum(equity >= b_equity for equity in placebo_equities)
    ) / (len(placebo_equities) + 1)
    p_value = min(1.0, 2.0 * min(lower_tail, upper_tail))

    # Also compute traditional percentile for reference
    percentile = num_better / len(placebo_equities)

    # Distribution statistics
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
        "method": "two_sided_monte_carlo_rank_plus_one",
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

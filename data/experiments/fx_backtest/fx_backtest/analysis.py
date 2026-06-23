"""Conditional probability analysis: P(win|stop_count=n), E[R|stop_count=n].

Core research question: Does consecutive stop count predict next trade outcome?
"""

from dataclasses import dataclass
from typing import List, Dict, Tuple
import math

from .engine import Trade, BacktestResult


@dataclass
class ConditionalStats:
    """Statistics for trades at a given stop_count."""

    stop_count: int
    n: int  # Sample size
    num_wins: int
    num_losses: int
    p_win: float  # Point estimate P(win | stop_count=n)
    p_win_ci_low: float  # 95% CI lower bound
    p_win_ci_high: float  # 95% CI upper bound
    mean_r: float  # E[R | stop_count=n]
    mean_r_ci_low: float  # 95% CI lower bound
    mean_r_ci_high: float  # 95% CI upper bound
    r_values: List[float] = None  # Raw R values for this bucket

    def to_dict(self) -> dict:
        return {
            "stop_count": self.stop_count,
            "n": self.n,
            "num_wins": self.num_wins,
            "num_losses": self.num_losses,
            "p_win": round(self.p_win, 4),
            "p_win_ci_low": round(self.p_win_ci_low, 4),
            "p_win_ci_high": round(self.p_win_ci_high, 4),
            "mean_r": round(self.mean_r, 4),
            "mean_r_ci_low": round(self.mean_r_ci_low, 4),
            "mean_r_ci_high": round(self.mean_r_ci_high, 4)
        }


def wilson_score_interval(successes: int, n: int, confidence: float = 0.95) -> Tuple[float, float]:
    """Compute Wilson score confidence interval for binomial proportion.

    More accurate than normal approximation for small n.

    Args:
        successes: Number of successes
        n: Sample size
        confidence: Confidence level (default 0.95)

    Returns:
        (lower_bound, upper_bound)
    """
    if n == 0:
        return (0.0, 1.0)

    p_hat = successes / n
    z = 1.96  # 95% confidence

    denominator = 1 + z**2 / n
    center = (p_hat + z**2 / (2 * n)) / denominator
    margin = z * math.sqrt((p_hat * (1 - p_hat) / n + z**2 / (4 * n**2))) / denominator

    lower = max(0.0, center - margin)
    upper = min(1.0, center + margin)

    return (lower, upper)


def mean_confidence_interval(values: List[float], confidence: float = 0.95) -> Tuple[float, float, float]:
    """Compute mean and confidence interval using t-distribution.

    Args:
        values: Sample values
        confidence: Confidence level

    Returns:
        (mean, ci_low, ci_high)
    """
    if not values:
        return (0.0, 0.0, 0.0)

    n = len(values)
    mean = sum(values) / n

    if n == 1:
        return (mean, mean, mean)

    # Sample variance
    variance = sum((x - mean) ** 2 for x in values) / (n - 1)
    std_error = math.sqrt(variance / n)

    # t-statistic for 95% CI (approximate for large n)
    # For n > 30, t ≈ 1.96
    # For small n, use conservative estimate
    if n > 30:
        t = 1.96
    elif n > 10:
        t = 2.228  # Approximate t for df=10
    else:
        t = 2.776  # Approximate t for df=5

    margin = t * std_error
    ci_low = mean - margin
    ci_high = mean + margin

    return (mean, ci_low, ci_high)


def compute_conditional_probabilities(trades: List[Trade], max_stop_count: int = 10) -> List[ConditionalStats]:
    """Compute conditional statistics by stop_count bucket.

    For each stop_count n, compute:
    - P(win | stop_count = n)
    - E[R | stop_count = n]
    - Confidence intervals
    - Sample size

    Args:
        trades: List of executed trades
        max_stop_count: Maximum stop_count to analyze

    Returns:
        List of ConditionalStats, one per stop_count bucket
    """
    # Group trades by stop_count_at_entry
    buckets: Dict[int, List[Trade]] = {}
    for trade in trades:
        n = trade.stop_count_at_entry
        if n > max_stop_count:
            continue
        if n not in buckets:
            buckets[n] = []
        buckets[n].append(trade)

    results = []

    for stop_count in range(max_stop_count + 1):
        if stop_count not in buckets or not buckets[stop_count]:
            # No data for this bucket
            results.append(ConditionalStats(
                stop_count=stop_count,
                n=0,
                num_wins=0,
                num_losses=0,
                p_win=0.0,
                p_win_ci_low=0.0,
                p_win_ci_high=0.0,
                mean_r=0.0,
                mean_r_ci_low=0.0,
                mean_r_ci_high=0.0,
                r_values=[]
            ))
            continue

        bucket_trades = buckets[stop_count]
        n = len(bucket_trades)

        # Count wins
        wins = [t for t in bucket_trades if t.pnl > 0]
        losses = [t for t in bucket_trades if t.pnl <= 0]
        num_wins = len(wins)
        num_losses = len(losses)

        # P(win | stop_count=n)
        p_win = num_wins / n if n > 0 else 0.0
        p_win_ci_low, p_win_ci_high = wilson_score_interval(num_wins, n)

        # E[R | stop_count=n]
        r_values = [t.r_multiple for t in bucket_trades]
        mean_r, mean_r_ci_low, mean_r_ci_high = mean_confidence_interval(r_values)

        results.append(ConditionalStats(
            stop_count=stop_count,
            n=n,
            num_wins=num_wins,
            num_losses=num_losses,
            p_win=p_win,
            p_win_ci_low=p_win_ci_low,
            p_win_ci_high=p_win_ci_high,
            mean_r=mean_r,
            mean_r_ci_low=mean_r_ci_low,
            mean_r_ci_high=mean_r_ci_high,
            r_values=r_values
        ))

    return results


def analyze_conditional_hypothesis(stats: List[ConditionalStats], min_total_trades: int = 20, min_bucket_size: int = 5) -> dict:
    """Analyze whether stop_count predicts outcome.

    Core hypothesis: P(win|n=k) increases with k (hazard rate hypothesis)

    Args:
        stats: Conditional statistics by stop_count
        min_total_trades: Minimum total trades required
        min_bucket_size: Minimum samples per bucket to consider valid

    Returns:
        Dictionary with hypothesis test results and interpretation
    """
    # Check total sample size
    total_trades = sum(s.n for s in stats)
    if total_trades < min_total_trades:
        return {
            "test": "INSUFFICIENT_DATA",
            "total_trades": total_trades,
            "min_required": min_total_trades,
            "result": f"Cannot test hypothesis: only {total_trades} trades (need {min_total_trades})",
            "recommendation": "Collect more data before drawing conclusions"
        }

    # Filter out buckets with insufficient sample size
    valid_buckets = [s for s in stats if s.n >= min_bucket_size]

    if len(valid_buckets) < 2:
        return {
            "test": "INSUFFICIENT_DATA",
            "valid_buckets": len(valid_buckets),
            "min_required": 2,
            "result": f"Cannot test hypothesis: fewer than 2 buckets with n >= {min_bucket_size}",
            "recommendation": "Null hypothesis (no predictive value) cannot be rejected"
        }

    # Simple trend test: does p_win increase with stop_count?
    p_win_values = [s.p_win for s in valid_buckets]
    stop_counts = [s.stop_count for s in valid_buckets]

    # Count increases vs decreases
    increases = sum(1 for i in range(len(p_win_values) - 1) if p_win_values[i+1] > p_win_values[i])
    decreases = sum(1 for i in range(len(p_win_values) - 1) if p_win_values[i+1] < p_win_values[i])

    # Check if confidence intervals overlap with baseline (n=0)
    baseline = stats[0] if stats[0].n > 0 else None

    overlaps = []
    if baseline and baseline.n >= min_bucket_size:
        for s in valid_buckets[1:]:
            # Do CIs overlap?
            overlap = not (s.p_win_ci_high < baseline.p_win_ci_low or s.p_win_ci_low > baseline.p_win_ci_high)
            overlaps.append(overlap)

    all_overlap = all(overlaps) if overlaps else True

    return {
        "test": "conditional_trend",
        "total_trades": total_trades,
        "valid_buckets": len(valid_buckets),
        "increases": increases,
        "decreases": decreases,
        "trend": "increasing" if increases > decreases else "decreasing" if decreases > increases else "flat",
        "all_cis_overlap_baseline": all_overlap,
        "interpretation": _interpret_conditional_test(increases, decreases, all_overlap, len(valid_buckets))
    }


def _interpret_conditional_test(increases: int, decreases: int, all_overlap: bool, n_buckets: int) -> str:
    """Interpret conditional probability test results."""
    if n_buckets < 3:
        return "Insufficient data to test hazard rate hypothesis (need at least 3 buckets with n>=5)"

    if all_overlap:
        return "No evidence that stop_count predicts win rate: all confidence intervals overlap with baseline"

    if increases > decreases * 2:
        return f"Weak evidence for hazard rate hypothesis: p_win increases in {increases}/{n_buckets-1} transitions, but interpret with caution (multiple comparisons not adjusted)"

    return "No consistent trend in p_win across stop_count buckets"


def compare_policies_paired(result_a: BacktestResult, result_b: BacktestResult) -> dict:
    """Paired comparison between two policies on the same trade events.

    Since A and B see the same trade events (only sizing differs),
    we can do a paired comparison of R-multiples.

    Args:
        result_a: Baseline policy result
        result_b: Test policy result

    Returns:
        Dictionary with comparison statistics
    """
    # Pair trades by event_id
    trades_a = {t.event_id: t for t in result_a.trades}
    trades_b = {t.event_id: t for t in result_b.trades}

    common_events = set(trades_a.keys()) & set(trades_b.keys())

    if not common_events:
        return {
            "error": "No common trade events between policies",
            "note": "This should not happen if policies use the same event stream"
        }

    # Paired differences in PnL
    differences = []
    for event_id in common_events:
        pnl_a = trades_a[event_id].pnl
        pnl_b = trades_b[event_id].pnl
        diff = pnl_b - pnl_a
        differences.append(diff)

    mean_diff = sum(differences) / len(differences)
    _, ci_low, ci_high = mean_confidence_interval(differences)

    # Total equity difference
    equity_diff = result_b.final_equity - result_a.final_equity
    return_diff = result_b.total_return - result_a.total_return

    return {
        "policy_a": result_a.policy_name,
        "policy_b": result_b.policy_name,
        "n_paired_trades": len(differences),
        "mean_pnl_diff": round(mean_diff, 2),
        "pnl_diff_ci_low": round(ci_low, 2),
        "pnl_diff_ci_high": round(ci_high, 2),
        "total_equity_diff": round(equity_diff, 2),
        "return_diff": round(return_diff, 4),
        "interpretation": _interpret_paired_comparison(mean_diff, ci_low, ci_high, result_a.policy_name, result_b.policy_name)
    }


def _interpret_paired_comparison(mean_diff: float, ci_low: float, ci_high: float, name_a: str, name_b: str) -> str:
    """Interpret paired comparison results."""
    if ci_low > 0:
        return f"{name_b} shows positive mean difference vs {name_a} (95% CI excludes 0)"
    elif ci_high < 0:
        return f"{name_a} shows positive mean difference vs {name_b} (95% CI excludes 0)"
    else:
        return f"No statistically significant difference between {name_a} and {name_b} (95% CI includes 0)"


def check_sample_adequacy(all_results: dict, min_total_trades: int = 20, min_placebo_seeds: int = 10) -> dict:
    """Check if sample size is adequate for statistical conclusions.

    Args:
        all_results: Dictionary of {scenario_name: {policy_name: BacktestResult}}
        min_total_trades: Minimum total trades required
        min_placebo_seeds: Minimum placebo seeds for G distribution

    Returns:
        Dictionary with adequacy check results
    """
    checks = {}

    for scenario_name, results in all_results.items():
        scenario_checks = {}

        # Check total trades
        if 'A' in results:
            total_trades = results['A'].num_trades
            scenario_checks['total_trades'] = {
                'value': total_trades,
                'adequate': total_trades >= min_total_trades,
                'threshold': min_total_trades
            }

        # Check placebo distribution (would need multiple G seeds)
        scenario_checks['placebo_distribution'] = {
            'implemented': False,
            'note': 'Single seed G used; multi-seed distribution not yet implemented',
            'threshold': min_placebo_seeds
        }

        # Overall adequacy for this scenario
        adequate = scenario_checks.get('total_trades', {}).get('adequate', False)
        scenario_checks['adequate'] = adequate
        scenario_checks['recommendation'] = (
            "Sample size adequate for preliminary analysis"
            if adequate else
            f"INSUFFICIENT_DATA: need at least {min_total_trades} trades for statistical conclusions"
        )

        checks[scenario_name] = scenario_checks

    return checks

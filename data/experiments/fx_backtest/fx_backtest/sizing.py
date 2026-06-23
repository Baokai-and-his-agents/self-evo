"""Position sizing policies: A/B/E/G.

All policies consume the same immutable trade event stream.
Only the position size calculation differs based on stop_count/state.
"""

from dataclasses import dataclass
from typing import List, Optional, Protocol
import random


@dataclass
class SizingContext:
    """Context information for sizing decision.

    Includes state variables that sizing policies may depend on.
    """
    event_id: int
    stop_count: int  # Consecutive stops since last win
    equity: float
    entry_price: float
    stop_price: float
    cumulative_loss: float = 0.0
    in_confirmed_trend: bool = False


class SizingPolicy(Protocol):
    """Protocol for position sizing policies."""

    def calculate_size(self, context: SizingContext) -> float:
        """Calculate position size (risk fraction of equity).

        Args:
            context: Current state and market context

        Returns:
            Risk fraction (e.g., 0.01 = 1% of equity at risk)
        """
        ...

    def reset(self):
        """Reset internal state (called after successful cycle or max stops)."""
        ...

    def get_name(self) -> str:
        """Return policy name."""
        ...


class FixedSizing:
    """A: Fixed risk repeated probes.

    Always risk the same fraction, regardless of stop count.
    """

    def __init__(self, risk_pct: float = 0.01):
        """Initialize fixed sizing.

        Args:
            risk_pct: Fixed risk per trade (default 1%)
        """
        self.risk_pct = risk_pct

    def calculate_size(self, context: SizingContext) -> float:
        """Return fixed risk fraction."""
        return self.risk_pct

    def reset(self):
        """No state to reset."""
        pass

    def get_name(self) -> str:
        return "A_Fixed"


class ArithmeticAfterLoss:
    """B: Bounded arithmetic sizing after losses.

    Risk increases arithmetically after each stop:
    r_n = min(r_0 + n * d, r_max)

    Resets to r_0 after a win or reaching K max stops.
    """

    def __init__(
        self,
        r_0: float = 0.01,
        d: float = 0.005,
        K: int = 5,
        r_max: float = 0.03,
        total_budget: float = 0.10
    ):
        """Initialize arithmetic sizing.

        Args:
            r_0: Initial risk per trade (1%)
            d: Increment per stop (0.5%)
            K: Maximum number of stops before reset
            r_max: Maximum risk per trade (3%)
            total_budget: Total risk budget before stopping (10%)
        """
        self.r_0 = r_0
        self.d = d
        self.K = K
        self.r_max = r_max
        self.total_budget = total_budget

    def calculate_size(self, context: SizingContext) -> float:
        """Calculate size based on stop count.

        Returns 0 only when budget exhausted (terminal condition).
        K cycles are handled by engine reset, not by returning 0.
        """
        n = context.stop_count

        # Budget exhausted (terminal)
        if context.cumulative_loss >= self.total_budget * context.equity:
            return 0.0

        # Normal sizing (even if n >= K, engine will handle reset)
        risk = min(self.r_0 + n * self.d, self.r_max)
        return risk

    def reset(self):
        """Reset called externally by engine after win or terminal failure."""
        pass

    def get_name(self) -> str:
        return "B_ArithmeticAfterLoss"


class ConfirmThenAmplify:
    """E: Fixed small probe + independent confirmation then one-time amplification.

    Start with small probe (0.5%). If independent confirmation signal triggers,
    amplify to larger size (2%).

    For MVP, "confirmation" is a simple rule: if profit >= 3.0 * initial_risk.
    This is NOT based on stop_count, so it's independent of the loss sequence.
    """

    def __init__(
        self,
        r_probe: float = 0.005,
        r_confirmed: float = 0.02,
        confirmation_r: float = 3.0
    ):
        """Initialize confirm-then-amplify sizing.

        Args:
            r_probe: Small probe risk (0.5%)
            r_confirmed: Amplified risk after confirmation (2%)
            confirmation_r: R multiple required for confirmation (3.0)
        """
        self.r_probe = r_probe
        self.r_confirmed = r_confirmed
        self.confirmation_r = confirmation_r
        self.confirmed = False

    def calculate_size(self, context: SizingContext) -> float:
        """Return probe or confirmed size.

        Note: In this simplified MVP, confirmation is checked externally
        by the engine based on current trade profit. The policy just
        returns the appropriate size based on state.
        """
        if context.in_confirmed_trend:
            return self.r_confirmed
        else:
            return self.r_probe

    def reset(self):
        """Reset confirmation state."""
        self.confirmed = False

    def get_name(self) -> str:
        return "E_ConfirmThenAmplify"


class PermutationPlacebo:
    """G: Placebo control - permute sizing values, not stop_count sequence.

    Key insight: G must see the SAME events as B (same event IDs, same multiset of
    risk fractions), but with the risk values shuffled across the valid event positions.

    This tests whether the TIMING of size increases matters, or only the DISTRIBUTION.

    CRITICAL: K (terminal condition) must NOT be permuted into position 0, which would
    truncate the event stream. We only permute the sizing values, not the control flow.
    """

    def __init__(
        self,
        r_0: float = 0.01,
        d: float = 0.005,
        K: int = 5,
        r_max: float = 0.03,
        total_budget: float = 0.10,
        seed: int = 42
    ):
        """Initialize permutation placebo.

        Args:
            r_0: Base risk (same as B)
            d: Increment (same as B)
            K: Max stops (same as B)
            r_max: Max risk (same as B)
            total_budget: Total risk budget (same as B)
            seed: Random seed for permutation
        """
        self.r_0 = r_0
        self.d = d
        self.K = K
        self.r_max = r_max
        self.total_budget = total_budget
        self.seed = seed

        # Pre-compute sizing values for stop_count 0..K-1
        # (K itself means cycle failure, handled by engine)
        self.risk_values = [min(self.r_0 + i * self.d, self.r_max) for i in range(self.K)]

        # Create permutation of these values
        self.permuted_risk_values = self._create_permutation()

    def _create_permutation(self) -> list:
        """Create deterministic permutation of risk values (not indices)."""
        random.seed(self.seed)
        permuted = self.risk_values.copy()
        random.shuffle(permuted)
        return permuted

    def calculate_size(self, context: SizingContext) -> float:
        """Calculate size using PERMUTED risk values.

        Budget check is same as B (terminal condition).
        K cycles are handled by engine reset, not by returning 0.
        """
        n = context.stop_count

        # Budget exhausted (terminal)
        if context.cumulative_loss >= self.total_budget * context.equity:
            return 0.0

        # If n >= K, return r_max (same behavior as B)
        # Engine will handle cycle reset
        if n >= self.K:
            return self.r_max

        # Return permuted risk value for this stop_count
        return self.permuted_risk_values[n]

    def reset(self):
        """No state to reset."""
        pass

    def get_name(self) -> str:
        return f"G_Placebo_seed{self.seed}"

    def get_risk_multiset(self) -> list:
        """Return the multiset of risk values (for verification)."""
        return self.permuted_risk_values.copy()


class ScheduledPermutationPlacebo:
    """G2: Schedule-based placebo - permute B's actual schedule.

    Takes B's realized schedule of (event_id, risk_fraction) pairs and
    shuffles both the order and the risk values independently using a seed.

    This creates a placebo that:
    1. Trades on the same event IDs as B (same multiset)
    2. Uses the same risk fractions as B (same multiset)
    3. But with shuffled timing - different risk on different events

    Used for post-hoc permutation test of B's actual realized trades.
    """

    def __init__(self, b_schedule: List[tuple], seed: int = 42):
        """Initialize schedule-based permutation placebo.

        Args:
            b_schedule: List of (event_id, risk_fraction) from B's actual trades
            seed: Random seed for permutation
        """
        if not b_schedule:
            raise ValueError("b_schedule cannot be empty")

        self.seed = seed
        self.original_schedule = b_schedule.copy()

        # Extract event IDs and risk fractions separately
        event_ids = [event_id for event_id, _ in b_schedule]
        risk_fractions = [risk for _, risk in b_schedule]

        # Shuffle both independently using the same seed
        rng = random.Random(seed)
        shuffled_event_ids = event_ids.copy()
        rng.shuffle(shuffled_event_ids)

        rng = random.Random(seed)
        shuffled_risks = risk_fractions.copy()
        rng.shuffle(shuffled_risks)

        # Create mapping from event_id to risk_fraction
        self.risk_by_event_id = dict(zip(shuffled_event_ids, shuffled_risks))

    def calculate_size(self, context: SizingContext) -> float:
        """Return scheduled risk for this event_id.

        Raises:
            ValueError: If event_id not in schedule (should never happen if
                        schedule was built from the same event stream)
        """
        if context.event_id not in self.risk_by_event_id:
            raise ValueError(
                f"Event ID {context.event_id} not found in schedule. "
                f"This means the schedule was not built from the same event stream."
            )

        return self.risk_by_event_id[context.event_id]

    def reset(self):
        """No state to reset - schedule is pre-determined."""
        pass

    def get_name(self) -> str:
        return f"G_ScheduledPlacebo_seed{self.seed}"

    def get_risk_multiset(self) -> list:
        """Return the multiset of risk values (for verification)."""
        return sorted(self.risk_by_event_id.values())


def create_default_policies() -> dict:
    """Create default A/B/E/G policies with MVP parameters.

    Returns:
        Dictionary mapping policy name to policy instance
    """
    return {
        "A": FixedSizing(risk_pct=0.01),
        "B": ArithmeticAfterLoss(r_0=0.01, d=0.005, K=5, r_max=0.03, total_budget=0.10),
        "E": ConfirmThenAmplify(r_probe=0.005, r_confirmed=0.02, confirmation_r=3.0),
        "G": PermutationPlacebo(r_0=0.01, d=0.005, K=5, r_max=0.03, total_budget=0.10, seed=42)
    }


def create_multi_seed_placebo(num_seeds: int = 10, base_seed: int = 42, r_0: float = 0.01, d: float = 0.005, K: int = 5, r_max: float = 0.03, total_budget: float = 0.10) -> List[PermutationPlacebo]:
    """Create multiple placebo policies with different seeds.

    For permutation test: run B against multiple G instances to build
    null distribution.

    Args:
        num_seeds: Number of different seeds
        base_seed: Starting seed value
        r_0: Base risk (same as B)
        d: Increment (same as B)
        K: Max stops (same as B)
        r_max: Max risk (same as B)
        total_budget: Total risk budget (same as B)

    Returns:
        List of placebo policies with different seeds
    """
    return [
        PermutationPlacebo(r_0=r_0, d=d, K=K, r_max=r_max, total_budget=total_budget, seed=base_seed + i)
        for i in range(num_seeds)
    ]

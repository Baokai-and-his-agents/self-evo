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
        """Calculate size based on stop count."""
        n = context.stop_count

        # Reached max stops or budget exhausted
        if n >= self.K or context.cumulative_loss >= self.total_budget * context.equity:
            return 0.0  # Stop trading

        # Arithmetic progression
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
    """G: Placebo control - permute stop_count -> size mapping.

    Uses the same sizing function as B (arithmetic progression),
    but with stop_count randomly shuffled.

    This tests whether the TIMING of size increases matters, or only
    the DISTRIBUTION of sizes.
    """

    def __init__(
        self,
        r_0: float = 0.01,
        d: float = 0.005,
        K: int = 5,
        r_max: float = 0.03,
        seed: int = 42
    ):
        """Initialize permutation placebo.

        Args:
            r_0: Base risk (same as B)
            d: Increment (same as B)
            K: Max stops (same as B)
            r_max: Max risk (same as B)
            seed: Random seed for permutation
        """
        self.r_0 = r_0
        self.d = d
        self.K = K
        self.r_max = r_max
        self.seed = seed

        # Create permutation map: actual stop_count -> permuted stop_count
        self.permutation_map = self._create_permutation()

    def _create_permutation(self) -> dict:
        """Create deterministic permutation of stop_count values."""
        random.seed(self.seed)
        values = list(range(self.K + 1))
        permuted = values.copy()
        random.shuffle(permuted)

        return {original: permuted[i] for i, original in enumerate(values)}

    def calculate_size(self, context: SizingContext) -> float:
        """Calculate size using PERMUTED stop_count."""
        actual_n = context.stop_count
        permuted_n = self.permutation_map.get(actual_n, actual_n)

        # Use B's arithmetic sizing formula with permuted n
        if permuted_n >= self.K:
            return 0.0

        risk = min(self.r_0 + permuted_n * self.d, self.r_max)
        return risk

    def reset(self):
        """No state to reset."""
        pass

    def get_name(self) -> str:
        return f"G_Placebo_seed{self.seed}"

    def get_permutation_map(self) -> dict:
        """Return the permutation map for inspection."""
        return self.permutation_map.copy()


def create_default_policies() -> dict:
    """Create default A/B/E/G policies with MVP parameters.

    Returns:
        Dictionary mapping policy name to policy instance
    """
    return {
        "A": FixedSizing(risk_pct=0.01),
        "B": ArithmeticAfterLoss(r_0=0.01, d=0.005, K=5, r_max=0.03, total_budget=0.10),
        "E": ConfirmThenAmplify(r_probe=0.005, r_confirmed=0.02, confirmation_r=3.0),
        "G": PermutationPlacebo(r_0=0.01, d=0.005, K=5, r_max=0.03, seed=42)
    }


def create_multi_seed_placebo(num_seeds: int = 10, base_seed: int = 42) -> List[PermutationPlacebo]:
    """Create multiple placebo policies with different seeds.

    For permutation test: run B against multiple G instances to build
    null distribution.

    Args:
        num_seeds: Number of different seeds
        base_seed: Starting seed value

    Returns:
        List of placebo policies with different seeds
    """
    return [
        PermutationPlacebo(r_0=0.01, d=0.005, K=5, r_max=0.03, seed=base_seed + i)
        for i in range(num_seeds)
    ]

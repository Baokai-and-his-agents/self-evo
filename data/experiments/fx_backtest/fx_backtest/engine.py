"""Backtest engine: execute trades with sizing policies, track equity and costs.

Core principle: All sizing policies see the same trade events.
Only position size differs based on policy logic.
"""

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

from .signals import TradeEvent
from .sizing import SizingPolicy, SizingContext


@dataclass
class Trade:
    """Executed trade with sizing applied."""

    event_id: int
    timestamp: datetime
    entry_price: float
    exit_price: float
    stop_price: float
    risk_fraction: float  # Fraction of equity at risk
    position_size: float  # Actual position size in base currency units (EUR for EURUSD)
    initial_risk: float  # Dollar risk = risk_fraction * equity
    pnl: float  # Dollar profit/loss (after costs)
    r_multiple: float  # PnL / initial_risk
    hit_stop: bool
    bars_held: int
    stop_count_at_entry: int  # Stop count when this trade entered
    equity_before: float
    equity_after: float
    cost: float = 0.0
    # E policy two-phase tracking (None for A/B/G single-phase trades)
    probe_risk: Optional[float] = None
    probe_units: Optional[float] = None
    probe_notional: Optional[float] = None
    probe_pnl: Optional[float] = None
    probe_cost: Optional[float] = None
    amplified_risk: Optional[float] = None
    amplified_units: Optional[float] = None
    amplified_notional: Optional[float] = None
    amplified_pnl: Optional[float] = None
    amplified_cost: Optional[float] = None

    def to_dict(self) -> dict:
        """Convert an executed trade to a JSON-safe dictionary."""
        data = dict(self.__dict__)
        data["timestamp"] = self.timestamp.isoformat()
        return data


@dataclass
class CostModel:
    """Transaction cost model for EURUSD.

    EURUSD specific:
    - Base currency: EUR
    - Quote currency: USD (also account currency)
    - Contract size: 100,000 EUR per standard lot
    - Pip size: 0.0001 (fourth decimal place)
    - Pip value: $10 per pip per standard lot
    """

    spread_pips: float = 0.0  # Bid-ask spread in pips
    commission_per_lot: float = 0.0  # Commission per standard lot (round-trip)
    slippage_pips: float = 0.0  # Average slippage in pips

    def calculate_cost(self, position_units: float, entry_price: float, exit_price: float) -> float:
        """Calculate total transaction cost for round-trip trade in USD.

        Args:
            position_units: Position size in base currency units (EUR for EURUSD)
            entry_price: Entry price (USD per EUR)
            exit_price: Exit price (USD per EUR)

        Returns:
            Total cost in USD (account currency)
        """
        # Convert units to standard lots (1 lot = 100,000 EUR)
        standard_lots = abs(position_units) / 100000.0

        # Pip value: $10 per pip per standard lot for EURUSD
        pip_value_per_lot = 10.0

        # Spread cost (paid on entry + exit = 2x)
        spread_cost = 2 * self.spread_pips * pip_value_per_lot * standard_lots

        # Commission (round-trip)
        commission_cost = self.commission_per_lot * standard_lots

        # Slippage (entry + exit = 2x)
        slippage_cost = 2 * self.slippage_pips * pip_value_per_lot * standard_lots

        return spread_cost + commission_cost + slippage_cost


@dataclass
class BacktestResult:
    """Results from running one sizing policy on trade events."""

    policy_name: str
    initial_equity: float
    final_equity: float
    trades: List[Trade] = field(default_factory=list)
    equity_curve: List[tuple] = field(default_factory=list)  # [(timestamp, equity)]

    # Summary statistics
    total_return: float = 0.0
    num_trades: int = 0
    num_wins: int = 0
    num_losses: int = 0
    win_rate: float = 0.0
    avg_win: float = 0.0
    avg_loss: float = 0.0
    avg_r: float = 0.0
    max_drawdown: float = 0.0
    max_drawdown_pct: float = 0.0

    # Cycle statistics
    num_cycles: int = 0
    num_cycle_failures: int = 0
    max_stop_count_reached: int = 0

    def compute_statistics(self):
        """Compute summary statistics from trades."""
        if not self.trades:
            return

        self.num_trades = len(self.trades)
        self.total_return = (self.final_equity / self.initial_equity) - 1.0

        wins = [t for t in self.trades if t.pnl > 0]
        losses = [t for t in self.trades if t.pnl <= 0]

        self.num_wins = len(wins)
        self.num_losses = len(losses)
        self.win_rate = self.num_wins / self.num_trades if self.num_trades > 0 else 0.0

        self.avg_win = sum(t.pnl for t in wins) / len(wins) if wins else 0.0
        self.avg_loss = sum(t.pnl for t in losses) / len(losses) if losses else 0.0
        self.avg_r = sum(t.r_multiple for t in self.trades) / self.num_trades if self.num_trades > 0 else 0.0

        # Max drawdown
        peak_equity = self.initial_equity
        max_dd = 0.0
        max_dd_pct = 0.0

        for timestamp, equity in self.equity_curve:
            if equity > peak_equity:
                peak_equity = equity

            drawdown = peak_equity - equity
            drawdown_pct = drawdown / peak_equity if peak_equity > 0 else 0.0

            if drawdown > max_dd:
                max_dd = drawdown
                max_dd_pct = drawdown_pct

        self.max_drawdown = max_dd
        self.max_drawdown_pct = max_dd_pct

    def compute_additional_metrics(self):
        """Compute additional metrics: log wealth, volatility, CVaR, turnover, etc."""
        if not self.trades:
            return {}

        import math

        # Terminal log wealth and mean log increment
        terminal_log_wealth = math.log(self.final_equity / self.initial_equity) if self.final_equity > 0 else -float('inf')
        mean_log_increment = terminal_log_wealth / self.num_trades if self.num_trades > 0 else 0.0

        # Arithmetic expectancy (mean PnL per trade)
        arithmetic_expectancy = sum(t.pnl for t in self.trades) / self.num_trades if self.num_trades > 0 else 0.0

        # Returns per trade (as fraction of equity at entry)
        returns = [t.pnl / t.equity_before for t in self.trades if t.equity_before > 0]

        # Volatility (standard deviation of returns)
        if len(returns) > 1:
            mean_return = sum(returns) / len(returns)
            variance = sum((r - mean_return) ** 2 for r in returns) / (len(returns) - 1)
            volatility = math.sqrt(variance)
        else:
            volatility = 0.0

        # Downside deviation (only negative returns)
        negative_returns = [r for r in returns if r < 0]
        if len(negative_returns) > 1:
            mean_negative = sum(negative_returns) / len(negative_returns)
            downside_variance = sum((r - mean_negative) ** 2 for r in negative_returns) / (len(negative_returns) - 1)
            downside_deviation = math.sqrt(downside_variance)
        else:
            downside_deviation = 0.0

        # CVaR (Conditional Value at Risk) - 5% worst tail
        sorted_returns = sorted(returns)
        tail_size = max(1, int(len(sorted_returns) * 0.05))
        worst_tail = sorted_returns[:tail_size]
        cvar_5pct = sum(worst_tail) / len(worst_tail) if worst_tail else 0.0

        # Turnover uses both E phases because each phase is separately traded.
        total_position_value = 0.0
        for t in self.trades:
            if t.probe_notional is not None or t.amplified_notional is not None:
                total_position_value += abs(t.probe_notional or 0.0)
                total_position_value += abs(t.amplified_notional or 0.0)
            else:
                total_position_value += abs(t.position_size * t.entry_price)

        turnover = total_position_value / self.initial_equity if self.initial_equity > 0 else 0.0

        # Total transaction cost
        total_cost = sum(t.cost for t in self.trades)

        # E replaces the probe at confirmation, so phase exposures are sequential.
        exposures = []
        for t in self.trades:
            if t.equity_before > 0:
                if t.probe_notional is not None or t.amplified_notional is not None:
                    probe_exposure = abs(t.probe_notional or 0.0)
                    amplified_exposure = abs(t.amplified_notional or 0.0)
                    exposures.extend([
                        probe_exposure / t.equity_before,
                        amplified_exposure / t.equity_before,
                    ])
                else:
                    exposure = abs(t.position_size * t.entry_price) / t.equity_before
                    exposures.append(exposure)

        avg_exposure = sum(exposures) / len(exposures) if exposures else 0.0
        max_exposure = max(exposures) if exposures else 0.0

        # Risk budget utilization (total initial risk / initial equity)
        total_initial_risk = sum(t.initial_risk for t in self.trades)
        risk_budget_utilization = total_initial_risk / self.initial_equity if self.initial_equity > 0 else 0.0

        return {
            "terminal_log_wealth": terminal_log_wealth,
            "mean_log_increment": mean_log_increment,
            "arithmetic_expectancy": arithmetic_expectancy,
            "volatility": volatility,
            "downside_deviation": downside_deviation,
            "cvar_5pct": cvar_5pct,
            "turnover": turnover,
            "total_cost": total_cost,
            "avg_exposure": avg_exposure,
            "max_exposure": max_exposure,
            "risk_budget_utilization": risk_budget_utilization,
            "num_cycles": self.num_cycles,
            "num_cycle_failures": self.num_cycle_failures
        }

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "policy_name": self.policy_name,
            "initial_equity": self.initial_equity,
            "final_equity": self.final_equity,
            "total_return": self.total_return,
            "num_trades": self.num_trades,
            "num_wins": self.num_wins,
            "num_losses": self.num_losses,
            "win_rate": self.win_rate,
            "avg_win": self.avg_win,
            "avg_loss": self.avg_loss,
            "avg_r": self.avg_r,
            "max_drawdown": self.max_drawdown,
            "max_drawdown_pct": self.max_drawdown_pct,
            "num_cycles": self.num_cycles,
            "num_cycle_failures": self.num_cycle_failures,
            "max_stop_count_reached": self.max_stop_count_reached,
            "additional_metrics": self.compute_additional_metrics(),
            "trades": [trade.to_dict() for trade in self.trades]
        }


class BacktestEngine:
    """Execute backtest with a sizing policy on trade events."""

    def __init__(
        self,
        initial_equity: float = 100000.0,
        cost_model: Optional[CostModel] = None
    ):
        """Initialize backtest engine.

        Args:
            initial_equity: Starting equity
            cost_model: Transaction cost model (default: zero cost)
        """
        self.initial_equity = initial_equity
        self.cost_model = cost_model or CostModel()

    def run(
        self,
        trade_events: List[TradeEvent],
        sizing_policy: SizingPolicy
    ) -> BacktestResult:
        """Run backtest with given sizing policy.

        Args:
            trade_events: Immutable list of trade events
            sizing_policy: Sizing policy to apply

        Returns:
            BacktestResult with trades and equity curve
        """
        result = BacktestResult(
            policy_name=sizing_policy.get_name(),
            initial_equity=self.initial_equity,
            final_equity=self.initial_equity
        )

        equity = self.initial_equity
        stop_count = 0
        cumulative_loss = 0.0

        result.equity_curve.append((trade_events[0].timestamp if trade_events else datetime.now(), equity))

        for event in trade_events:
            policy_max_k = getattr(sizing_policy, 'K', None)
            policy_budget = getattr(sizing_policy, 'total_budget', None)
            reached_k = policy_max_k is not None and stop_count >= policy_max_k
            reached_budget = (
                policy_budget is not None
                and cumulative_loss >= policy_budget * equity
            )
            if reached_k or reached_budget:
                result.num_cycle_failures += 1
                result.max_stop_count_reached = max(
                    result.max_stop_count_reached,
                    stop_count
                )
                stop_count = 0
                cumulative_loss = 0.0
                sizing_policy.reset()

            # Handle E policy with confirmation: split into probe + amplified phases
            if event.has_confirmation() and sizing_policy.get_name().startswith("E_"):
                # Phase 1: Entry -> Confirmation (probe sizing)
                stop_distance = event.entry_price - event.stop_price
                risk_per_unit = stop_distance

                context_probe = SizingContext(
                    event_id=event.event_id,
                    stop_count=stop_count,
                    equity=equity,
                    entry_price=event.entry_price,
                    stop_price=event.stop_price,
                    cumulative_loss=cumulative_loss,
                    in_confirmed_trend=False  # Not confirmed yet
                )

                risk_fraction_probe = sizing_policy.calculate_size(context_probe)
                initial_risk_probe = equity * risk_fraction_probe
                position_size_probe = initial_risk_probe / risk_per_unit if risk_per_unit > 0 else 0.0

                # PnL for phase 1: entry -> confirmation
                pnl_probe_before_cost = position_size_probe * (event.confirmation_price - event.entry_price)
                cost_probe = self.cost_model.calculate_cost(position_size_probe, event.entry_price, event.confirmation_price)
                pnl_probe = pnl_probe_before_cost - cost_probe

                equity += pnl_probe

                # Phase 2: Confirmation -> Exit (amplified sizing)
                # Recalculate risk_per_unit for amplified phase using confirmation_price as entry
                amplified_stop_distance = event.confirmation_price - event.stop_price
                amplified_risk_per_unit = amplified_stop_distance

                context_amplified = SizingContext(
                    event_id=event.event_id,
                    stop_count=stop_count,
                    equity=equity,
                    entry_price=event.confirmation_price,  # Re-entry at confirmation price
                    stop_price=event.stop_price,
                    cumulative_loss=cumulative_loss,
                    in_confirmed_trend=True  # Confirmed
                )

                risk_fraction_amplified = sizing_policy.calculate_size(context_amplified)
                initial_risk_amplified = equity * risk_fraction_amplified
                position_size_amplified = initial_risk_amplified / amplified_risk_per_unit if amplified_risk_per_unit > 0 else 0.0

                # PnL for phase 2: confirmation -> exit
                pnl_amplified_before_cost = position_size_amplified * (event.exit_price - event.confirmation_price)
                cost_amplified = self.cost_model.calculate_cost(position_size_amplified, event.confirmation_price, event.exit_price)
                pnl_amplified = pnl_amplified_before_cost - cost_amplified

                # Total PnL and cost
                pnl = pnl_probe + pnl_amplified
                cost = cost_probe + cost_amplified
                initial_risk = initial_risk_probe + initial_risk_amplified

                equity_before = equity - pnl_probe
                equity += pnl_amplified
                equity_after = equity

                # Use amplified position size for recording (actual final exposure)
                position_size = position_size_amplified
                risk_fraction = risk_fraction_amplified

            else:
                # Standard single-phase execution (A/B/G or E without confirmation)
                stop_distance = event.entry_price - event.stop_price
                risk_per_unit = stop_distance

                context = SizingContext(
                    event_id=event.event_id,
                    stop_count=stop_count,
                    equity=equity,
                    entry_price=event.entry_price,
                    stop_price=event.stop_price,
                    cumulative_loss=cumulative_loss,
                    in_confirmed_trend=False
                )

                # Get risk fraction from policy
                risk_fraction = sizing_policy.calculate_size(context)

                if risk_fraction <= 0.0:
                    raise ValueError(
                        f"{sizing_policy.get_name()} returned non-positive risk "
                        f"for event {event.event_id}"
                    )

                # Calculate position size
                initial_risk = equity * risk_fraction
                position_size = initial_risk / risk_per_unit if risk_per_unit > 0 else 0.0

                # Calculate PnL: position_size * (exit_price - entry_price)
                if event.exit_price is not None:
                    pnl_before_cost = position_size * (event.exit_price - event.entry_price)
                else:
                    pnl_before_cost = 0.0

                # Apply transaction costs
                cost = self.cost_model.calculate_cost(position_size, event.entry_price, event.exit_price)
                pnl = pnl_before_cost - cost

                # Update equity
                equity_before = equity
                equity += pnl
                equity_after = equity

            # Calculate R-multiple
            r_multiple = pnl / initial_risk if initial_risk > 0 else 0.0

            # Create trade record with optional two-phase data for E policy
            if event.has_confirmation() and sizing_policy.get_name().startswith("E_"):
                # E policy with confirmation: record both phases
                trade = Trade(
                    event_id=event.event_id,
                    timestamp=event.timestamp,
                    entry_price=event.entry_price,
                    exit_price=event.exit_price,
                    stop_price=event.stop_price,
                    risk_fraction=risk_fraction,
                    position_size=position_size,
                    initial_risk=initial_risk,
                    pnl=pnl,
                    r_multiple=r_multiple,
                    hit_stop=event.hit_stop,
                    bars_held=event.bars_held,
                    stop_count_at_entry=stop_count,
                    equity_before=equity_before,
                    equity_after=equity_after,
                    cost=cost,
                    probe_risk=initial_risk_probe,
                    probe_units=position_size_probe,
                    probe_notional=position_size_probe * event.entry_price,
                    probe_pnl=pnl_probe,
                    probe_cost=cost_probe,
                    amplified_risk=initial_risk_amplified,
                    amplified_units=position_size_amplified,
                    amplified_notional=position_size_amplified * event.confirmation_price,
                    amplified_pnl=pnl_amplified,
                    amplified_cost=cost_amplified
                )
            else:
                # Single-phase trade (A/B/G or E without confirmation)
                trade = Trade(
                    event_id=event.event_id,
                    timestamp=event.timestamp,
                    entry_price=event.entry_price,
                    exit_price=event.exit_price,
                    stop_price=event.stop_price,
                    risk_fraction=risk_fraction,
                    position_size=position_size,
                    initial_risk=initial_risk,
                    pnl=pnl,
                    r_multiple=r_multiple,
                    hit_stop=event.hit_stop,
                    bars_held=event.bars_held,
                    stop_count_at_entry=stop_count,
                    equity_before=equity_before,
                    equity_after=equity_after,
                    cost=cost
                )
            result.trades.append(trade)
            result.equity_curve.append((event.timestamp, equity))

            # Update stop count and cycle state
            if event.hit_stop:
                stop_count += 1
                cumulative_loss += abs(pnl) if pnl < 0 else 0.0
            else:
                # Win or breakeven: reset after successful trade
                if pnl > 0:
                    stop_count = 0
                    cumulative_loss = 0.0
                    sizing_policy.reset()
                    result.num_cycles += 1

        result.final_equity = equity
        result.compute_statistics()

        return result

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
    position_size: float  # Actual position size (units)
    initial_risk: float  # Dollar risk = risk_fraction * equity
    pnl: float  # Dollar profit/loss
    r_multiple: float  # PnL / initial_risk
    hit_stop: bool
    bars_held: int
    stop_count_at_entry: int  # Stop count when this trade entered
    equity_before: float
    equity_after: float
    cost: float = 0.0


@dataclass
class CostModel:
    """Transaction cost model."""

    spread_pips: float = 0.0  # Bid-ask spread in pips
    commission_per_lot: float = 0.0  # Commission per standard lot
    slippage_pips: float = 0.0  # Average slippage
    pip_value: float = 10.0  # Dollar value of 1 pip for 1 standard lot

    def calculate_cost(self, position_size: float, entry_price: float, exit_price: float) -> float:
        """Calculate total transaction cost for round-trip trade.

        Args:
            position_size: Position size in lots
            entry_price: Entry price
            exit_price: Exit price

        Returns:
            Total cost in dollars
        """
        # Spread cost (entry + exit)
        spread_cost = 2 * self.spread_pips * self.pip_value * abs(position_size)

        # Commission (entry + exit)
        commission_cost = 2 * self.commission_per_lot * abs(position_size)

        # Slippage
        slippage_cost = 2 * self.slippage_pips * self.pip_value * abs(position_size)

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
            "max_stop_count_reached": self.max_stop_count_reached
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
        in_confirmed_trend = False

        result.equity_curve.append((trade_events[0].timestamp if trade_events else datetime.now(), equity))

        for event in trade_events:
            # Build sizing context
            stop_distance = event.entry_price - event.stop_price
            risk_per_unit = stop_distance

            context = SizingContext(
                event_id=event.event_id,
                stop_count=stop_count,
                equity=equity,
                entry_price=event.entry_price,
                stop_price=event.stop_price,
                cumulative_loss=cumulative_loss,
                in_confirmed_trend=in_confirmed_trend
            )

            # Get risk fraction from policy
            risk_fraction = sizing_policy.calculate_size(context)

            # If policy returns 0, stop trading (reached K or budget)
            if risk_fraction <= 0.0:
                result.max_stop_count_reached = stop_count
                break

            # Calculate position size
            initial_risk = equity * risk_fraction
            position_size = initial_risk / risk_per_unit if risk_per_unit > 0 else 0.0

            # Calculate PnL from event's raw_r
            if event.raw_r is not None:
                pnl_before_cost = initial_risk * (event.raw_r / abs(event.raw_r / ((event.exit_price / event.entry_price) - 1))) if event.raw_r != 0 else 0.0
                # Simplified: PnL = position_size * (exit_price - entry_price)
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

            # Create trade record
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
                # Win or breakeven: check for confirmation or reset
                if r_multiple >= 3.0:  # Confirmation threshold for E policy
                    in_confirmed_trend = True

                # Reset after successful trade
                if pnl > 0:
                    stop_count = 0
                    cumulative_loss = 0.0
                    in_confirmed_trend = False
                    sizing_policy.reset()
                    result.num_cycles += 1

            # Check if reached max stop count (cycle failure)
            policy_max_k = getattr(sizing_policy, 'K', None)
            if policy_max_k and stop_count >= policy_max_k:
                result.num_cycle_failures += 1
                stop_count = 0
                cumulative_loss = 0.0
                sizing_policy.reset()

        result.final_equity = equity
        result.compute_statistics()

        return result

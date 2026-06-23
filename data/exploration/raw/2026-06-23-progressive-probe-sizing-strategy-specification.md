# Progressive Probe Position Sizing - Strategy Specification

**Date:** 2026-06-23
**Worker:** scout-worker-fx-sizing-01
**Run ID:** 2026-06-23-fx-sizing-001

---

## 1. 状态机定义

### 1.1 状态空间

```
States = {IDLE, PROBE, CONFIRMED, TERMINAL_SUCCESS, TERMINAL_FAILURE}
```

**IDLE（空闲）：**
- 初始状态，无持仓
- 等待 entry signal
- n = 0（连续止损计数器归零）

**PROBE（震荡试探）：**
- 已入场，试探性仓位
- 仓位大小：r_n = min(r_0 + n × d, r_max)（算术递增）
- 或：r_n = min(r_0 × m^n, r_max)（几何递增）
- 累计止损次数：n ∈ [0, K]

**CONFIRMED（趋势确认）：**
- 当前持仓盈利 >= R_confirm × r_n
- 趋势被认为建立
- 可选：继续加仓（pyramiding）或保持

**TERMINAL_SUCCESS（成功完成）：**
- 总盈利 >= 目标 R × 初始风险
- 退出持仓，重置状态到 IDLE
- n = 0

**TERMINAL_FAILURE（失败终止）：**
- n >= K（达到最大档位）
- 或累计亏损 >= 总风险预算
- 退出所有持仓，重置到 IDLE 或进入冷却期
- n = 0

### 1.2 转移规则

```
IDLE → PROBE:
  条件: Entry signal 触发
  动作: 开仓 r_0，n = 0

PROBE → PROBE (止损递增):
  条件: 当前持仓止损触发，n < K，累计亏损 < Budget
  动作: n += 1，开新仓 r_n

PROBE → CONFIRMED:
  条件: 当前持仓盈利 >= R_confirm × r_n
  动作: 标记趋势确认，可选加仓

PROBE → TERMINAL_FAILURE:
  条件: n >= K 或累计亏损 >= Budget
  动作: 清仓，n = 0，进入 IDLE 或冷却期

CONFIRMED → TERMINAL_SUCCESS:
  条件: 总盈利 >= R_target
  动作: 平仓获利，n = 0，回到 IDLE

CONFIRMED → TERMINAL_FAILURE:
  条件: 趋势反转，触及 trailing stop
  动作: 平仓，n = 0，回到 IDLE

TERMINAL_* → IDLE:
  条件: 自动转移（成功或失败后）
  动作: 重置所有状态变量
```

### 1.3 状态变量

```python
# 持久状态
state: State = IDLE
n: int = 0  # 连续止损次数
cumulative_loss: float = 0.0  # 累计亏损
total_risk_budget: float = 0.10  # 10% 权益
entry_history: List[Entry] = []  # 入场记录

# 仓位参数
r_0: float = 0.01  # 初始风险（1% 权益）
d: float = 0.005  # 算术递增步长（0.5%）
m: float = 1.5  # 几何递增倍数
K: int = 5  # 最大档位
r_max: float = r_0 + K * d  # 或 r_0 * m^K

# 确认参数
R_confirm: float = 3.0  # 趋势确认所需 R 倍数
R_target: float = 5.0  # 总目标 R 倍数
```

---

## 2. 伪代码实现

### 2.1 主循环

```python
def run_progressive_probe_strategy(market_data, initial_equity):
    """
    Progressive Probe Position Sizing Strategy

    WARNING: This strategy is experimental and carries high risk.
    Core assumption (stop-loss sequences predict trend) is NOT supported by evidence.
    """

    # 初始化
    state = State.IDLE
    n = 0
    cumulative_loss = 0.0
    equity = initial_equity
    positions = []

    for bar in market_data:
        # 状态机主逻辑
        if state == State.IDLE:
            if entry_signal(bar):
                state = State.PROBE
                n = 0
                cumulative_loss = 0.0
                position = open_position(
                    size=calculate_position_size(equity, r_0, bar.atr),
                    stop_loss=bar.price - 2 * bar.atr,
                    entry_price=bar.price
                )
                positions.append(position)
                log(f"IDLE -> PROBE: Open {position.size} at {bar.price}")

        elif state == State.PROBE:
            # 检查现有仓位
            for pos in positions:
                pnl = pos.calculate_pnl(bar.price)

                # 止损触发
                if bar.price <= pos.stop_loss:
                    cumulative_loss += abs(pnl)
                    close_position(pos)
                    positions.remove(pos)

                    # 判断是否继续递增
                    if n >= K:
                        state = State.TERMINAL_FAILURE
                        log(f"PROBE -> TERMINAL_FAILURE: Reached max retries K={K}")
                        break

                    if cumulative_loss >= total_risk_budget * equity:
                        state = State.TERMINAL_FAILURE
                        log(f"PROBE -> TERMINAL_FAILURE: Budget exhausted")
                        break

                    # 递增仓位
                    n += 1
                    new_size = calculate_position_size(
                        equity,
                        min(r_0 + n * d, r_max),  # 算术递增
                        bar.atr
                    )
                    new_position = open_position(
                        size=new_size,
                        stop_loss=bar.price - 2 * bar.atr,
                        entry_price=bar.price
                    )
                    positions.append(new_position)
                    log(f"Stop loss #{n}: Open larger {new_size} at {bar.price}")

                # 趋势确认
                elif pnl >= R_confirm * pos.initial_risk:
                    state = State.CONFIRMED
                    log(f"PROBE -> CONFIRMED: Profit {pnl:.2f}, R={pnl/pos.initial_risk:.2f}")
                    break

        elif state == State.CONFIRMED:
            # 检查目标达成
            total_pnl = sum(pos.calculate_pnl(bar.price) for pos in positions)

            if total_pnl >= R_target * r_0 * equity:
                for pos in positions:
                    close_position(pos)
                positions.clear()
                equity += total_pnl
                state = State.IDLE
                log(f"CONFIRMED -> TERMINAL_SUCCESS: Total profit {total_pnl:.2f}")

            # 检查反转（trailing stop）
            elif any(bar.price <= pos.trailing_stop for pos in positions):
                for pos in positions:
                    close_position(pos)
                total_pnl = sum(pos.pnl for pos in positions)
                positions.clear()
                equity += total_pnl
                state = State.IDLE
                log(f"CONFIRMED -> IDLE: Trailing stop hit, profit {total_pnl:.2f}")

        elif state == State.TERMINAL_FAILURE:
            # 清仓
            for pos in positions:
                close_position(pos)
            positions.clear()
            state = State.IDLE
            log(f"TERMINAL_FAILURE -> IDLE: Reset after failure")

    return equity, positions
```

### 2.2 辅助函数

```python
def calculate_position_size(equity, risk_pct, atr):
    """
    计算仓位大小（volatility-normalized）

    Args:
        equity: 当前权益
        risk_pct: 风险百分比（如 0.01 = 1%）
        atr: Average True Range（波动率代理）

    Returns:
        position_size: 仓位大小（单位：lots 或 contracts）
    """
    risk_amount = equity * risk_pct
    stop_distance = 2 * atr  # 2 ATR 止损

    # Forex: position_size = risk_amount / (stop_distance * pip_value)
    # Futures: position_size = risk_amount / (stop_distance * point_value)

    position_size = risk_amount / (stop_distance * pip_value)

    return round_to_lot_size(position_size)


def entry_signal(bar):
    """
    入场信号（示例：20-day breakout）

    实际实现应基于具体策略，如：
    - Donchian channel breakout
    - Moving average crossover
    - Support/resistance breakout
    """
    return bar.price > bar.high_20_day


def open_position(size, stop_loss, entry_price):
    """
    开仓
    """
    position = Position(
        size=size,
        entry_price=entry_price,
        stop_loss=stop_loss,
        trailing_stop=None,  # 初始无 trailing stop
        initial_risk=abs(entry_price - stop_loss) * size
    )
    return position


def close_position(position):
    """
    平仓
    """
    position.exit_price = current_market_price()
    position.pnl = (position.exit_price - position.entry_price) * position.size
    log(f"Close position: PnL = {position.pnl:.2f}")
```

---

## 3. 关键参数配置

### 3.1 实验参数网格（非推荐值）

```python
# 初始风险
r_0_grid = [0.005, 0.01, 0.02]  # 0.5%, 1%, 2%

# 算术递增步长
d_grid = [0.0025, 0.005, 0.01]  # 0.25%, 0.5%, 1%

# 几何递增倍数
m_grid = [1.5, 2.0]

# 最大档位
K_grid = [3, 5, 10]

# 总风险预算
budget_grid = [0.05, 0.10, 0.15]  # 5%, 10%, 15%

# 趋势确认 R
R_confirm_grid = [2, 3, 5]

# 目标 R
R_target_grid = [3, 5, 10]
```

**重要说明：**
- 这些参数仅作实验网格，**非推荐配置**
- 参数选择高度依赖市场、频率、信号质量
- 需要通过 walk-forward validation 验证
- **警告**：大 K 或高 budget 会增加破产风险

### 3.2 风险控制参数

```python
# 单市场最大 units（参考 Turtle）
max_units_per_market = 4

# 跨市场相关性限制
max_units_correlated_markets = 6
max_units_all_markets = 12

# 单方向（long 或 short）最大 units
max_units_single_direction = 12

# 每日最大交易次数
max_trades_per_day = 3

# 冷却期（失败后）
cooldown_period_days = 5
```

---

## 4. 实现注意事项

### 4.1 交易成本建模

```python
def calculate_total_cost(n_trades, spread, commission, swap_per_day):
    """
    完整成本模型

    Args:
        n_trades: 交易次数
        spread: Bid-ask spread（pips）
        commission: 每 lot 佣金
        swap_per_day: 隔夜利息（per lot per day）

    Returns:
        total_cost: 总成本
    """
    spread_cost = n_trades * spread * pip_value
    commission_cost = n_trades * commission
    swap_cost = holding_days * swap_per_day

    return spread_cost + commission_cost + swap_cost
```

**成本影响：**
- 递增策略增加交易次数（n 次试探 + 1 次成功）
- 每次试探成本 = spread + commission
- Break-even R 必须包含成本：R_min = (L_n + n × cost) / r_n

### 4.2 滑点与 Gap 处理

```python
def apply_slippage(order_price, slippage_model):
    """
    滑点建模

    - 正常市场：0.5-1 pip
    - 新闻事件：2-5 pips
    - 低流动性：3-10 pips
    - Gap（周末、新闻）：可能超过止损距离
    """
    if is_news_event():
        slippage = random.uniform(2, 5)
    elif is_low_liquidity():
        slippage = random.uniform(3, 10)
    else:
        slippage = random.uniform(0.5, 1)

    executed_price = order_price + slippage  # Long 时
    return executed_price
```

**Gap 风险：**
- 周末 gap 可能导致止损无法执行于预期价格
- 实际亏损可能 > r_n
- 递增仓位放大 gap 风险

### 4.3 保证金与杠杆约束

```python
def check_margin_requirement(position_size, leverage, equity):
    """
    检查保证金是否充足

    Forex 典型杠杆：50:1, 100:1, 500:1
    保证金 = position_value / leverage
    """
    position_value = position_size * contract_size * current_price
    required_margin = position_value / leverage

    if required_margin > equity * 0.80:  # 保留 20% 缓冲
        raise InsufficientMarginError(
            f"Required {required_margin}, available {equity * 0.80}"
        )

    return True
```

**杠杆风险：**
- 递增仓位可能触及保证金上限
- 强制平仓风险
- 高杠杆放大亏损

### 4.4 数据质量与回测陷阱

```python
# 避免 lookahead bias
def get_bar_data(timestamp):
    """
    只使用 timestamp 之前的数据
    """
    return historical_data[historical_data.timestamp < timestamp]

# 避免 survivorship bias
def load_currency_pairs(start_date, end_date):
    """
    包含已下市或流动性丧失的货币对
    """
    return all_pairs_including_delisted

# Tick data vs OHLC
def use_tick_data_for_stop():
    """
    止损触发应基于 tick data，非 bar close
    否则可能低估止损频率
    """
    pass
```

---

## 5. 与经典策略的对比实现

### 5.1 对照组 A：固定仓位

```python
def fixed_position_baseline(market_data, equity, r_fixed=0.01):
    """
    基准：固定仓位重复试探
    """
    for bar in market_data:
        if entry_signal(bar):
            size = calculate_position_size(equity, r_fixed, bar.atr)
            position = open_position(size, stop_loss, entry_price)
            # 无递增，每次独立交易
```

### 5.2 对照组 B：Anti-Martingale（盈利后加仓）

```python
def anti_martingale(market_data, equity, r_0=0.01):
    """
    Anti-Martingale：盈利后递增
    """
    current_risk = r_0

    for bar in market_data:
        if previous_trade_won:
            current_risk = min(current_risk * 1.5, r_max)  # 盈利后增加
        elif previous_trade_lost:
            current_risk = r_0  # 亏损后重置

        size = calculate_position_size(equity, current_risk, bar.atr)
```

### 5.3 对照组 C：Turtle Pyramiding

```python
def turtle_pyramiding(market_data, equity, r_0=0.01, max_units=4):
    """
    Turtle：趋势确认后盈利加仓
    """
    units = []

    for bar in market_data:
        if entry_signal(bar) and len(units) == 0:
            unit = open_position(...)
            units.append(unit)

        # 盈利 0.5N 后加仓
        if len(units) > 0 and len(units) < max_units:
            last_unit = units[-1]
            if bar.price > last_unit.entry + 0.5 * bar.atr:
                new_unit = open_position(...)
                units.append(new_unit)
```

---

## 6. 验证清单

### 6.1 代码验证

- [ ] 状态转移逻辑正确
- [ ] 止损递增计数器 n 正确更新
- [ ] 累计亏损计算准确
- [ ] 达到 K 或 Budget 时正确终止
- [ ] 无 lookahead bias
- [ ] 交易成本完整建模
- [ ] 保证金约束检查

### 6.2 数学验证

- [ ] Break-even R 公式与手算一致
- [ ] 累计亏损 L_n 与公式匹配
- [ ] Risk of ruin 概率计算正确
- [ ] Budget 约束下最大 K 计算正确

### 6.3 回测验证

- [ ] 对照组 A-G 同时运行
- [ ] Walk-forward validation（5 年训练，1 年测试）
- [ ] 跨币对验证
- [ ] 极端情景测试（2008, 2015 Swiss, 2020 COVID）
- [ ] Monte Carlo 模拟（1000+ runs）
- [ ] 序列置换测试（检验路径依赖价值）

---

## 7. 重要警告

**本策略为研究实验，非盈利验证：**

1. **核心假设未验证**：止损序列提供 regime 信息的假设在 Query 1-9 中未找到支持证据
2. **Martingale 风险**：若假设不成立，本策略继承有限 Martingale 的风险特征
3. **实证反对**：主流文献一致建议止损后减仓，非增仓
4. **高破产风险**：即使有上限 K，连续失败仍可能导致巨额亏损
5. **成本敏感**：多次试探增加交易成本，可能侵蚀盈利

**适用场景（理论上）：**
- 若能证明止损序列确实预测趋势到来
- 若有可靠的 regime detection 方法
- 若成本极低且无滑点

**不适用场景：**
- 大多数真实交易环境
- 散户账户（高成本、高滑点、小资金）
- 缺乏 edge 的信号

**建议：**
- 优先使用 Anti-Martingale（盈利后加仓）
- 优先使用 Turtle Pyramiding（趋势确认后加仓）
- 优先使用 Fixed-Fractional Kelly（根据 edge 调整）
- **仅在充分验证假设后**考虑本策略

---

**Strategy Specification 完成。**

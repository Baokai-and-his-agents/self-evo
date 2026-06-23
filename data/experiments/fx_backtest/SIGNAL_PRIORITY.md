# 信号处理规则文档

## 同一 Bar 多信号处理优先级

当同一根 K 线内同时出现多个信号时，处理优先级如下：

### 1. 止损优先（最高优先级）

**规则：** 如果当前 bar 的 low <= stop_price，立即止损退出。

**理由：**
- 止损是风险控制的核心，必须优先执行
- 在真实交易中，止损订单通常是挂单，会在触及时立即成交
- 避免"假设能够先退出再止损"的回测偏差

**实现位置：** `signals.py:218-240`

```python
# Check stop first (intrabar)
if bar.low <= stop_price:
    exit_price = stop_price
    # ... 立即退出，不检查其他信号
    in_position = False
    continue
```

### 2. 退出信号（中等优先级）

**规则：** 如果未触及止损，检查 Donchian 低点退出信号。

**实现：** 退出信号在 **下一根 bar open** 执行（无 lookahead）。

**实现位置：** `signals.py:242-260`

```python
# Check exit signal
donchian_low = self.compute_donchian_low(bars, i, self.exit_period)
if donchian_low is not None and bar.close < donchian_low:
    if i + 1 < len(bars):
        exit_price = bars[i + 1].open  # 下一根 bar open
```

### 3. 入场信号（最低优先级）

**规则：** 只在不持仓时检查入场信号。

**实现：** 入场信号在 **下一根 bar open** 执行。

**实现位置：** `signals.py:179-202`

```python
if not in_position:
    donchian_high = self.compute_donchian_high(bars, i, self.entry_period)
    if bar.close > donchian_high:
        if i + 1 < len(bars):
            entry_price = bars[i + 1].open  # 下一根 bar open
```

### 4. 确认信号（E 策略专用）

**规则：** 确认信号在持仓期间独立检测，不影响止损/退出优先级。

**触发条件：** `bar.high >= entry_price + confirmation_r_threshold * stop_distance`

**实现位置：** `signals.py:208-216`

**特性：**
- 确认信号只记录时间戳和价格，不触发交易动作
- 由 backtest engine 在执行时区分 probe 和 amplified 阶段
- 独立于 stop_count 序列（符合 Issue #18 要求）

---

## 优先级总结

| 优先级 | 信号类型 | 执行时机 | 相互排斥 |
|--------|---------|---------|---------|
| 1 | 止损 | 当前 bar（intrabar） | 与退出互斥 |
| 2 | 退出信号 | 下一 bar open | 与止损互斥 |
| 3 | 入场信号 | 下一 bar open | 需不持仓 |
| 4 | 确认信号（E） | 记录时间戳，不立即执行 | 不影响其他信号 |

**关键设计：**
1. 止损 > 退出 > 入场
2. 所有信号都不使用 lookahead（只用当前及过去 bar）
3. 确认信号是状态记录，不是交易动作
4. 同一根 bar 不会既止损又正常退出

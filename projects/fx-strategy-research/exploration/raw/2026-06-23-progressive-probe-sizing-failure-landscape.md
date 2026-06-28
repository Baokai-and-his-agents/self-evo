# Progressive Probe Position Sizing - Failure Landscape

**Date:** 2026-06-23
**Worker:** scout-worker-fx-sizing-01
**Run ID:** 2026-06-23-fx-sizing-001

---

## 1. 失效模式分类

### 1.1 理论失效（根本性）

**F1. 核心假设不成立：止损序列无预测性**

**失效机制：**
- 假设：连续 n 次止损 → P(趋势即将到来) ↑
- 实证（Query 9）：false breakout 不预测趋势，50-70% breakout 为 false
- 后果：若 p 和 R 恒定（i.i.d.），递增仓位仅重新分配风险，无增量价值
- **退化为有限 Martingale**：继承 fat tail risk，高破产概率

**检测方法：**
```python
def test_stop_loss_predictive_power(historical_data):
    """
    测试止损序列是否预测趋势
    """
    sequences = extract_stop_loss_sequences(historical_data)

    for seq in sequences:
        n_stops = len(seq.stops)
        next_trade_result = seq.next_trade_outcome

        # H0: P(win | n stops) = P(win)（无预测性）
        # H1: P(win | n stops) > P(win)（有预测性）

    p_value = chi_square_test(sequences)

    if p_value > 0.05:
        print("WARNING: Stop-loss sequences do NOT predict trend")
        print("Strategy degenerates to limited Martingale")
```

**应对措施：**
- 若测试失败，**放弃本策略**
- 转向 Anti-Martingale（盈利后加仓）
- 或使用 Regime detection（HMM, change-point）明确识别状态

---

**F2. Martingale 风险特征：Fat Tail**

**失效机制：**
- 即使有上限 K，连续 K 次失败累计亏损 L_K 可能巨大
- 算术递增：L_5 = 10%（r_0=1%, d=0.5%）
- 几何递增：L_5 = 31 × r_0（m=2）
- 小概率事件（(1-p)^K）导致大亏损（L_K）

**数值示例：**
- p=0.4, K=5: P(5 连亏) = 0.6^5 = 7.78%
- p=0.3, K=5: P(5 连亏) = 0.7^5 = 16.8%
- **每 6-13 个周期爆一次大亏**

**检测方法：**
- Monte Carlo 模拟 1000 runs
- 记录最大单周期亏损分布
- Kurtosis > 3 表明 fat tail 存在

**应对措施：**
- 设置更严格的 Budget 上限
- 使用更小的 K（3 instead of 10）
- 算术递增优于几何递增

---

**F3. i.i.d. 假设破裂：序列相关性**

**失效机制：**
- 若止损序列正自相关（输了更容易继续输）
- 递增仓位会在最不利时期加大暴露
- 类似 Gambler's fallacy 的反向陷阱

**实证风险：**
- Barber & Odean (2000): 亏损后增加活动的交易者年化跑输 3.8%
- 连亏期间决策质量下降（tilt, revenge trading）

**检测方法：**
```python
def test_autocorrelation(trade_results):
    """
    测试交易结果自相关性
    """
    acf = autocorrelation(trade_results, lag=1)

    if acf > 0.1:
        print("WARNING: Positive autocorrelation detected")
        print("Losing streaks tend to cluster")
        print("Increasing size after losses is dangerous")
```

---

### 1.2 市场结构失效

**F4. 持续震荡，趋势不出现**

**失效机制：**
- 假设：震荡 → 趋势切换
- 现实：震荡可能持续数月（range-bound market）
- 连续 K 次止损，到达上限，无趋势出现
- 累计亏损 L_K，无大 R 盈利覆盖

**历史案例：**
- EUR/USD 2014-2015: 18 个月窄幅震荡
- GBP/USD 2019 Q2-Q3: 持续 whipsaw
- 任何货币对在 low volatility regime

**检测方法：**
- ADX < 20 持续超过 60 天
- Bollinger Bands 宽度 < 历史 20 percentile
- 20-day high/low range < 1 ATR

**应对措施：**
- **Regime filter**：ADX < 20 时禁用策略
- **Time limit**：震荡超过 N 天后强制退出
- **Budget hard stop**：达到预算后立即停止

---

**F5. 假突破密集，成本侵蚀**

**失效机制：**
- 多次试探 → 多次 spread + commission
- 每次成本 c，n 次累计 n × c
- Break-even R 上升：R_min = (L_n + n × c) / r_n
- 高成本可能使任何 R 都不够

**数值示例：**
- Spread: 2 pips, Commission: $5/lot
- 5 次试探，每次 1 lot: 成本 = (2 × 5 + 5 × 5) = $35
- 若 r_5 = $3000, 成本占比 = 35/3000 = 1.17%
- R_min 上升 1.17%

**高成本场景：**
- Exotic pairs（高 spread）
- 小账户（佣金占比大）
- 高频试探（日内多次）

**应对措施：**
- 仅交易主要货币对（EUR/USD, GBP/USD 等）
- 避免 exotic pairs
- 限制每日试探次数（如最多 3 次）

---

**F6. 滑点与 Gap：止损执行失败**

**失效机制：**
- 止损设定 2 ATR，但实际执行可能偏离
- 正常滑点：0.5-1 pip（可接受）
- 新闻滑点：2-5 pips（侵蚀利润）
- Gap 跳空：周末、重大新闻，可能 10-50 pips
- 实际亏损 > r_n，破坏 break-even 计算

**历史案例：**
- 2015-01-15 Swiss Franc unpegging: EUR/CHF gap 3000+ pips
- 2019-01-03 Flash crash: AUD/JPY, USD/JPY gap 几百 pips
- 周末 gap 常见于地缘政治事件

**风险放大：**
- 递增仓位在大 n 时暴露更大
- r_5 = 3.5%，gap 导致亏损 5%，超出预期 40%+

**应对措施：**
- **避免持仓过周末**（重大新闻周除外）
- **Guaranteed stop**（若 broker 提供，虽然成本更高）
- **Gap insurance**：预留额外缓冲（如 Budget × 1.5）
- **新闻日历过滤**：ECB, Fed, NFP 前后暂停交易

---

**F7. 趋势延迟：确认太晚**

**失效机制：**
- 趋势建立需要时间
- 早期仍可能触及止损（假突破）
- 等待 R_confirm（如 3R）确认，可能错过早期最佳入场
- 递增到大仓位时，趋势可能已进行一半

**Trade-off：**
- 早确认：假信号多，频繁进入 CONFIRMED 后反转
- 晚确认：错过早期低成本入场，大仓位进场晚

**检测方法：**
- 回测中记录"确认时已错过的 R"
- 若平均错过 > 2R，确认太晚

**应对措施：**
- 使用多级确认：1R 初步，3R 完全
- 或在 PROBE 阶段允许小规模 pyramiding（如 Turtle 0.5N）

---

**F8. 趋势反转：大仓位回吐**

**失效机制：**
- 经过 n 次递增，终于进入 CONFIRMED
- 持有大仓位（r_n = r_max）
- 趋势突然反转（V 型或新闻驱动）
- Trailing stop 触及，但因仓位大，回吐金额显著

**类似 PR #14 Pyramiding 风险：**
- Pyramiding 在趋势后期持有最大仓位
- 反转时亏损放大

**数值示例：**
- 经 5 次试探，r_5 = 3.5%
- 进入 CONFIRMED，盈利 5R
- 反转，trailing stop 触及，回吐 2R
- 净盈利 3R，但若固定仓位 1% 则 3R × 1% = 3%
- 本策略 3R × 3.5% = 10.5%（更好）
- **但若回吐 4R，则 1R × 3.5% = 3.5%（仍盈利但不如预期）**

**应对措施：**
- **Tighter trailing stop**：CONFIRMED 后缩小至 1 ATR
- **Partial profit taking**：达到 3R 时平仓 50%
- **Volatility filter**：ATR 突然扩大 2× 时收紧止损

---

### 1.3 执行与心理失效

**F9. 过度优化（Overfitting）**

**失效机制：**
- 大参数空间：r_0, d, m, K, Budget, R_confirm, R_target
- 7 个参数，每个 3 个值 = 3^7 = 2187 组合
- 回测中找到"最优"参数，但 out-of-sample 失败
- 曲线拟合噪音，非真实 edge

**检测方法：**
- Walk-forward 验证：训练集 vs 测试集 Sharpe 差异 > 50%
- 参数微小变化导致结果剧变（不稳定）
- Monte Carlo 置换后策略失效

**应对措施：**
- **简化参数空间**：固定部分参数（如 r_0=1%）
- **Robust optimization**：选择参数稳定区域，非单点最优
- **Out-of-sample 优先**：只报告 OOS 结果

---

**F10. 执行纪律崩溃**

**失效机制：**
- 连续 3-4 次止损后，心理压力增大
- 质疑策略，跳过第 5 次入场（恰好是趋势开始）
- 或相反：亏急眼，超出 K 继续加仓（无限 Martingale）
- Revenge trading, FOMO, loss aversion

**心理陷阱：**
- "已经亏了 8%，再试一次"（Sunk cost fallacy）
- "这次一定是真突破"（Confirmation bias）
- "不能让前面的亏损白费"（Escalation of commitment）

**应对措施：**
- **完全自动化执行**：无人工干预
- **预设 K 和 Budget**：硬性限制，代码强制
- **冷静期**：失败后强制休息 5 天
- **日志审计**：记录每次决策，事后复盘

---

**F11. 资金管理崩溃：Kelly 严重偏离**

**失效机制：**
- 递增仓位可能远超 Kelly 最优
- Kelly f* = (p×R - q) / R
- 若 p=0.4, R=3: f* = (0.4×3 - 0.6)/3 = 0.2（20%）
- 但 r_5 = 3.5% 可能已接近或超过 fractional Kelly (0.25 × 20% = 5%)
- Over-betting 导致几何增长率下降

**检测方法：**
```python
def check_kelly_violation(position_size, equity, p, R):
    kelly_full = (p * R - (1 - p)) / R
    kelly_half = 0.5 * kelly_full

    position_pct = position_size / equity

    if position_pct > kelly_half:
        print(f"WARNING: Over-betting Kelly")
        print(f"Position {position_pct:.2%} > Kelly-half {kelly_half:.2%}")
```

**应对措施：**
- **Kelly 上限**：r_n 不得超过 Kelly-half
- **动态调整**：若 Kelly 下降（p 或 R 下降），减小 r_n

---

**F12. 保证金不足与强制平仓**

**失效机制：**
- 递增到大仓位，margin requirement 上升
- 其他持仓也占用 margin
- 权益因前期亏损下降
- Margin call → 强制平仓，在最不利价格退出

**数值示例：**
- 初始权益 $100k
- 经 5 次止损，累计亏 $10k，剩余 $90k
- r_5 = 3.5% × $90k = $3150
- 若杠杆 50:1，需 margin = $3150 × 100 / 50 = $6300
- 加上其他持仓，可能触及 80% margin 上限

**应对措施：**
- **保守 margin 使用**：总 margin 不超过权益 50%
- **动态 equity 更新**：r_n 基于当前权益，非初始
- **Margin buffer**：预留 20% 权益作缓冲

---

### 1.4 数据与基础设施失效

**F13. 数据质量问题**

**失效机制：**
- Tick data 缺失 → 止损触发时间错误
- OHLC 回测 → 低估止损频率（intra-bar 止损未捕捉）
- Survivorship bias → 只测试存活的货币对
- Lookahead bias → 使用未来数据

**应对措施：**
- **Tick data 验证**：至少在关键时期（2008, 2015, 2020）使用 tick
- **Bid-ask spread 建模**：不使用 mid price
- **包含下市品种**：如 CHF pairs 在 2015 前后

---

**F14. Broker 限制与拒绝**

**失效机制：**
- 高频试探触发 broker 反洗钱警报
- Scalping 限制（部分 broker 禁止短期高频）
- 最大订单大小限制（尤其小 broker）
- 拒绝订单：市场波动大时

**应对措施：**
- 选择支持 scalping 的 ECN broker
- 分散到多个 broker（避免单点失败）
- 使用 limit order 而非 market order（减少拒单）

---

**F15. 技术故障**

**失效机制：**
- 网络中断 → 无法平仓
- 服务器宕机 → 止损未执行
- API rate limit → 订单延迟
- Bug in code → 错误的 n 计数或仓位计算

**应对措施：**
- **Redundancy**：多路网络，备用服务器
- **Manual override**：保留手动平仓能力
- **Extensive testing**：单元测试、集成测试、压力测试
- **Monitoring & alerts**：实时监控，异常立即报警

---

## 2. 失效概率估计

### 2.1 理论失效

| 失效模式 | 概率 | 影响 | 风险等级 |
|---------|------|------|---------|
| F1. 核心假设不成立 | **高（>70%）** | 毁灭性 | 极高 |
| F2. Fat tail 风险 | 中（每 10-20 周期） | 重大 | 高 |
| F3. 序列相关性 | 中 | 中等 | 中 |

**结论：** 理论失效概率高，尤其 F1。若 Query 9 结论正确（false breakout 不预测趋势），策略根基不牢。

### 2.2 市场结构失效

| 失效模式 | 概率 | 影响 | 风险等级 |
|---------|------|------|---------|
| F4. 持续震荡 | 高（30-40% 时间） | 重大 | 高 |
| F5. 成本侵蚀 | 中 | 中等 | 中 |
| F6. Gap/滑点 | 低（但极端） | 重大 | 高 |
| F7. 趋势延迟 | 中 | 中等 | 中 |
| F8. 趋势反转 | 中 | 中等 | 中 |

**结论：** 市场结构失效频繁，尤其 F4（震荡市场占 30-40% 时间）。需强 regime filter。

### 2.3 执行与心理失效

| 失效模式 | 概率 | 影响 | 风险等级 |
|---------|------|------|---------|
| F9. Overfitting | 高（手动优化时） | 重大 | 高 |
| F10. 执行纪律崩溃 | 中（人工交易） | 重大 | 高 |
| F11. Kelly 偏离 | 中 | 中等 | 中 |
| F12. 保证金不足 | 低（若监控） | 重大 | 中 |

**结论：** 自动化可降低 F10，但 F9 overfitting 风险仍高。需严格 walk-forward 验证。

### 2.4 数据与基础设施失效

| 失效模式 | 概率 | 影响 | 风险等级 |
|---------|------|------|---------|
| F13. 数据质量 | 低（若审计） | 中等 | 中 |
| F14. Broker 限制 | 低 | 中等 | 低 |
| F15. 技术故障 | 低（若冗余） | 重大 | 中 |

**结论：** 基础设施失效概率低，但需冗余和监控。

---

## 3. 综合失效风险评估

### 3.1 最可能失效路径

**路径 1：核心假设失效（F1）→ Martingale 风险（F2）→ Fat tail 亏损**
- 概率：高
- 时间：前 20-50 个周期
- 后果：账户 drawdown 10-20%

**路径 2：持续震荡（F4）→ 成本侵蚀（F5）→ 达到 Budget 上限**
- 概率：中
- 时间：震荡市场期间（30-40% 时间）
- 后果：周期性 5-10% 亏损，无大盈利覆盖

**路径 3：Gap 事件（F6）→ 超出止损 → Budget 瞬间耗尽**
- 概率：低（年化 1-2 次）
- 时间：黑天鹅事件
- 后果：单次 10-30% 亏损

### 3.2 最严重失效场景

**Scenario A：Swiss Franc 式 Gap**
- 假设：持有 r_5 = 3.5% 仓位 EUR/CHF
- 事件：SNB unpegging，gap 30%
- 止损失效：实际亏损 3.5% × 30% / 2% = 52.5% equity（假设 2% 预期止损）
- **结果：账户破产**

**Scenario B：18 个月震荡**
- 假设：EUR/USD 2014-2015 style range
- 每月 2 个完整周期，每次 K=5 失败
- 每周期亏损 10%（L_K）
- 18 个月 × 2 = 36 个周期
- **即使部分成功，累计 drawdown > 50%**

### 3.3 失效早期信号

**红色警报（立即停止）：**
- [ ] 连续 3 个完整周期（3×K 次试探）无成功
- [ ] Drawdown > 20%
- [ ] Gap 事件导致单次亏损 > 5%
- [ ] ADX < 15 持续 > 90 天（极度震荡）

**黄色警告（减小仓位）：**
- [ ] 连续 2 个周期失败
- [ ] Drawdown 10-20%
- [ ] Win rate < 20%（远低于预期）
- [ ] ATR 下降 > 50%（波动率崩溃）

**绿色正常：**
- [ ] Win rate 30-40%
- [ ] Drawdown < 10%
- [ ] 平均每 5-10 周期有 1 次大盈利（5R+）

---

## 4. 失效后处理方案

### 4.1 止损规则（策略层面）

```python
# 策略止损
if cumulative_equity_drawdown > 0.20:
    stop_all_trading()
    enter_review_period(30_days)

if consecutive_failed_cycles > 3:
    stop_all_trading()
    re_evaluate_assumptions()
```

### 4.2 资金保护

```python
# 分段风险预算
phase_1_budget = 0.05  # 5% equity
phase_2_budget = 0.10  # 另外 5%
phase_3_budget = 0.15  # 另外 5%

# 达到一个阶段后，等待审查
if cumulative_loss > phase_1_budget:
    pause_trading()
    require_manual_approval_for_phase_2()
```

### 4.3 降级方案

**若策略失效，降级到更安全策略：**

1. **Anti-Martingale**：盈利后加仓（实证支持）
2. **Fixed-Fractional Kelly**：根据 edge 调整（Thorp 验证）
3. **Turtle Pyramiding**：趋势确认后加仓（1983-1987 验证）
4. **Fixed position**：固定仓位重复试探（基准）

### 4.4 复盘与学习

**每次失败后：**
- 记录失败模式（F1-F15 中哪个）
- 分析是否可预防
- 更新过滤规则
- 重新测试假设（尤其 F1）

---

## 5. 适用边界明确化

### 5.1 理论上可能适用的场景

**极窄条件（全部满足才考虑）：**
1. ✓ 已实证验证：止损序列确实预测趋势（p-value < 0.01）
2. ✓ 低成本环境：spread < 0.5 pip, 无佣金
3. ✓ 主要货币对：EUR/USD, GBP/USD（高流动性）
4. ✓ 趋势市场：ADX > 25，过去 60 天有 2+ 个 > 5R 趋势
5. ✓ 充足资金：账户 > $50k（承受 K 次试探）
6. ✓ Regime filter：仅在特定 regime 启用
7. ✓ 完全自动化：无人工干预

**即使满足上述条件，仍建议 pilot 测试：**
- 小账户（$5k-$10k）
- 限定时间（3-6 个月）
- 严格 monitoring

### 5.2 明确不适用的场景

**禁止使用：**
- ✗ 散户小账户（< $10k）
- ✗ 高成本 broker（spread > 2 pips）
- ✗ Exotic pairs（低流动性）
- ✗ 震荡市场（ADX < 20）
- ✗ 无 regime filter
- ✗ 手动执行（心理压力过大）
- ✗ 未验证核心假设

---

## 6. 最终风险评级

| 维度 | 评分 | 说明 |
|------|------|------|
| 理论风险 | **极高** | 核心假设未验证（F1） |
| 市场风险 | **高** | 震荡市场频繁失效（F4） |
| 执行风险 | 中 | 可通过自动化降低 |
| 极端风险 | **高** | Gap 事件可能致命（F6） |
| 综合风险 | **极高** | 不推荐实盘使用 |

**结论：**
- 本策略为**研究实验**，非盈利验证
- 核心假设（止损序列预测趋势）在 Query 9 中**未找到支持**
- 若假设不成立，策略退化为有限 Martingale，继承其风险
- **强烈建议：** 优先使用实证支持的策略（Anti-Martingale, Turtle, Kelly）
- 仅在充分验证假设且满足严格条件后，考虑小规模 pilot 测试

---

**Failure Landscape 完成。**

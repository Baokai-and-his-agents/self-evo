# Issue #20 数据源决策摘要

**决策日期**: 2026-06-23  
**决策人**: agent clawbie  
**Issue**: https://github.com/Baokai-and-his-agents/self-evo/issues/20

## 决策结果

### 主数据源: ECB USD/EUR Reference Rate

✅ **选定**: European Central Bank (ECB) USD/EUR daily reference rate

**理由**:
1. 许可明确且宽松（允许免费使用、复制、分发、修改）
2. 官方权威数据源（欧洲央行）
3. API 访问完善且稳定
4. 历史覆盖完整（1999-至今，满足 2005-2025 要求）
5. 无自动化下载限制
6. 无数据库存储限制
7. 无数据共享限制

### 不使用的数据源: Dukascopy

❌ **不采用**: Dukascopy Historical Data Export

**原因**: `DATA_LICENSE_BLOCKED`
- Terms of Use 明确禁止自动化下载（需书面授权）
- 明确禁止数据库存储
- 禁止数据共享/转让
- 仅允许个人非商业手动下载单次使用
- 不符合可复现研究的要求

---

## ECB 数据特征

### 数据规格

| 属性 | 值 |
|------|-----|
| 数据源 | European Central Bank |
| 系列代码 | EXR.D.USD.EUR.SP00.A |
| 频率 | 日线 (Daily) |
| 价格类型 | Reference rate (2:15 pm CET) |
| 货币对 | USD/EUR (需转换为 EUR/USD) |
| 历史范围 | 1999-01-04 至今 |
| 数据点 | 仅收盘价 (Close) |
| OHLC | ❌ 无 Open/High/Low |
| 成交量 | ❌ 无 |
| 精度 | 4 位小数 |
| 格式 | CSV, JSON, XML |
| API | RESTful HTTP API |
| 许可 | ECB Copyright Policy - Free use with attribution |

### 关键限制

1. **仅收盘价**: 无 OHLC 数据
2. **参考价**: 非实际可交易价格（无 bid/ask spread）
3. **货币对方向**: USD/EUR 需转换为 EUR/USD

---

## 对 Issue #20 的影响

### 必须调整的内容

#### 1. 策略定义调整

**原计划** (mvp_daily.json):
- Donchian Channel: 基于过去 N 日的 High/Low
- ATR volatility: 基于 True Range (High, Low, Close)

**调整后**:
- Donchian Channel: 基于过去 N 日的 **Close**
- Volatility: 基于 Close-to-Close **标准差**

**实现差异**:
```python
# 原定义（需要 OHLC）
donchian_upper = max(high[-period:])
donchian_lower = min(low[-period:])
atr = ema(true_range(high, low, close), period)

# 调整后（仅需 Close）
donchian_upper = max(close[-period:])
donchian_lower = min(close[-period:])
volatility = rolling_std(close_returns, period)
```

#### 2. 实验协议更新

在 Issue #20 的实验协议中添加：

```markdown
## 数据限制声明

### 数据源特征
- **来源**: European Central Bank (ECB)
- **系列**: USD/EUR daily reference rate (2:15 pm CET)
- **价格类型**: 单一参考价，非可交易 bid/ask
- **限制**: 无 OHLC，仅日收盘价

### 策略调整
- **Donchian Channel**: 基于收盘价突破（替代传统 High/Low 突破）
- **Volatility**: Close-to-Close 标准差（替代 ATR）
- **标记**: `REFERENCE_RATE_LIMITATION`

### 成本建模
- **Zero cost**: 无交易成本
- **Conservative cost**: 
  - 估计 bid-ask spread: 2 pips (0.0002)
  - 估计滑点: 1 pip (0.0001)
  - 总估计成本: 3 pips per round trip
  - 标记: `ESTIMATED_COST` (因无实际 bid/ask 数据)

### Rollover 建模
- **状态**: `ROLLOVER_NOT_MODELED`
- **理由**: ECB reference rate 不包含隔夜利息
- **影响**: Conservative cost 场景未包含 swap/rollover 成本
```

#### 3. 配置文件调整

`configs/mvp_daily.json` 需要更新：
- 移除 ATR 相关参数
- 添加 Close-based volatility 参数
- 添加数据源元数据

#### 4. 文档要求

所有使用 ECB 数据的地方必须包含归属：

```
数据来源: European Central Bank (ECB)
数据系列: EUR/USD daily reference exchange rate
原始系列: EXR.D.USD.EUR.SP00.A (USD/EUR)
API: https://data-api.ecb.europa.eu/service/
访问日期: 2026-06-23
许可: ECB Copyright Policy - Free use with attribution
引用: European Central Bank. Euro foreign exchange reference rates.
```

---

## 实施计划更新

### Phase 1: 数据源调查 ✅ COMPLETED

- ✅ 调查 Dukascopy → 结论: DATA_LICENSE_BLOCKED
- ✅ 调查 ECB API → 结论: 适合作为主数据源
- ✅ 评估许可条款 → 结论: 无阻碍
- ✅ 确认数据字段 → 结论: 仅收盘价，需调整策略

### Phase 2: 下载器与 Adapter 实现

**更新后的任务**:

1. **ECB 下载器**
   - 实现 `data/sources/ecb/downloader.py`
   - 从 ECB API 下载 USD/EUR 数据
   - 支持日期范围参数
   - 实现重试逻辑
   - 生成下载 manifest (SHA256, 行数, 日期范围)

2. **数据规范化 Adapter**
   - 实现 `data/adapters/ecb_adapter.py`
   - USD/EUR → EUR/USD 转换
   - 提取 date, close 字段
   - 验证时间排序
   - 检查缺失和异常值
   - 输出规范化 CSV

3. **数据存储**
   - 原始 CSV: `state/download-cache/fx-backtest/ecb/raw/`
   - 规范化 CSV: `state/download-cache/fx-backtest/ecb/normalized/`
   - Manifest: `state/download-cache/fx-backtest/ecb/manifest.json`
   - ⚠️ 确保 `.gitignore` 排除 `state/download-cache/`

### Phase 3: 数据质量检查

**新增检查项**:
- Close price 合理性（> 0, 日变动 < 5%）
- 货币对转换正确性
- 无需 OHLC 不变量检查（因无 OHLC）

### Phase 4: 实验配置冻结

**更新任务**:
- 修改 `configs/mvp_daily.json` 为 Close-based 策略
- 添加数据源元数据
- 记录策略调整理由

### Phase 5-8: 保持不变

回测、分析、测试、PR 流程保持不变。

---

## 风险与缓解

### 已识别风险

| 风险 | 影响 | 缓解措施 | 状态 |
|------|------|---------|------|
| 无 OHLC 数据 | 策略定义需调整 | 使用 Close-based 定义，明确记录 | ✅ 可接受 |
| 非交易价格 | 回测结果是理论值 | 说明限制，保守成本增加 spread | ✅ 可接受 |
| 货币对方向 | 需要转换 | Adapter 自动转换并测试 | ✅ 可控 |
| API 可用性 | 下载可能中断 | 重试逻辑，本地缓存 | ✅ 可控 |

### 不可接受风险

❌ **无** - 所有已识别风险均已有缓解措施。

---

## 验收标准更新

### 原标准（Issue #20）

- ✅ 单命令可以从已有缓存重现规范化、回测和报告
- ✅ 下载步骤可独立执行并有重试、校验和清晰错误信息
- ✅ 原始大文件未进入 Git
- ✅ 时间切分与参数在结果生成前固定并写入配置
- ✅ OOS 没有参与参数选择
- ✅ A/B/E/G 使用相同完整事件流，G 实际风险多重集与 B 相同
- ✅ 样本不足时拒绝强结论
- ✅ 现有 fx_backtest 与仓库测试不回归
- ✅ `git diff --check` 和 validator 无 WARN/BLOCK

### 新增标准

- ✅ ECB 数据来源明确归属
- ✅ 策略调整（Close-based）在配置和报告中明确记录
- ✅ `REFERENCE_RATE_LIMITATION` 标记存在于相关文档
- ✅ USD/EUR → EUR/USD 转换正确性已测试
- ✅ 货币对转换的单元测试通过

---

## 相关文档

- [Dukascopy 调查报告](dukascopy-investigation.md)
- [Dukascopy Terms 分析](dukascopy-terms-analysis.md)
- [ECB 评估报告](ecb-evaluation.md)
- [Issue #20](https://github.com/Baokai-and-his-agents/self-evo/issues/20)

---

**状态**: Phase 1 完成，进入 Phase 2  
**下一步**: 实现 ECB 下载器和 adapter

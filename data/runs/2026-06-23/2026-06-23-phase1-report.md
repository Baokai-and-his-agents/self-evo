# Issue #20 Phase 1 完成报告

**报告日期**: 2026-06-23
**Agent**: clawbie
**Branch**: agent/fx-backtest-worker-01/20-eurusd-baseline
**Issue**: https://github.com/Baokai-and-his-agents/self-evo/issues/20

---

## Phase 1 状态

⚠️ **Phase 1: 数据源调查** - 部分完成，暂停在数据源选择门

**当前状态**: DATA_SOURCE_DECISION_REQUIRED
**原因**: 未找到可用的 OHLC 数据源，ECB 仅适合交叉校验

---

## 调查成果

### 1. Dukascopy Historical Data Export

**结论**: ⚠️ **DATA_TERMS_UNCLEAR**

**已调查**:
- 网站通用 Terms of Use
- 发现禁止自动化访问"WEBSITE"（scraper, bot, spider）
- 发现禁止将"WEBSITE"存储在数据库中
- 仅限个人非商业使用

**未调查**:
- Historical Data Export 功能的专项条款
- JForex API 许可协议
- 账户内历史数据的使用边界

**不确定的场景**:
- "WEBSITE"是否包括导出的 CSV 文件？
- "数据库"是否包括本地研究缓存？
- 手动导出后的文件是否可以编程处理？

**文档**:
- `docs/data-sources/dukascopy-investigation.md`
- `docs/data-sources/dukascopy-terms-analysis.md`

---

### 2. ECB USD/EUR Reference Rate

**结论**: ✅ **适合用于交叉校验**
**结论**: ❌ **不能作为主数据源**

**许可评估**:
- ✅ 许可明确且宽松（ECB Copyright Policy）
- ✅ 允许免费使用、复制、分发、修改
- ✅ 无自动化下载限制
- ✅ 无数据库存储限制
- ✅ 仅需引用来源

**数据特征**:
- 来源: European Central Bank
- 系列: EXR.D.USD.EUR.SP00.A
- 频率: 日线（每交易日 2:15 pm CET）
- 价格: Reference rate（单一收盘价）
- 覆盖: 1999-至今

**关键限制**:
- ❌ 仅有单一收盘价，无 OHLC
- ❌ 无法支持 PR #19 的 Donchian High/Low + ATR 定义
- ❌ 改为 Close-based 策略违反预注册协议（禁止调参/改定义）

**用途**:
- ✅ 用于主数据源的 close 价格抽样交叉校验
- ❌ 不能作为主回测数据源

**文档**:
- `docs/data-sources/ecb-evaluation.md`

---

## 交付物清单

1. ✅ `docs/data-sources/dukascopy-investigation.md` - Dukascopy 初步调查
2. ✅ `docs/data-sources/dukascopy-terms-analysis.md` - Terms 详细分析（标记 DATA_TERMS_UNCLEAR）
3. ✅ `docs/data-sources/ecb-evaluation.md` - ECB 完整评估（定位为交叉校验用途）
4. ✅ `docs/data-sources/data-source-decision.md` - 当前状态摘要
5. ✅ `docs/data-sources/ohlc-data-sources-matrix.md` - OHLC 数据源对比矩阵（部分完成）
6. ✅ `data/tasks/TASKS.md` - 更新任务追踪
7. ❌ 删除根目录 `TASKS.md`（已执行）

---

## 关键约束

### Issue #20 预注册协议

1. **策略定义已冻结** (PR #19)
   - Donchian Channel: 基于 **High/Low**
   - ATR volatility: 基于 **True Range** (H, L, C)
   - 同柱止损: 需要区分 entry bar 内的 **High/Low**

2. **禁止调参/改定义**
   > "本轮不得搜索 entry period、exit period、ATR period、ATR multiplier、confirmation R 或 sizing 参数。若发现配置存在实现错误，只能修复错误，并说明修复前后；不得因为收益不佳而调整。"

3. **ECB 定位明确**
   > "ECB reference rate 不是可交易 OHLC，不能作为主回测数据；只用于方向、数量级、日期覆盖和异常点抽查。"

**结论**: 将策略改为 Close-based 属于**更换策略**，不是数据 adapter，违反预注册协议。

---

## 下一步行动

### Phase 1 继续: 补充 OHLC 数据源调查

需要调查以下候选数据源：

#### 优先级 1: Dukascopy 专项条款澄清
- [ ] 调查 Historical Data Export 页面的专项条款
- [ ] 调查 JForex API 文档中的许可说明
- [ ] 或联系 Dukascopy 获取明确说明

#### 优先级 2: OANDA v20 API
- [ ] 阅读 OANDA API 文档
- [ ] 确认历史数据获取方式和许可条款
- [ ] 测试 API 访问（如果可行）

#### 优先级 3: Yahoo Finance (yfinance)
- [ ] 测试 EURUSD=X 数据可用性
- [ ] 检查 2005-2025 覆盖和 OHLC 完整性
- [ ] 验证数据质量
- [ ] 调查 Terms of Service

#### 优先级 4: QuantConnect
- [ ] 阅读 QuantConnect 文档
- [ ] 确认数据导出能力

### Phase 1 输出目标

完成后生成：
- OHLC 数据源对比矩阵（完整版）
- 每个数据源的详细评估文档
- 推荐方案和理由
- 提交给人类批准

### Phase 2-8 暂停

在人类批准主数据源前：
- ❌ 不下载数据
- ❌ 不实现下载器
- ❌ 不运行历史回测
- ❌ 不修改策略定义
- ❌ 不修改 `configs/mvp_daily.json`

---

## 风险与限制

| 风险 | 影响 | 缓解措施 | 状态 |
|------|------|---------|------|
| Dukascopy 许可不明 | 可能无法使用 | 调查专项条款或寻找替代 | ⏳ 进行中 |
| ECB 无 OHLC | 不能作为主数据源 | 仅用于交叉校验 | ✅ 已接受 |
| 策略定义已冻结 | 不能改为 Close-based | 必须找到 OHLC 数据源 | ⚠️ 约束 |
| 可能需要付费数据 | 增加成本 | 优先免费/学术许可数据 | ⏳ 待定 |

---

## 统计

- **文档创建**: 5 个 Markdown 文件
- **数据源评估**: 2 个（Dukascopy 部分, ECB 完整）
- **待调查数据源**: 3 个（OANDA, QuantConnect, Yahoo Finance）
- **代码行数**: 0（Phase 1 仅调研）
- **Git 提交**: 待定（等待审查修正完成）

---

## 审查反馈响应

根据 PR #21 审查反馈 (comment #4779323586)，已完成以下修正：

1. ✅ 将 ECB 从"主数据源"降级为"仅用于交叉校验"
2. ✅ 删除所有"Close-based 策略"决策
3. ✅ 将 Dukascopy 结论从 DATA_LICENSE_BLOCKED 改为 DATA_TERMS_UNCLEAR
4. ✅ 删除根目录 TASKS.md，保留 data/tasks/TASKS.md
5. ✅ 创建 OHLC 数据源调查矩阵框架
6. ⏳ 更新 PR 描述（进行中）
7. ⏳ 运行 git diff --check 和 validator（待定）

---

## 相关文档

- Issue: https://github.com/Baokai-and-his-agents/self-evo/issues/20
- PR: https://github.com/Baokai-and-his-agents/self-evo/pull/21
- PR #19 (策略定义): https://github.com/Baokai-and-his-agents/self-evo/pull/19
- [OHLC 数据源矩阵](../../docs/data-sources/ohlc-data-sources-matrix.md)
- [数据源决策摘要](../../docs/data-sources/data-source-decision.md)

---

**当前状态**: Phase 1 部分完成，暂停在数据源选择门
**等待**: 人类批准主数据源或进一步调查指令
**下一步**: 补充 OANDA / QuantConnect / Yahoo Finance 调查，或等待决策

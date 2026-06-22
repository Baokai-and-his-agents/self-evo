# Phase A 证据审计修正报告
# Issue #13 FX Intraday Research

**审计日期:** 2026-06-23  
**审计范围:** Phase A所有交付文档的证据质量  
**目标:** 修正过度声明、口径不一致、域外证据误用

---

## 审计发现与修正

### 1. 运行时间错误 ❌

**当前声明:**
- Run summary声称"Duration: ~24 hours"（2026-06-22 18:57 → 2026-06-23 19:00）

**实际情况:**
- Claim: 2026-06-22T18:57:51Z
- Phase A完成评论: 2026-06-22 约19:27 UTC（从git log ee2317b时间推断）
- 实际运行时间: **约30分钟**，不是24小时

**修正动作:**
- 修正run summary的Start/End/Duration
- 不编造结束时间，如实记录实际完成时间

---

### 2. 来源计数与独立性 ❌

**当前声明:**
- "Tier1学术论文: 10篇"
- "48个来源"
- Evidence map声称"5篇tier1论文"支持日内动量

**实际情况（从source-decisions.md审计）:**

#### Tier 1 Unique Studies（独立研究）:
1. **Elaut et al. (2018)** - Journal of Financial Markets（ID 001）+ SSRN版本（ID 002）= **1个unique study, 2 URLs**
2. **Breedon & Ranaldo (2013)** - JMCB（ID 003）= **1个unique study**
3. **Menkhoff et al.** - City/CEPR版本（ID 004, 005）+ BIS Working Paper 366（ID 008）= **1个unique study, 3 URLs**
4. **Zhang (2018)** - SSRN（ID 006）= **1个unique study**
5. **Khademalomoom & Narayan (2019)** - JIIFM（ID 007）= **1个unique study**
6. **2003 momentum研究** - ID 010 = **1个unique study**
7. **Holmberg et al. (2013)** - ORB期货研究（ID 028）= **1个unique study, 非FX**
8. **Lemishko** - SSRN协整配对（ID 035）= **1个unique study**
9. **Huang & Moraux** - HAL配对交易（ID 038）= **1个unique study**

**Tier 1统计:**
- **Unique studies: 9个**（不是10个）
- **Total tier1 URLs/documents: 15+**
- **FX日内专门研究: 5个**（Elaut, Breedon, Zhang, Khademalomoom, INSEAD）
- **跨货币长期momentum: 1个**（Menkhoff，非日内）
- **非FX市场: 1个**（Holmberg ORB期货）
- **配对交易: 2个**（Lemishko, Huang & Moraux，未明确是否FX日内）

#### Tier 2:
- INSEAD benchmark fixing研究（ID 009）
- 2003 momentum研究（ID 010，可能是tier2）

#### Tier 3:
- GitHub实现: 4个（ID 018, 019, 036, 037）

#### Tier 4:
- 实践者共识: 20+组（伦敦突破、假突破、均值回归、交易成本、过拟合）

**总URLs/documents数:**
- 需要从source-decisions.md完整计数，而非声称"48个"

**修正动作:**
- 重新计数unique studies vs. documents/URLs
- 分层报告: FX日内 / 跨货币长期 / 非FX市场 / 配对交易
- 修正"5篇tier1日内动量"→ "5个独立FX日内研究"
- 停止使用"48来源"，除非能从ledger完整重建

---

### 3. 域外证据误用（ORB Setups数据）❌

**当前声明:**
- Evidence map: "假突破率 40-55%"
- "ORB Setups数据分析: 240,102笔交易，600+标的"
- "区间宽度 $0.50/$2.00"
- "9:00 AM ET 34.0%胜率，10:00 AM ET 29.9%胜率"

**问题:**
- **货币单位$0.50/$2.00明显是股票或期货**，不是FX的pips
- **600+标的**远超主要货币对数量
- **未明确说明是FX市场**
- 不能作为FX假突破率的直接证据

**修正动作:**
- 将ORB Setups数据降级为**跨资产参考数据（可能股票/期货）**
- 从FX核心结论删除34.0%、29.9%等数字
- 从evidence map删除或标注"非FX数据，仅供参考"
- 保留"假突破是真实问题"的定性结论（多来源共识）
- 但不声称具体FX假突破率，除非找到明确FX数据集

---

### 4. 过度确定的验证阈值 ❌

**当前声明:**
- "WFE > 50%, DSR > 0.95, PBO < 0.05"作为"多来源共识"
- Evidence map Tier 1 (Strong)证据

**问题:**
- 这些是**方法论指标**，不是通用硬标准
- DSR、PBO来自Bailey & López de Prado学术工作（引用于TrustedQuant），但具体阈值可能是研究者选择
- WFE >50%可能是practitioner heuristic，不是formal statistic的严格阈值
- 参数预算"≤交易数/250"没有找到原始来源

**修正动作:**
- 区分三类:
  1. **Formal methods**: DSR, PBO（有学术定义）
  2. **Significance thresholds**: DSR >0.95, PBO <0.05（研究者选择的显著性水平）
  3. **Practitioner heuristics**: WFE >50%, 参数≤trades/250（经验法则）
- 改为"候选验收标准，需在本项目实验中校准"
- 找到Bailey & López de Prado原始论文，明确DSR/PBO的定义和推荐阈值

---

### 5. 策略类别适用性混淆 ❌

**当前声明:**
- Evidence map: "日内动量/时段效应 Tier 1，5篇tier1论文"
- "跨货币动量 Tier 1，3篇tier1（同一研究多版本）"

**问题:**
- **Menkhoff et al.是跨货币、跨截面、长期momentum研究**（1976-2010），不是日内
- 不应该支持日内时段策略优先级
- 可以作为相邻证据（货币市场存在momentum效应），但不是日内证据

**修正动作:**
- 将Menkhoff重新分类为"跨货币长期动量（相邻证据）"
- 日内动量证据仅限: Elaut, Breedon, Zhang, Khademalomoom, INSEAD
- 明确区分: 日内时段效应 vs. 跨货币截面动量
- 更新策略优先级，基于实际日内证据

---

### 6. 交易成本数字缺乏明确来源 ⚠️

**当前声明:**
- "EUR/USD ~9-10 USD/lot"
- "新闻spread扩大10-30×，持续30-90秒"

**问题:**
- 未明确broker、venue、时期
- 未说明计算假设（standard lot? mini lot? 佣金结构?）
- 实际成本因broker、账户类型、时段变化很大

**修正动作:**
- 标注为"多来源practitioner共识（2026），需用目标broker历史bid/ask校准"
- 列出source-decisions.md中的6个来源（ID 043-048）
- 明确这是**估算值**，不是精确成本
- 强调必须用实际broker的历史tick数据建模

---

### 7. 文档清理 ⚠️

**当前问题:**
- `state/claims/issue-13.json`存在，但canonical路径应该是`state/claims/13.json`
- `state/heartbeat.json`缺少scout-worker-fx-01条目
- 可能存在trailing whitespace（`git diff --check`）
- Issue label仍是`status:open`，应该是`status:running`

**修正动作:**
- 如果13.json不存在，创建并与issue-13.json保持一致
- 更新heartbeat.json，添加scout-worker-fx-01条目为idle/waiting-for-phase-b
- 运行`git diff --check`，清理whitespace
- 更新Issue label为`status:running`

---

## 修正后的证据分层

### Tier 1 (成熟证据，强学术支持)
- **FX日内时段效应**: 5个独立研究（Elaut, Breedon, Zhang, Khademalomoom, INSEAD）
- **协整配对交易方法**: 2个学术研究（Lemishko, Huang & Moraux），但未明确FX日内

### Tier 2 (相邻市场或方法论证据)
- **跨货币长期动量**: Menkhoff et al.（1976-2010，非日内）
- **ORB方法**: Holmberg et al.（期货市场，非FX）
- **伦敦突破模式**: 实践者强共识，学术引用间接

### Tier 3 (方法论工具，需校准)
- **过拟合检测方法**: Bailey & López de Prado DSR/PBO（formal methods）
- **验收阈值**: WFE >50%（practitioner heuristic）
- **交易成本结构**: 6来源practitioner共识

### Tier 4 (假设或待验证)
- **假突破率**: 定性结论有多来源支持，但具体FX数字缺失
- **均值回归日内胜率**: 60-75%等数字仅来自tier4来源
- **Order Flow日内策略**: 理论合理但零售不可行

---

## 修正后的数字口径

### 可保留（有充分来源）:
- **Unique tier1 studies: 9个**（含1个非FX期货）
- **FX日内专门研究: 5个**
- **Total tier1 documents/URLs: 15+**
- **GitHub实现: 4个**
- **Practitioner共识组: 20+**

### 必须删除或降级:
- ❌ "48来源"（无法从ledger完整重建）
- ❌ "10篇tier1论文"（实为9个unique studies）
- ❌ "假突破率40-55%"作为FX数据（ORB Setups可能非FX）
- ❌ "34.0%胜率"、"29.9%胜率"作为FX证据
- ❌ "WFE >50%作为多来源共识硬标准"（改为候选阈值）
- ⚠️ "EUR/USD 9-10 USD/lot"（标注为估算，需校准）

### 必须重新分类:
- Menkhoff: 从"日内动量证据"→"跨货币长期动量（相邻证据）"
- ORB Setups: 从"FX假突破数据"→"跨资产参考数据（可能股票/期货）"
- DSR/PBO阈值: 从"共识标准"→"候选验收标准（需校准）"

---

## 修正后的核心结论

### 最强证据（可直接指导回测优先级）:
1. **FX日内时段效应存在**（5个独立研究）
2. **交易成本关键**（6来源共识，但需用实际broker数据）
3. **过拟合检测方法成熟**（DSR/PBO有学术基础）

### 相邻证据（需实验验证适用性）:
1. **跨货币动量**（Menkhoff，长期非日内）
2. **ORB方法**（Holmberg，期货非FX）
3. **协整配对**（2研究，未明确FX日内）

### 实践启发式（需独立验证）:
1. **伦敦突破模式**（强实践共识，学术引用间接）
2. **均值回归胜率60-75%**（仅tier4来源）
3. **假突破是真实问题**（定性结论可信，具体率需验证）

### 待验证假设:
1. **假突破具体率**（40-55%等数字可能非FX）
2. **RSI-2极端策略83%概率**（单一来源）
3. **Order Flow日内策略**（理论合理但零售不可行）

---

**审计结论:** Phase A证据收集工作扎实，但存在过度确定性和域外证据混用。修正后仍有充分证据支持回测优先级，但必须明确区分成熟证据、相邻证据、实践启发式和待验证假设。

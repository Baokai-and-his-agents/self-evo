---
title: "日报：自主 Agent 生态系统研究"
date: 2026-06-21
issue: 7
type: decision_report
researcher: scout-worker-01
status: complete
---

# 日报：Issue #7 - 自主 Agent 生态系统

## 执行摘要

对自主 agent 生态系统的调研揭示了一个日趋成熟但充满风险的格局。生产级模式已存在：持久执行平台（Temporal 35k★）、可观测性基础设施（Langfuse 29k★）、GitHub 原生工作流。但 agent 试点失败被广泛报道（成本失控、无限循环），基准测试分数在实际任务中可能误导。

**核心发现**：Self-evo 的 file-first、人工审查方法与谨慎的生产模式一致。前进路径是**优先自主 Scout 垂直切片**，配合成本控制和边界执行。

---

## 研究概况（保守的最低点）

**Search queries executed**: 113 total across all roles
- Autonomous loops & GitHub: 35 searches, 15 deep fetches, 19 retained sources
- Multi-agent coordination: 29 searches, 23 fetched documents
- Memory & context: 27 successful deep fetches across 14 system categories
- Observability & safety: 24 repository/API inspection calls, 85 repositories surfaced, 16 selected
- Critic research: 47 repository/API inspection calls, 30 archived frameworks in sample, plus 8 papers and 4 coordination repos

**Unique systems evaluated**: 48 retained after deduplication
- 7 durable execution platforms
- 12 active multi-agent frameworks (30 archived frameworks identified in critic sample)
- 8 memory systems
- 5 observability platforms
- 6 evaluation benchmarks
- 6 safety/security tools
- 4 GitHub integration patterns

**Overlap caveat**: Same repo found via multiple queries. GitHub search returns forks and integrations. Deduplication applied; counts represent unique systems analyzed, not raw search hits.

**Deep analysis**: 10 systems with architecture-level review (Temporal, LangGraph, Mem0, ENGRAM, OpenHands, Langfuse, CrewAI, OKF, Restate, SWE-bench).

**Critic validation**: Identified 30 archived frameworks (biased search: focused on failure indicators, not representative sample). Zero public issues for "agent cost" or "coordination failure" suggests evidence gap.

---

## 一级主要路线：优先 Scout 垂直切片

**原则**：优先交付项目声明的首要目标——一个能主动探索、过滤并生成面向决策的日报的侦查系统。

**Scout 垂直切片范围**：

1. **批准资源注册表** (`rules/RESOURCE_APPROVALS.yaml`)
   - 能力分层：`public-web-read` 作为 scope（HTTP GET 公开资源、遵守 robots.txt）
   - 具体来源为业务 allowlist：GitHub/Hacker News/arXiv/Product Hunt 等
   - 登录/token/付费访问需新资源审批 proposal
   - Schema 定义：`data/exploration/scout-source-registry.schema.yaml`

2. **手动触发，预留调度占位**
   - 用户在本地运行 Scout worker：`python scripts/workers/scout_runner.py --issue <N>`
   - `rules/EXPLORATION_POLICY.md` 定义批准来源、每日限额
   - 后续：添加计划调用

3. **增量 cursor 和去重**
   - 每来源跟踪 last-seen 时间戳
   - 跳过已处理项目（按 URL/ID）
   - Cursor 存储在本地 gitignored `state/scout_cursor.json`

4. **保留/拒绝 ledger 带证据**
   - 每项：保留（带理由）或拒绝（带理由）
   - 决策存储在 gitignored `data/exploration/raw/<date>-<source>-ledger.jsonl`
   - 精简 ledger（tracked）存储在 `data/exploration/raw/<date>-<source>-decisions.md`：URL/ID、日期、标题、keep/reject、理由、来源类型
   - 人类可审阅溯源，daily report 链接到 tracked decisions 文件

5. **边界高 token 研究**
   - Scout runner 强制执行：最大墙上时钟时间、最大扫描来源数、最大保留项目数、最大 Claude 调用次数
   - 不承诺内部 LLM 调用级硬 token 上限（hooks 看不到）
   - 未知 token/成本进入 telemetry 标记为 "unknown" 带解释

6. **每日决策报告**
   - 一份复用图谱（现有工作调研）
   - 一项实验/技能/项目候选
   - 证据链接到 tracked ledger

7. **人工审查标签**
   - 用户通过 GitHub Issue/PR comment 或 review labels 给出反馈：`relevant`、`irrelevant`、`deep-dive`、`pause`
   - Agent 将 GitHub 反馈同步为 tracked `data/exploration/review_labels/<date>.yaml` 记录
   - Agent 读取评论/标签需要明确 repo read 权限；写 GitHub 由 clawbie 身份且在批准 scope 内
   - 未来：preference learner 汇总模式

**Scout Runner/Wrapper**（执行边界）：
- 本地脚本 `scripts/workers/scout_runner.py`，启动 Claude CLI worker 执行 Scout 任务
- 权限前置：需 `data/proposals/rule_changes/2026-06-22-scout-runner-script-permissions.md` 获 jlcbk 批准
- 捕获可用的结构化 CLI 输出/用量
- 强制执行：最大运行时（墙上时钟）、最大 Claude 进程调用数、最大重试、扫描/保留限制
- 检测：工具调用重复、无进展、生命周期违规
- 写入：终止时部分结果、cursor/完整 ledger 到 gitignored state、精简 decisions 到 tracked
- 提交到 repo：仅摘要、tracked decisions、schemas（不含增长的运行时状态）
- `.gitignore` 文件：`state/.gitignore`、`data/exploration/raw/.gitignore`
- 测试：`python data/tests/test_runtime_ignore.py` 验证 gitignore 规则

**时间线**：3-4 周到工作的 Scout 垂直切片

**权衡**：
- ✅ 交付用户首要声明目标（主动探索）
- ✅ 用真实业务价值测试高 token 工作流
- ✅ 将遥测和预算控制嵌入实际工作（非分离基础设施）
- ✅ 生成可审查的每日输出用于偏好学习
- ⚠️  每次运行高 token 成本（通过每日限制和 runner 强制执行缓解）
- ⚠️  需要批准外部来源（通过资源批准工作流缓解）

**成功标准**（Scout 运行后衡量）：
- Scout 在预算内生成非空日报
- 人工审查时间 <30 分钟每报告
- 相关性在 4 周内改进（通过人工标签衡量）
- 零失控成本（runner 终止有效）

---

## 次要路线：Scout 证明后

### 路线 B：Scout 评估 + 留出集

**时机**：Scout 垂直切片运行后、扩展前

**范围**：
- 创建留出评估集（非从 repo 已解决 Issues）
- 定义 Scout 质量指标：新颖性、相关性、证据质量、可操作转换、重复率
- 单独定义 Builder 质量指标（测试、验收）
- 包括人工基线（时间、质量）用于对比

**为何之后**：Scout 存在前无法评估 Scout

---

### 路线 C：观察到的失败可靠性

**时机**：Scout 显示特定失败模式后（崩溃、重复、预算超支）

**范围**：
- 添加从 cursor 恢复（幂等重启）
- 改进去重（跨来源、语义相似度）
- 基于观察到的失败调优 runner 限制

**为何之后**：Scout 运行前不知道需要哪些可靠性特性

---

### 路线 D：内存索引（条件性）

**时机**：仅当衡量到检索失败（查询慢、精度低）

**范围**：
- 添加 OKF 时间戳（`created`、`modified`）到 frontmatter
- 在 gitignored 本地索引或仅追加事件日志中跟踪访问/使用（非通过修改 Markdown）
- 实验：SQLite FTS 用于关键词搜索
- 对比用户活跃的 OpenViking adapter
- 条件性：embeddings 仅当 FTS 不足时

**为何之后**：尚无检索瓶颈证据。Markdown 保持权威。

---

### 路线 E：多 Agent（条件性）

**时机**：仅当单 agent Scout 显示吞吐量瓶颈（队列 >5 来源，无法完成每日扫描）

**范围**：
- 并行来源扫描器（每来源一个）
- 层级聚合（manager 组合报告）
- Worktree 隔离处理文件冲突

**为何之后**：无证据表明单 agent 不足。多 agent 增加协调复杂性。

---

### 路线 F：外部可观测性 / 持久工作流（条件性）

**时机**：仅当本地调试痛苦或恢复开销高

**范围**：
- 评估 Langfuse（自托管）vs 本地 JSONL 遥测
- 评估 Temporal/Restate 用于检查点（如衡量到恢复痛点）

**为何之后**：本地遥测和简单重试可能足够。仅当合理时添加外部依赖。

---

## 推荐实施顺序

### 阶段 A：自主 Scout 垂直切片（第 1-4 周）

**Issue A.1**：Scout 源注册和手动触发
- 在 `rules/RESOURCE_APPROVALS.yaml` 定义批准来源（GitHub/HN/arXiv；Product Hunt 门控在批准+API 可用）
- Agent 不得直接修改 `rules/RESOURCE_APPROVALS.yaml` 或 `rules/EXPLORATION_POLICY.md`
- 若需新来源（如 Product Hunt），Agent 写 `data/proposals/rule_changes/` proposal 和 GitHub 审批请求，由 jlcbk 修改/批准 rules
- 构建 Scout runner wrapper（启动、强制执行限制、捕获输出）
- 手动调用：用户运行 `python scripts/scout_runner.py`

**Issue A.2**：Cursor、ledger 和边界扫描
- 每来源跟踪 last-seen（gitignored cursor 状态）
- 按 URL/ID 去重
- 完整保留/拒绝 ledger 带证据（gitignored JSONL）
- 精简 decisions 文件（tracked Markdown）：URL/ID、日期、标题、keep/reject、理由、来源类型
- Runner 强制执行：最大运行时、最大来源、最大扫描/保留项目、最大重试
- Runner 使用 data/config 或现有 rules 的只读结果，不绕过规则

**Issue A.3**：每日决策报告生成
- Scout worker 生成：复用图谱、一项实验/技能/项目候选、证据链接
- 证据链接到 tracked decisions 文件（非 gitignored ledger）
- 提交摘要和 decisions（非原始 ledger 或 cursor 状态）

**Issue A.4**：人工审查标签工作流
- 人类主要通过 GitHub Issue/PR comment 或 review labels 给出反馈：`relevant`、`irrelevant`、`deep-dive`、`pause`
- Agent 将这些反馈同步为 tracked `data/exploration/review_labels/<date>.yaml` 记录
- Agent 读取评论/标签需要明确 repo read 权限；任何写 GitHub 操作仍由 clawbie 身份且在批准 scope 内
- 未来：preference learner 分析标签模式

**Issue A.4**：人工审查标签工作流
- 人类主要通过 GitHub Issue/PR comment 或 review labels 给出反馈：`relevant`、`irrelevant`、`deep-dive`、`pause`
- Agent 将这些反馈同步为 tracked `data/exploration/review_labels/<date>.yaml` 记录
- Agent 读取评论/标签需要明确 repo read 权限；任何写 GitHub 操作仍由 clawbie 身份且在批准 scope 内
- 未来：preference learner 分析标签模式

### 阶段 B：Scout 留出评估（第 5-6 周，Scout 运行后）

**Issue B.1**：留出集和 Scout 质量指标
- 创建独立留出任务（非从 repo 历史以避免答案泄漏）
- 定义 Scout 指标：新颖性、相关性、证据、可操作转换、重复率
- 单独的 Builder 指标：测试通过、验收
- 人工基线用于对比

**Issue B.2**：针对留出集衡量 Scout
- 在留出集上运行 Scout
- 对比人工基线
- 记录成功率、成本、失败模式

### 阶段 C：可靠性改进（观察到的失败触发）

**Issue C.1**：恢复和幂等性（如观察到崩溃）
**Issue C.2**：改进去重（如观察到重复）
**Issue C.3**：内存索引（如检索慢/不精确）
**Issue C.4**：多 agent（如吞吐量瓶颈已证明）
**Issue C.5**：外部可观测性（如调试痛苦）
**Issue C.6**：持久工作流（如恢复开销高）

---

## 一个即时实验

**实验**：在完整 Scout 实现前原型 Scout runner 强制执行

**假设**：Runner 可以在构建完整 Scout 前强制执行墙上时钟、进程数和生命周期限制

**步骤**：
1. 编写最小 Scout runner wrapper（启动 Claude CLI、强制执行超时）
2. 用虚拟任务测试（如"扫描 5 个 HN 项目"）
3. 验证：超时有效、部分结果写入、干净退出

**时间线**：1 天

**成本**：<$5

**成功标准**：
- Runner 在超时时终止
- 部分结果保留
- 无僵尸进程

**学习价值**：在投资完整 Scout 前验证强制执行方法

---

## 一个要学习的技能

**技能**：设计带基于 cursor 恢复的幂等探索 agents

**为什么**：Scout 将被中断（预算、超时、崩溃）。必须无需重新扫描即可恢复。

**学习路径**：
1. 研究 cursor 模式（Stripe API、GitHub 分页、数据库 offset/limit）
2. 为多来源 Scout 设计 cursor schema（每来源 last-seen 时间戳/ID）
3. 实现幂等性：相同输入 + 相同 cursor = 相同输出
4. 测试：中断、恢复、验证无重复

**时间线**：4 小时

**产出**：理解基于 cursor 的恢复用于 Scout 可靠性

---

## 待决策事项

### 决策 1：Scout 垂直切片优先级

**问题**：批准 Scout 作为首要实现优先级？

**选项**：
1. **是，Scout 优先** — 交付用户声明目标，测试高 token 工作流（推荐）
2. 否，基准测试/遥测基础设施优先 — 在构建前衡量
3. 否，内存索引优先 — 在探索前处理检索

**推荐**：是，Scout 优先。将遥测/预算嵌入 Scout runner（非分离基础设施）。

---

### 决策 2：Scout 源批准

**问题**：批准初始 Scout 来源（GitHub/HN/arXiv 公开只读，Product Hunt 当批准时）？

**风险**：网络出口、速率限制、潜在 IP 封禁

**推荐**：批准用于公开只读。GitHub/HN/arXiv 基础访问无需 API 密钥。Product Hunt 当资源批准授予时。

---

### 决策 3：Scout 预算

**问题**：批准每日 Scout 预算？

**选项**：
- 选项 A：2 小时墙上时钟、20 来源扫描、50 项目保留、10 Claude 调用
- 选项 B：4 小时墙上时钟、40 来源扫描、100 项目保留、20 Claude 调用
- 选项 C：用户定义限制在 `rules/EXPLORATION_POLICY.md`

**推荐**：选项 A 用于 MVP（更紧限制，基于观察需求迭代）

---

### 决策 4：之后触发

**问题**：确认延后工作的条件触发？

**条件门**（Scout 运行后衡量）：
- [ ] 内存索引：仅当衡量到检索失败
- [ ] 多 agent：仅当吞吐量瓶颈已证明
- [ ] 外部可观测性：仅当本地调试痛苦
- [ ] 持久工作流：仅当衡量到恢复痛点

**推荐**：确认门。不构建投机基础设施。

---

## 风险和缓解

### 风险 1：每日 Scout 运行的高 token 成本

**缓解**：Runner 强制执行每日限制（来源、项目、运行时）。终止时部分结果。

---

### 风险 2：Scout 产生的不相关发现

**缓解**：人工审查标签提供反馈。迭代提示和过滤逻辑。

---

### 风险 3：依赖外部资源的可用性问题

**缓解**：基于 cursor 的恢复。尊重速率限制头。指数退避。

---

### 风险 4：Runner 强制执行不足

**缓解**：用虚拟任务原型 runner 优先（1 天）。在完整 Scout 前验证强制执行。

---

## Scout MVP 的成功指标

**质量**（Scout 运行后衡量）：
- [ ] 每日报告已生成（非空）
- [ ] 人工审查时间 <30 分钟
- [ ] 相关性在 4 周内改进（通过人工标签）

**成本**（衡量和强制执行）：
- [ ] 零预算超支（runner 终止有效）
- [ ] 每次运行成本：待衡量和优化

**可靠性**（Scout 运行后衡量）：
- [ ] 完成率：待衡量
- [ ] 从中断恢复：待实现和测试

---

## Self-Evo 差异化（不同于死亡框架）

**为何进化生存必要**：
1. Agent 试点失败被广泛报道（成本失控、无限循环）
2. 无审查门的完全自主 agents 有质量死亡螺旋风险
3. 框架锁定造成依赖风险

**Self-evo Scout 策略**：
1. **人工审查门**：每日报告在依据推荐行动前审查
2. **内置成本控制**：Runner 强制执行限制，不承诺无法实现的内部调用级上限
3. **File-first**：Ledger、cursor、telemetry 在 gitignored state；仅摘要提交
4. **基于原语**：SQLite、git、标准工具。不依赖框架生存。
5. **证据驱动**：先交付 Scout，衡量瓶颈，仅当合理时添加复杂性
6. **增量自主**：手动触发 → 计划调用 → 偏好学习

**关键对比**：Scout 不是通用 agent 框架。它是带人工审查的边界探索工作流。

---

## 下一步行动（审查后）

1. **人类审查此报告** → 批准 Scout 优先级、来源、预算
2. **原型 Scout runner** → 1 天，验证强制执行
3. **实现 Scout 垂直切片** → 3-4 周（Issues A.1-A.4）
4. **运行 Scout 4 周** → 收集人工标签，衡量质量/成本
5. **评估 Scout** → 留出集、指标（Issue B.1-B.2）
6. **条件性改进** → 基于衡量的失败（阶段 C）

---

## 业务逻辑修订

本节记录业务逻辑审查识别优先级错位后的变更：

1. **Scout 垂直切片移至首要优先级** — 曾延后到第 15 项 / 阶段 3。现在阶段 A。

2. **Runner 强制执行边界澄清** — 无法承诺内部 LLM 调用级硬 token 上限（hooks 看不到）。Runner 强制执行：墙上时钟、进程数、扫描/保留限制、生命周期。

3. **基准测试答案泄漏修复** — 留出集必须独立，非从 repo 已解决 Issues。

4. **内存访问跟踪修正** — 不在读取时修改 Markdown。使用 gitignored 索引或仅追加事件日志。

5. **遥测嵌入 Scout** — 非分离基础设施。Scout runner 捕获 CLI 暴露的；未知保持未知。

6. **state/budget.db 不跟踪状态** — 增长的运行时状态（ledger、cursor、telemetry）保持 gitignored。仅提交摘要/schemas。

7. **移除主动侦查延后语言** — Scout 就是主动侦查。现在首要优先级，非延后。

8. **移除固定数字阈值** — 无">1000 tasks/day"、"read updates accessed"等。本地衡量后设置阈值。

9. **Ledger 可审阅性** — 原始 HTTP/API payload、下载缓存、cursor、dedupe cache、telemetry 保持 gitignored。精简 source/query/decision ledger（URL/ID、日期、标题/metadata、keep/reject、理由、来源类型）tracked 在 `data/exploration/raw/`。Daily report 链接到 tracked ledger。

10. **治理边界** — Agent/worker 不得直接修改 `rules/RESOURCE_APPROVALS.yaml` 或 `rules/EXPLORATION_POLICY.md`。若需新来源，Agent 写 `data/proposals/rule_changes/` proposal 和 GitHub 审批请求，由 jlcbk 修改/批准 rules。Runner 使用只读规则。

11. **人工反馈入口** — 人类主要通过 GitHub Issue/PR comment 或 review labels 给出反馈。Agent 将这些同步为 tracked `data/exploration/review_labels/` 记录。Agent 读评论/标签需明确 repo read 权限；写 GitHub 由 clawbie 身份且在批准 scope。

**业务的核心架构推荐**：
- Scout 垂直切片作为首要业务目标
- 人工审查门（每日报告工作流）
- 原语优于框架（SQLite、git、Markdown）
- Runner 强制执行限制（墙上时钟、进程数、扫描/保留）
- 基于 cursor 的幂等恢复
- Markdown 权威，数据库作为索引
- 证据驱动的升级（衡量瓶颈后添加复杂性）
- Tracked ledger 用于人工审阅，gitignored 原始数据

---

**每日报告结束**

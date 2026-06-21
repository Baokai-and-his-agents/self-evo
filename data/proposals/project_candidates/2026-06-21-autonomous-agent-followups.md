---
title: "项目候选：自主 Agent 生态系统后续 Issues"
date: 2026-06-21
parent_issue: 7
type: project_candidates
status: proposed
---

# 项目候选：自主 Agent 生态系统后续 Issues

## 概述

基于 Issue #7 研究，这些子 Issues 代表具体实现工作。**业务审查后优先级重新排序**：自主 Scout 垂直切片现在是首要，通用基础设施延后直到衡量需求触发。

**尚未创建这些 GitHub Issues**。本文档提出候选供人工审查。批准后，按推荐顺序创建 Issues。

---

## 阶段 A：自主 Scout 垂直切片（主要业务目标）

### Issue #A.1：Scout 源注册和 Runner Wrapper

**类型**：Feature (Scout MVP)
**目标**：通过批准来源启用边界 Scout 执行
**预计工期**：1 周

**范围**：
- 只读检查 `rules/RESOURCE_APPROVALS.yaml`，仅把其中已批准的公开来源交给 Runner
- Agent 不得直接修改 `rules/RESOURCE_APPROVALS.yaml` 或 `rules/EXPLORATION_POLICY.md`
- 若 GitHub/HN/arXiv/Product Hunt 等目标来源尚未批准，候选任务应：
  - Agent 写 `data/proposals/rule_changes/<date>-<topic>-resource-approval.md` proposal 和 GitHub 审批请求
  - 由 `jlcbk` 修改或批准 `rules/` 中的规则文件后，Runner 才允许该来源
- 构建 Scout runner wrapper 脚本（`scripts/scout_runner.py`）
- Runner 启动 Claude CLI worker 执行 Scout 任务
- Runner 强制执行：最大墙上时钟时间（可配置，如 2 小时）、最大 Claude 进程调用数（如 10）、最大重试（如 3）
- Runner 捕获：可用的结构化 CLI 输出/用量、退出码、墙上时钟持续时间
- 未知 token/成本记录为 "unknown" 带解释（hooks 不暴露内部调用级指标）
- Runner 使用 data/config 或现有 rules 的只读结果，不绕过规则
- 手动调用：用户运行 `python scripts/scout_runner.py --issue <N>`

**验收标准**：
- [ ] Runner 能读取现有资源审批结果，并拒绝任何未批准来源
- [ ] 对尚未批准的目标来源，存在 `data/proposals/rule_changes/` proposal 和 GitHub 人工审批请求
- [ ] 只有在 `jlcbk` 完成人工批准后，对应来源才可进入 Runner
- [ ] Scout runner 脚本存在且启动 Claude CLI
- [ ] Runner 强制执行墙上时钟超时（超出时终止进程）
- [ ] Runner 强制执行最大调用数（N 个 Claude 进程后停止）
- [ ] Runner 捕获 CLI 输出并将运行遥测写入 gitignored `state/telemetry/<date>/<run-id>.jsonl`
- [ ] Runner 在终止时写入部分结果（信号处理器）
- [ ] 手动调用先记录在 `data/` 下的使用文档或 proposal；如需进入 `rules/EXPLORATION_POLICY.md`，必须另走人工批准的规则变更

**前置依赖**：None

**风险**：低（手动触发、仅批准来源、边界执行）

**所需权限**：
- 网络出口到批准来源（公开只读）
- 启动 Claude CLI 子进程
- 写入 `state/telemetry/`（gitignored）
- 超时时杀死子进程

**推荐顺序**：A.1（首要）

---

### Issue #A.2：Cursor、去重和保留/拒绝账本

**类型**：Feature (Scout MVP)
**目标**：启用幂等恢复和证据支持的过滤
**预计工期**：1 周

**范围**：
- 在 gitignored `state/scout_cursor.json` 中每来源跟踪 last-seen cursor（时间戳或项目 ID）
- 去重：按 URL/ID 跳过已处理项目（精确匹配，gitignored cache）
- 完整保留/拒绝 ledger：每项决策带理由记录在 gitignored `data/exploration/raw/<date>-<source>-ledger.jsonl`（HTTP/API payload、下载缓存保持 gitignored）
- 精简 decisions ledger（tracked）：记录在 `data/exploration/raw/<date>-<source>-decisions.md`，包含 URL/ID、日期、标题/metadata、keep/reject、理由、来源类型，不含大段版权内容
- Runner 强制执行：最大扫描来源数（如 20）、每来源最大扫描项目数（如 100）、最大保留项目数（如 50）
- 恢复：下次运行时加载 cursor 并跳过已处理
- 提交到 repo：仅聚合摘要和 tracked decisions（非原始 ledger 或 cursor 状态）

**验收标准**：
- [ ] Cursor 跟踪：Scout 在 `state/scout_cursor.json`（gitignored）存储每来源 last-seen
- [ ] 去重：恢复时跳过重复项目（测试验证）
- [ ] 完整 Ledger：每项带 keep/reject 决策和理由记录在 gitignored JSONL
- [ ] 精简 Decisions：tracked Markdown 包含 URL/ID、日期、标题、keep/reject、理由、来源类型
- [ ] Runner 强制执行扫描/保留限制（超出时停止）
- [ ] 恢复：Scout 从 cursor 恢复无需重新扫描（测试验证）
- [ ] 仅摘要提交：gitignored 状态（cursor、完整 ledger、cache）排除在 repo 外，tracked decisions 提交

**前置依赖**：Issue #A.1（runner wrapper）

**风险**：中（cursor schema 必须处理多样来源格式，去重可能遗漏语义重复）

**所需权限**：
- 读/写 `state/scout_cursor.json`（gitignored）
- 写完整 ledger 到 `data/exploration/raw/`（gitignored JSONL）
- 写精简 decisions 到 `data/exploration/raw/`（tracked Markdown）
- 提交摘要到 repo（仅 tracked 文件）

**推荐顺序**：A.2（第二）

---

### Issue #A.3：每日决策报告生成

**类型**：Feature (Scout MVP)
**目标**：生成人类可审查的可操作输出
**预计工期**：1 周

**范围**：
- Scout worker 将扫描结果合成为每日决策报告
- 报告结构：复用图谱（现有工作调研）、一项实验/技能/项目候选、证据链接到 tracked decisions ledger
- 报告存储在 tracked `data/exploration/daily_reports/<date>-<topic>.md`
- 报告 frontmatter：date、issue、status、researcher
- Runner 验证报告存在才完成运行

**验收标准**：
- [ ] 每日报告生成具有必需结构（复用图谱、候选、证据）
- [ ] 报告 frontmatter 包括：date、issue、status、researcher
- [ ] 报告存储在 tracked `data/exploration/daily_reports/`
- [ ] 证据链接引用 tracked decisions ledger 条目（按 ID 或 URL），非远端不可见的 gitignored 文件
- [ ] Runner 验证报告文件存在才标记运行完成
- [ ] 报告是人类可读 Markdown（非原始 JSON 转储）

**前置依赖**：Issue #A.2（ledger 提供证据）

**风险**：低（报告生成是综合任务，Claude 擅长此）

**所需权限**：
- 写入 `data/exploration/daily_reports/`（tracked）
- 读取 tracked decisions ledger 从 `data/exploration/raw/`

**推荐顺序**：A.3（第三）

---

### Issue #A.4：人工审查标签工作流

**类型**：Feature (Scout MVP)
**目标**：为偏好学习启用反馈循环
**预计工期**：3 天

**范围**：
- 人类主要通过 GitHub Issue/PR comment 或已定义 review labels 给出反馈：`relevant`、`irrelevant`、`deep-dive`、`pause`
- Agent 将这些反馈同步成 tracked `data/exploration/review_labels/<date>.yaml` 记录，便于后续 preference analysis
- 标签 schema：item_id、item_url、label、reason（可选）
- Agent 读取评论/标签需要明确 repo read 权限；任何写 GitHub 操作仍由 clawbie 身份且在批准 scope 内
- 未来：preference learner 分析标签历史以改进过滤
- MVP：仅手动标签，无自动偏好学习

**验收标准**：
- [ ] 标签 schema 记录在 `data/exploration/review_labels/README.md`
- [ ] 创建示例标签文件
- [ ] 用户工作流记录：审查报告 → 通过 GitHub comment/labels 添加反馈 → Agent 同步到 YAML 文件 → 提交
- [ ] 标签存储在 tracked `data/exploration/review_labels/`
- [ ] Agent 读评论/标签的 repo read 权限明确；写 GitHub 由 clawbie 身份
- [ ] MVP 无自动偏好学习（未来增强）

**前置依赖**：Issue #A.3（报告提供待标签项目）

**风险**：低（手动工作流，无自动化）

**所需权限**：
- 读取每日报告
- 读取 GitHub Issue/PR comments（需明确 repo read 权限）
- 写入 `data/exploration/review_labels/`（tracked）
- 写 GitHub 由 clawbie 身份且在批准 scope 内

**推荐顺序**：A.4（第四）

---

## 阶段 B：Scout 留出评估（Scout 运行后）

### Issue #B.1：Scout 留出集和质量指标

**类型**：Evaluation
**目标**：独立于训练数据衡量 Scout 质量
**预计工期**：1 周

**范围**：
- 创建独立留出集（非从 repo 已解决 Issues 以避免答案泄漏）
- 定义 Scout 质量指标：新颖性（% 新发现）、相关性（% 人工批准）、证据质量（链接有效、声明支持）、可操作转换（% 导向实验/技能）、重复率（% 冗余）
- 单独定义 Builder 质量指标：测试通过率、验收标准满足
- 包括人工基线：人类执行相同 Scout 任务，对比时间和质量

**验收标准**：
- [ ] 创建 10-20 个独立 Scout 任务的留出集
- [ ] 留出任务在 repo 历史中无解决方案（通过 git grep 验证）
- [ ] Scout 指标定义和记录
- [ ] Builder 指标单独定义
- [ ] 人工基线协议记录
- [ ] 留出集存储在 `data/benchmarks/scout_holdout/`

**前置依赖**：Scout 垂直切片运行（Issues A.1-A.4）

**风险**：中（留出集质量取决于任务选择，指标可能需要迭代）

**所需权限**：
- 读取 repo 历史（验证无答案泄漏）
- 写入 `data/benchmarks/scout_holdout/`（tracked）

**触发条件**：Scout 运行后完成，扩展前

**推荐顺序**：B.1（第五）

---

### Issue #B.2：在留出集上运行 Scout 并测量

**类型**：Evaluation
**目标**：量化 Scout 成功率、成本、失败模式
**预计工期**：3 天

**范围**：
- 在留出集上运行 Scout（10-20 任务）
- 衡量：成功率（% 任务有效输出）、新颖率、相关率、可操作转换、重复率、每任务成本、每任务时间
- 对比人工基线：质量增量、时间增量
- 记录失败模式：速率限制、低质量来源、不相关发现
- 生成评估报告在 `data/benchmarks/scout_eval_<date>.md`

**验收标准**：
- [ ] Scout 在所有留出任务上运行
- [ ] 收集指标：成功、新颖性、相关性、可操作转换、重复、成本、时间
- [ ] 包括人工基线对比
- [ ] 失败模式分类带示例
- [ ] 评估报告记录发现和推荐
- [ ] 决策：继续扩展、迭代提示或转换方法

**前置依赖**：Issue #B.1（留出集）

**风险**：低（只读评估，无生产变更）

**所需权限**：
- 运行 Scout（消耗预算）
- 写入 `data/benchmarks/`（tracked）

**触发条件**：Scout 运行后完成，扩展前

**推荐顺序**：B.2（第六）

---

## 阶段 C：可靠性改进（观察到的失败触发）

### Issue #C.1：Scout 可靠性（恢复、去重）

**类型**：Enhancement
**目标**：处理 Scout 运行观察到的失败模式
**预计工期**：1 周

**范围**（条件性，取决于观察到的失败）：
- 如观察到崩溃：改进恢复鲁棒性，验证 cursor 正确性
- 如观察到重复：添加语义去重（embedding 相似度）
- 如观察到速率限制：添加指数退避，尊重速率限制头
- 如观察到无进展：检测并终止卡住的扫描

**验收标准**：
- [ ] Scout 运行的失败模式记录
- [ ] 针对性修复实现（仅针对观察到的失败）
- [ ] 为修复的失败模式添加回归测试
- [ ] Scout 可靠性指标改进（在留出或实时运行上衡量）

**前置依赖**：Scout 垂直切片运行、评估完成

**风险**：低（针对性修复，证据驱动）

**所需权限**：与 Scout 垂直切片相同

**触发条件**：仅当 Scout 运行或评估中观察到特定可靠性失败时完成

**推荐顺序**：C.1（第七，条件性）

---

### Issue #C.2：内存索引（条件性）

**类型**：Enhancement
**目标**：仅当衡量为瓶颈时处理检索性能
**预计工期**：2 周

**范围**（条件性，取决于衡量的检索失败）：
- 添加 OKF 时间戳（`created`、`modified`）到内存 frontmatter（不添加 `accessed` 或读取时修改）
- 在 gitignored 本地索引（`state/memory_access.db`）或仅追加事件日志中跟踪访问/使用
- 实验：SQLite FTS 用于关键词搜索，衡量精度/召回
- 对比用户活跃的 OpenViking adapter（如可用）
- 条件性：仅当 FTS 精度不足时添加 embeddings
- 归档/恢复协议：仅手动、可逆、需要冷却提案 + 人工批准

**验收标准**：
- [ ] 检索瓶颈衡量和记录（查询慢、精度低）
- [ ] OKF 时间戳添加到内存（仅 created、modified）
- [ ] 访问跟踪在 gitignored 索引（Markdown 文件不修改）
- [ ] SQLite FTS 实验完成并记录结果
- [ ] OpenViking 对比（如可用）
- [ ] 推荐：采用 FTS、采用 embeddings 或保持仅文件
- [ ] 归档/恢复协议记录（手动、可逆）

**前置依赖**：无（内存系统独立）

**风险**：低（仅添加，Markdown 保持权威）

**所需权限**：
- 读/写 `data/memory/`（仅 frontmatter）
- 创建 `state/memory_access.db`（gitignored）
- 创建 `state/memory_fts.db` 用于实验（gitignored）

**触发条件**：仅当衡量到检索失败时完成（慢、不精确或召回问题）

**推荐顺序**：C.2（第八，条件性）

---

### Issue #C.3：多 Agent 协调（条件性）

**类型**：Enhancement
**目标**：仅当吞吐量瓶颈已证明时启用并行 Scout 执行
**预计工期**：2-3 周

**范围**（条件性，取决于衡量的吞吐量瓶颈）：
- 并行来源扫描器：每来源一个 Scout worker
- 层级聚合：manager Scout 组合每来源报告
- Worktree 隔离：每 Scout worker 在独立 git worktree
- 协调：SQLite 基于租约的认领（state/coordination.db，gitignored）
- 状态聚合：父 Issue 跟踪子 Scout 进度

**验收标准**：
- [ ] 吞吐量瓶颈记录：单 Scout 无法在时间预算内扫描所有来源
- [ ] 并行 Scouts 实现带 worktree 隔离
- [ ] Manager Scout 聚合每来源报告
- [ ] SQLite 租约协调防止重复扫描
- [ ] 集成测试：3 个 Scouts 并行扫描不同来源，manager 组合
- [ ] 协调开销衡量且可接受（<总时间 30%）

**前置依赖**：Scout 垂直切片运行、评估完成

**风险**：高（协调复杂性、worktree 开销、可能不改进吞吐量）

**所需权限**：
- 创建 git worktrees
- 写入 `state/coordination.db`（gitignored）
- 生成多个 Scout 进程

**触发条件**：仅当 Scout 评估显示吞吐量瓶颈时完成（无法在预算内扫描所有来源）

**推荐顺序**：C.3（第九，条件性）

---

### Issue #C.4：外部可观测性对比（条件性）

**类型**：Infrastructure（可选）
**目标**：仅当本地遥测不足时评估外部平台
**预计工期**：1 周

**范围**（条件性，取决于调试痛点）：
- 对比 Langfuse（自托管）、Arize Phoenix、OpenLLMetry
- 集成一个平台（推荐 Langfuse 自托管 Docker）
- 运行 Scout 启用外部可观测性
- 对比本地 JSONL 遥测：功能、开销、调试工作流
- 在外部数据传输前需要明确用户批准

**验收标准**：
- [ ] 本地遥测瓶颈记录（调试不足）
- [ ] 对比文档覆盖 3+ 工具带成本/功能矩阵
- [ ] 一个工具集成并测试
- [ ] 并列对比：相同 Scout 运行的本地 vs 外部
- [ ] 推荐带理由
- [ ] 用户选入门防止自动外部传输
- [ ] 自托管选项验证（Docker Compose）

**前置依赖**：Scout 垂直切片运行带本地遥测

**风险**：中（外部依赖、数据传输需要批准）

**所需权限**：
- 网络出口到外部服务（需用户批准）
- 安装可观测性 SDK
- 写凭证到配置（用户提供）

**触发条件**：仅当本地遥测不足以调试 Scout 失败时完成

**推荐顺序**：C.4（第十，条件性）

---

### Issue #C.5：持久工作流引擎（条件性）

**类型**：Infrastructure（高级）
**目标**：仅当衡量到恢复痛点时添加检查点
**预计工期**：2-3 周

**范围**（条件性，取决于恢复痛点）：
- 评估 Temporal、Restate、Inngest 或自定义检查点
- 在 Scout 阶段边界实现检查点（扫描 → 综合 → 报告）
- 恢复协议：崩溃或超时时从检查点恢复
- 测试：中途杀死 Scout，恢复，验证无重复工作

**验收标准**：
- [ ] 恢复痛点记录：X% 的 Scout 运行将受益于检查点
- [ ] 工作流引擎评估并选择一个（或自定义设计）
- [ ] 检查点在阶段边界实现
- [ ] 恢复测试：Scout 恢复无需重做已完成工作
- [ ] 成本开销衡量且可接受
- [ ] 推荐：何时使用 vs 简单重试

**前置依赖**：Scout 垂直切片运行、失败模式衡量

**风险**：高（外部依赖或大量自定义代码）

**所需权限**：
- 写检查点状态到 `state/checkpoints/`（gitignored）
- 网络访问工作流引擎（如云）
- 从保存状态恢复 Scout 执行

**触发条件**：仅当 Scout 恢复痛点衡量为实质性时完成（在观察失败后设置阈值，非提前）

**推荐顺序**：C.5（第十一，条件性）

---

## 实施顺序摘要

**阶段 A：自主 Scout 垂直切片（MVP）** — 3-4 周
1. Issue #A.1：Scout 源注册和 runner wrapper
2. Issue #A.2：Cursor、去重和保留/拒绝 ledger
3. Issue #A.3：每日决策报告生成
4. Issue #A.4：人工审查标签工作流

**阶段 B：Scout 评估** — 1-2 周（Scout 运行后）
5. Issue #B.1：Scout 留出集和质量指标
6. Issue #B.2：针对留出集运行 Scout 并衡量

**阶段 C：条件性改进** — 由衡量的失败触发
7. Issue #C.1：Scout 可靠性（仅当观察到特定失败时）
8. Issue #C.2：内存索引（仅当检索瓶颈衡量时）
9. Issue #C.3：多 agent 协调（仅当吞吐量瓶颈已证明时）
10. Issue #C.4：外部可观测性（仅当本地遥测不足时）
11. Issue #C.5：持久工作流（仅当恢复痛点衡量时）

---

## 阶段 A（Scout MVP）的成功标准

**完成 Issues #A.1-A.4 后**：
- [ ] Scout 在预算内生成每日决策报告
- [ ] 人工审查时间 <30 分钟每报告
- [ ] 零预算超支（runner 终止有效）
- [ ] Scout 从中断恢复无重复
- [ ] 用户可标签项目用于未来偏好学习

---

## 风险和缓解

### 风险：Scout 产生的不相关发现

**缓解**：人工审查标签提供反馈。迭代提示和过滤逻辑。用留出集衡量质量（阶段 B）。

---

### 风险：每日 Scout 运行的高 token 成本

**缓解**：Runner 强制执行每日限制（来源、项目、运行时）。终止时部分结果。基于观察成本调优限制。

---

### 风险：依赖外部资源的可用性问题

**缓解**：基于 cursor 的恢复。尊重速率限制头。指数退避。未来：缓存和增量刷新。

---

### 风险：Runner 强制执行不足

**缓解**：在完整 Scout 前用虚拟任务测试 runner。验证超时、进程终止、部分结果。

---

## 业务逻辑修订

本文档在业务逻辑审查识别优先级错位后重新排序：

1. **自主 Scout 垂直切片移至阶段 A（首要优先级）** — 曾是第 15+ 项 / 阶段 3。现在是 issues A.1-A.4。

2. **通用基础设施延后至阶段 C（条件性）** — 基准测试、遥测、内存索引、多 agent、可观测性、持久工作流现在由衡量需求触发，非投机构建。

3. **Scout runner 强制执行边界澄清** — 无法承诺内部 LLM 调用级硬 token 上限。Runner 强制执行：墙上时钟、进程数、扫描/保留限制、生命周期。

4. **基准测试答案泄漏修复** — 留出集必须独立，非从 repo 已解决 Issues（Issue B.1）。

5. **内存访问跟踪修正** — 不在读取时修改 Markdown。使用 gitignored 索引或仅追加事件日志（Issue C.2）。

6. **遥测嵌入 Scout runner** — 非分离基础设施。Scout runner 捕获 CLI 暴露的；未知保持未知（Issue A.1）。

7. **state/ 文件澄清为 gitignored** — 增长的运行时状态（cursor、完整 ledger、telemetry、coordination.db）保持 gitignored。仅提交摘要/schemas 和 tracked decisions。

8. **移除固定数字阈值** — 无"1000 tasks/day"、"read updates accessed timestamp"、"固定成功率"。本地衡量后设置阈值。

9. **评估轨道分离** — Scout 质量（新颖性、相关性、证据、可操作转换、重复率）vs Builder 质量（测试、验收）vs 人工基线（Issue B.1-B.2）。

10. **Ledger 可审阅性** — 完整原始 HTTP/API payload、下载缓存、cursor、dedupe cache、telemetry 保持 gitignored。精简 decisions ledger（tracked）记录 URL/ID、日期、标题、keep/reject、理由、来源类型。Daily report 链接到 tracked decisions。

11. **治理边界** — Agent/worker 不得直接修改 `rules/RESOURCE_APPROVALS.yaml` 或 `rules/EXPLORATION_POLICY.md`。若需新来源，Agent 写 `data/proposals/rule_changes/` proposal 和 GitHub 审批请求。由 jlcbk 修改/批准 rules 后，worker 才认为正式批准。Runner 使用只读规则结果。

12. **人工反馈入口** — 人类主要通过 GitHub Issue/PR comment 或 review labels 给出反馈。Agent 将这些同步为 tracked `data/exploration/review_labels/` 记录。Agent 读评论/标签需明确 repo read 权限；写 GitHub 由 clawbie 身份且在批准 scope。

**业务的核心架构推荐**：
- Scout 垂直切片作为首要优先级（交付用户声明目标）
- Runner 强制执行限制（墙上时钟、进程数、扫描/保留）
- 基于 cursor 的幂等恢复
- 人工审查门（每日报告工作流）
- Markdown 权威，数据库作为 gitignored 索引
- 证据驱动的升级（衡量瓶颈后添加复杂性）
- 原语优于框架（SQLite、git、Markdown）
- Tracked ledger 用于人工审阅，gitignored 原始数据
- 治理边界：Agent 提案规则变更，人类批准

---

**项目候选结束**

**下一步行动**：人类审查提出的 Issues，批准实施顺序，为阶段 A 创建 GitHub Issues。

**Phase B: Scout Evaluation** — 1-2 weeks (after Scout operational)
5. Issue #B.1: Scout holdout set and quality metrics
6. Issue #B.2: Run Scout against holdout and measure

**Phase C: Conditional Improvements** — triggered by measured failures
7. Issue #C.1: Scout reliability (only if specific failures observed)
8. Issue #C.2: Memory indexing (only if retrieval bottleneck measured)
9. Issue #C.3: Multi-agent coordination (only if throughput bottleneck proven)
10. Issue #C.4: External observability (only if local telemetry insufficient)
11. Issue #C.5: Durable workflow (only if recovery pain measured)

---

## 阶段 A（Scout MVP）的成功标准

**完成 Issues #A.1-A.4 后**：
- [ ] Scout produces daily decision report within budget
- [ ] Human review time <30 min per report
- [ ] Zero budget overruns (runner termination works)
- [ ] Scout resumes from interruption without duplicates
- [ ] User can label items for future preference learning

---

## 风险和缓解

### 风险：Scout 产生的不相关发现

**缓解**：Human review labels provide feedback. Iterate prompts and filtering logic. Measure quality with holdout (Phase B).

---

### 风险：每日 Scout 运行的高 token 成本

**缓解**：Runner enforces daily limits (sources, items, runtime). Partial results on termination. Tune limits based on observed costs.

---

### 风险：依赖外部资源的可用性问题

**缓解**：Cursor-based resumption. Respect rate limit headers. Exponential backoff. Future: cache and incremental refresh.

---

### 风险：Runner 强制执行不足

**缓解**：Test runner with dummy task before full Scout. Validate timeout, process termination, partial results.

---

## 业务逻辑修订

This document was reordered after business-logic review identified priority misalignment:

1. **Autonomous Scout vertical slice moved to Phase A (first priority)** — Was items 15+ / Phase 3. Now issues A.1-A.4.

2. **Generic infrastructure deferred to Phase C (conditional)** — Benchmark, telemetry, memory indexing, multi-agent, observability, durable workflow now triggered by measured needs, not built speculatively.

3. **Scout runner enforcement boundary clarified** — Cannot promise hard per-internal-LLM-call token cap. Runner enforces: wall-clock, process count, scan/keep limits, lifecycle.

4. **Benchmark answer leakage fixed** — Holdout set must be independent, not from repo's solved Issues (Issue B.1).

5. **Memory access tracking corrected** — Do NOT mutate Markdown on read. Use gitignored index or append-only event log (Issue C.2).

6. **Telemetry embedded in Scout runner** — Not detached infrastructure. Scout runner captures what CLI exposes; unknown stays unknown (Issue A.1).

7. **state/ files clarified as gitignored** — Growing runtime state (cursor, ledger, telemetry, coordination.db) stays gitignored. Only summaries/schemas committed.

8. **Removed fixed numeric thresholds** — No "1000 tasks/day", "read updates accessed timestamp", "fixed success rates". Measure locally, then set thresholds.

9. **Evaluation tracks separated** — Scout quality (novelty, relevance, evidence, actionable conversion, duplicate rate) vs Builder quality (tests, acceptance) vs human baseline (Issue B.1-B.2).

**业务的核心架构推荐**：
- Scout vertical slice as first priority (delivers user's stated goal)
- Runner-enforced limits (wall-clock, process count, scan/keep)
- Cursor-based idempotent resumption
- Human review gates (daily report workflow)
- Markdown canonical, database as gitignored index
- Evidence-based escalation (measure bottleneck before adding complexity)
- Primitives over frameworks (SQLite, git, Markdown)

---

**项目候选结束**

**下一步行动**：Human reviews proposed Issues, approves implementation order, creates GitHub Issues for Phase A.

---
title: "复用图谱：自主 Agent 生态系统"
date: 2026-06-21
issue: 7
type: reuse_map
status: complete
---

# 复用图谱：Self-Evo 应直接采用、改造或新建的方案

## 决策框架

**直接采用（Adopt）**：直接使用，只需少量集成工作
**改造采用（Adapt）**：组合模式或为 self-evo 的 file-first 方法修改
**拒绝（Reject）**：不符合 self-evo 目标或架构
**新建（Build）**：不存在成熟方案，需要新实现

---

## 直接采用

### 1. Google Open Knowledge Format (OKF) v0.1

**方案**：Markdown+YAML 记忆标准，带时间戳和链接约定。

**集成方式**：
```yaml
---
name: short-kebab-case-slug
description: one-line summary
created: 2026-06-21T10:30:00Z
modified: 2026-06-21T15:45:00Z
metadata:
  type: user | feedback | project | reference
---

Memory content with [[linked-memory]] references.
```

**注意**：不要添加会在读取时修改的 `accessed` 时间戳。如需访问跟踪，使用独立的 gitignored 索引或仅追加的事件日志。

**工作量**：1 天（添加 created/modified 字段，更新记忆写入函数）

**优势**：
- 符合标准（面向未来）
- Git 原生（无破坏性变更）
- 支持遗忘实验的时间衰减评分（如需要）

**风险**：无（仅添加，Markdown 保持权威）

---

### 2. 本地结构化遥测（JSONL + OpenTelemetry）

**方案**：基于文件的结构化日志，使用 OpenTelemetry 兼容 schema 进行本地分析。

**集成方式**：Scout runner wrapper 捕获可用的结构化 CLI 输出/使用数据，写入 gitignored `state/telemetry/<date>/<run-id>.jsonl`，使用标准 spans。

```python
import json
from datetime import datetime

def log_span(name, issue_id, metadata, start, end, tokens_used=None):
    event = {
        "timestamp": datetime.utcnow().isoformat(),
        "span_name": name,
        "issue_id": issue_id,
        "metadata": metadata,
        "duration_ms": int((end - start) * 1000),
        "tokens_used": tokens_used if tokens_used is not None else "unknown",
        "trace_id": f"issue-{issue_id}"
    }
    # Write to gitignored state/telemetry/, not tracked in repo
    with open(f"state/telemetry/{date.today()}/{issue_id}.jsonl", "a") as f:
        f.write(json.dumps(event) + "\n")
```

**工作量**：嵌入 Scout runner（Issue A.1），无需独立基础设施项目

**优势**：
- 零外部依赖
- 仅本地（未经批准不传输到外部）
- OpenTelemetry 兼容（未来迁移路径）
- 按 issue/agent/day 跟踪成本（CLI 可暴露时）
- 无需云访问即可事后分析

**风险**：CLI 不暴露内部调用级指标时 token/成本为未知（记录为 "unknown"）

---

### 3. ResearchPlanAssignOps 模式

**方案**：带阶段门和人工审查的层级 Issue 分解。

**模式**：
1. 人工提交父 Issue
2. Scout agent 研究，生成计划
3. 人工审查计划，批准阶段
4. 执行 agent 处理已批准阶段
5. 创建 Draft PR，人工审查
6. 重复下一阶段

**集成方式**：编入 `rules/ISSUE_WORKFLOW.md`，在 GitHub 中使用阶段标签。

**工作量**：1 周（工作流文档、阶段转换逻辑、GitHub 标签自动化）

**优势**：
- 符合 self-evo 的人工审查原则
- 生产验证模式（用于研究自动化）
- 成本控制的自然检查点

**风险**：无（编入现有意图）

---

### 3. Scout 留出评估集

**方案**：Scout 质量评估的独立任务套件，避免答案泄漏。

**集成方式**：从新任务创建留出集，不要从已知良好结果在 repo 历史中的已完成 Issues 创建。

```yaml
# data/benchmarks/scout_holdout/task-001-new-domain.yml
task_id: scout-task-001
description: "Explore emerging observability patterns in distributed systems"
input_context: ["Current tech landscape, not in repo history"]
expected_outputs:
  - "data/exploration/daily_reports/*.md"
  - "data/exploration/reuse_maps/*.md"
success_criteria:
  - report_created: true
  - markdown_valid: true
  - frontmatter_present: true
  - evidence_links: {min: 5}
  - no_answer_leakage: true  # Verify no solution in repo history
```

**工作量**：1 周（创建独立留出任务、定义 Scout 特定指标、运行基线）

**优势**：
- 衡量实际 Scout 工作流（非通用编码）
- 验证新颖性发现、相关性过滤、证据质量
- 避免答案泄漏（留出集独立于 repo 历史）
- 分离 Scout 质量（探索）和 Builder 质量（实现）

**风险**：留出集设计质量影响评估有效性

---

### 4. SWE-bench 可选对比

**方案**：标准编码 agent 基准测试（500 个已验证任务）用于可选对比。

**集成方式**：在 self-evo 原生基准测试建立基线后运行。

**工作量**：3-4 天（设置评估工具、在 Verified 子集上运行 Claude Code、收集指标）

**优势**：
- 将 self-evo 编码 worker 能力与行业标准对比
- 识别编码特定差距与研究/探索模式
- 外部有效性（同行对比）

**风险**：计算成本（完整 Verified 运行约 $50-100）

**优先级**：P2（可选验证，非主要衡量）

---

### 5. SQLite 基于租约的协调

**方案**：带 TTL + 心跳的任务认领，用于多 agent 协调。

**Schema**：
```sql
CREATE TABLE task_claims (
  task_id TEXT PRIMARY KEY,
  agent_id TEXT NOT NULL,
  claimed_at INTEGER NOT NULL,
  expires_at INTEGER NOT NULL,
  heartbeat_at INTEGER NOT NULL
);

-- Atomic claim with CAS
INSERT OR IGNORE INTO task_claims (task_id, agent_id, claimed_at, expires_at, heartbeat_at)
VALUES (?, ?, ?, ?, ?);
```

**集成方式**：`state/coordination.db` 配合租约库（Python 实现约 200 行）。

**工作量**：1 周（schema、认领/释放/心跳函数、过期清理）

**优势**：
- 无外部依赖（SQLite 内置）
- 验证模式（AutoGPT、agent-coordinator）
- 自动处理 agent 崩溃

**风险**：仅单主机（MVP 足够）

---

## 改造组合

### 5. 外部可观测性对比（需批准门控）

**方案**：在本地遥测验证后，对比 Langfuse vs OpenLLMetry 用于生产可观测性。

**集成方式**：仅在本地 JSONL 遥测建立基线需求后。

**Langfuse**：
- 优势：丰富 UI、会话重放、prompt 版本控制
- 劣势：外部依赖、需要自托管或云账户
- 成本：约 $0-49/月（云）或托管开销

**OpenLLMetry**：
- 优势：供应商中立、OpenTelemetry 标准、导出灵活性
- 劣势：需要独立后端（Jaeger/Zipkin/Grafana）
- 成本：自托管基础设施

**决策标准**：
1. 本地遥测不足以调试？（先尝试 2-3 个 Issues）
2. 需要实时监控 vs 事后分析？（异步分析可能足够）
3. 需要多用户访问？（单用户 MVP 可能不需要仪表板）

**工作量**：每个选项 2-3 天（SDK 集成、span 插桩、仪表板设置）

**优先级**：P2（仅在本地遥测瓶颈测量后）

---

### 6. 混合记忆架构（File + Index）

**模式**：Markdown 文件作为真实来源，SQLite FTS + embeddings 用于检索。

**改造自**：Cognee（多存储）、Mem0（提取）、ENGRAM（类型化检索）

**架构**：
```
data/memory/hot/           # Canonical Markdown+YAML
state/memory_index.db      # SQLite FTS + vector extension
  - memories table (id, file_path, content_hash)
  - fts_index (full-text search)
  - embeddings (vector similarity)
```

**集成方式**：
- **阶段 1**：仅 SQLite FTS（关键词搜索，1 周）
- **阶段 2**：当记忆数超过测量阈值时添加 embeddings（2 周）—— 由实际检索精度指标触发，待定
- **阶段 3**：遗忘机制（时间衰减 + 访问频率，1 周）

**优势**：
- 扩展到 1000+ 条记忆
- 保持 git 原生工作流
- 数据库可从文件重建（非权威）

**风险**：索引过时（记忆变更时重建）

---

### 7. 三层终止防御

**模式**：多个独立安全限制防止失控执行。

**改造自**：Autonomous-agents.io 建议、生产 agent 部署

**层级**：
1. **每 issue token 预算**（如 100k tokens）：超过时硬停止
2. **工具调用深度限制**（如 50 次调用）：防止无限循环
3. **墙上时钟超时**（如 4 小时）：捕获挂起进程

**集成方式**：`rules/SAFETY_LIMITS.md` 由任务执行工具强制执行。

**工作量**：3-4 天（预算跟踪、深度计数器、超时包装器、人工覆盖协议）

**优势**：
- 防止 agent 部署中广泛报告的失控失败模式
- 优雅降级（返回部分结果）
- 向利益相关者证明自主执行合理性

**风险**：误报（合法的长时间运行任务）

---

### 8. 遗忘机制

**模式**：时间衰减 + 访问频率评分，带归档标志。

**改造自**：遗忘问题研究（来源研究报告其测试集上准确率从 13% 提升到 39%，增益 3 倍）

**评分**：
```python
def memory_score(created, modified, accessed, access_count):
    age_days = (now - created).days
    recency_days = (now - accessed).days

    # Time decay: 30-day half-life
    time_factor = 0.5 ** (age_days / 30)

    # Access reinforcement: log scale
    access_factor = log(1 + access_count)

    # Recent access boost
    recency_boost = 1.5 if recency_days < 7 else 1.0

    return time_factor * access_factor * recency_boost
```

**归档策略**：分数 <0.1 → 移至 `data/memory/archive/`，从检索中排除。

**工作量**：1 周（评分函数、归档工作流、恢复协议）

**优势**：
- 防止无限制累积
- 改进检索精度（信噪比）
- 可逆（人工可恢复已归档记忆）

**风险**：重要记忆的过早归档

---

### 9. Worktree 隔离用于并行 Agents

**模式**：Git worktrees 防止文件冲突。

**改造自**：Claude Code 原生 worktree 支持

**集成方式**：处理不同 Issues 的 Agents 使用独立 worktrees。

```bash
# Agent 1 claims Issue #7
git worktree add .worktrees/issue-7 -b agent/worker-01/7

# Agent 2 claims Issue #8
git worktree add .worktrees/issue-8 -b agent/worker-02/8
```

**工作量**：已可用（Claude Code 内置），仅需编入协议。

**优势**：
- 零文件冲突
- 并行执行无协调开销
- 失败的 agents 留下可清理的 worktrees

**风险**：磁盘空间（worktrees 是完整检出）

---

## 拒绝和延后

### 10. 拒绝：图数据库用于记忆

**系统**：Neo4j、Graphiti

**原因**：昂贵的索引（根据 Graphiti 基准测试，100 个事实需要 5 秒）、单 agent 增益边际。来源研究报告混合检索（向量 + 关键词）以更低成本实现可比收益。

**决策**：使用 SQLite 关系处理显式链接（`[[name]]` 语法），而非图遍历。

---

### 11. 拒绝：Agent 控制的记忆编辑

**系统**：Letta 的基于工具的记忆编辑

**原因**：Self-evo 故意需要人工审查。自动编辑引入幻觉累积。

**决策**：Agents 提议记忆变更（通过 Draft PRs），人工批准。

---

### 12. 拒绝：Swarm 协调用于 MVP

**系统**：OpenAI Swarm、自主任务认领

**原因**：层级模式在生产多 agent 部署中普遍（来源特定：autonomous-agents.io 调查）。Swarm 增加复杂性，对 self-evo 的阶段工作流无验证收益。

**决策**：层级分配（manager 分配 Issues 给 agents），而非自主认领。

---

### 13. 延后：Temporal/Restate 持久执行

**原因**：SQLite 任务队列足以应对当前规模。持久执行开销在证明瓶颈前不合理。

**升级触发**：任务量或协调复杂性证明 SQLite 瓶颈（本地测量，非预设阈值）或需要跨主机协调。

---

### 13. 延后：向量数据库

**系统**：Pinecone、Weaviate、Qdrant

**原因**：SQLite vector extension 在当前规模处理记忆。外部向量 DB 增加部署复杂性。

**升级触发**：记忆数增长 + 测量的检索精度降级证明语义搜索必要性。

---

### 14. 延后：Scout 垂直切片之外的主动侦查基础设施

**原因**：Scout 垂直切片（阶段 A）提供核心能力。额外基础设施（偏好学习器、多源编排、语义去重）应仅在 Scout 运行且识别出测量需求后添加。

**升级触发**：Scout 运行且特定瓶颈测量（如低相关率、高重复率、吞吐量不足）。

---

### 16. 延后：Prompt 注入防御

**系统**：tldrsec 防御、prompt-guard

**原因**：Claude 有内置安全性。Self-evo 的人工审查门捕获恶意指令。

**升级触发**：对抗输入变得常见或多 agent 场景增加攻击面。

---

## 新建（无成熟方案）

### 17. 新建：带边界执行的 Scout Runner

**缺口**：无框架提供 Scout 特定的边界执行（来源、项目、墙上时钟、进程数）。

**需求**：
- 启动 Claude CLI worker 执行 Scout 任务
- 强制执行：最大墙上时钟时间、最大 Claude 进程调用数、最大扫描来源数、最大扫描/保留项目数
- 捕获：可用的结构化 CLI 输出/使用、退出码、持续时间
- 将未知 token/成本记录为 "unknown"（hooks 不暴露内部 LLM 调用级指标）
- 终止：超时信号处理器，写入部分结果
- 恢复：加载 cursor，跳过已处理项目

**实现**：
```python
class ScoutRunner:
    def run(self, issue_id, config):
        # Launch Claude CLI subprocess
        # Enforce wall-clock timeout
        # Monitor process count
        # Capture structured output
        # Terminate on limits
        # Write partial results
        pass
```

**工作量**：嵌入 Scout 垂直切片（Issue A.1-A.2），约 1 周

**优先级**：P0（使能 Scout 垂直切片）

---

### 18. 新建：Scout Cursor 和账本系统

**缺口**：无成熟 cursor/ledger 模式用于多来源探索 agents。

**需求**：
- 每来源 cursor 跟踪（上次查看的时间戳或项目 ID）
- 去重缓存（按 URL/ID，后续语义）
- 完整运行 ledger 记录每个项目的保留/拒绝决策，作为本地调试证据
- 精简 decisions ledger 提交到 Git，供 GitHub 上的人类审阅和重建决策
- 幂等恢复（加载 cursor，跳过已处理）
- Gitignored 状态：原始 HTTP/API payload、下载缓存、cursor、dedupe cache、完整 ledger JSONL、telemetry
- Tracked 决策证据：URL/ID、日期、标题或 metadata、keep/reject、理由、来源类型；不包含大段版权内容

**Schema**：
```json
// state/scout_cursor.json (gitignored)
{
  "github": {"last_seen": "2026-06-21T12:00:00Z"},
  "hackernews": {"last_id": 40123456},
  "arxiv": {"last_date": "2026-06-20"}
}

// data/exploration/raw/2026-06-21-github-ledger.jsonl (gitignored)
{"item_id": "repo/123", "url": "...", "decision": "keep", "reason": "Novel observability pattern", "timestamp": "..."}
{"item_id": "repo/124", "url": "...", "decision": "reject", "reason": "Duplicate of existing source", "timestamp": "..."}
```

```markdown
<!-- data/exploration/raw/2026-06-21-github-decisions.md (tracked) -->
- id: repo/123
  url: https://example.com/repo/123
  date: 2026-06-21
  source_type: github
  decision: keep
  reason: 提供可复用的可观测性模式
```

日报只链接 tracked decisions 条目，不链接远端审阅者无法访问的本地 ledger。

**工作量**：嵌入 Scout 垂直切片（Issue A.2），约 1 周

**优先级**：P0（使能幂等 Scout）

---

### 19. 新建：记忆访问跟踪（条件性）

**缺口**：Self-evo 需要访问/使用统计用于遗忘实验，而不修改权威 Markdown。

**需求**（仅当测量到检索瓶颈时）：
- 跟踪记忆读取/使用而不修改 Markdown 文件
- 在可重建的 gitignored 索引或仅追加日志中存储访问事件
- 支持时间衰减 + 访问频率评分
- 归档策略：仅手动、可逆、需要冷却期提案 + 人工批准

**实现**：
```python
# state/memory_access.db (gitignored, rebuildable)
CREATE TABLE access_log (
  memory_name TEXT,
  accessed_at INTEGER,
  access_type TEXT  -- read, update, link
);

# OR append-only event log
# state/memory_events.jsonl (gitignored)
{"memory": "okf-validates-file-first", "event": "read", "timestamp": "2026-06-21T12:00:00Z"}
```

**工作量**：1 周（访问跟踪、遗忘评分、归档/恢复协议）

**优先级**：P2（条件性，取决于测量的检索瓶颈）

---

## 集成顺序（推荐序列）

### 阶段 A：自主 Scout 垂直切片（第 1-4 周）

1. **Scout 源注册和 runner wrapper**（1 周）—— 已批准来源、边界执行、嵌入本地遥测
2. **Cursor、去重和保留/拒绝账本**（1 周）—— 幂等恢复、证据支持的过滤
3. **每日决策报告生成**（1 周）—— 复用图谱、实验/技能/项目候选、人工可审查输出
4. **人工审查标签工作流**（3 天）—— 偏好学习的反馈循环

### 阶段 B：Scout 评估（第 5-6 周，Scout 运行后）

5. **Scout 留出集和质量指标**（1 周）—— 独立留出（无答案泄漏）、Scout vs Builder vs 人工指标
6. **针对留出集运行 Scout 并测量**（3 天）—— 成功率、成本、失败模式、与人工基线对比

### 阶段 C：条件性改进（由观察到的 Scout 失败触发）

7. **Scout 可靠性**（1 周）—— 恢复、语义去重、速率限制处理（仅当观察到失败时）
8. **记忆索引**（2 周）—— OKF 时间戳（仅 created/modified，不修改读取）、SQLite FTS、OpenViking 对比（仅当测量到检索瓶颈时）
9. **多 agent 协调**（2-3 周）—— 带 worktree 隔离的并行 Scouts（仅当证明吞吐量瓶颈时）
10. **外部可观测性对比**（1 周）—— Langfuse vs OpenLLMetry（仅当本地遥测不足以调试时）
11. **持久工作流引擎**（2-3 周）—— Temporal/Restate 检查点（仅当测量到恢复痛点时）

---

## 缺失部分摘要

**关键（现在构建）**：
- Token 预算强制执行
- 记忆检索 API

**重要（在 MVP 中构建）**：
- GitHub Issue 分解协议
- 遗忘机制

**锦上添花（延后）**：
- 主动侦查
- 高级语义搜索
- 跨主机协调

**已可用（采用）**：
- 本地结构化遥测（JSONL + OpenTelemetry schema）
- Self-evo 原生任务基准测试
- OKF 记忆标准
- SQLite 租约协调
- Worktree 隔离
- ResearchPlanAssignOps 模式

---

## 架构决策摘要

| 决策 | 选择 | 理由 |
|----------|--------|-----------|
| 记忆格式 | Markdown+YAML (OKF) | Git 原生、透明、符合标准 |
| 记忆检索 | SQLite FTS → embeddings | 扩展到 1000+ 条记忆，渐进复杂性 |
| 协调 | 基于租约（SQLite） | 无外部依赖，验证模式 |
| 可观测性 | 本地 JSONL → 外部（需批准门控） | File-first 带可选云升级 |
| 工作流 | ResearchPlanAssignOps | 人工审查门、阶段执行 |
| 安全性 | 三层终止 | 冗余限制、优雅降级 |
| 多 agent | 层级（延后 swarm） | 层级模式在调查中普遍 |
| 持久执行 | 延后（SQLite 足够） | 仅当证明瓶颈时升级 |
| 评估 | Self-evo 原生 → SWE-bench 可选 | 先测量实际工作流 |

---

**复用图谱结束**

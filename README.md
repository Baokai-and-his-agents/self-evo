# self-evo

一个以 GitHub 为协调平面、以本地 Code Agent 为执行者、以文件和 Git 历史为长期事实源的个人自主执行系统。

它的目标不是做一个等待提问的聊天机器人，而是让一个或多个 Agent 长期协助人类：

- 接收任务、链接、技能名称和长期方向；
- 主动调研外部资料，优先复用已有成果；
- 把模糊想法拆成可执行、可验收的工作；
- 在权限和预算边界内学习、实验和交付；
- 将结果沉淀为项目资产、技能、记忆和下一步决策；
- 通过 GitHub Issue、Draft PR 和中文审阅材料与人类持续协作。

> 当前阶段：单 Agent 协作协议、GitHub 交付流程、安全 Hooks、运行验证器和 Scout 研究路线已经建立；Autonomous Scout 的实际 Runner、增量抓取、定时运行和多 Agent 调度仍待实现。

## 项目目标

self-evo 希望建立一个可以长期演化的“人类 + Agent”工作系统。

人类负责目标、偏好、资源授权和最终决策；Agent 负责消耗时间与模型能力完成调研、学习、实验、实现和整理。系统通过明确的文件协议与 GitHub 审计，使工作能够跨会话、跨日期、跨 Agent 接续，而不依赖某一次聊天上下文。

核心产出不是信息堆积，而是行动资产：

- 可执行任务和项目候选；
- 有证据的研究结论与复用图谱；
- 可重复运行的脚本、Demo 和工作流；
- 可复用技能与经验；
- 可人工修订的长期记忆；
- 对下一步“做什么、为什么做”的清晰判断。

## 核心原则

1. **文件是长期事实源**  
   Markdown、YAML、JSON 和 Git 历史保存规则、决策、记忆与交付物。外部记忆系统只能作为索引或增强层。

2. **GitHub 是协调与审计平面**  
   Issue 负责任务状态，分支和 PR 负责文件型交付，评论和标签负责人类反馈。GitHub 不承载高频遥测、大文件缓存或私密凭证。

3. **运营方式与运营项目分离**  
   `rules/**` 是 Agent 只读的治理区；`data/**` 是运营方式自身的工作区（系统级记忆、审计、提案、任务镜像）；`projects/<项目名>/**` 是各业务项目的产出区（实验、调研、运行记录、项目记忆）。Agent 若认为规则需要变化，只能提交 proposal，由人类批准后修改规则。

4. **先复用，再自研**  
   面对长期方向或构建任务，Agent 应先调查教程、工具、项目、模板、案例和现有 workflow，并说明采用、组合或自研的理由。

5. **主动性必须有边界**  
   Agent 可以主动探索，但必须受权限、资源、运行时间、调用次数、来源数量和人工审查约束。

6. **复杂性由证据触发**  
   先跑通单 Agent 和真实业务闭环；只有出现可测量瓶颈后，才引入多 Agent、向量数据库、外部可观测性或持久工作流引擎。

## 系统架构

```text
人类
  │  创建 Issue、提供反馈、批准资源与规则、审阅和合并
  ▼
GitHub
  │  任务状态、claim、分支、Draft PR、审计记录
  ▼
本地 Code Agent（Claude Code 等）
  │  读取规则、认领任务、调研/学习/实现、提交证据
  ├── rules/      治理规则，只读
  ├── data/       运营方式自身：系统记忆、审计、提案、任务镜像
  ├── projects/   业务项目产出：实验、调研、运行记录、项目记忆
  ├── state/      claim、heartbeat 和本地运行状态
  └── scripts/    Hooks、Validator 和后续 Worker 工具
```

运营方式与运营项目两个区域：

| 区域/平面 | 作用 | 典型内容 |
|---|---|---|
| `rules/` | 定义 Agent 能做什么、如何审批（运营方式） | 权限、任务、GitHub、记忆、探索策略 |
| `data/` | 保存运营方式自身的工作成果 | 系统记忆、审计、proposal、任务镜像、系统调研 |
| `projects/<项目名>/` | 保存各业务项目的产出 | 实验、研究、run summary、项目记忆 |
| `state/` | 保存运行协调状态 | claims、heartbeat、cursor、cache |
| `.github/` | 提供 GitHub 协作入口 | Issue 模板、PR 模板、CODEOWNERS |

## 工作流程

### 1. 人类提出任务

任务以 GitHub Issue 为第一事实源。可以是：

- `type:scout`：调研外部生态、机会或长期方向；
- `type:learn`：学习技能、文档或工具；
- `type:build`：实现代码、脚本、文章或其它交付物；
- `type:review`：审查结果、风险和决策；
- `type:memory`：整理或更新长期记忆；
- `type:rule-proposal`：讨论治理规则变化。

临时想法也可以先写入 `data/tasks/INBOX.md`，成熟后再转为 Issue。

### 2. Agent 启动并加载规则

在仓库根目录启动 Code Agent，然后输入：

```text
Read rules/START_HERE.md and follow it exactly.
```

Agent 将继续读取任务、权限、资源、GitHub、记忆和探索规则。

### 3. Agent 认领一个 Issue

每次运行只处理一个已认领任务，并记录：

- worker identity；
- run id；
- agent 分支；
- lease 到期时间；
- 本地 claim 和 heartbeat。

推荐分支格式：

```text
agent/<worker>/<issue-number>-<slug>
```

### 4. 执行与记录

Agent 在权限范围内调研、学习、实验或实现，并保留：

- 使用的来源和已有成果调查；
- 关键判断、失败和限制；
- 修改的文件与测试结果；
- 需要人类确认的事项；
- 可进入长期记忆的候选；
- 清晰的下一步行动。

### 5. 文件型交付进入 Draft PR

只要修改了 tracked 文件，执行任务的 Agent 必须用自己的 GitHub 身份：

1. 提交 agent 分支；
2. push 分支；
3. 创建 Draft PR；
4. 链接原 Issue；
5. 释放 claim，将任务转入 review。

当前身份模型：

- `clawbie`：Agent 身份，负责 Issue 评论、agent 分支和 Draft PR；
- `jlcbk`：人类身份，负责审批、规则变更、Ready、合并和最终决策。

面向人类审阅的 Issue、PR、run summary 和决策报告默认使用中文；代码、命令、路径和必要技术标识保留英文。

### 6. 人类审阅与反馈

人类通过 PR review、Issue comment 和 labels：

- 批准或要求修改；
- 选择项目候选；
- 标记 `relevant`、`irrelevant`、`deep-dive`、`pause`；
- 批准资源、规则或高风险动作；
- 决定是否合并。

合并后的结果继续沉淀到运行记录、项目决策、技能或记忆提案中。

## 当前能力

### 已实现

- **Agent 启动协议**：`rules/START_HERE.md` 是空上下文 Agent 的统一入口。
- **GitHub 原生任务流**：Issue、claim、lease、agent branch、Draft PR、人工审批与合并。
- **双身份治理**：Agent 负责执行和提交，人类负责授权和最终决策。
- **路径与权限策略**：区分只读规则区、Agent 工作区、需提案路径和禁止动作。
- **资源审批表**：已批准仓库 Issue/分支工作，以及公开网页、搜索和文档的只读访问。
- **运行状态记录**：claims、heartbeat、任务镜像和 run summary。
- **安全 Hooks**：Claude Code `PreToolUse` 和 `Stop` hooks，可审计危险命令、越界写入、敏感文件访问和生命周期问题。
- **运行验证器**：检查 agent 分支、claim、Draft PR、run summary、任务状态和越权文件修改。
- **自动化测试**：覆盖策略矩阵、Git 集成、runtime ignore 和 Scout 来源 schema。
- **文件优先记忆**：hot/cold memory、memory proposal、人工冷却与恢复原则。
- **探索工作流**：exploration brief、capability map、existing-work survey、reuse map、项目候选和决策报告。
- **运行时数据隔离**：telemetry、cursor、数据库、缓存和完整 ledger 保持本地且 gitignored；精简决策证据可以进入 Git。
- **Scout 来源契约**：已定义来源 registry schema，以及能力批准与具体来源 allowlist 的分层模型。

### 尚未实现

- 可运行的 `scripts/workers/scout_runner.py`；
- 实际的 `data/exploration/scout-sources.yaml` 来源实例；
- 来源抓取、cursor、跨运行去重和恢复；
- 自动生成每日 Scout 决策报告；
- GitHub 人工反馈自动同步到 review labels；
- 定时唤醒和长期无人值守 supervisor；
- GitHub Issue 与本地任务镜像的自动同步；
- 多 Agent 自动分工、并发 claim 和结果聚合；
- 大文件、PDF、视频和媒体资产的统一外部存储适配；
- OpenViking、SQLite FTS 或其它记忆索引的正式接入。

## 发展规划

### 阶段 A：Autonomous Scout 垂直切片

当前最高优先级是交付一个真实可运行、受边界约束的 Scout：

1. 批准 `scripts/workers/**` 权限方案；
2. 建立来源 registry 实例和 Scout runner；
3. 实现 cursor、去重和可恢复 ledger；
4. 生成面向决策的日报与项目候选；
5. 接入 GitHub 人工反馈标签。

Runner 首先强制执行可实际控制的边界：

- 最大墙上时钟时间；
- 最大 Claude 进程调用数；
- 最大重试次数；
- 最大来源、扫描项目和保留项目数量；
- 超时后的子进程终止与部分结果保留。

内部模型调用级 token/cost 如果执行接口不可见，将明确记录为 `unknown`，不伪装成可强制控制。

### 阶段 B：Scout 评估

Scout 可运行后再建立：

- 独立留出任务集，避免从已解决 Issue 泄漏答案；
- 新颖性、相关性、证据质量、可操作转换和重复率指标；
- 人类执行相同任务的时间与质量基线；
- 成本、成功率和失败模式报告。

### 阶段 C：按瓶颈扩展

以下能力不预先建设，只在测量到真实问题后启动：

- 恢复和语义去重；
- SQLite FTS、OpenViking 或 embeddings 记忆索引；
- 多 Agent 并行 Scout 与 worktree 隔离；
- Langfuse、OpenLLMetry 等外部可观测性；
- Temporal、Restate 等持久工作流；
- Docker 或更严格的 sandbox 执行环境。

## 所需资源

### 基础资源

| 资源 | 用途 | 当前要求 |
|---|---|---|
| Git | 版本、分支、审计和交付 | 必需 |
| GitHub 仓库 | Issue、PR、评论和身份协调 | 必需 |
| 人类 GitHub 账号 | 审批、合并、规则与资源授权 | 必需 |
| Agent GitHub 账号 | claim、评论、agent 分支、Draft PR | 推荐独立账号，write 权限即可 |
| 本地 Code Agent | 实际调研、学习和执行 | 当前主要使用 Claude Code |
| Python 3 | Hooks、Validator 和测试 | 必需，需在 Agent 运行环境的 `PATH` 中可见 |
| GitHub CLI `gh` | Agent 的 GitHub 操作和状态检查 | 推荐 |

### 模型与计算资源

- 需要一个可以长期执行代码、文件和 Git 操作的 Agent 运行时；
- Scout 和深度调研适合使用高 token 配额与大上下文模型；
- 第一阶段不要求云服务器、GPU、向量数据库或付费 API；
- 任何付费服务、私有凭证、服务器、GPU 或外部存储都必须先进入资源审批流程；
- 凭证只通过环境变量或本地安全配置引用，禁止提交到仓库。

### 当前已批准的外部能力

- `github-repo-issue-and-branch-work`：读取 Issue、评论、创建 agent 分支、push agent 分支、创建 Draft PR；
- `public-web-read`：读取公开页面、搜索公开网络、读取公开文档。

这些批准不包含：

- 登录私人账号；
- 使用 API token 或私有凭证；
- 付费 API；
- 对外发布、发帖或联系用户；
- merge PR 或绕过保护；
- 修改 `rules/**` 为 Agent 自己授权。

### 大文件与媒体

GitHub 只保存可审阅的代码、配置、摘要、索引和决策记录。大型 PDF、视频、原始媒体、下载缓存和完整遥测不应直接进入仓库。

后续适配原则：

- 文件保存在本地工作区、对象存储或专用资产库；
- Git 中只保存 manifest、hash、来源、权限、处理状态和结果摘要；
- Agent 通过稳定引用读取资产；
- 私密或受版权限制的原始内容不得上传到公开仓库。

## 快速开始

### 人类

1. 克隆仓库并安装 Git、Python 3、Claude Code 和 GitHub CLI。
2. 分别登录人类 GitHub 身份和 Agent GitHub 身份。
3. 按 [Claude Code 配置指南](docs/CLAUDE_CODE_SETUP.md)安装或手动接入 safety hooks。
4. 在 GitHub 创建一个任务 Issue。
5. 在仓库根目录启动 Agent，并输入：

```text
Read rules/START_HERE.md and follow it exactly.
```

### Agent

1. 读取 `rules/START_HERE.md` 及其要求的规则。
2. 选择并认领一个 Issue。
3. 检查权限和资源审批。
4. 创建 agent 分支并执行任务。
5. 写入证据、run summary 和必要 proposal。
6. 修改 tracked 文件时，由 Agent 身份创建 Draft PR。
7. 释放 claim，等待人类审阅。

### 验证仓库能力

```bash
python scripts/tests/test_matrix.py
python scripts/tests/test_integration.py
python data/tests/test_runtime_ignore.py
python data/tests/test_scout_schema.py
```

运行特定 Issue 的生命周期验证：

```bash
python scripts/validate_run.py --issue <number>
```

## 目录导航

| 路径 | 内容 |
|---|---|
| [`rules/START_HERE.md`](rules/START_HERE.md) | Agent 唯一启动入口 |
| [`docs/autonomous-agent-blueprint.md`](docs/autonomous-agent-blueprint.md) | 完整项目蓝图 |
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | 当前架构摘要 |
| [`docs/DECISIONS.md`](docs/DECISIONS.md) | 已确认的长期决策 |
| [`data/tasks/`](data/tasks/) | 本地任务镜像、Inbox、Review、Done（含 `project` 归属字段） |
| [`data/runs/`](data/runs/) | 运营方式自身的运行摘要（业务项目 run 见对应 `projects/`） |
| [`data/exploration/`](data/exploration/) | 系统自身调研、日报、复用图谱（业务项目调研见对应 `projects/`） |
| [`data/memory/`](data/memory/) | 系统级热记忆、冷记忆和记忆提案 |
| [`data/proposals/`](data/proposals/) | 规则、资源和项目候选提案 |
| [`projects/fx-strategy-research/`](projects/fx-strategy-research/) | 业务项目产出区：FX 量化策略研究的实验、调研、运行记录与项目记忆 |
| [`scripts/README.md`](scripts/README.md) | Hooks、Validator 和测试说明 |
| [`rules/RESOURCE_APPROVALS.yaml`](rules/RESOURCE_APPROVALS.yaml) | 已批准的外部资源能力 |

## 安全与治理

- Agent 不得直接修改 `rules/**`；
- Agent 不得读取或提交密码、token、私钥等秘密；
- Agent 不得直接 push `main`、自行 Ready 或合并 PR；
- 未批准的外部资源必须先申请；
- 文件型交付必须经过 Agent Draft PR 和人类审阅；
- Hooks 当前默认是 `audit` 模式，只记录、不阻止；
- 提升到 `pretool-enforce` 或 `full-enforce` 前，应先审查误报和漏报；
- 当前 GitHub 保护部分依赖身份分离、CODEOWNERS、协议和人工合并，不能把它误认为绝对安全边界。

## 项目状态说明

仓库仍在快速演化。GitHub Issue 是任务状态的权威来源，本地 `data/tasks/TASKS.md` 目前是人工同步的镜像，可能短暂落后于 GitHub。

当前最有价值的下一步不是增加更多框架，而是批准并实现 Scout Runner 权限方案，完成第一个可持续产生决策报告的 Autonomous Scout 垂直切片。

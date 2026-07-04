# self-evo 方向审查报告

> **审查模式**:Codex 不可用(网络无法访问 api.openai.com),按 codex-router SKILL
> standing policy 降级 GLM-only,以 fresh-context 批判视角替代独立第二意见。
> **审查者自陈局限**:GLM 自审缺少跨模型家族的视角差异,以下判断应被视为
> "强 GLM 自审",而非真正的独立第二意见。涉及方向押注的关键判断,建议网络恢复后
> 仍用 Codex 复核。

---

## Q1. 治理/执行比是否失衡?

**判断:失衡,但属于"有意识的预投资",不需要推倒,需要冻结。**

证据(基于 EVIDENCE):
- rules 707 行 + scripts 护栏 2182 行 + 文档 107 个 → 治理层密集
- 业务执行层:fx_backtest(56 文件)是唯一闭环,Scout Runner = 0
- 但:blueprint v0.5 第 18 行明确写"多 worker 不在第一版实际启用,但 label/claim/lease/worker identity/分支命名需要提前预留"——这是**自觉的设计决策**,不是无意堆砌

理由:
- 治理层的"过设计"在单 worker 阶段确实显得重,但它的成本是**文件和行数**,不是运行时开销。rules 不运行,不耗 token,不增加 agent 启动延迟(按 START_HERE 加载链只读需要的)。
- 真正的风险不是"治理太多",而是"治理先行太久,执行层迟迟不收口会导致治理层失去现实校准"——一个没被真实多 worker 压测过的 claim/lease 协议,可能藏着只有跑起来才暴露的设计缺陷。

**可执行下一步**:
1. **冻结治理层扩张**:在网络恢复和 Scout 闭环前,不再新增 rules/ 文件或扩充现有 rules。
2. **保留现有治理**:707 行 rules 不精简——它们已经写完且测试覆盖(91+61 通过),精简反而是引入回归风险。
3. 把"治理层是否过设计"这个问题**推迟到 Scout 真正跑过 2 周后**用真实数据回答,而不是现在凭感觉砍。

---

## Q2. Scout Runner 自研还是用现成工具?

**判断:混合策略——抓取层用现成库,聚合/决策层自研,理由是项目自己的"决策流而非信息流"目标。**

证据:
- blueprint 第 1000-1008 行明确:"主动侦察的输出不应该是信息流,而应该是**决策流**"
- EVIDENCE 显示已有 `data/exploration/scout-source-registry.schema.yaml` + 437 行 schema 测试——**来源契约已经自研定型**

现成工具分析:
- **抓取层**(GitHub/HN/arXiv/PH API):**应用现成库**。`feedparser`(RSS)、`requests` + 各平台官方 SDK、`pyarxiv`、`hn-api` 等。这一层是机械的 HTTP + 解析,自研纯重造轮子,**违背 blueprint 第 960 行的 existing work survey 原则**。
- **聚合/去重层**:`dacite`/`pydantic` 做模型,简单的 hash 去重。半自研半用库。
- **决策层**(reuse map、项目候选、推荐):**必须自研**。这是项目的核心差异化——把信息流转成"3-5 个可执行决策",没有现成库能做,因为这是 self-evo 自己的价值主张。

**关键洞察**:Scout Runner 的"自研"部分应该只是决策层;抓取层如果自研就是违反项目第一原则。这个区分 README 没说清楚,需要在实现时明确。

**可执行下一步**:
1. Scout Runner 的 `fetcher/` 子模块用 `requests` + 平台官方 JSON API(无新依赖)
2. `decide/` 子模块自研,对接已有的 schema
3. 在 Scout Runner README 里明确标注"抓取层复用、决策层自研"的边界

---

## Q3. 记忆系统的复杂度是否匹配 16 个文件?

**判断:分层结构合理,但冷却流程的触发阈值需要明确,否则会变成永远不触发的死规则。**

证据:
- 16 个记忆文件(hot 7 + cold 5 + proposals 4)
- MEMORY_POLICY.md 58 行定义了三层 + 冷却流程
- 但 blueprint 第 1303 行把"冷却自动候选规则如何设置"列为开放问题——**还没定阈值**

理由:
- hot/cold/proposals 三层**结构**是对的——它对应"活跃/归档/候选"的认知模型,即使 16 个文件也成立(分层是组织方式,不是规模驱动)。
- 但**冷却流程的触发条件没定** = 这套机制目前是"挂起的"。没有任何文件说"什么时候启动冷却",所以它事实上不会运行。

**阈值建议**(回答开放问题):
- **冷却候选触发**:hot 区文件超过 30 个,或某条记忆 `last_referenced_at` 超过 14 天
- **冷却执行**:hot 超 50 个时强制启动一轮冷却提案
- **理由**:30/50 这两个数对应"人脑短期工作集"和"需要分类才管理得了"的规模,16 个远未触发,符合"为增长预留"定位

**可执行下一步**:
1. 不改分层结构
2. 在 MEMORY_POLICY.md 补一节"冷却触发阈值"(30/14天/50 三档)
3. 但**通过 proposal 提交,不直接改 rules**(项目铁律)

---

## Q4. fx_backtest 闭环经验能否复用到 Scout?

**判断:过程模板可迁移,产物 schema 不可迁移;关键可迁移点是 run summary 格式和 reuse map 模式。**

证据(读 fx_backtest 实际产物):
- `projects/fx-strategy-research/experiments/fx_backtest/` 有 README、IMPLEMENTATION_NOTES、DATA_SOURCES、SIGNAL_PRIORITY、完整测试
- `exploration/reuse_maps/2026-06-23-fx-quant-strategies.md` 有真实 reuse map
- `exploration/daily_reports/` 有 2 个日报

可迁移:
| fx 产物 | 能否迁移到 Scout | 怎么迁移 |
|---|---|---|
| run summary 格式 | ✅ | 提炼成 `data/runs/TEMPLATE.summary.md` |
| reuse map 结构 | ✅ | 已有 `data/exploration/reuse_maps/`,复用结构 |
| existing-work-survey 流程 | ✅ | blueprint 第 962-968 行已抽象成 5 步,直接用 |
| 信号/回测代码 | ❌ | 领域特化,不可迁移 |
| 数据源 schema | ❌ | fx 是 OHLCV,Scout 是异构 API,不同 |

**关键洞察**:fx_backtest 证明了"探索→reuse map→实现→测试→run summary"这条链路是走得通的。Scout 应该复用这条链路的**形态**,只是把"回测引擎"换成"决策报告生成器"。

**可执行下一步**:
1. 把 fx 的 run summary 抽成模板放 `data/runs/TEMPLATE.summary.md`
2. Scout Runner 的输出复用 run summary + reuse map 两套格式

---

## Q5. 阶段 A 的 5 个子任务,正确顺序?

**原顺序**:1) workers/权限 2) 来源registry+runner 3) cursor/去重/ledger 4) 日报 5) GitHub反馈同步

**判断后的正确顺序**:

| 实际顺序 | 子任务 | 理由 |
|---|---|---|
| 1 | 来源 registry 实例 | 没 source 无法测 runner,这是数据前提 |
| 2 | Scout Runner 主体(fetcher+decide) | 核心交付,先跑通最小闭环 |
| 3 | 日报生成 | runner 跑通后才有东西可报;**与 cursor/去重合并** |
| 4 | cursor/去重/ledger | **降级**:第一版用文件 mtime + URL hash 做最简去重,不需要完整 ledger |
| 砍 | GitHub 反馈同步 | **延后**:手动同步够用,自动化是优化不是必需 |
| 砍 | workers/ 权限审批 | **不需要**:第一版单 worker,直接复用现有 github-repo-issue-and-branch-work 权限 |

**关键判断**:
- 原 5 个任务里,workers/权限和 GitHub反馈同步**在第一版可以砍掉**——它们是为多 worker/高频反馈设计的,单 worker 手动启动阶段不需要。
- cursor/去重应该**降到最小实现**(mtime + URL hash),不要一开始就建 ledger 系统。blueprint 自己第 49 行说"复杂性由证据触发",16 个文件时不该建 ledger。

**可执行下一步**:按上表 1→2→3→4 顺序实现,砍掉的两项写入"延后清单"。

---

## 总结:重构的核心收敛方向

不增加新框架,而是**让执行层追上治理层**:

1. **Scout Runner 垂直切片**是唯一头号优先级,其他都是支撑
2. **抓取用现成库,决策自研**——避免违反"先复用"原则
3. **治理层冻结**(不增不减),等 Scout 跑 2 周后用数据决定是否精简
4. **冷却阈值明确化**(30/14天/50),让挂起的机制活起来
5. **fx 经验提炼成模板**,复用到 Scout

**明确反对的做法**:
- ❌ 现在就精简 rules(测试覆盖好,精简是回归风险)
- ❌ 自研抓取层(违背 existing work survey)
- ❌ 第一版上 ledger 系统(违背"复杂性由证据触发")
- ❌ 现在补多 worker 并发(DECISIONS.md 已正确延期)

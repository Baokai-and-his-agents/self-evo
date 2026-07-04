我按 EVIDENCE 快照回答。先说明一个冲突：当前工作区的 [README.md](/Users/cui/.zcode/self-evo-work/README.md:177) 已写明 Scout Runner 已实现，和证据包里 “Scout Runner = 0” 冲突。下面判断以 [docs/REFACTOR-evidence-pack.md](/Users/cui/.zcode/self-evo-work/docs/REFACTOR-evidence-pack.md:42) 这个快照为准。

**Q1 治理/执行比**

判断：调整。保留现有治理，冻结扩张，不立即精简。

理由：707 行 rules + 2182 行 scripts 护栏，对 0 行 Scout 执行层确实失衡；但 rules 不是空壳，8 个规则文件齐全且 START_HERE 加载链完整，166 个测试通过，说明这是有实质约束的治理层，不是纯文档堆砌。现在精简会破坏已有安全边界；继续扩张则会让治理脱离真实执行反馈。

下一步：不要再新增 `rules/` 内容；先把 `scripts/workers/scout_runner.py` 的最小闭环补出来。若要固化，走 `data/proposals/rule_changes/` 提一条“Scout 稳定期治理冻结”规则。

**Q2 Scout Runner 自研还是复用**

判断：调整。抓取层必须复用，决策层可以自研。全量自研 Scout Runner 违背“先复用再自研”。

理由：blueprint 明确要求先 existing work survey，且第一批来源本身就是 GitHub REST、HN API、arXiv API、PH API、RSS。成熟组件已经存在：RSS/Atom 可用 [feedparser](https://feedparser.readthedocs.io/en/latest/)；GitHub 用 [REST Search API](https://docs.github.com/en/rest/search/search)；HN 有 [官方 API](https://github.com/HackerNews/API)；arXiv 有 [官方 API/RSS](https://info.arxiv.org/help/api/index.html)；Product Hunt 有 [GraphQL API](https://api.producthunt.com/v2/docs)。这些不应自研。

但 blueprint 还要求输出“决策流而非信息流”：reuse map、实验建议、技能建议、商机建议。现成 aggregator 只能给信息流，不能替代 self-evo 的项目判断。因此 Runner 应是薄编排：复用抓取/API/RSS解析，自研去重、评分、日报和项目候选生成。

下一步：在 `data/exploration/reuse_maps/` 先写 Scout reuse map；实现时把 `fetch` 层限定为标准库/API/成熟库，把 `decide/report` 层作为项目自研核心。

**Q3 记忆系统复杂度**

判断：保留分层，但现在不启动冷却。16 个文件不需要主动冷却流程。

理由：hot 7 + cold 5 + proposals 4 的规模很小；三层结构本身合理，因为它区分“默认加载”“归档”“候选审批”。真正的问题不是分层，而是冷却流程没有触发阈值，会变成仪式性规则。

阈值建议：hot 文件数超过 30 才生成冷却候选；单条 hot memory 超过 30 天未引用且非 pinned，才进入候选；hot 超过 50 时必须做一轮冷却 proposal。用户偏好、当前目标、长期决策默认 pinned，不因时间自动冷却。

下一步：只在 `rules/MEMORY_POLICY.md` 增补 “Cooldown Triggers”，但必须通过 `data/proposals/rule_changes/` 提案，不直接改 rules。当前已有 14 天阈值的提案我会调整为 30 天，更适合个人长期系统。

**Q4 fx_backtest 能否复用到 Scout**

判断：能复用工作法和交付模板，不能复用领域模型。

可迁移：run summary 结构、reuse map 结构、existing-work survey、单命令运行、测试先行、已知限制诚实记录、数据/权限/许可阻塞显式写出。fx_backtest 的 run summary 已经包含 deliverables、tests、status、limitations、next steps，这正适合作为 Scout 运行摘要模板。

不可迁移：OHLC 数据模型、Donchian/ATR 信号、A/B/E/G sizing、回测 engine、P(win|stop_count) 等统计分析。这些是 FX 领域闭环，不应污染 Scout。

下一步：从 `projects/fx-strategy-research/runs/...fx-backtest-001.summary.md` 提炼 `data/runs/TEMPLATE.summary.md`；为 Scout 增加 `data/exploration/reuse_maps/TEMPLATE.scout.md` 或直接约定 reuse map 字段。

**Q5 阶段 A 顺序**

判断：调整顺序，并砍掉两项第一版非必要项。

正确顺序：

1. 最小权限确认：只确认 `scripts/workers/**` 可放 Runner、公开只读来源已批准；不要扩成 worker 框架工程。
2. 建立 `data/exploration/scout-sources.yaml`：没有来源实例，Runner 无法真实验收。
3. 实现最小 Scout Runner：抓取层复用 API/RSS/库，内置 URL hash 去重和 cursor；不要先建完整 ledger。
4. 生成决策日报：输出到 `data/exploration/daily_reports/`，必须是行动建议，不是链接列表。
5. GitHub 反馈同步延后：单 worker 手动 review 够用，不是执行层为 0 时的阻塞项。

可砍/延后：完整 ledger、语义去重、GitHub feedback→labels 自动同步、Issue↔本地镜像自动同步、定时 supervisor、多 Agent 并发。现在最短路径是让执行层追上治理层。
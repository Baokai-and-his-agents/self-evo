# Scout Runner (Stage A)

Autonomous Scout 的执行层垂直切片。抓取已批准的公开只读来源,去重,生成决策导向的日报。

## 设计原则(对应 reuse map)

参见 `data/exploration/reuse_maps/2026-07-04-scout-runner.md`:

- **抓取层全部复用**:stdlib urllib + xml.etree,唯一依赖 PyYAML(用于解析 sources registry;自写的极简 parser 被证明不可靠,已移除)
- **决策层自研**:dedupe + keep budget + daily report(blueprint "决策流而非信息流")
- **接口契约**:对接 `data/exploration/scout-source-registry.schema.yaml`(项目已定义)

## 强制边界(README 阶段 A + blueprint 第 1094-1099 行)

Runner 强制执行以下硬限制,超限即停止并保留部分结果:

| 边界 | 默认值 | CLI 参数 |
|---|---|---|
| 总墙上时钟 | 600s | `--max-wall-clock` |
| 来源数上限 | 20 | `--max-sources` |
| 每来源扫描上限 | 50 | `--max-items-per-source` |
| 保留项目总数 | 80 | `--max-items-kept` |
| 单来源重试 | 2 | `--max-retries` |
| 单次 HTTP 超时 | 15s | `--request-timeout` |

**Token/Cost:** fetch 接口(urllib/gh)不暴露模型 token 用量,如实记录为 `unknown`,不伪装可强制控制(README 阶段 A 诚实规则)。

## 前置条件

- Python 3(README 资源表已要求)
- PyYAML ≥ 5.1(解析 sources registry;自写 parser 被证明不可靠已移除)

```bash
pip3 install -r scripts/workers/requirements.txt
```

## 用法

```bash
# 默认边界
python3 scripts/workers/scout_runner.py

# 自定义边界(快速测试)
python3 scripts/workers/scout_runner.py --max-wall-clock 30 --max-items-kept 5

# 指定 sources 文件
python3 scripts/workers/scout_runner.py --sources-file path/to/sources.yaml
```

## 输出

- **日报:** `data/exploration/daily_reports/<run-id>-scout.md`(决策候选列表 + 决策建议区块)
- **去重游标:** `state/scout-cursor.json`(跨运行 URL hash 去重)
- **stdout:** 运行摘要(来源成功数、保留项目数、耗时)

## 测试

```bash
python3 scripts/tests/test_scout_runner.py
```

42 个单元测试,网络无关(解析器喂入固定内容,边界强制逻辑独立测试)。

## 已知限制 (Known Limitations)

诚实记录第一版的边界,不掩盖:

### 1. GitHub Trending 抓取的是导航链接,不是真实 trending 仓库
**原因:** github.com/trending 用 JavaScript 动态渲染仓库列表,纯 HTML 抓取(urllib)只能拿到页面导航栏(features/copilot、features/actions 等),拿不到真实 trending 仓库卡片。
**影响:** `github-trending-daily` 来源的产物质量低(导航链接而非仓库)。
**不做的解决:** ❌ 不引入无头浏览器(Playwright/Selenium)——杀鸡用牛刀,违背"复杂性由证据触发"。
**可行的解决(待人工决策):**
- (a) 改用 GitHub Search API(`gh api search/repositories?q=created:>YYYY-MM-DD&sort=stars`)——需要 github-repo-issue-and-branch-work scope,已批准
- (b) 接入 GitHub trending 的第三方镜像(如 `gh-trending-api`)(需评估稳定性)
- (c) 第一版接受这个限制,Scout 暂时不覆盖 GitHub trending

### 2. 去重是 URL hash,不是语义去重
**原因:** 第一版用 SHA256(url) 做去重,符合 blueprint 第 49 行"复杂性由证据触发"。
**何时升级:** cursor 文件超过 1000 条 URL,或出现真实的"同一内容不同 URL 重复"问题。

### 3. 无语义相关性打分
**原因:** 第一版保留所有抓到的项目,相关性判断留给人工 review(写入决策建议区块)。
**何时升级:** 日均保留项目稳定超过 30 个,人工 review 负担变大时,引入 preference learner。

### 4. Token/Cost 不可观测
**原因:** urllib/gh CLI 不暴露模型 token 用量。
**应对:** 如实标记 `unknown`(已在 report 和 dataclass 体现),不伪装。

## 不做的事(对应审查报告 Q5 砍掉的)

- ❌ Product Hunt API(需 token,未批准)
- ❌ 完整 ledger 系统(16 文件不需要)
- ❌ GitHub 反馈→labels 自动同步(单 worker 阶段手动够用)
- ❌ 多 Agent 并发(DECISIONS.md 已延期)

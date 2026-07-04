# self-evo 重构 Run Summary

> **⚠️ 修订说明 (v2, 2026-07-04 晚):** 本文件是重构当时的快照,文中"Codex 不可用"
> 是**当时的真实状态**。但后来排查发现根因是 shell 缺代理环境变量(系统代理 1082
> 不被 CLI 读取),修复后 Codex 恢复可用,并完成了 **4 轮独立审查**:
> - `docs/REFACTOR-direction-review-by-codex.md` — 方向审查(5 问)
> - `docs/REFACTOR-cooldown-recheck-by-codex.md` — 14↔30 天定向裁决
> - `docs/REFACTOR-final-review-by-codex.md` — 最终复核(抓出 5 个真 bug)
> - `docs/REFACTOR-fixes-recheck-by-codex.md` — 修复复核(抓出 2 部分+3 回归)
>
> 最终代码已经过两轮 Codex 复核 + 全部修复。**阅读本文件时,下方"Codex 不可用"
> 的陈述应理解为"重构当时的临时状态",最终状态以 4 份 Codex 审查文档为准。**

**Date:** 2026-07-04
**Worker:** refactor-worker-01 (GLM-only, Codex 不可用降级)
**Run ID:** 2026-07-04-refactor-001
**Branch:** refactor/direction-review-and-scout-skeleton
**Project:** self-evo

## Execution Summary

完成 self-evo 方向审查 + Scout Runner 垂直切片交付 + 治理/记忆 proposal + 文档对齐。重构按 codex-router balanced profile 路由执行,因环境网络无法访问 OpenAI,Codex 任务按 SKILL standing policy 降级为 GLM-only。

## Deliverables

### Code / Implementation
- **`scripts/workers/scout_runner.py`** (487 行): Stage A Scout Runner 主体
  - 强制边界:墙钟/来源数/保留数/重试/超时(6 类,全可 CLI 配置)
  - 4 类来源解析:RSS/Atom(命名空间无关)、JSON API、web HTML
  - URL hash 跨运行去重 + cursor 持久化
  - 决策导向日报生成
- **`scripts/tests/test_scout_runner.py`** (275 行): 42 个单元测试,网络无关

### Tests
- ✅ 全部 4 个可跑测试套件通过:91 + 61 + 14 + 42 = **208 通过, 0 失败**
- ⚠️ test_scout_schema.py 仍因 jsonschema 依赖缺失跳过(**重构前已存在,非回归**)

### Documentation
- `docs/REFACTOR-evidence-pack.md`:GLM 机械核查证据包(给 Codex 的输入)
- `docs/REFACTOR-direction-review.md`:方向审查报告(5 个核心问题判断)
- `docs/REFACTOR-route-log.md`:路由日志(诚实记录 Codex 不可用)
- `docs/REFACTOR-summary.md`:本文件
- `data/exploration/reuse_maps/2026-07-04-scout-runner.md`:复用地图
- `scripts/workers/README.md`:Runner 设计、边界、用法、已知限制
- `data/runs/TEMPLATE.summary.md`:从 fx 经验提炼的通用 run summary 模板
- README.md 更新:已实现/尚未实现清单对齐 + 阶段 A 进度 + 目录导航

### Proposals (遵守 rules 只读铁律)
- `data/proposals/rule_changes/2026-07-04-memory-cooldown-thresholds.md`:记忆冷却阈值
- `data/proposals/rule_changes/2026-07-04-governance-freeze-during-scout-stabilization.md`:治理冻结期

## Current Status

| 维度 | 状态 |
|---|---|
| 方向审查 | ✅ 完成(Codex 降级, fresh-context GLM 替代) |
| Scout Runner 实现 | ✅ 完成 + 端到端闭环验证(3 真实来源, 11s, 5 项保留) |
| 测试 | ✅ 208 通过 0 失败(新增 42 个 scout_runner 测试) |
| 治理/记忆 proposal | ✅ 完成(待人类审批,未碰 rules/) |
| 文档对齐 | ✅ 完成 |
| Codex 第二意见 | ❌ 不可用(网络),关键判断建议网络恢复后复核 |

## Key Findings

1. **README 100% 诚实**:13 项"已实现"全有据,10 项"未实现"全真缺失(核查证据见 evidence-pack)
2. **治理/执行失衡但合理**:707 行 rules + 2182 行护栏 vs 0 行执行层 → Scout Runner 补上了执行层,治理层建议冻结非精简
3. **"先复用再自研"在 Scout 上的应用**:抓取层复用 stdlib(零依赖),决策层自研(无现成库能做"信息→决策"转换)
4. **GitHub Trending 限制**:纯 HTML 抓取受 JS 渲染限制,诚实记录为 known limitation,不引入无头浏览器
5. **Token/Cost 不可观测**:urllib/gh 不暴露模型 token,如实标 unknown 不伪装

## Acceptance Criteria Check

- [x] 方向是否正确判断(审查报告 5 个问题均给出明确判断)
- [x] 结构是否合理评估(治理/执行失衡诊断 + 收敛方案)
- [x] 任务分解与路由执行(9 个工作包, 1b/2b 标 Codex, 其余 GLM)
- [x] 真实交付 Scout Runner 闭环(非 PPT)
- [x] 全程遵守项目铁律(rules 只读 → proposal; 先复用 → reuse map)

## Memory Candidates

可进入长期记忆的候选(写入 data/memory/proposals/memory/):
- "纯 HTML 抓取无法获取 JS 渲染内容(GitHub Trending 类),第一版接受限制不引入浏览器"
- "URL hash 去重在 1000 条以内足够,超过才需语义去重"
- "urllib/gh CLI 不暴露模型 token,fetch 层 token cost 永远是 unknown"

## Route Log

- profile: **balanced** (用户选)
- Codex 升级尝试:1b 方向审查 → **失败(网络无法访问 api.openai.com)**
- 降级处理:按 SKILL.md standing policy,标记 GLM-only,fresh-context GLM 替代第二意见
- 2b 边界设计:原标 Codex,因 Codex 不可用 + 边界需求已在 README/blueprint 明确指定 → GLM 直接实现
- 总 Codex 调用:1 次(失败), 0 token 消耗
- 总 GLM 执行:9 个工作包全完成

## Next Steps

**需要 human 拍板(写入 data/tasks/REVIEW.md):**
1. 审批 2 份 rule_change proposal(记忆阈值 + 治理冻结)——批准后由人类修改 rules/
2. GitHub Trending 限制的三选一(改 Search API / 第三方镜像 / 接受限制)
3. 网络恢复后,是否用 Codex 复核方向审查的 5 个判断(当前是 GLM 自审)

**可自动执行:**
- 应用 patch 到真实仓库:`git apply ~/.zcode/self-evo-work.patch`(在真实 clone 中)
- 跑 Scout Runner 验证:`python scripts/workers/scout_runner.py --max-wall-clock 60`

## Sources / Evidence

- patch 文件:`~/.zcode/self-evo-work.patch` (1567 行, 13 新文件 + 1 修改)
- 工作目录:`~/.zcode/self-evo-work` (branch: refactor/direction-review-and-scout-skeleton)
- 端到端运行证据:`data/exploration/daily_reports/2026-07-04T11-12-48Z-scout.md`

## 不做的事(诚实清单)

- ❌ 没有碰 rules/(全部走 proposal,等人类审批)
- ❌ 没有引入新 Python 依赖(scout_runner 纯 stdlib)
- ❌ 没有引入无头浏览器(GitHub Trending 限制接受)
- ❌ 没有自建 ledger 系统(降级为 URL hash + cursor)
- ❌ 没有伪装修复 test_scout_schema(jsonschema 缺失是环境问题,标注非回归)

# Run Summary 模板
# Template — 每次任务执行结束后复制此文件,填入实际内容
# 来源:从 projects/fx-strategy-research/runs/ 的真实 run summary 提炼
# 用法:cp data/runs/TEMPLATE.summary.md data/runs/<date>/<run-id>.summary.md

<!--
复用自 fx_backtest 闭环验证过的格式 (审查报告 Q4 结论:过程模板可迁移)
Scout Runner 的日报是数据流,run summary 是任务执行流,两者职责不同:
  - Scout daily report: 来源抓取 → 决策候选 (被动)
  - run summary: 任务执行 → 交付证据 (主动)
-->

**Date:** YYYY-MM-DD
**Worker:** <worker-identity>
**Run ID:** YYYY-MM-DD-<slug>-NNN
**Issue:** #<number>
**Branch:** agent/<worker>/<issue-number>-<slug>
**Project:** <self-evo | fx-strategy-research | ...>

## Execution Summary

一两句话说清本次 run 做了什么、是否成功。

## Deliverables

### Code / Implementation
- 具体交付物清单(文件、模块、功能)

### Tests
- 测试状态(全过/部分失败/未跑)
- 测试文件清单

### Documentation
- 新增或更新的文档

## Current Status

| 维度 | 状态 |
|---|---|
| Pipeline | ✅/⚠️/❌ |
| Tests | ✅/⚠️/❌ |
| Data | ✅/⚠️/❌ |
| Blocked | 无 / 描述阻塞点 |

## Key Findings

(执行过程中的关键发现、限制、意外)

## Acceptance Criteria Check

逐条对照 Issue 的验收标准,标记是否达成:
- [ ] 验收标准 1
- [ ] 验收标准 2

## Memory Candidates

可进入长期记忆的候选(写入 data/memory/proposals/memory/):
- 候选 1
- 候选 2

## Route Log

如果本次 run 触发了模型路由(Codex 升级等),记录:
- profile: <savings|balanced|...>
- 升级项: <task> / <reason>
- outcome: <成功|失败|部分>

## Next Steps

- 下一步行动 1
- 下一步行动 2
- 需要 human 拍板的事项(写入 data/tasks/REVIEW.md)

## Sources / Evidence

(来源链接、引用、证据文件路径)

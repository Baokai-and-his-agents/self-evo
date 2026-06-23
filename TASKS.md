# Issue #20 任务追踪

**Claimed by**: agent clawbie  
**Claimed at**: 2026-06-23T00:00:00Z  
**Last heartbeat**: 2026-06-23T00:00:00Z  
**Branch**: agent/fx-backtest-worker-01/20-eurusd-baseline  
**Issue**: https://github.com/Baokai-and-his-agents/self-evo/issues/20

## 任务状态

### Phase 1: 数据源调查与许可审核
- [ ] 调查 Dukascopy Historical Data Export 使用条款
- [ ] 记录数据字段定义和价格类型说明
- [ ] 确认研究使用边界
- [ ] 调查 ECB API 作为交叉校验源

### Phase 2: 下载器与 Adapter 实现
- [ ] 实现 Dukascopy 数据下载器
- [ ] 实现数据规范化 adapter
- [ ] 实现 ECB API 校验工具
- [ ] 建立 state/download-cache/fx-backtest 目录结构

### Phase 3: 数据质量检查
- [ ] Schema 验证
- [ ] 时间排序与重复检查
- [ ] 周末/节假日处理验证
- [ ] OHLC 不变量检查
- [ ] 异常值检测
- [ ] ECB 交叉校验
- [ ] 生成数据质量报告

### Phase 4: 实验配置冻结
- [ ] 固定时间切分 (2005-2016 / 2017-2020 / 2021-2025)
- [ ] 冻结 mvp_daily.json 配置
- [ ] 记录 rollover 建模状态
- [ ] 生成实验协议文档

### Phase 5: 回测执行
- [ ] Full period 回测 (A/B/E/G, zero/conservative cost)
- [ ] Development period 回测
- [ ] Validation period 回测
- [ ] OOS period 回测

### Phase 6: 结果分析与报告
- [ ] 生成交易统计
- [ ] 计算风险指标
- [ ] 条件概率分析
- [ ] Placebo 分布检验
- [ ] 生成中文实验报告
- [ ] 生成机器可读 JSON

### Phase 7: 测试与验证
- [ ] 下载器 mock 测试
- [ ] Schema 测试
- [ ] 时区和聚合测试
- [ ] 无 lookahead 验证
- [ ] 事件流一致性测试
- [ ] 现有测试不回归

### Phase 8: 文档与 PR
- [ ] 生成 run summary
- [ ] 更新 TASKS.md
- [ ] 运行 git diff --check
- [ ] 运行 validator
- [ ] 创建 Draft PR

## 进度记录

### 2026-06-23 初始化
- 创建分支 agent/fx-backtest-worker-01/20-eurusd-baseline
- 创建 TASKS.md 追踪文件
- 准备开始 Phase 1: 数据源调查

## 阻塞与风险

- 需要确认 Dukascopy 使用条款是否允许研究使用
- 需要确认是否能获得 2005 年起的完整数据
- 日线跨夜 rollover 建模可能需要标记 ROLLOVER_NOT_MODELED

## 备注

- 严格串行执行，不启动 subagent
- 所有 GitHub 面向人类的内容使用中文
- 原始大文件不提交 Git
- OOS 结果只运行一次，不回头调参

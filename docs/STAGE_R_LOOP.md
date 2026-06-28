# Stage R Loop

Stage R 是 self-evo 的第一个 loop-native 工作模式。它让 agent 可以被手动唤醒，读取 GitHub Issues，产出本地候选工作，执行一次 advisory runtime review，然后停止；整个过程不修改仓库的 canonical 文件，也不写入 GitHub 状态。

它的目标不是一步到位实现完整自动化，而是在一个清晰、安全、可理解的边界里，让 loop 先产生有用结果。

## Stage R 做什么

一次 Stage R tick 会：

1. 检查 `.self-evo/runtime/` 是否已被 Git 忽略。
2. 通过 `gh issue list` 只读读取打开的 GitHub Issues。
3. 选择零个或一个适合处理的 issue。
4. 在 `.self-evo/runtime/runs/<run_id>/` 下写入一个运行目录。
5. 产出 runtime-only 的候选工作 artifact。
6. 执行一次 advisory Runtime Review。
7. 停止。

no-op 是合法结果。如果当前没有适合处理的 issue，tick 可以什么任务都不选，但仍然写出 artifact 解释为什么这次不工作。

## Stage R 不做什么

Stage R 不会：

- 写 tracked repository files
- 写 GitHub comments、labels、statuses、issues 或 pull requests
- 创建 branches、commits、pushes 或 merges
- 把 `proposed.patch` 应用到 checkout
- 把 runtime artifacts promote 成 canonical project files
- 作为 scheduler 运行
- 启动多个 worker

这个边界是 Stage R 最重要的设计选择：tick 可以产生有用工作，但不能静默获得真正的仓库权威。

## Runtime 记录与 Canonical 记录

runtime 输出只放在：

```text
.self-evo/runtime/**
```

这个路径被 Git 忽略。runtime 输出是本地的、可丢弃的、非权威的候选工作记录。

canonical 记录是仓库中被追踪的项目文件，例如：

```text
rules/**
data/**
state/**
docs/**
scripts/**
.github/**
```

修改 canonical 记录必须走正常仓库流程：branch、commit、review、merge。Stage R 不执行这个 promote 步骤。

## 运行目录约定

每次 tick 都会写入一个运行目录：

```text
.self-evo/runtime/runs/<run_id>/
```

必需 artifact：

```text
input.json
decision.md
result.json
```

条件 artifact：

```text
work.md
evidence.md
proposed.patch
review.md
```

artifact 含义：

- `input.json`：tick 使用的 issue 和 runtime 上下文摘要
- `decision.md`：为什么选择某个 issue，或者为什么这次 no-op
- `work.md`：针对所选 issue 的候选分析
- `evidence.md`：issue 元数据、runtime 边界证据和置信度
- `proposed.patch`：候选 patch 文本；Stage R 永远不会应用它
- `review.md`：advisory Runtime Review 输出
- `result.json`：机器可读的状态和 artifact 索引

## 结果状态

`result.json.status` 是以下之一：

```text
work
noop
error
```

常见的 `result.json.outcome`：

```text
ready_for_promote
needs_revision
no_suitable_issue
fetch_failed
runtime_boundary_violation
```

`ready_for_promote` 只表示候选 patch 通过了 `git apply --check`，并且 runtime review 给出 approved。它不表示 patch 已经被应用、合并，或者被人类接受。

## Runtime Review

Runtime Review 是 advisory 的。它读取 runtime artifacts，并写入 `review.md`。

它可能给出：

```text
approved
needs_revision
rejected
abstain
```

Runtime Review 不允许编辑 worker artifacts，不允许写 GitHub，不允许应用 patch，不允许 promote 文件，也不能替代人类最终审批。

## Patch 处理

Stage R 可以写 `proposed.patch`，但永远不会应用它。

patch 校验只限于：

```bash
git apply --check .self-evo/runtime/runs/<run_id>/proposed.patch
```

实现还会拒绝不安全 patch path，例如绝对路径或包含 `..` 的路径。校验成功只表示 patch 对当前 checkout 来说“机械上可应用”，不代表语义正确。

## 如何运行

手动运行：

```bash
python scripts/loop_runtime_tick.py
python scripts/loop_runtime_tick.py --json
python scripts/loop_runtime_tick.py --label risk:low --limit 10 --json
python scripts/loop_runtime_tick.py --offline-noop --json
```

多个 `--label` 使用 GitHub CLI 的 AND 语义：issue 必须同时带有所有指定 label 才会被 `gh issue list` 返回。

退出码：

- `0`：tick 完成，并写出 success 或 no-op 结果
- `1`：tick 写出了 runtime artifacts，但 `result.json.status` 是 `error`
- `2`：tick 在正常完成前遇到 runtime boundary violation

## Promote 是未来工作

Promote 不属于 Stage R。

未来可以有一个 promote 命令读取已经 review 过的 Stage R run，把 `proposed.patch` 应用到真实 checkout，运行验证，创建 branch，commit，并打开 draft PR。这个步骤必须是显式的，并且需要人类授权。

在此之前，Stage R 输出都只是候选工作。

## 未来的 Loop Map

Stage R 是一个可以手动调用的 tick，不是完整 loop system。

未来可能包括：

- governance loop
- issue intake loop
- PR babysitter loop
- task execution loop
- memory reflection loop

这些未来 loop 应该建立在 Stage R 的边界之上，而不是削弱这个边界。

## 初始实现

Stage R 的初始实现来自：

- PR #24：Stage R runtime boundary 和 no-op tick
- PR #25：只读 issue intake、候选 artifacts、patch check 和 Runtime Review

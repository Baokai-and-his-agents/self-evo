**结论：不建议按当前 README 表述合并。** 代码有一个可运行的 Stage A 骨架，但 README 对“已实现”的描述偏高，且 `scout_runner.py` 本身有几个真 bug。

**主要问题**

1. **README 高估了真实来源闭环。**  
   [README.md](/Users/cui/.zcode/self-evo-work/README.md:177) 说 HN / arXiv / GitHub Trending 来源实例已建立，并且 Runner 跑通真实来源闭环；但现有报告 [2026-07-04T11-12-48Z-scout.md](/Users/cui/.zcode/self-evo-work/data/exploration/daily_reports/2026-07-04T11-12-48Z-scout.md:10) 里 5 条全是 GitHub 导航链接。HN topstories 返回 ID 数组，`parse_json_items()` 只接受 dict，所以产出 0；arXiv 是 Atom XML，但 source 标成 `type: api`，会走 JSON parser，也产出 0。GitHub Trending 已知只抓导航。这算 README 高估。

2. **“对接 schema/approved sources”没有真正实现。**  
   schema 明确说 Runner 要验证 resource approval 和 scope 子集 [scout-source-registry.schema.yaml](/Users/cui/.zcode/self-evo-work/data/exploration/scout-source-registry.schema.yaml:109)，但代码只 `safe_load` YAML 后直接信任 `base_url` [scout_runner.py](/Users/cui/.zcode/self-evo-work/scripts/workers/scout_runner.py:143)。没有 schema 校验、没有 `access_mode` / `resource_approval_id` / `required_scopes` 校验，也没有限制 URL scheme 必须是 public HTTP(S)。

3. **硬墙钟不是硬限制。**  
   `run_scout()` 只在每个 source 开始前检查 wall clock [scout_runner.py](/Users/cui/.zcode/self-evo-work/scripts/workers/scout_runner.py:403)。一旦进入 `fetch_source()`，单个 source 仍可跑满 `request_timeout_seconds * max_retries_per_source`。所以 `--max-wall-clock 1` 仍可能阻塞几十秒，这和 “强制墙钟边界” 不一致。

4. **跨运行去重有预算 bug。**  
   `dedupe()` 会先把所有 unique URL 加入 `seen` [scout_runner.py](/Users/cui/.zcode/self-evo-work/scripts/workers/scout_runner.py:221)，然后 `run_scout()` 再按 `max_items_kept` 截断 [scout_runner.py](/Users/cui/.zcode/self-evo-work/scripts/workers/scout_runner.py:417)。结果是超过保留预算、没有进入日报的项目也会写进 cursor，以后永远不会再出现。

5. **自写 YAML fallback 是真问题，不只是限制。**  
   我用只读 probe 确认 `_parse_sources_minimal(data/exploration/scout-sources.yaml)` 返回 `[]`。它解析不了当前示例里的 `- id: ...` 形式 [scout_runner.py](/Users/cui/.zcode/self-evo-work/scripts/workers/scout_runner.py:174)。当前机器有 PyYAML 6.0.3，所以正常路径没暴露；但 README/代码强调裸 Python、零依赖时，这个 fallback 是坏的。

**Q1 回答**

狭义看，代码确实有：来源数/保留数/重试/timeout 的基本限制、URL hash 去重、日报生成。  
但“强制边界 + 去重 + 决策日报”不是完全兑现：墙钟不硬，去重 cursor 有预算污染 bug，schema/approval 没接上。README 里“真实来源闭环”“对接 schema”“HN / arXiv / GitHub Trending 并列已建立”都偏高。

**Q2 回答**

- GitHub Trending：不是可忽略限制。workers README 的记录是诚实的，但主 README 把它作为已建立来源并列展示，算高估；应修复、禁用，或在主 README 明确“当前不产生真实仓库”。
- 自写 YAML parser：应该修复。当前 fallback 对示例文件不可用。
- 无语义去重：可以接受的诚实标注；但要先修掉 URL 去重的 cursor 预算 bug。
- token cost unknown：可以接受，代码也如实记录 `unknown`。

**Q3 回答**

有之前可能漏掉的问题：source parser/source 类型错配、schema/approval 未校验、硬墙钟漏洞、cursor over-budget 污染、YAML fallback 失效、CLI 边界值未校验。另有小问题：`python` 命令在当前环境不存在，README 用法应考虑 `python3`；`subprocess`、`RAW_DIR`、`_is_relative_to` 未使用。  
我没有改文件；完整测试未跑，只做了静态审查和只读 `python3` probe。
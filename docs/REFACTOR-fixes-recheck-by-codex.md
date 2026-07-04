**结论：不建议直接合并。**  
按当前工作区内容看，5 项里有 3 项到位、2 项部分到位；另外实际修复还没有全部进暂存区，`git diff --cached` 仍是旧版本。

**逐项判断**

1. **HN/arXiv 产出 0：到位**  
   HN 已新增 2-hop `fetch_hn_topstories()`，arXiv 已改成 `type: rss`。日报 `2026-07-04T14-10-35Z-scout.md` 也证明了真实产出：HN 8 条、arXiv 7 条。代码位置：[scout_runner.py](/Users/cui/.zcode/self-evo-work/scripts/workers/scout_runner.py:352)、[scout-sources.yaml](/Users/cui/.zcode/self-evo-work/data/exploration/scout-sources.yaml:20)。

2. **schema/approval 校验缺失：部分到位**  
   `access_mode`、`resource_approval_id`、scope subset、URL scheme 都有校验，并且 approvals 读不到会 fail closed：[scout_runner.py](/Users/cui/.zcode/self-evo-work/scripts/workers/scout_runner.py:126)。  
   但 `required_scopes` 缺失或空数组会通过，因为代码用 `source.get("required_scopes", []) or []`，违反 schema 的 `minItems: 1` 约束：[scout_runner.py](/Users/cui/.zcode/self-evo-work/scripts/workers/scout_runner.py:178)。这不是立即越权，但属于 schema 绕过。

3. **自写 YAML parser：到位**  
   `_parse_sources_minimal` 已移除，PyYAML 缺失时明确报 `ScoutBoundaryError`：[scout_runner.py](/Users/cui/.zcode/self-evo-work/scripts/workers/scout_runner.py:201)。这个决策合理，修那个半吊子 parser 不如要求 PyYAML。

4. **墙钟不硬：部分到位**  
   HN 2-hop loop 内确实检查了 `deadline_ts`：[scout_runner.py](/Users/cui/.zcode/self-evo-work/scripts/workers/scout_runner.py:369)。  
   但普通 source 仍走不带 deadline 的 `fetch_with_retries()`，一旦在 deadline 前进入 fetch，仍可能阻塞到 `request_timeout * retries`：[scout_runner.py](/Users/cui/.zcode/self-evo-work/scripts/workers/scout_runner.py:277)、[scout_runner.py](/Users/cui/.zcode/self-evo-work/scripts/workers/scout_runner.py:424)。所以 8s→9s 的实测改善是真的，但全局硬墙钟还没完全成立。

5. **cursor 预算污染：到位**  
   现在先截断 `all_items`，再 `dedupe()` 更新 `seen`：[scout_runner.py](/Users/cui/.zcode/self-evo-work/scripts/workers/scout_runner.py:528)。我用只读 probe 确认 24 条截到 15 后，`kept=15` 且 `seen=15`。  
   小边界：如果前 15 条里有旧 cursor 重复项，最终 kept 可能少于预算；但不会再污染 over-budget cursor。

**其它问题**

- 死代码清理到位：`subprocess`、`RAW_DIR`、`_is_relative_to`、`_parse_sources_minimal` 都不在当前代码里了。但 docstring 还写着 `subprocess.run(timeout=...)`，是残留文档：[scout_runner.py](/Users/cui/.zcode/self-evo-work/scripts/workers/scout_runner.py:7)。
- 当前修复没有全部暂存：`scripts/workers/scout_runner.py`、`data/exploration/scout-sources.yaml`、`state/scout-cursor.json` 都是 `AM`。如果只合并 index，关键修复会丢。
- 文档有回归：现在代码要求 PyYAML，但 `scripts/workers/README.md` 和 `docs/REFACTOR-summary.md` 仍说“零新依赖/纯 stdlib”。
- `state/scout-cursor.json` 是运行时 cursor，却被加入暂存；这和 README 里 cursor 保持本地/gitignored 的说法冲突。

所以不能给“全部通过”。建议补上 `required_scopes` 非空校验、让普通 fetch 也尊重剩余 deadline、更新文档，并重新整理暂存区后再合并。
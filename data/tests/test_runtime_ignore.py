#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试运行时路径 gitignore 规则

验证：
1. state/ 下的运行时文件（telemetry、checkpoints、cursor、*.db、caches）被 gitignore
2. state/ 下的治理文件（claims、heartbeat）不被 gitignore
3. data/exploration/raw/ 下的原始 ledger 和 caches 被 gitignore
4. data/exploration/raw/ 下的精简 decisions 不被 gitignore

使用 git check-ignore --no-index 验证，不创建实际文件。
兼容 Windows 和 stdlib-only。
"""

import subprocess
import sys
import os
from pathlib import Path

# 强制 UTF-8 输出在 Windows 上
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


def check_ignore(repo_root: Path, path: str) -> bool:
    """
    使用 git check-ignore --no-index 检查路径是否被忽略

    返回 True 如果路径被忽略，False 如果不被忽略
    """
    try:
        result = subprocess.run(
            ["git", "check-ignore", "--no-index", path],
            cwd=repo_root,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False
        )
        # git check-ignore 退出码 0 表示路径被忽略
        return result.returncode == 0
    except Exception as e:
        print(f"错误：无法运行 git check-ignore: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    # 找到 repo 根目录
    repo_root = Path(__file__).resolve().parent.parent.parent

    print(f"测试 repo: {repo_root}")
    print()

    # 定义测试用例：(路径, 应该被忽略)
    test_cases = [
        # state/ 运行时文件（应该被忽略）
        ("state/telemetry/test.jsonl", True),
        ("state/checkpoints/test", True),
        ("state/scout_cursor.json", True),
        ("state/test.db", True),
        ("state/download-cache/test", True),
        ("state/dedupe-cache/test", True),

        # state/ 治理文件（不应该被忽略）
        ("state/claims/7.json", False),
        ("state/heartbeat.json", False),

        # data/exploration/raw/ 原始数据（应该被忽略）
        ("data/exploration/raw/2026-06-22-test-ledger.jsonl", True),
        ("data/exploration/raw/payload-cache/test", True),
        ("data/exploration/raw/download-cache/test", True),
        ("data/exploration/raw/dedupe-cache/test", True),

        # data/exploration/raw/ 精简文件（不应该被忽略）
        ("data/exploration/raw/sample-decisions.md", False),
        ("data/exploration/raw/2026-06-22-test-decisions.md", False),
    ]

    failed = []

    for path, should_be_ignored in test_cases:
        is_ignored = check_ignore(repo_root, path)

        if is_ignored == should_be_ignored:
            status = "[PASS]"
            color = "\033[32m"  # 绿色
        else:
            status = "[FAIL]"
            color = "\033[31m"  # 红色
            failed.append((path, should_be_ignored, is_ignored))

        reset = "\033[0m"
        expected = "应忽略" if should_be_ignored else "不应忽略"
        actual = "已忽略" if is_ignored else "未忽略"

        print(f"{color}{status}{reset} {path}: {expected}, 实际 {actual}")

    print()

    if failed:
        print(f"\033[31m失败：{len(failed)} 个测试未通过\033[0m")
        print()
        for path, should_be_ignored, is_ignored in failed:
            expected = "被忽略" if should_be_ignored else "不被忽略"
            actual = "被忽略" if is_ignored else "不被忽略"
            print(f"  {path}: 预期 {expected}，实际 {actual}")
        sys.exit(1)
    else:
        print(f"\033[32m成功：所有 {len(test_cases)} 个测试通过\033[0m")
        sys.exit(0)


if __name__ == "__main__":
    main()

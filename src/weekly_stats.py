#!/usr/bin/env python3
"""定时任务入口：刷新 README 统计，并在 GitHub Actions 中提交变更。

仅由 .github/workflows/stats.yml 调用，本地手动跑也可以用：
    GITHUB_TOKEN=xxx python src/weekly_stats.py
"""

from __future__ import annotations

import os
import sys

import generate_stats


def main() -> int:
    if not os.getenv("GITHUB_TOKEN"):
        print("[warn] 未检测到 GITHUB_TOKEN，使用未认证请求（有速率限制）", file=sys.stderr)
    return generate_stats.main(["--user", os.getenv("GITHUB_USER", "kurtio")])


if __name__ == "__main__":
    raise SystemExit(main())

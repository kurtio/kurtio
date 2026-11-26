#!/usr/bin/env python3
"""拉取 GitHub 用户统计并写入 README 的 STATS 区块。

用法：
    python src/generate_stats.py --dry-run     # 只打印，不修改文件
    python src/generate_stats.py               # 写入 README.md
    GITHUB_TOKEN=xxx python src/generate_stats.py --user kurtio

只依赖标准库，方便在 CI 里直接运行。Token 从环境变量读取，绝不写进仓库。
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
API = "https://api.github.com"

START = "<!-- STATS:START -->"
END = "<!-- STATS:END -->"


def fetch_user(username: str, token: str | None = None, timeout: int = 15) -> dict:
    """调用 GitHub REST API 获取用户公开信息。"""
    req = urllib.request.Request(
        f"{API}/users/{username}",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": f"{username}-profile-stats",
        },
    )
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def render_stats(data: dict) -> str:
    """把 API 返回的数据渲染成 Markdown 区块内容。"""
    name = data.get("login") or data.get("name") or "unknown"
    public_repos = data.get("public_repos", 0)
    followers = data.get("followers", 0)
    created = (data.get("created_at") or "")[:10] or "未知"

    rows = [
        ("账号", f"@{name}"),
        ("公开仓库", str(public_repos)),
        ("关注者", str(followers)),
        ("注册时间", created),
    ]
    lines = ["", "| 指标 | 数值 |", "| --- | --- |"]
    lines += [f"| {k} | {v} |" for k, v in rows]
    lines += ["", f"_更新于 {datetime.datetime.now():%Y-%m-%d %H:%M}（UTC+8）_", ""]
    return "\n".join(lines)


def update_readme(text: str, block: str) -> str:
    """替换 README 中 STATS:START / STATS:END 之间的内容。"""
    pattern = re.compile(
        re.escape(START) + r".*?" + re.escape(END),
        re.DOTALL,
    )
    replacement = f"{START}{block}{END}"
    if not pattern.search(text):
        raise ValueError("README 中缺少 STATS 标记区块")
    return pattern.sub(replacement, text, count=1)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="更新 README 中的 GitHub 统计区块")
    parser.add_argument("--user", default=os.getenv("GITHUB_USER", "kurtio"))
    parser.add_argument("--dry-run", action="store_true", help="只打印结果，不写文件")
    parser.add_argument("--offline", action="store_true", help="使用示例数据，便于本地验证")
    args = parser.parse_args(argv)

    token = os.getenv("GITHUB_TOKEN")
    if args.offline:
        data = {
            "login": args.user,
            "public_repos": 12,
            "followers": 34,
            "created_at": "2019-03-01T00:00:00Z",
        }
    else:
        try:
            data = fetch_user(args.user, token)
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as exc:
            print(f"[warn] 拉取失败，回退到离线示例数据：{exc}", file=sys.stderr)
            data = {
                "login": args.user,
                "public_repos": 0,
                "followers": 0,
                "created_at": "",
            }

    block = render_stats(data)
    text = README.read_text(encoding="utf-8")
    new_text = update_readme(text, block)

    if args.dry_run:
        print(block)
        return 0

    README.write_text(new_text, encoding="utf-8")
    print(f"[ok] 已更新 {README}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

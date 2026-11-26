# src

个人主页相关的脚本，只依赖 Python 标准库（测试需要 pytest）。

| 文件 | 作用 |
| --- | --- |
| `generate_stats.py` | 拉取 GitHub 用户统计，写入 README 的 `STATS` 区块 |
| `weekly_stats.py` | 供 GitHub Actions 定时调用的薄封装 |
| `tests/` | 离线单元测试 |

## 本地运行

```bash
python -m pip install -r requirements.txt
python src/generate_stats.py --offline --dry-run   # 不联网试跑
python src/generate_stats.py                      # 写入 README
python -m pytest src/tests -q
```

需要真实数据时，在环境变量里放 Token（不要写进任何文件）：

```bash
export GITHUB_TOKEN="ghp_xxx"
python src/generate_stats.py --user kurtio
```

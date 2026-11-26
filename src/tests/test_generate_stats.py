"""generate_stats.py 的单元测试，全部离线运行。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import generate_stats as gs  # noqa: E402


def test_render_stats_contains_fields():
    data = {
        "login": "kurtio",
        "public_repos": 12,
        "followers": 34,
        "created_at": "2019-03-01T00:00:00Z",
    }
    block = gs.render_stats(data)
    assert "@kurtio" in block
    assert "| 公开仓库 | 12 |" in block
    assert "| 关注者 | 34 |" in block
    assert "2019-03-01" in block


def test_update_readme_replaces_block():
    text = f"# Title\n\n{gs.START}\nold\n{gs.END}\n\nfooter\n"
    out = gs.update_readme(text, "\n\nnew\n")
    assert "old" not in out
    assert "new" in out
    assert out.count(gs.START) == 1 and out.count(gs.END) == 1


def test_update_readme_raises_without_markers():
    import pytest

    with pytest.raises(ValueError):
        gs.update_readme("no markers here", "x")


def test_main_dry_run_does_not_write(capsys, monkeypatch, tmp_path):
    readme = tmp_path / "README.md"
    readme.write_text(f"{gs.START}{gs.END}", encoding="utf-8")
    monkeypatch.setattr(gs, "README", readme)
    code = gs.main(["--offline", "--dry-run"])
    assert code == 0
    captured = capsys.readouterr()
    assert "公开仓库" in captured.out
    assert readme.read_text(encoding="utf-8") == f"{gs.START}{gs.END}"

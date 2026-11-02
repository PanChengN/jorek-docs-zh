"""
_paths.py — 统一解析上游仓库与文档目录的位置。

为什么单独抽出来：
  上游 JOREK 仓库和它的 docs/ 副本不在本仓库内部，位置因人而异。
  把路径写死会把维护者的本地目录结构带进开源仓库，而且别人 clone 后跑不了。
  因此这里按「环境变量 > 本地配置 > 通用默认值」解析。

优先级：
  1. 环境变量  JOREK_DOCS_DIR / JOREK_REPO
  2. 仓库根目录的 upstream.local.yml（已在 .gitignore 中，不入库）
  3. 默认值    ../upstream/docs 与 ../upstream/repo

upstream.local.yml 示例：
  docs_dir: ../upstream/docs
  repo:     ../upstream/repo
"""
from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG_FILE = ROOT / "upstream.local.yml"

DEFAULTS = {
    "docs_dir": "../upstream/docs",
    "repo": "../upstream/repo",
}


def _load_config() -> dict:
    if not CONFIG_FILE.exists():
        return {}
    try:
        import yaml
    except ImportError:
        return {}
    try:
        return yaml.safe_load(CONFIG_FILE.read_text(encoding="utf-8")) or {}
    except Exception:
        return {}


def _resolve(key: str, env: str) -> Path:
    cfg = _load_config()
    raw = os.environ.get(env) or cfg.get(key) or DEFAULTS[key]
    p = Path(raw).expanduser()
    return p if p.is_absolute() else (ROOT / p).resolve()


def upstream_docs() -> Path:
    """上游 Wiki 的 Markdown 源码目录（对应仓库的 docs/）。"""
    return _resolve("docs_dir", "JOREK_DOCS_DIR")


def upstream_repo() -> Path:
    """上游 JOREK 仓库的本地克隆（用于 git diff 检测文档变更）。"""
    return _resolve("repo", "JOREK_REPO")


def require(path: Path, what: str) -> Path:
    if not path.exists():
        raise SystemExit(
            f"找不到{what}：{path}\n"
            f"请在 {CONFIG_FILE.name} 中配置，或设置环境变量。示例：\n"
            f"  docs_dir: ../upstream/docs\n"
            f"  repo:     ../upstream/repo"
        )
    return path

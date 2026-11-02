#!/usr/bin/env python3
"""
sync_upstream.py — 把 JOREK 官方 Wiki（Jekyll 站点）同步为本仓库的中文站骨架。

核心目标：**版式与英文原站完全一致，只有语言不同。**

做法：
  * 主题、配色、页头页脚、CSS/JS、图片等素材全部原样复制上游文件，不重写；
  * 每个页面的 front matter 全字段保留（nav_order / has_children / layout …），
    仅把 title / parent / grand_parent 替换为中文；
  * 尚无译文的页面保留官方英文正文，只在顶部加一条"尚未翻译"提示，
    因此导航层级、目录结构与原站逐页对应；
  * 绝不覆盖已存在的文件——译文只需替换 `zh/<path>.md` 对应内容即可。

用法：
    python3 tools/sync_upstream.py --init     # 首次：建骨架 + 复制素材 + 生成页面
    python3 tools/sync_upstream.py --new      # 上游新增页面时：只补缺失页
    python3 tools/sync_upstream.py --report   # 翻译进度统计
"""
from __future__ import annotations

import argparse
import filecmp
import re
import shutil
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
UPSTREAM = ROOT.parent / "02_技术文档" / "官方Wiki源码"
TITLES_FILE = ROOT / "i18n" / "titles.yml"
UPSTREAM_BASE = "https://iterorganization.github.io/JOREK"

# 原样复制的素材目录（保证版式、配色、图标与原站一致）
# 注意：除了顶层的 assets/，各页面子目录下也有 assets/（页面级图片），
# 必须一并复制，否则图片会 404、版式与英文站不一致。
ASSET_DIRS = ["_includes", "_sass"]
# 不参与本地构建的路径
EXCLUDE = ["tools", "i18n", ".venv", "Gemfile", "Gemfile.lock", "README.md",
           "TRANSLATING.md", "_site", ".git"]

MARKER = "<!-- untranslated-notice -->"


def split_front_matter(text: str) -> tuple[str, dict, str]:
    """返回 (front matter 原文, 解析后的 dict, 正文)。"""
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
    if not m:
        return "", {}, text
    raw = m.group(1)
    fm: dict = {}
    for line in raw.split("\n"):
        if ":" in line and not line.lstrip().startswith("#"):
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return raw, fm, text[m.end():]


def unquote(v: str) -> str:
    return v.strip().strip('"').strip("'")


def load_titles() -> dict[str, str]:
    data = yaml.safe_load(TITLES_FILE.read_text(encoding="utf-8")) or {}
    return {k: v for k, v in (data.get("titles") or {}).items()}


def upstream_pages() -> list[Path]:
    pages = []
    for md in sorted(UPSTREAM.rglob("*.md")):
        rel = md.relative_to(UPSTREAM)
        if any(p.startswith("_") or p in {"assets", "node_modules"} for p in rel.parts[:-1]):
            continue
        if rel.parts[0].startswith("_"):
            continue
        pages.append(rel)
    return pages


def rewrite_front_matter(raw_fm: str, zh: str | None) -> str:
    """只改 title / parent / grand_parent 三行，其余字段与顺序保持不变。

    上游个别页面（如 physics/kinetic_models/initialization.md）的 front matter
    里根本没有 title 字段，此时补一行中文 title，否则 Jekyll 的导航会退化成文件名。
    """
    lines = raw_fm.split("\n")
    out = []
    has_title = any(re.match(r"^\s*title\s*:", ln) for ln in lines)
    for line in lines:
        if re.match(r"^\s*title\s*:", line) and zh:
            indent = line[: len(line) - len(line.lstrip())]
            out.append(f'{indent}title: "{zh}"')
        else:
            out.append(line)
    if not has_title and zh:
        out.insert(0, f'title: "{zh}"')
    return "\n".join(out)


def placeholder_notice(en_title: str, rel: Path) -> str:
    stem = rel.as_posix()[:-3]
    url = f"{UPSTREAM_BASE}/" if stem == "index" else f"{UPSTREAM_BASE}/{stem}.html"
    return (
        f"{MARKER}\n"
        f'<div class="warning" markdown="1">\n'
        f'**本页尚未翻译**，以下为 JOREK 官方英文原文。\n\n'
        f'原文页面：[{en_title}]({url})　·　'
        f'源文件：`{rel.as_posix()}`\n'
        f'</div>\n\n'
    )


def build_page(rel: Path, titles: dict[str, str]) -> tuple[str, str]:
    """返回 (页面内容, 状态)。状态：translated / untranslated"""
    src = UPSTREAM / rel
    text = src.read_text(encoding="utf-8", errors="replace")
    fm_raw, fm_dict, body = split_front_matter(text)
    en_title = unquote(fm_dict.get("title", "")) or rel.stem
    zh = titles.get(en_title)

    new_fm = rewrite_front_matter(fm_raw, zh)
    # parent / grand_parent 也要换成中文，否则导航层级断链
    out_lines = []
    for line in new_fm.split("\n"):
        m = re.match(r"^(\s*(?:parent|grand_parent)\s*:\s*)(.+)$", line)
        if m:
            val = unquote(m.group(2))
            out_lines.append(f'{m.group(1)}"{titles.get(val, val)}"')
        else:
            out_lines.append(line)
    new_fm = "\n".join(out_lines)

    header = f"---\n{new_fm}\n---\n\n"
    if body.lstrip().startswith(MARKER):
        body = body.split("\n", 1)[1] if "\n" in body else ""

    return header + placeholder_notice(en_title, rel) + body.lstrip("\n"), "untranslated"


def copy_assets(dry: bool) -> list[str]:
    copied = []
    # 1) 主题相关目录：_includes/、_sass/
    for d in ASSET_DIRS:
        src_root = UPSTREAM / d
        if not src_root.exists():
            continue
        for f in src_root.rglob("*"):
            if not f.is_file():
                continue
            rel = f.relative_to(UPSTREAM)
            dst = ROOT / rel
            if dst.exists() and filecmp.cmp(f, dst, shallow=False):
                continue
            copied.append(rel.as_posix())
            if not dry:
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, dst)
    # 2) 所有 assets/ 目录（顶层与页面级图片、附件）
    for src_dir in UPSTREAM.rglob("assets"):
        if not src_dir.is_dir():
            continue
        for f in src_dir.rglob("*"):
            if not f.is_file():
                continue
            rel = f.relative_to(UPSTREAM)
            dst = ROOT / rel
            if dst.exists() and filecmp.cmp(f, dst, shallow=False):
                continue
            copied.append(rel.as_posix())
            if not dry:
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, dst)
    return copied


def write_config(dry: bool) -> None:
    """以官方 _config.yml 为基底，只改站点标识与主题加载方式。"""
    src = (UPSTREAM / "_config.yml").read_text(encoding="utf-8")
    out = src.replace("title: JOREK Wiki", "title: JOREK 中文文档")
    out = out.replace("description: JOREK project documentation",
                      "description: JOREK 非线性扩展 MHD 代码中文文档（基于官方 Wiki 翻译）")
    out = out.replace('remote_theme: just-the-docs/just-the-docs@v0.10.0',
                      'theme: just-the-docs')
    out = out.replace('  - jekyll-remote-theme\n', '')
    out = out.replace('footer_content: "JOREK Documentation"',
                      'footer_content: "JOREK 文档中文版 · 原文版权归 JOREK 团队所有"')
    out = out.replace('back_to_top_text: "Back to top"', 'back_to_top_text: "返回顶部"')
    # 关键：上游的 url/baseurl 指向官方站点，必须换成中文站自己的，
    # 否则所有导航链接都会带上 /JOREK 前缀而失效。
    out = out.replace('url: "https://iterorganization.github.io"',
                      'url: "https://panchengn.github.io"')
    out = out.replace('baseurl: "/JOREK"', 'baseurl: "/jorek-docs-zh"')
    out += (
        "\n# ===== 中文站附加配置 =====\n"
        "lang: zh-CN\n"
        "exclude:\n" + "".join(f"  - {e}\n" for e in EXCLUDE)
    )
    if not dry:
        (ROOT / "_config.yml").write_text(out, encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--init", action="store_true", help="首次建站（含覆盖骨架文件）")
    ap.add_argument("--new", action="store_true", help="只补缺失页面")
    ap.add_argument("--report", action="store_true", help="翻译进度")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if not UPSTREAM.exists():
        sys.exit(f"错误：找不到上游 Wiki 源码：{UPSTREAM}")

    titles = load_titles()
    pages = upstream_pages()

    if args.report:
        done, undone, untitled = [], [], []
        for rel in pages:
            dst = ROOT / rel
            if not dst.exists():
                undone.append(rel)
                continue
            head = dst.read_text(encoding="utf-8", errors="replace")[:600]
            (undone if MARKER in head else done).append(rel)
        for rel in pages:
            _, fm_one, _ = split_front_matter((UPSTREAM / rel).read_text(encoding="utf-8", errors="replace"))
            if unquote(fm_one.get("title", "")) not in titles:
                untitled.append(rel)
        total = len(pages)
        print(f"页面总数：{total}")
        print(f"已翻译：{len(done)}（{len(done)/total*100:.0f}%）｜"
              f"沿用英文：{len(undone)}")
        print(f"缺中文标题：{len(untitled)}")
        for r in untitled:
            print(f"  ! {r.as_posix()}")
        print("\n已翻译：")
        for r in done:
            print(f"  ✓ {r.as_posix()}")
        return 0

    write_config(args.dry_run)
    copied = copy_assets(args.dry_run)

    created = skipped = 0
    for rel in pages:
        dst = ROOT / rel
        if dst.exists():
            skipped += 1
            continue
        content, _ = build_page(rel, titles)
        created += 1
        if not args.dry_run:
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_text(content, encoding="utf-8")

    print(f"素材文件：复制/更新 {len(copied)} 个（_includes / _sass / assets 原样沿用）")
    print(f"页面：新建 {created}，已存在跳过 {skipped}，上游共 {len(pages)}")
    if args.dry_run:
        print("（dry-run，未写入）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""
verify_site.py — 中文站验收检查（本地一键运行）。

检查四件事：
  1. 是否还有未翻译的页面
  2. 每页结构指纹（代码块 / 公式 / 标题 / 链接 / 表格）是否与英文原文一致
  3. 页面引用的图片是否都存在（对照上游，区分"我们漏了"与"上游本来就没有"）
  4. front matter 是否规范

用法：
    python3 tools/verify_site.py            # 摘要
    python3 tools/verify_site.py --verbose  # 逐条列出问题
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _paths import upstream_docs  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
UP = upstream_docs()
SKIP_DIRS = {"i18n", "tools", "_site"}
SKIP_FILES = {"README.md", "TRANSLATING.md", "NOTICE.md", "THIRD_PARTY_LICENSES.md"}


def body(text: str) -> str:
    return re.sub(r"^---\n.*?\n---\n", "", text, count=1, flags=re.S)


def fingerprint(text: str) -> dict:
    b = body(text)
    return {
        "code": len(re.findall(r"^```", b, re.M)),
        "math": b.count("$$"),
        "heading": len(re.findall(r"^#{1,6} ", b, re.M)),
        "link": len(re.findall(r"\]\(", b)),
        "table": len(re.findall(r"^\|", b, re.M)),
        "image": len(re.findall(r"!\[", b)) + len(re.findall(r"<img", b)),
    }


def md_files() -> list[Path]:
    out = []
    for f in sorted(ROOT.rglob("*.md")):
        if not f.is_file():
            continue
        if any(p in SKIP_DIRS for p in f.relative_to(ROOT).parts):
            continue
        if f.name in SKIP_FILES:
            continue
        out.append(f)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    if not UP.exists():
        print(f"找不到上游文档目录：{UP}")
        return 2

    files = md_files()
    untranslated, fp_bad, fm_bad = [], [], []
    total_han = 0

    up_missing = set()   # 上游自己就缺的图片引用

    for f in files:
        rel = f.relative_to(ROOT)
        text = f.read_text(encoding="utf-8", errors="replace")
        if "untranslated-notice" in text:
            untranslated.append(str(rel))
        if not text.startswith("---\n"):
            fm_bad.append(str(rel))
        total_han += len(re.findall(r"[\u4e00-\u9fff]", body(text)))

        src = UP / rel
        if not src.exists():
            continue
        a, b = fingerprint(src.read_text(encoding="utf-8", errors="replace")), fingerprint(text)
        diff = {k: (a[k], b[k]) for k in a if a[k] != b[k]}
        if diff:
            fp_bad.append((str(rel), diff))

    # 图片引用核对（只报"上游有、我们缺"的真实缺口）
    ours_missing = []
    for f in files:
        text = f.read_text(encoding="utf-8", errors="replace")
        b = body(text)
        defs = {m.group(1).lower(): m.group(2).strip()
                for m in re.finditer(r"^\[([^\]]+)\]:\s*(\S+)", b, re.M)}
        refs = re.findall(r"!\[[^\]]*\]\(([^)\s]+)", b)
        refs += re.findall(r'<img[^>]+src="([^"]+)"', b)
        for name in re.findall(r"!\[[^\]]*\]\[([^\]]*)\]", b):
            if name and name.lower() in defs:
                refs.append(defs[name.lower()])
        for r in refs:
            if not r or r.startswith(("http", "//", "data:", "mailto")):
                continue
            r = r.split()[0].strip("\"'")
            if "?" in r:
                r = r.split("?")[0]
            target = (f.parent / r).resolve()
            if not target.exists():
                # 判断上游是否同样缺失
                up_file = UP / f.relative_to(ROOT)
                up_ref_missing = not (up_file.parent / r).resolve().exists()
                if not up_ref_missing:
                    ours_missing.append((str(f.relative_to(ROOT)), r))
                else:
                    up_missing.add((str(f.relative_to(ROOT)), r))

    print(f"页面总数：{len(files)}｜中文正文：{total_han:,} 字")
    print(f"未翻译页面：{len(untranslated)}")
    print(f"结构指纹不一致：{len(fp_bad)}")
    print(f"front matter 异常：{len(fm_bad)}")
    print(f"图片缺失（我们漏复制）：{len(ours_missing)}")
    print(f"图片缺失（上游本身就没有）：{len(up_missing)}")

    if args.verbose:
        for p in untranslated:
            print(f"  [未译] {p}")
        for p, d in fp_bad:
            print(f"  [结构] {p}: {d}")
        for p in fm_bad:
            print(f"  [front matter] {p}")
        for p, r in ours_missing:
            print(f"  [缺图] {p} → {r}")

    bad = len(untranslated) + len(fp_bad) + len(fm_bad) + len(ours_missing)
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())

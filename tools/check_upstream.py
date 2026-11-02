#!/usr/bin/env python3
"""
check_upstream.py — 检测 JOREK 上游文档（docs/ 目录）是否有更新。

用途：
  * 默认模式：输出一行确定性状态，供 cron 的 monitor 判断"是否变化"
  * --detail：列出具体的新增 / 修改 / 删除页面
  * --accept：把当前上游状态记为新的基线（在完成一轮同步后执行）

基线文件：.upstream-baseline（记录 commit 与 docs 目录树的哈希）

用法：
    python3 tools/check_upstream.py            # 状态行
    python3 tools/check_upstream.py --detail   # 变更明细
    python3 tools/check_upstream.py --accept   # 接受当前上游为新基线
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _paths import upstream_repo  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
REPO = upstream_repo()      # 上游仓库的本地克隆
BASELINE = ROOT / ".upstream-baseline"
BRANCH = "origin/develop"


def git(*args: str, check: bool = False) -> str:
    r = subprocess.run(["git", "-C", str(REPO), *args],
                       capture_output=True, text=True)
    if check and r.returncode != 0:
        sys.exit(f"git {' '.join(args)} 失败：{r.stderr.strip()}")
    return r.stdout.strip()


def read_baseline() -> tuple[str, str]:
    if not BASELINE.exists():
        return "", ""
    parts = BASELINE.read_text(encoding="utf-8").split()
    commit = parts[0] if parts else ""
    tree = parts[1] if len(parts) > 1 else ""
    return commit, tree


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--detail", action="store_true", help="列出变更明细")
    ap.add_argument("--accept", action="store_true", help="把当前上游记为基线")
    ap.add_argument("--no-fetch", action="store_true", help="跳过网络拉取")
    args = ap.parse_args()

    if not REPO.exists():
        sys.exit(f"找不到上游仓库：{REPO}")

    if not args.no_fetch:
        git("fetch", "--quiet", "origin", "develop")

    head = git("rev-parse", BRANCH)
    tree = git("rev-parse", f"{BRANCH}:docs")
    base_commit, base_tree = read_baseline()

    if args.accept:
        BASELINE.write_text(f"{head} {tree}\n", encoding="utf-8")
        print(f"基线已更新：{head[:9]} (docs tree {tree[:9]})")
        return 0

    status = "same" if (base_tree and tree == base_tree) else "changed"
    if not base_tree:
        status = "uninitialized"

    # 默认模式：一行确定性输出，cron monitor 用它判断是否唤醒
    print(f"docs_tree={tree} baseline_tree={base_tree or '-'} status={status}")

    if args.detail and status != "same":
        if not base_tree:
            print("\n尚无基线，无法给出差异。先记录基线：")
            print("  python3 tools/check_upstream.py --accept")
            return 0

        base_commit_ref = base_commit or f"{tree}"
        out = git("diff", "--name-status", base_commit_ref, BRANCH, "--", "docs")
        added, modified, deleted, renamed = [], [], [], []
        for line in out.splitlines():
            parts = line.split("\t")
            if len(parts) < 2:
                continue
            code, path = parts[0], parts[-1]
            path = path.replace("docs/", "", 1)
            if code.startswith("A"):
                added.append(path)
            elif code.startswith("M"):
                modified.append(path)
            elif code.startswith("D"):
                deleted.append(path)
            elif code.startswith("R"):
                renamed.append(f"{parts[1].replace('docs/','',1)} → {path}")

        print(f"\n上游文档变更（{base_commit[:9] or '?'} → {head[:9]}）")
        for label, items in (("新增", added), ("修改", modified),
                             ("删除", deleted), ("重命名", renamed)):
            if items:
                print(f"\n{label} {len(items)} 页：")
                for p in items:
                    print(f"  {p}")

        # 对照中文站的落地状态
        print("\n中文站现状：")
        for p in added:
            print(f"  [未收录] {p}" if not (ROOT / p).exists() else f"  [已有文件] {p}")
        for p in modified:
            exists = (ROOT / p).exists()
            translated = exists and "untranslated-notice" not in (ROOT / p).read_text(
                encoding="utf-8", errors="replace")
            print(f"  [{'已译，需复核' if translated else '未译' if exists else '缺失'}] {p}")
        for p in deleted:
            print(f"  [应移除] {p}" + ("（中文站仍有）" if (ROOT / p).exists() else ""))

        print("\n同步步骤：")
        print("  1. 更新本地副本：git -C <上游仓库> pull")
        print("  2. 覆盖 Wiki 副本：rsync -a --delete <上游仓库>/docs/ <本地 Wiki 副本>/")
        print("  3. 补新增页面：python3 tools/sync_upstream.py --new")
        print("  4. 重译变更页面，运行 tools/verify_site.py 验收")
        print("  5. 记录基线：python3 tools/check_upstream.py --accept")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

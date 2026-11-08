#!/usr/bin/env python3
"""根据现有 lock 里的技能—上游对应关系，重算两侧哈希。

技能清单与上游路径的唯一真相源是 mattpocock.lock 本身（MAPPING.md 已删除）。
上游 commit 变了时用 `python3 scripts/gen_lock.py --commit <sha> --date <iso8601>`。
"""
import argparse
import hashlib
import pathlib
import re
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
LOCK = ROOT / "mattpocock.lock"
UPSTREAM = ROOT.parent / "upstream"  # 仅开发时存在，用于取上游文件哈希


def parse(text: str):
    pairs = []
    cur = None
    for line in text.splitlines():
        m = re.match(r"^  (w-[\w-]+):\s*$", line)
        if m:
            cur = m.group(1)
            continue
        m = re.match(r"^    upstream:\s*(\S+)\s*$", line)
        if m and cur:
            pairs.append((cur, m.group(1)))
    return pairs


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--commit")
    ap.add_argument("--date")
    ap.add_argument("--no-hash", action="store_true", help="只改 commit/date，保留既有哈希")
    args = ap.parse_args()

    text = LOCK.read_text(encoding="utf-8")
    pairs = parse(text)
    if not pairs:
        raise SystemExit("lock 中未找到技能条目")

    m_commit = re.search(r"^commit:\s*(\S+)", text, re.M)
    m_date = re.search(r"^upstream_date:\s*(\S+)", text, re.M)
    commit = args.commit or (m_commit.group(1) if m_commit else "")
    date = args.date or (m_date.group(1) if m_date else "")
    if not commit:
        raise SystemExit("lock 中缺少 commit")

    out = [
        "upstream: https://github.com/mattpocock/skills",
        "repo: https://github.com/wxxxcxx/skills",
        f"commit: {commit}",
        f"upstream_date: {date}",
        "note: 只记录上游 commit 与文件哈希，不保存英文原文（需要时用 git show 取回）",
        "skills:  # 技能与上游路径的唯一对应表",
    ]
    for local, upstream in sorted(pairs):
        uf = UPSTREAM / "skills" / upstream.removeprefix("skills/") / "SKILL.md"
        zf = ROOT / ("engineering" if (ROOT / "engineering/.apm/skills" / local).exists() else "general") / ".apm/skills" / local / "SKILL.md"
        u = hashlib.sha256(uf.read_bytes()).hexdigest() if uf.exists() else "unknown"
        z = hashlib.sha256(zf.read_bytes()).hexdigest() if zf.exists() else "unknown"
        out += [f"  {local}:", f"    upstream: {upstream}", f"    upstream_sha256: {u}", f"    zh_sha256: {z}"]

    LOCK.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"已更新 {len(pairs)} 个技能，commit {commit[:8]}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""从 `git diff --name-status` 的 stdin 聚合出每个上游技能的改动统计。"""
import sys
import collections

status = collections.defaultdict(lambda: collections.Counter())
for line in sys.stdin:
    parts = line.rstrip("\n").split("\t")
    if len(parts) < 2:
        continue
    st, path = parts[0], parts[-1]
    seg = path.split("/")
    if len(seg) < 3:
        continue
    status[f"{seg[1]}/{seg[2]}"][st[0]] += 1

if not status:
    print("共 0 个技能有改动")
    raise SystemExit(0)

print(f"{'上游技能':44} 改动")
for skill in sorted(status):
    tag = " ".join(f"{k}{v}" for k, v in sorted(status[skill].items()))
    print(f"{skill:44} {tag}")
print()
print(f"共 {len(status)} 个技能有改动")

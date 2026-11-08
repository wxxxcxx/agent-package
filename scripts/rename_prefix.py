#!/usr/bin/env python3
"""统一改技能前缀：目录名、frontmatter name、交叉引用、prompt 文件名、mapping、lock。

用法：
    python3 scripts/rename_prefix.py woz- w- [--dry]

name 字段只允许 a-z0-9-，且不能以 - 开头/结尾、不能出现 --，前缀必须满足这些规则。
"""
import argparse
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent


def validate(prefix: str) -> None:
    if not re.fullmatch(r"[a-z0-9]+-", prefix):
        sys.exit(f"前缀不合法：{prefix!r}（只允许 a-z0-9 加一个结尾连字符，如 w-）")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("old")
    ap.add_argument("new")
    ap.add_argument("--dry", action="store_true")
    args = ap.parse_args()
    validate(args.new)

    changes = []

    # 1. 目录改名
    for pkg in ("engineering", "general"):
        base = ROOT / pkg / ".apm" / "skills"
        if not base.exists():
            continue
        for d in sorted(base.iterdir()):
            if d.is_dir() and d.name.startswith(args.old):
                target = d.with_name(args.new + d.name[len(args.old):])
                changes.append(("目录", d, target))
                if not args.dry:
                    d.rename(target)

    # 2. prompt 文件名
    for pkg in ("engineering", "general"):
        base = ROOT / pkg / ".apm" / "prompts"
        if not base.exists():
            continue
        for f in sorted(base.iterdir()):
            if f.name.startswith(args.old):
                target = f.with_name(args.new + f.name[len(args.old):])
                changes.append(("prompt", f, target))
                if not args.dry:
                    f.rename(target)

    # 3. 文本内容
    targets = [
        p
        for p in ROOT.rglob("*")
        if p.is_file()
        and ".git" not in p.parts
        and p.suffix in {".md", ".yaml", ".yml", ".lock", ".sh", ".py"}
        and p.name != pathlib.Path(__file__).name
    ]
    for p in targets:
        s = p.read_text(encoding="utf-8")
        if args.old not in s:
            continue
        changes.append(("内容", p, args.old + " -> " + args.new))
        if not args.dry:
            p.write_text(s.replace(args.old, args.new), encoding="utf-8")

    for kind, a, b in changes:
        print(f"{kind}\t{a}\t{b}")
    print(f"\n共 {len(changes)} 处" + ("（dry run）" if args.dry else ""))


if __name__ == "__main__":
    main()

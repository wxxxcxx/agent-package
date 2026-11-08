#!/usr/bin/env bash
# 上游同步：比对 mattpocock/skills 的改动，产出待翻译清单
#
#   scripts/sync.sh            只报告（默认）
#   scripts/sync.sh --stage    把有改动的上游文件导出到临时目录，供翻译
#   scripts/sync.sh --bump     更新 mattpocock.lock 里的 commit（同步完成后用）
#
set -euo pipefail

UPSTREAM_URL="https://github.com/mattpocock/skills"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOCK="$REPO_ROOT/mattpocock.lock"
STAGE_DIR="${TMPDIR:-/tmp}/w-sync-stage"
WORK="${TMPDIR:-/tmp}/w-upstream.git"

MODE="${1:---report}"

[ -f "$LOCK" ] || { echo "找不到 mattpocock.lock"; exit 1; }
OLD_COMMIT="$(grep -m1 '^commit:' "$LOCK" | awk '{print $2}')"
[ -n "$OLD_COMMIT" ] || { echo "mattpocock.lock 里没有 commit 字段"; exit 1; }

if [ ! -d "$WORK" ]; then
  git clone --quiet "$UPSTREAM_URL" "$WORK"
else
  git -C "$WORK" fetch --quiet --tags origin
fi
NEW_COMMIT="$(git -C "$WORK" rev-parse origin/HEAD)"

if [ "$OLD_COMMIT" = "$NEW_COMMIT" ]; then
  echo "已是最新：$NEW_COMMIT"
  exit 0
fi

echo "上游  $OLD_COMMIT"
echo "  →   $NEW_COMMIT"
echo

# 逐个 skill 聚合改动
git -C "$WORK" diff --name-status "$OLD_COMMIT" "$NEW_COMMIT" -- skills \
  | python3 "$REPO_ROOT/scripts/aggregate_changes.py"

if [ "$MODE" = "--stage" ]; then
  rm -rf "$STAGE_DIR"; mkdir -p "$STAGE_DIR"
  git -C "$WORK" diff --name-only "$OLD_COMMIT" "$NEW_COMMIT" -- skills \
    | while read -r f; do
        [ -z "$f" ] && continue
        out="$STAGE_DIR/$f"
        mkdir -p "$(dirname "$out")"
        git -C "$WORK" show "$NEW_COMMIT:$f" > "$out" 2>/dev/null || true
      done
  echo "已导出到 $STAGE_DIR"
  echo "翻译流程：对每个文件准备三个输入 —— 旧英文、新英文、现有中文，输出最小中文补丁"
fi

if [ "$MODE" = "--bump" ]; then
  python3 "$REPO_ROOT/scripts/gen_lock.py" --commit "$NEW_COMMIT" --date "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
fi

# agent-package

本仓库是 [mattpocock/skills](https://github.com/mattpocock/skills) 的修改版，所有技能以 `x-` 前缀重命名。使用 [APM](https://github.com/anomalyco/agent-package-manager) 管理打包和编译。

## 包结构

| 包                | 路径                  | 依赖                  |
| ----------------- | --------------------- | --------------------- |
| `woz` (根)        | `./apm.yml`           | general + engineering |
| `x-general`     | `general/apm.yml`     | 无                    |
| `x-engineering` | `engineering/apm.yml` | `../general`          |

- 根 `apm.yml` 为顶层编排，不直接包含技能
- `engineering` 依赖 `general`，所以 `.agents/skills/` 中通用和工程技能并存

## 技能组织

- `general/.apm/skills/x-*/` — 通用技能
- `engineering/.apm/skills/x-*/` — 工程技能
- `general/.apm/prompts/x-*.prompt.md` — 通用 prompt（`disable-model-invocation: true` 的技能）
- `engineering/.apm/prompts/x-*.prompt.md` — 工程 prompt （`disable-model-invocation: true` 的技能）

## 同步流程

上游 `mattpocock/skills`，用 `mattpocock.lock` 记录同步点，**不保存英文原文**。

1. `scripts/sync.sh` —— 读 lock 里的 commit，拉上游，`git diff old..new -- skills`，按技能聚合输出改动清单
2. `scripts/sync.sh --stage` —— 把有改动的上游文件导出到 `$TMPDIR/x-sync-stage/`，供翻译
3. 翻译：每个文件三个输入 —— 旧英文（`git show <old>:path`）、新英文（当前 HEAD）、现有中文译文 → 只产出受影响段落的最小中文补丁
4. 写入 `skills/x-*/`：`name:` frontmatter 必须是 `x-` 前缀；正文内的技能引用改成 `x-*`；代码块与命令不译
5. `disable-model-invocation: true` 的技能要同步补 `.apm/prompts/x-*.prompt.md`
6. 跑 `scripts/sync.sh --bump` 更新 lock 的 commit 与时间，`apm.yml` 的 `version` 递增
7. `git diff` 复核：新增 / 修改 / 删除 / 重命名四类是否与报告一致

## 注意事项

- `engineering/MAPPING.md` 和 `general/MAPPING.md` 是技能与上游路径的对应表，新增或删除技能必须同步更新
- `mattpocock.lock` 里每个技能记两个哈希：`upstream_sha256`（上游文件）与 `zh_sha256`（本地译文）。后者与当前文件不符，说明有人手改过，同步时应跳过自动覆盖
- 上游删除的技能（如 `resolving-merge-conflicts`）要连同产物、prompt 一起删


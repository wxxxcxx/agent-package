# skills

本仓库是 [mattpocock/skills](https://github.com/mattpocock/skills) 的修改版，所有技能以 `w-` 前缀重命名。使用 [APM](https://github.com/anomalyco/agent-package-manager) 管理打包和编译。

## 包结构

| 包                | 路径                  | 依赖                  |
| ----------------- | --------------------- | --------------------- |
| `w-skills` (根)        | `./apm.yml`           | general + engineering |
| `w-general`     | `general/apm.yml`     | 无                    |
| `w-engineering` | `engineering/apm.yml` | `../general`          |

- 根 `apm.yml` 为顶层编排，不直接包含技能
- `engineering` 依赖 `general`，所以 `.agents/skills/` 中通用和工程技能并存

## 技能组织

- `general/.apm/skills/w-*/` — 通用技能
- `engineering/.apm/skills/w-*/` — 工程技能
- `general/.apm/prompts/w-*.prompt.md` — 通用 prompt（`disable-model-invocation: true` 的技能）
- `engineering/.apm/prompts/w-*.prompt.md` — 工程 prompt （`disable-model-invocation: true` 的技能）

## 同步流程

上游 `mattpocock/skills`，用 `mattpocock.lock` 记录同步点，**不保存英文原文**。

1. `scripts/sync.sh` —— 读 lock 里的 commit，拉上游，`git diff old..new -- skills`，按技能聚合输出改动清单
2. `scripts/sync.sh --stage` —— 把有改动的上游文件导出到 `$TMPDIR/w-sync-stage/`，供翻译
3. 翻译：每个文件三个输入 —— 旧英文（`git show <old>:path`）、新英文（当前 HEAD）、现有中文译文 → 只产出受影响段落的最小中文补丁
4. 写入 `skills/w-*/`：`name:` frontmatter 必须是 `w-` 前缀；正文内的技能引用改成 `w-*`；代码块与命令不译
5. `disable-model-invocation: true` 的技能要同步补 `.apm/prompts/w-*.prompt.md`
6. 跑 `scripts/sync.sh --bump` 更新 lock 的 commit 与时间，`apm.yml` 的 `version` 递增
7. `git diff` 复核：新增 / 修改 / 删除 / 重命名四类是否与报告一致

## 译文规范

翻译任何技能文件（`SKILL.md` 及其引用的 `.md`）之前，先读 [docs/TRANSLATION.md](./docs/TRANSLATION.md)。以下是必须遵守的硬规则：

1. **语域是书面、克制。** 不写口语、俚语、语气词（「就很」「挺」「搞」「弄」「其实吧」）。目标是中文技术文档，不是对话。
2. **重写，不搬运。** 允许拆句、合句、调序、删冗余；只要求信息不丢，不要求句句对齐。
3. **清除翻译腔。** 「……的参考」「允许你」「的情况下」「对于……来说」「进行／加以／予以」「被……所……」一律改写；英文 em dash 多改冒号或断句。
4. **禁止直译式复合名词。** 名词堆叠（`tracer-bullet vertical slices`）必须拆成短句，例如「只打通一条窄而完整的路径，做完即可独立验证」。隐喻（曳光弹、深模块、战争迷雾）不直接当中文名词使用，首次出现用一句话解释它指什么。
5. **英文术语保留原词**（spec、ticket、seam、adapter、commit、subagent 等），首次出现补一句中文解释，不要自造译名。产品名、命令、路径、代码块、frontmatter 一律不动。
6. **优先沿用中文里已有的说法。** 英文名词直译成中文复合词，往往只有读过原书的人才懂。例：deepening → 「把一组浅模块合并成一个深模块」，不写「深化」；locality → 「改动集中在一处」，不写「局部性」；architectural friction → 「改动困难的地方／痛点」，不写「摩擦点」；single source of truth → 「单一真相来源」，不写「真相源」；variance lever → 「每次跑出来结果都不一样」，不写「方差杠杆」；carry the signal → 「真正说明问题的那几行」，不写「承载信号」；walk the codebase → 「通读一遍」，不写「走查」；seam → 保留 seam，首次出现写「换掉实现时调用方不用改的那条边界」。
7. **改完自检**：遮住英文原文能否独立读通；有无口语词与语气词；术语首次出现是否附解释；代码、路径、命令是否原样。
8. **不译**：`.sh` 脚本、`CREDITS.md` 之类的致谢文件。
9. **动词用书面语。** 「收成／收进／收口」「挂在」「落盘」这类口语动词，改写成「合并成」「写进／在」「收尾」「归在」「写进文件」。

技能之间互相引用的名字、文件名、目录名，以及 `docs/` 下文档中的示例路径，必须与仓库实际结构一致——改名时一并更新，避免出现坏链。

## 注意事项

- `mattpocock.lock` 是技能与上游路径的唯一对应表（`scripts/gen_lock.py` 维护），新增或删除技能时同步更新
- `mattpocock.lock` 里每个技能记两个哈希：`upstream_sha256`（上游文件）与 `zh_sha256`（本地译文）。后者与当前文件不符，说明有人手改过，同步时应跳过自动覆盖
- 上游删除的技能（如 `resolving-merge-conflicts`）要连同产物、prompt 一起删


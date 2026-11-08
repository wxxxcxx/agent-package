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

翻译任何技能文件（`SKILL.md` 及其引用的 `.md`）之前，先读 [docs/TRANSLATION.md](./docs/TRANSLATION.md)。

**核心是一条**：译文要能让没读过原文的中文读者独立理解，同时不改变原意。下面八条是达成这条的约束，冲突时以核心那条为准。


1. **先读懂，再落笔。** 译之前先用自己的话把这一段的意思说一遍。说不出来说明还没读懂；照着单词换词，出来的东西必然生硬。

2. **概念优先于词。** 同一个英文词在不同段落里承担的概念可能不同，中文该跟着概念走，而不是跟着那个词走。不要建立「英文词 → 中文词」的固定对应，那会把一个词的多种用法压成一种，反过来窄化原意。术语真正需要固定的是**概念**，不是拼写。

3. **判生死的问句是「读者能不能从字面理解」。** 能，就按字面写；不能，就把动作说出来。英文用一个名词短语装下的东西（`tracer-bullet vertical slices`、`deepening opportunities`），中文若照搬会变成读者猜不透的堆叠，此时写成一句话，把「做什么」说清楚。

4. **意译必须核对边界。** 换掉一个词，先问：它比原词范围窄了还是宽了？把 deepening 写成「合并」就是窄了——合并只是其中一种手段。改词之后，回头对照上一段/下一段的用法，确认同一个概念在全文仍然指同一件事。窄化比生硬更危险，因为生硬会被读者发现，窄化不会。

5. **英文术语保留原词**（spec、ticket、seam、adapter、commit、subagent 等），首次出现时用一句中文说明它指什么；不要自造译名，也不要给同一个概念换着说法。产品名、命令、路径、代码块、frontmatter 一律不动。

6. **句式服从中文。** 书面、克制，动词承担语义；清除「……的参考」「允许你」「的情况下」「对于……来说」「进行／加以／予以／被……所……」这类骨架；英文 em dash 多改冒号或断句。不写口语、俚语与语气词。

7. **双向自检。** 译完先遮住英文读中文：读得通吗，用词是中文技术写作里会出现的吗。再反过来只看中文：能不能复原出英文那一段的意思，有没有多出原文没有的断言、漏掉原文的限定。两步都过，才算译完。

8. **不译**：`.sh` 脚本、`CREDITS.md` 之类的致谢文件。

技能之间互相引用的名字、文件名、目录名，以及 `docs/` 下文档中的示例路径，必须与仓库实际结构一致——改名时一并更新，避免出现坏链。

## 注意事项

- `mattpocock.lock` 是技能与上游路径的唯一对应表（`scripts/gen_lock.py` 维护），新增或删除技能时同步更新
- `mattpocock.lock` 里每个技能记两个哈希：`upstream_sha256`（上游文件）与 `zh_sha256`（本地译文）。后者与当前文件不符，说明有人手改过，同步时应跳过自动覆盖
- 上游删除的技能（如 `resolving-merge-conflicts`）要连同产物、prompt 一起删


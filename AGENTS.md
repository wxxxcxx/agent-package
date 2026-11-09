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

翻译任何技能文件（`SKILL.md` 及其引用的 `.md`）都适用。英文原文不存于仓库，需要时用 `mattpocock.lock` 记录的 commit 取回。

**唯一的目标**：没读过原文的中文读者能独立读懂，读到的意思与原文一致。以下各条都为达成它服务，冲突时以它为准。译文读着顺、却让读者以为原文说了另一件事，比读着生硬更糟——生硬会被发现，误读不会。

### 落笔之前

1. **先读懂。** 用自己的话把这一段复述一遍。复述不出来说明还没读懂；此时照着单词换词，产出的必然是生硬的东西。
2. **分清文体。** 这一段是定义、步骤、取舍，还是警告？文体对了，句子才立得住。

### 词怎么处理

3. **跟概念走，不跟单词走。** 同一英文词在不同段落里可能承担不同概念，中文应随概念变化，不必逐处对应同一个中文词。**不要建立「英文词 → 中文词」的固定对照表**：那种表会把一个词的多种用法压成一种，看似统一，实则窄化。
4. **判据是「读者能不能从字面理解」。** 能，就按字面写；不能，就把动作说出来。英文惯于把复杂的偏正短语当名词用，中文照搬会变成读者猜不透的堆叠；这时写成一个短句，说清做什么、结果是什么。
5. **意译必须核对边界。** 换掉一个词之后，问三句：比原词范围窄了吗？宽了吗？同一概念在别处还是这个说法吗？窄化最隐蔽——它读起来毫不违和，却悄悄丢掉原文的一部分。把 deepening 写成「合并」就是窄化，合并只是其中一种手段。
6. **术语只有一个名字。** 一部分保留英文原词（spec、seam、adapter、commit、frontier、smart zone），一部分统一译成中文（ticket→工单、subagent→子代理、primary source→主源）。首次出现时把英文原词括注一次，此后全文只用那一个说法——术语的职责是让同一个东西永远叫同一个名字，混用两种叫法等于制造两个概念。
7. **不改的东西**：代码块、命令、路径、变量名、frontmatter、产品名。存在 `GLOSSARY.md` 时，采用其中说法。

### 句子怎么写

8. **书面、克制，动词承担语义。** 写「执行 X」，不写「X 的执行」。
9. **清除英文骨架。** 「……的参考」「允许你」「的情况下」「对于……来说」「进行／加以／予以／被……所……」这类句式，是英文句法套着中文汉字，改写成中文的说法。
10. **服从中文语序。** 英文的前提从句在句首时，中文可后置或拆句；一句塞三个从句就拆成三句；一句之内「的」不超过两个。
11. **第二人称从简。** 原文的 you 多数可省。不用口语、俚语、语气词；「须、应、不得」这类书面情态词可用，但一句之内不叠加。
12. **标点**：中文全角；英文术语与中文之间留一个空格；冒号优先于破折号；列表项以动词或名词开头，行尾不加句号。

### 收笔之前

13. **正向读一遍**：遮住英文，中文单独读得通吗？用词是中文技术写作里会出现的吗？
14. **反向核一遍**：只看中文，能否复原英文那一段的意思？有没有多出原文没有的断言，有没有漏掉原文的限定、条件、例外？
15. **对照上一版**：与既有译文逐段比，确认信息没丢，也没有为了通顺而删掉难译的部分。

### 不译的内容

`.sh` 脚本、`CREDITS.md` 之类的致谢文件。脚本里的注释保持英文，改动容易在复制粘贴时出错。

## 注意事项

- `mattpocock.lock` 是技能与上游路径的唯一对应表（`scripts/gen_lock.py` 维护），新增或删除技能时同步更新
- `mattpocock.lock` 里每个技能记两个哈希：`upstream_sha256`（上游文件）与 `zh_sha256`（本地译文）。后者与当前文件不符，说明有人手改过，同步时应跳过自动覆盖
- 上游删除的技能（如 `resolving-merge-conflicts`）要连同产物、prompt 一起删


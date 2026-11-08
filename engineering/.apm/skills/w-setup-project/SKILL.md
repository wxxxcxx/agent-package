---
name: w-setup-project
description: "为工程类技能配置本仓库：设置 issue tracker、分诊标签词表与领域文档布局。首次使用其他工程技能之前运行一次。"
disable-model-invocation: true
---

# 初始化项目

搭好工程类技能所依赖的仓库级配置：

- **Issue tracker**：issue 存放在哪里（默认为 GitHub；本地 Markdown 亦可开箱使用）
- **分诊标签**：五个规范分诊角色各自对应的标签字符串
- **领域文档**：`GLOSSARY.md` 与 ADR 的位置，以及读取它们的约定

本技能由提示驱动，而非固定脚本。先探查，呈现所见，与用户确认，最后再写入。

## 流程

### 1. 探查

查看当前仓库的初始状态。凡有文件就读，不作假设：

- `git remote -v` 与 `.git/config`：是否 GitHub 仓库，是哪一个
- 根目录的 `AGENTS.md` 与 `CLAUDE.md`：是否存在，其中是否已有 `## Agent skills` 一节
- 根目录的 `GLOSSARY.md` 与 `GLOSSARY-MAP.md`，以及旧名的 `CONTEXT.md`／`CONTEXT-MAP.md`。存在旧文件时，提议用 `git mv` 改为 `GLOSSARY` 命名，并同步改写 `docs/agents/domain.md` 中的相应名称
- `docs/adr/` 以及各 `src/*/docs/adr/` 目录
- `docs/agents/`：本技能此前的产物是否已存在
- `.scratch/`：说明本地 Markdown 的 tracker 约定已在使用
- 是否安装了 `triage` 技能（与本技能同级的 `triage` 目录，或可用技能列表中有 `triage`）。这决定第二节是否执行
- 单体仓库特征：`pnpm-workspace.yaml`、`package.json` 中的 `workspaces` 字段，或含有各自 `src/` 的 `packages/*`。这些只在真正的大型多包仓库中出现；没有则视为单上下文，绝大多数仓库都是如此

### 2. 呈现结论并逐节确认

概括已有与缺失的内容，随后按节推进。一节一问，答复后再进入下一节。

每节先给出推荐答案，使用户一个词即可采纳。只有该选择确实存在分岔时才附一句说明；探查已解决问题的节直接跳过（未安装 `triage` 时跳过第二节；非单体仓库时跳过第三节）。

**第一节：Issue tracker。**

> 说明：「issue tracker」指本仓库的 issue 存放之处。`to-tickets`、`triage`、`to-spec` 等技能从中读取，也向其写入。它们需要知道是调用 `gh issue create`、在 `.scratch/` 下写 Markdown 文件，还是遵循你描述的其他流程。请选择你实际为本仓库跟踪工作的那个位置。

默认取向：这些技能为 GitHub 而设计。若 `git remote` 指向 GitHub，推荐之；若指向 GitLab（`gitlab.com` 或自建实例），推荐 GitLab。其余情况（或用户另有偏好）给出以下选项：

- **GitHub**：issue 存放于仓库的 GitHub Issues（使用 `gh` 命令行）
- **GitLab**：issue 存放于仓库的 GitLab Issues（使用 [`glab`](https://gitlab.com/gitlab-org/cli) 命令行）
- **本地 Markdown**：issue 以文件形式存放在本仓库 `.scratch/<feature>/` 下（适合个人项目或没有远端的仓库）
- **其他**（Jira、Linear 等）：请用户用一段话描述工作流程，本技能原样记录为自由文本

将选择写入 `docs/agents/issue-tracker.md`。GitHub 与 GitLab 模板均带有一个「把 PR 也当作请求入口」的开关，默认**关闭**。保持关闭，且不要主动提出：确有需要的人日后可自行在文件中打开。

GitHub 或 GitLab tracker 需要一个可访问的仓库。用户选定之后，若没有 `git remote` 指向该主机，先向其索取仓库 URL 并接好（必要时 `git init`，再 `git remote add origin <url>`），然后继续。完成标志是在本目录下 `gh repo view`／`glab repo view` 能打印出该项目；做不到就停下，告知用户缺少什么。

**第二节：分诊标签词表。** 未安装 `triage` 技能时整节跳过（探查结果已知），未安装的技能不需要标签。

若已安装，只问一个问题：

> 是否沿用默认的分诊标签？（推荐：**是**）

默认值即五个规范角色，标签字符串与名称一致：`needs-triage`、`needs-info`、`ready-for-agent`、`ready-for-human`、`wontfix`。回答「是」时原样写入。只有用户明确回答「否」时（通常是因为其 tracker 已使用其他名称，例如用 `bug:triage` 表示 `needs-triage`），才收集映射，使 `triage` 套用既有标签而非另建重复标签。

**第三节：领域文档。** 默认为**单上下文**（仓库根目录一个 `GLOSSARY.md` 加一个 `docs/adr/`）。这适合几乎所有的仓库，无需询问，直接写入。

仅当探查发现单体仓库特征时，才提供**多上下文**选项（根目录 `GLOSSARY-MAP.md` 指向各上下文的 `GLOSSARY.md`），并确认采用哪种布局。

### 3. 确认并修改

向用户展示草稿：

- 将加入 `CLAUDE.md` 或 `AGENTS.md` 的 `## Agent skills` 区块（择一规则见第 4 步）
- `docs/agents/issue-tracker.md`、`docs/agents/domain.md`、`docs/agents/triage-labels.md` 的内容（最后一份仅在安装 `triage` 时）

写入之前交由用户修改。

### 4. 写入

**选择要编辑的文件：**

- 存在 `CLAUDE.md`，编辑它
- 否则存在 `AGENTS.md`，编辑它
- 两者都不存在时，询问用户要建哪一个，不要代为决定

已有 `CLAUDE.md` 时绝不另建 `AGENTS.md`，反之亦然；始终编辑已存在的那个。

所选文件中已存在 `## Agent skills` 区块时，就地更新其内容，不要追加重复区块。不要覆盖用户对周边章节的修改。

区块内容：

```markdown
## Agent skills

### Issue tracker

[issue 存放位置的一句话摘要]. See `docs/agents/issue-tracker.md`.

### Triage labels

[标签词表的一句话摘要]. See `docs/agents/triage-labels.md`.

### Domain docs

[布局的一句话摘要："single-context" 或 "multi-context"]. See `docs/agents/domain.md`.
```

仅当安装了 `triage` 且第二节已执行时，才包含 `### Triage labels` 子区块并写入 `docs/agents/triage-labels.md`；否则两者一并省略。

第二节在 GitHub 或 GitLab 上执行时，为 tracker 缺失的每个标签建好（`gh label create`／`glab label create`）。

随后以本技能目录中的种子模板为起点写入文档：

- [issue-tracker-github.md](./issue-tracker-github.md)：GitHub issue tracker
- [issue-tracker-gitlab.md](./issue-tracker-gitlab.md)：GitLab issue tracker
- [issue-tracker-local.md](./issue-tracker-local.md)：本地 Markdown issue tracker
- [triage-labels.md](./triage-labels.md)：标签映射（仅在安装 `triage` 时）
- [domain.md](./domain.md)：领域文档的读取约定与布局

「其他」类型的 tracker，按用户描述从零撰写 `docs/agents/issue-tracker.md`。

### 5. 完成

告知用户配置完成，以及此后哪些工程技能会读取这些文件。说明日后可直接编辑 `docs/agents/*.md`；只有在需要更换 issue tracker 或彻底重来时，才需重跑本技能。

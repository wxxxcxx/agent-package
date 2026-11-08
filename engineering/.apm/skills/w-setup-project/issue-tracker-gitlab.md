# Issue tracker：GitLab

本仓库的 issue 与规格存放在 GitLab Issues 中，一切操作使用 [`glab`](https://gitlab.com/gitlab-org/cli) 命令行。

## 约定

- **创建 issue**：`glab issue create --title "..." --description "..."`。多行描述用 heredoc；传 `--description -` 可打开编辑器
- **读取 issue**：`glab issue view <number> --comments`。要机器可读输出加 `-F json`
- **列出 issue**：`glab issue list -O json`，配合适当的 `--label` 过滤
- **评论**：`glab issue note <number> --message "..."`。GitLab 把评论称作 note
- **加／去标签**：`glab issue update <number> --label "..."` / `--unlabel "..."`。多个标签可用逗号分隔，或重复该参数
- **关闭**：`glab issue close <number>`。该命令不接受关闭评论，所以先用 `glab issue note <number> --message "..."` 发布说明，再关闭
- **合并请求**：GitLab 把 PR 称作 merge request。用 `glab mr create`、`glab mr view`、`glab mr note` 等——形状与 `gh pr ...` 一致，只是 `pr` 换成 `mr`，`comment`/`--body` 换成 `note`/`--message`

仓库由 `git remote -v` 推断——在克隆目录内运行时 `glab` 会自动识别。

## 把合并请求当作分诊入口

**MR 作为请求入口：否。** _（若本仓库把外部 MR 视作功能请求，改为 `yes`；`/w-triage` 会读这个开关。）_

设为 `yes` 时，MR 与 issue 走同一套标签与状态，使用 `glab mr` 的对应命令：

- **读取 MR**：`glab mr view <number> --comments`，diff 用 `glab mr diff <number>`
- **列出待分诊的外部 MR**：`glab mr list -O json`，只保留作者不是项目成员或所有者的 MR（即贡献者的 MR，而非维护者进行中的工作）
- **评论／打标签／关闭**：`glab mr note`、`glab mr update --label`/`--unlabel`、`glab mr close`

与 GitHub 不同，GitLab 的 issue 与 MR 分开编号，明确维护者指的是哪一侧之后，`#42` 不会歧义。

## 技能说「发布到 issue tracker」时

创建一个 GitLab issue。

## 技能说「取回相关工单」时

执行 `glab issue view <number> --comments`。

## 探路操作

由 `/w-wayfinder` 使用。**地图**是一张 issue，**子** issue 作为工单。

- **地图**：一张带 `wayfinder:map` 标签的 issue，正文含 Notes / Decisions-so-far / 迷雾三节。`glab issue create --label wayfinder:map`。（在支持原生 epic 的 GitLab 版本上，可用 epic 承载地图；带标签的 issue 则在任何版本都可用。）
- **子工单**：描述顶部写 `Part of #<map>`，并与地图建立关联（`glab issue create --linked-issues <map> --link-type relates_to`），标签为 `wayfinder:<type>`（`research`／`prototype`／`grilling`／`task`）。认领后指派给推动地图的开发者
- **阻塞**：GitLab 的**原生阻塞链接**——界面上可见的规范表示。用 `/blocked_by #<n>` 快捷动作添加，以 note 形式发布（`glab issue note <child> --message "/blocked_by #<blocker>"`）。原生阻塞链接属 Premium／Ultimate 功能；免费版（或功能不可用）时退回到描述顶部的 `Blocked by: #<n>, #<n>` 行。所有阻塞方关闭时，该工单解除阻塞
- **前沿查询**：用 `glab api projects/:id/issues/<map>/links` 列出地图的子 issue，保留带 `wayfinder:<type>` 标签且未关闭者；剔除仍有未关闭阻塞方者——原生 `blocked_by` 链接指向未关闭 issue（`glab api projects/:id/issues/<child-iid>/links`）、`Blocked by` 行里仍有未关闭 issue、以及已指派者；按地图顺序取第一个
- **认领**：`glab issue update <n> --assignee @me`，是该会话的第一次写操作
- **解决**：`glab issue note <n> --message "<answer>"`，再 `glab issue close <n>`，然后向地图的 Decisions-so-far 追加一条上下文指针（摘要加链接）

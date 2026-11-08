# Issue tracker：GitHub

本仓库的 issue 与规格存放在 GitHub Issues 中，一切操作使用 `gh` 命令行。

## 约定

- **创建 issue**：`gh issue create --title "..." --body "..."`。多行正文用 heredoc
- **读取 issue**：`gh issue view <number> --comments`，用 `jq` 过滤评论，同时取回标签
- **列出 issue**：`gh issue list --state open --json number,title,body,labels,comments --jq '[.[] | {number, title, body, labels: [.labels[].name], comments: [.comments[].body]}]'`，配合适当的 `--label` 与 `--state` 过滤
- **评论**：`gh issue comment <number> --body "..."`
- **加／去标签**：`gh issue edit <number> --add-label "..."` / `--remove-label "..."`
- **关闭**：`gh issue close <number> --comment "..."`

仓库由 `git remote -v` 推断——在克隆目录内运行时 `gh` 会自动识别。

## 把 PR 当作分诊入口

**PR 作为请求入口：否。** _（若本仓库把外部 PR 视作功能请求，改为 `yes`；`/w-triage` 会读这个开关。）_

设为 `yes` 时，PR 与 issue 走同一套标签与状态，使用 `gh pr` 的对应命令：

- **读取 PR**：`gh pr view <number> --comments`，diff 用 `gh pr diff <number>`
- **列出待分诊的外部 PR**：`gh pr list --state open --json number,title,body,labels,author,authorAssociation,comments`，只保留 `authorAssociation` 为 `CONTRIBUTOR`、`FIRST_TIME_CONTRIBUTOR` 或 `NONE` 的条目（去掉 `OWNER`／`MEMBER`／`COLLABORATOR`）
- **评论／打标签／关闭**：`gh pr comment`、`gh pr edit --add-label`/`--remove-label`、`gh pr close`

GitHub 的 issue 与 PR 共用同一套编号，裸写 `#42` 可能指任一者——先用 `gh pr view 42` 解析，失败再退回 `gh issue view 42`。

## 技能说「发布到 issue tracker」时

创建一个 GitHub issue。

## 技能说「取回相关工单」时

执行 `gh issue view <number> --comments`。

## 探路操作

由 `/w-wayfinder` 使用。**地图**是一张 issue，**子** issue 作为工单。

- **地图**：一张带 `wayfinder:map` 标签的 issue，正文含 Notes / Decisions-so-far / 迷雾三节。`gh issue create --label wayfinder:map`
- **子工单**：与地图关联为 GitHub sub-issue（走 sub-issues 端点的 `gh api`）。未启用 sub-issue 时，把子 issue 加入地图正文的任务列表，并在子正文顶部写 `Part of #<map>`。标签：`wayfinder:<type>`（`research`／`prototype`／`grilling`／`task`）。认领后指派给推动地图的开发者
- **阻塞**：GitHub 的**原生 issue 依赖**——界面可见的规范表示。用 `gh api --method POST repos/<owner>/<repo>/issues/<child>/dependencies/blocked_by -F issue_id=<blocker-db-id>` 添加，其中 `<blocker-db-id>` 是阻塞方的数字**数据库 id**（`gh api repos/<owner>/<repo>/issues/<n> --jq .id`，**不是** `#number`，也不是 `node_id`）。GitHub 通过 `issue_dependencies_summary.blocked_by` 报告尚未关闭的阻塞方，这就是当前的闸口。依赖功能不可用时，退回到子正文顶部的 `Blocked by: #<n>, #<n>` 行。所有阻塞方关闭时，该工单解除阻塞
- **前沿查询**：列出地图的未关闭子 issue（`gh issue list --state open`，限定在地图的 sub-issue／任务列表内），剔除仍有未关闭阻塞方者（`issue_dependencies_summary.blocked_by > 0`，或 `Blocked by` 行里仍有未关闭 issue）与已指派者；按地图顺序取第一个
- **认领**：`gh issue edit <n> --add-assignee @me`，是该会话的第一次写操作
- **解决**：`gh issue comment <n> --body "<answer>"`，再 `gh issue close <n>`，然后向地图的 Decisions-so-far 追加一条说明（摘要加链接）

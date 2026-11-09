# Issue tracker：GitHub

本仓库的 issue 与规格存放在 GitHub Issues 中，一切操作使用 `gh` 命令行。

## 约定

- **创建 issue**：`gh issue create --title "..." --body "..."`。多行正文用 heredoc
- **读取 issue**：`gh issue view <number> --json number,title,body,labels,comments`
- **列出 issue**：`gh issue list --state open --json number,title,body,labels,comments --jq '[.[] | {number, title, body, labels: [.labels[].name], comments: [.comments[].body]}]'`，配合适当的 `--label` 与 `--state` 过滤
- **把某个 issue 变成另一个的子 issue**：`gh issue create --parent <parent> ...`，或事后 `gh issue edit <parent> --add-sub-issue <child>`（需 `gh` 2.94 以上）。旧版 `gh`：`gh api --method POST repos/<owner>/<repo>/issues/<parent>/sub_issues -F sub_issue_id=<child-db-id>`（用数据库 id，见下方**阻塞**）。若 sub-issue 不可用，在子正文顶部写 `Part of #<parent>`
- **阻塞**：GitHub 的**原生 issue 依赖**——界面可见的规范表示。用 `gh issue create --blocked-by <n>,<n> ...` 或 `gh issue edit <child> --add-blocked-by <blocker>` 添加（需 `gh` 2.94 以上）。旧版 `gh`：`gh api --method POST repos/<owner>/<repo>/issues/<child>/dependencies/blocked_by -F issue_id=<blocker-db-id>`，其中 `<blocker-db-id>` 是阻塞方的数字**数据库 id**（`gh api repos/<owner>/<repo>/issues/<n> --jq .id`，**不是** `#number`，也不是 `node_id`）。依赖功能不可用时，退回到子正文顶部的 `Blocked by: #<n>, #<n>` 行。所有阻塞方关闭时，该 ticket 解除阻塞
- **统计未关闭的阻塞方**：`gh api repos/<owner>/<repo>/issues/<n> --jq .issue_dependencies_summary.blocked_by`（只算未关闭的；为 0 表示可开工）。`gh issue view <n> --json blockedBy` 会把已关闭的也列出来，须过滤：`--jq '[.blockedBy.nodes[] | select(.state == "OPEN")] | length'`
- **评论**：`gh issue comment <number> --body "..."`
- **加／去标签**：`gh issue edit <number> --add-label "..."` / `--remove-label "..."`
- **关闭**：先用 `gh issue comment <number> --body "..."` 发布说明，再 `gh issue close <number>`。对已关闭的 issue 使用 `gh issue close --comment`，评论会被丢弃且仍返回 0

仓库由 `git remote -v` 推断；在克隆目录内运行时 `gh` 会自动识别。

只把 issue 提交到用户自己的仓库。除非用户就是所有者，否则永远不要提交到 `mattpocock/skills`（这些技能的来源仓库）。在 fork 中，`gh` 可能默认指向上游父仓库，所以一次会话里第一次 `gh issue create` 之前，先用 `gh repo view --json nameWithOwner` 确认目标，若不是用户自己的仓库就先与其确认。

## 把 PR 当作分诊入口

**PR 作为请求入口：否。** _（若本仓库把外部 PR 视作功能请求，改为 `yes`；`/w-triage` 会读这个开关。）_

设为 `yes` 时，PR 与 issue 走同一套标签与状态，使用 `gh pr` 的对应命令：

- **读取 PR**：`gh pr view <number>`，再 `gh pr view <number> --comments`（非 TTY 下 `--comments` 只打印评论，不含正文），diff 用 `gh pr diff <number>`
- **列出待分诊的外部 PR**：`gh api --paginate 'repos/{owner}/{repo}/pulls?state=open' --jq '.[] | select(.author_association | IN("OWNER","MEMBER","COLLABORATOR") | not) | {number, title, author: .user.login, author_association, labels: [.labels[].name]}'`
- **评论／打标签／关闭**：`gh pr comment`、`gh pr edit --add-label`/`--remove-label`、`gh pr close`

GitHub 的 issue 与 PR 共用同一套编号，裸写 `#42` 可能指任一者——先用 `gh pr view 42` 解析，失败再退回 `gh issue view 42`。

## 技能说「发布到 issue tracker」时

创建一个 GitHub issue。

## 技能说「取回相关 ticket」时

执行 `gh issue view <number> --comments`。

## 探路操作

由 `/w-wayfinder` 使用。**地图**是一张 issue，子 issue 即 ticket。

- **地图**：一张带 `wayfinder:map` 标签的 issue，正文含 Notes / Decisions-so-far / 迷雾三节。`gh issue create --label wayfinder:map`
- **子 issue**：与地图关联为 GitHub sub-issue（见上方约定）。标签：`wayfinder:<type>`（`research`／`prototype`／`grilling`／`task`）。认领后指派给推动地图的开发者
- **阻塞**：见上方约定中的**阻塞**。所有阻塞方关闭时，该 ticket 解除阻塞
- **frontier 查询**：列出地图的未关闭子 issue（`gh issue list --state open`，限定在地图的 sub-issue／任务列表内），剔除仍有未关闭阻塞方者（见上方**统计未关闭的阻塞方**）与已指派者；按地图顺序取第一个
- **认领**：`gh issue edit <n> --add-assignee @me`，是该会话的第一次写操作
- **解决**：`gh issue comment <n> --body "<answer>"`，再 `gh issue close <n>`，然后向地图的 Decisions-so-far 追加一条上下文指针（摘要加链接）

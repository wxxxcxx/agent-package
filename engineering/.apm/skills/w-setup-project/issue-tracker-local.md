# Issue tracker：本地 Markdown

本仓库的 issue 与规格（spec）以 Markdown 文件形式存放在 `.scratch/` 下。

## 约定

- 一个功能一个目录：`.scratch/<feature-slug>/`
- 规格位于 `.scratch/<feature-slug>/spec.md`
- 实现工单一工单一文件，位于 `.scratch/<feature-slug>/issues/<NN>-<slug>.md`，从 `01` 起编号——绝不合并成单个工单文件
- 分诊状态记在每个 issue 文件顶部附近的 `Status:` 行（角色字符串见 `triage-labels.md`）
- 评论与对话历史追加到文件末尾的 `## Comments` 标题之下

## 技能说「发布到 issue tracker」时

在 `.scratch/<feature-slug>/` 下新建文件，目录不存在则创建。

## 技能说「取回相关工单」时

读取所引用路径的文件。用户通常会直接给出路径或工单号。

## 探路操作

由 `/w-wayfinder` 使用。**地图**是一个文件，每张工单对应一个**子**文件。

- **地图**：`.scratch/<effort>/map.md`，正文含 Notes / Decisions-so-far / 迷雾三节
- **子工单**：`.scratch/<effort>/issues/NN-<slug>.md`，从 `01` 起编号，正文写问题。`Type:` 行记录工单类型（`research`／`prototype`／`grilling`／`task`），`Status:` 行记录 `claimed`／`resolved`
- **阻塞**：顶部附近的 `Blocked by: NN, NN` 行。所列文件全部为 `resolved` 时，该工单解除阻塞
- **前沿**：扫描 `.scratch/<effort>/issues/`，取未关闭、未阻塞、未被认领的文件，编号最小者优先
- **认领**：动工前先写 `Status: claimed` 并保存
- **解决**：在 `## Answer` 标题下追加答案，置 `Status: resolved`，再把一条上下文指针（摘要加链接）追加到 `map.md` 的 Decisions-so-far

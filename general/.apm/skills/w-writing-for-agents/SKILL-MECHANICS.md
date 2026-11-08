# Skill 机制

[`writing-for-agents`](SKILL.md) 的 skill 专属分支：当文档本身是一份 skill 时，哪些地方不同（frontmatter、调用方式的选择、路由型 skill）。其余写法仍然是 `SKILL.md` 里的通用参考。

## 调用方式

两个选择，交换的是两种负载：

- **模型可调用**的 skill 保留 `description`，agent 能自己触发它，其他 skill 也能调到它。你依然可以手打它的名字：模型调用**始终包含**用户可达；description 只增加 agent 的发现能力，从不剥夺人的调用权。description 是这个 skill 的顶层上下文指针，被迫常驻：用永久的上下文负载换可发现性。内容全是参考的模型可调用 skill，也是共享参考的一个落脚点——别的 skill 能调它，于是多个 skill 共用的参考可以只放一处。机制：不写 `disable-model-invocation`，并写一条面向模型的 description，承载触发分支（`SKILL.md` 里关于指针的写法完全适用）。
- **用户调用**的 skill 把 description 从 agent 的可及范围里摘掉：只有人打出名字才能调，别的 skill 也调不到。零上下文负载，但它花的是认知负载——**你得当那个记得它存在的索引**。机制：设 `disable-model-invocation: true`；`description` 变成面向人的：一行摘要，去掉触发词列表。

只有当 agent 必须自己够到它、或别的 skill 必须调用它时，才选模型调用。如果它永远只靠手打，就做成用户调用，一分上下文负载都不用付。

两个用户调用的 skill 都需要同一份共享参考时，它不能放在任何一方：没有 description，谁也叫不动谁。把它推到 skill 体系之外的普通文件里——任何 skill 都能指向的外部参考。

## 按调用方式拆分

拆分中的"调用切法"（"序列切法"在 `SKILL.md` 里）：当你有一个独立的领头词应当单独触发它（一个你在 prompt 里真的会用的触发词），或者别的 skill 必须调到它时，就切出一个模型可调用的 skill。新加的常驻 description 要付上下文负载，所以这份独立可达性必须值这个价。

## 路由型 skill

当用户调用的 skill 多到你记不住时，这份堆积的认知负载靠一个**路由 skill** 来治：一个用户调用的 skill，点名其他 skill 以及各自该在什么时候用，于是人只需要记住一个。它只能提示，永远无法触发它们——用户调用的 skill 没有 description，除了人，谁也够不到。

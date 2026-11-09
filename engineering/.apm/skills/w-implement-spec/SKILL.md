---
name: w-implement-spec
description: "把 /w-to-spec 与 /w-to-tickets 的产出落地成代码。"
disable-model-invocation: true
---

你拿到了一份 spec，以及归在它下面、描述如何实现的 ticket。

issue tracker 应当已经提供给你；如果没有，让用户先跑 `/w-setup-project`。

目标是：**整份 spec 在一个集成分支上实现完毕**，每张 ticket 都按 issue tracker 的关闭方式结束。

ticket 不是步骤清单，而是一张**任务图**，彼此之间有阻塞关系。这意味着任何时刻都存在一个**前沿**——已经就绪、可以开工的那一批。

每个 subagent 都从干净的上下文窗口开始。

与 subagent 的通信要稀疏，主要靠**上下文指针**：指向 spec、ticket、研究笔记、已有提交。不要重复指针已经能拿到的信息。

**实现型 subagent** 尽量放到后台跑，以获得最大并发。

## 步骤

1. 读 spec 和 ticket，理解任务图。

2. （可选）用一个**探索型 subagent** 完成 ticket 所需的调研——相关代码文件或外部文档。要保证它能写文件：把 markdown 笔记存到仓库之外的目录，供后续所有 subagent 读取。这样**实现型 subagent** 就能专注于实现，而不是边做边找。

3. 建集成分支。如果 issue tracker 通过 PR 关闭 issue，或用户要求，就在第 5 步首次合并后开一个 draft PR（分支上还没有提交时开不了），标明它会关闭该 spec 与相关 ticket。

4. 每张 ticket 用一个全新的**实现型 subagent**，各自在自己的 worktree、自己的分支上：
   - 开工前确认自己的 worktree 基于集成分支，不是就 reset 过去；
   - 调用 Skill 工具执行 `w-tdd` 把 ticket 做出来；
   - 汇报完成之前，先把集成分支的最新 commit 合并进自己的分支。

5. 一个**实现型 subagent** 完成后，用一个**合并型 subagent** 把它的改动合进集成分支。

6. 如果这改变了前沿，就再起若干**实现型 subagent** 处理新就绪的 ticket——这样并发才能拉满。

7. 全部 ticket 完成后，在集成分支上调用 Skill 工具执行 `w-code-review`。用一个全新的**实现型 subagent** 一次性修完评审提出的问题。

8. 如果存在 draft PR，把它标记为 ready for review；否则按 issue tracker 的方式逐张关闭 ticket，并汇报集成分支。

9. 清理所有**实现型 subagent** 的 worktree。

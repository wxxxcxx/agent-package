---
name: w-implement
description: "按 spec 或一组 ticket 实现一块工作。"
disable-model-invocation: true
---

实现用户在 spec 或 ticket 里描述的工作。

如果用户传了 ticket 引用，先从 issue tracker 取回来，开工前报出它的标题。引用有歧义就问。

在事先约定的接缝上，尽量调用 Skill 工具执行 `w-tdd`。

定期跑类型检查、定期跑单个测试文件，最后完整跑一次全量测试。

做完后，调用 Skill 工具执行 `w-code-review` 评审这次工作。

把工作提交到当前分支。

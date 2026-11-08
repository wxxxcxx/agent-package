---
name: w-handoff
description: 把当前对话压缩成一份交接文档，供另一个 agent 接着做。
argument-hint: "下一个会话用来做什么？"
disable-model-invocation: true
---

写一份交接文档，概述当前对话，使全新的 agent 能接着往下做。保存到操作系统临时目录（`$TMPDIR`，否则 `/tmp`；Windows 为 `%TEMP%`），不要写进当前工作区。

文档中给出「建议调用的技能」一节，写明下一个 agent 应当调用哪些技能。

不要重复其他产物（spec、计划、ADR、issue、提交、diff）中已有的内容，改为按路径或链接引用。

隐去任何敏感信息，例如 API key、密码、可识别个人身份的信息。

若用户传入了参数，将其视为对下一个会话聚焦内容的描述，据此调整文档。

# Skills

本项目包含 18 个为 AI 编程助手（如 Claude Code、OpenCode 等）设计的 **skills**（技能指令集），分为工程（Engineering）和通用（General）两大类。每个 skill 是一个标准化的指令文件，指导 AI 以可预测、可重复的方式完成特定任务。

> 本集源自 [mattpocock/skills](https://github.com/mattpocock/skills)，经个性化调整后以 `my-` 前缀发布。

## 目录结构

```
skills/
├── engineering/              # 工程类（13个）
│   ├── my-guide/              技能路由
│   ├── my-codebase-design/    深度模块设计词汇
│   ├── my-diagnosing-bugs/    Bug 诊断流程
│   ├── my-domain-modeling/    领域模型维护
│   ├── my-grill-with-docs/    带文档生成的方案拷问
│   ├── my-implement/          通用实现入口
│   ├── my-improve-codebase-architecture/ 架构改进报告
│   ├── my-init/               项目配置
│   ├── my-prototype/          快速原型
│   ├── my-tdd/                测试驱动开发
│   ├── my-to-issues/          PRD → Issues
│   ├── my-to-prd/             对话 → PRD
│   └── my-triage/             Issue 分类流转
│
└── general/             # 效率类（5个）
    ├── my-grill-me/           方案拷问（无代码库版）
    ├── my-grilling/           拷问引擎核心
    ├── my-handoff/            跨会话交接
    ├── my-teach/              多会话教学
    └── my-writing-great-skills/  Skill 编写指南
```

---

## 工程类 (Engineering)

| Skill | 调用方式 | 核心职责 | 输入 -> 产出 | 详细说明 |
|-------|---------|---------|-------------|---------|
| **my-guide** | 用户调用 | 技能路由与导航 | 自然语言问题 -> 推荐具体 skill/流程 | 作为所有用户调用型 skills 的入口路由器，完整描述"想法→实现"主流程及其分支。当你不确定该用哪个 skill 时，从这里开始。它会分析你的意图，指向正确的路径：有代码库就走 `my-grill-with-docs`，想学东西就走 `my-teach`，想打磨想法就走 `my-grill-me` 等。本质是一个专家系统，把用户的模糊需求映射到精确的 skill 流程上。 |
| **my-codebase-design** | 模型调用 | 架构设计共享词汇 | 设计需求 -> 深度模块设计方案 | 提供一套精确的架构设计语言：**Module**（模块——任何有接口和实现的东西）、**Interface**（接口——调用者需知道的一切，含签名+不变量+顺序约束+错误模式）、**Depth**（深度——小接口背后的大实现）、**Seam**（接缝——可替换行为的位置）、**Adapter**（适配器——满足接口的具体实现）、**Leverage**（杠杆效应——调用者单位学习成本获得的能力）、**Locality**（局部性——变更集中在单点而非散布）。核心原则：删除测试（删掉这模块复杂度真消失了吗？）、接口即测试面、单适配器=假设的接缝/双适配器=真实的接缝。另含 DEEPENING.md（依赖分类与加深策略）和 DESIGN-IT-TWICE.md（并行子代理探索接口多方案）。 |
| **my-diagnosing-bugs** | 模型调用 | 严谨 Bug 诊断 | 用户报告异常 -> 修复 + 回归测试 | **6 阶段不可跳过**：**Phase 1（反馈循环）**——花最大精力构建一个紧致、确定、快速的 pass/fail 信号，这是调试的核心技能。不构建反馈循环之前不能进入假设。提供 10 种构建方式：失败测试→curl/HTTP→CLI 脚本→无头浏览器→回放捕获→一次性 harness→fuzz→二分→差异对比→人肉循环模板。循环必须可 red（能捕获此特定 bug）、确定、快速、可由 agent 运行。**Phase 2（复现+最小化）**——确认 red 后逐步削减输入/配置/数据到最小还能 red 的场景。**Phase 3（假设）**——生成 3-5 个可证伪假说并排名展示给用户。每个必须能用"如果 X 是原因，那么改变 Y 会让 bug 消失/恶化"表达。**Phase 4（检测）**——用一个探针对应一个预测，每次只改一个变量。用 `[DEBUG-xxxx]` 前缀标记日志方便清理。性能问题先测基准再二分。**Phase 5（修复）**——在正确 seam 写回归测试（先 fail → 修复 → pass → 原场景验证）。**Phase 6（清理+事后分析）**——去 instrumentation、删原型、问"什么本可预防"。 |
| **my-domain-modeling** | 模型调用 | 领域模型构建与打磨 | 用户讨论 -> CONTEXT.md / ADRs | 主动构建和打磨项目的"通用语言"：维护 `CONTEXT.md` 术语表（纯词汇，无实现细节）、在对话中实时捕捉术语定义、当用户使用模糊或冲突术语时立即指出、通过具体场景推敲边界。与代码交叉验证——发现矛盾时提出警示。**ADR 纪律**：仅在满足全部三个条件时创建——(1) 难以逆转、(2) 无上下文令人惊讶、(3) 有真实权衡。非此跳过。用 CONTEXT-FORMAT.md 和 ADR-FORMAT.md 格式。单上下文时 CONTEXT.md 放根目录，多上下文时用 CONTEXT-MAP.md 指向各子目录。 |
| **my-grill-with-docs** | 用户调用 | 方案拷问 + 文档生成 | 用户想法 -> 经过打磨的方案 + CONTEXT.md + ADRs | 本质是 `my-grilling` + `my-domain-modeling` 的组合。**有状态**——适用于已有代码库的场景。在一次会话中，先通过拷问式访谈（一次一个问题，等待反馈后继续）把用户的想法沿设计树走到底，同时实时产出 `CONTEXT.md` 术语表和 ADR。对话产生的内容被保留下来，成为代码库的一部分。常用于主流程的"想法→实现"第一步。 |
| **my-implement** | 用户调用 | 通用功能实现 | PRD/Issues -> 已实现 + 已提交的代码 | 基于 PRD 或 issue 实现功能。规则：优先在可用接缝处用 TDD（`/my-tdd`），定期运行类型检查，按单文件测试——全量测试的顺序验证，完成后用 `/review` 审查，最后提交到当前分支。核心理念：把实现规约为一个可重复的消耗过程，减少手工决策。 |
| **my-improve-codebase-architecture** | 用户调用 | 架构改进建议 | 代码库 -> HTML 架构报告 -> 选定改进项的 grilling | 三阶段流程：**Phase 1（探索）**——先读 CONTEXT.md 和 ADRs，然后用 Explore 子代理扫描代码库，感受摩擦点：哪里需要跨多文件理解？哪里模块浅（接口≈实现）？哪里为可测试性提取了纯函数但真实 bug 藏在其调用方式中？哪里接缝泄露耦合？用"删除测试"验证直觉。**Phase 2（HTML 报告）**——写自包含 HTML 到系统临时目录，用 Tailwind CDN + Mermaid CDN 做可视化。每个候选方案包含：涉及文件、问题描述、英文解决方案、效益（用 Leverage/Locality 表达）、before/after 对比图、推荐强度徽章（Strong/Worth exploring/Speculative）。末尾推荐首选。**Phase 3（Grilling）**——用户选定一项后，运行 `my-grilling` 讨论约束/依赖/模块形状/测试策略。与 `my-domain-modeling` 联动——命名新模块时更新 CONTEXT.md，被拒绝时有理由就写 ADR。 |
| **my-prototype** | 用户调用 | 一次性快速原型 | 待验证问题 -> 可运行原型 + 决策记录 | 两个分支任选其一：**Logic 分支**——为状态/业务逻辑问题构建迷你终端交互应用，推动状态机走通难在纸上推演的情况。**UI 分支**——生成多个激进不同的 UI 变体，放在同一路由下通过 URL search param + 底部栏切换。**硬规则**：(1) 从第一天就标记为一次性；(2) 一条命令可运行；(3) 默认无持久化，状态在内存中；(4) 无测试无错误处理；(5) 每次操作后展示全部状态；(6) 回答完问题后要么删除要么吸收到正式代码。唯一值得保留的是答案——捕获到 commit/ADR/issue 或 NOTES.md 中。 |
| **my-init** | 用户调用 | 一次性项目配置 | 裸仓库 -> 可运行工程 skills 的仓库 | 在首次使用工程类 skills 前运行一次。三步配置：**A. Issue Tracker**——选 GitHub（gh CLI）、GitLab（glab CLI）、本地 Markdown（`.scratch/\<feature\>/`）、或其他（用户描述流程，记录为自由格式）。如需 GitHub/GitLab，额外问 PR 是否算请求面。**B. Triage Labels**——映射 5 个标准状态标签：`needs-triage`（待评估）、`needs-info`（等报告人）、`ready-for-agent`（可被 AFK agent 领取）、`ready-for-human`（需人类处理）、`wontfix`（不处理），默认就是名称本身。**C. Domain Docs**——单上下文（一个 CONTEXT.md + docs/adr/）或多上下文（CONTEXT-MAP.md + 各子目录的 CONTEXT.md）。结果写入 `AGENTS.md`/`CLAUDE.md` 的 `## Agent skills` 块 + `docs/agents/` 下的三个种子配置文件。 |
| **my-tdd** | 模型调用 | 测试驱动开发 | 行为需求 -> 通过测试 + 实现 | **哲学**：测试通过公开接口验证行为，而非实现细节。好测试是集成风格的——它描述系统做了什么而非怎么做。**反模式：水平切片**——不许一次性写完所有测试再写实现（会测试"想象的"行为）。**正确方式：垂直切片/示踪子弹**——一个测试 → 一段实现 → 重复。**四阶段**：**Planning**——确认接口变更、验证行为优先级、识别深度模块机会、列行为清单、用户批准。**Tracer Bullet**——写第一个行为测试→看它 fail→写最小代码通过。**Incremental Loop**——逐行为重复，一次只测一个，不过度设计。**Refactor**——全绿后去重、加深度、应用 SOLID、跑测试验证。从不 RED 时重构。 |
| **my-to-issues** | 用户调用 | PRD → Isssue 拆分 | 计划/PRD -> 一组垂直切片 issue | 把 PRD 或计划拆解为可独立领取的 issue。**核心方法论：垂直切片**——每个 issue 是一条贯穿所有集成层（schema → API → UI → 测试）的窄路径，完成后独立可验证/可演示。任何"预重构"应作为第一个 issue。流程：收集上下文 → (可选)探索代码库以使用正确领域词汇 → 起草垂直切片列表 → 与用户确认粒度/依赖关系 → 按依赖顺序发布到 issue tracker（blocker 先发），应用 `ready-for-agent` 标签。Issue 模板包含：父引用、构建内容、验收条件、阻塞关系。 |
| **my-to-prd** | 用户调用 | 对话 → PRD 合成 | 当前对话 -> PRD（已发布到 tracker） | **不做采访**——只综合当前会话中已讨论的内容。流程：(1) 探索代码库理解现状。(2) 勾勒测试接缝——优先用已有接缝、选最高接缝、理想情况只有一个。(3) 用模板写 PRD 并发布到 issue tracker，应用 `ready-for-agent`。PRD 模板包含：Problem Statement（用户视角）、Solution（用户视角）、User Stories（大量，`As an actor, I want... so that...` 格式）、Implementation Decisions（模块/接口/技术决策，不含文件路径，原型产生的精华代码可内联）、Testing Decisions（什么构成好测试、测哪些模块、类似测试的先例）、Out of Scope、Further Notes。 |
| **my-triage** | 用户调用 | Issue 分类流转 | 原始 Issue/PR -> 已标记 + 含 agent brief 的 Issue | 将 issue 和外部 PR 通过状态机流转。**2 个分类角色**：`bug`/`enhancement`。**5 个状态角色**：`needs-triage` → `needs-info`/`ready-for-agent`/`ready-for-human`/`wontfix`。`needs-info` 在报告人回复后回到 `needs-triage`。**工作流**：(1) 收集上下文——读 issue/PR 全文、解析之前 triage 笔记、搜索代码库查是否已实现或之前被拒（读 `.out-of-scope/*.md`）。(2) 推荐——给维护者推荐分类+状态+理由。(3) 验证声称——对 bug 复现、对 PR 检出 diff 跑测试。(4) 必要时 Grilling——用 `my-grilling` + `my-domain-modeling` 打磨模糊需求。(5) 应用结果——`ready-for-agent` 写 agent brief、`ready-for-human` 写类似结构但注明原因、`needs-info` 用模板发问、`wontfix` 根据原因处理（已实现→指向代码、拒绝的 enhancement→写入`.out-of-scope/`）。所有 AI 生成的评论前缀 `> *This was generated by AI during triage.*`。 |

---

## 通用类 (General)

| Skill | 调用方式 | 核心职责 | 输入 -> 产出 | 详细说明 |
|-------|---------|---------|-------------|---------|
| **my-grill-me** | 用户调用 | 方案拷问（无代码库版） | 用户想法 -> 打磨后的清晰方案 | 和 `my-grill-with-docs` 本质相同（都运行 `my-grilling` 引擎），但**无状态**——不保存任何本地文件、不创建 `CONTEXT.md`。适用于你没有代码库、或者在正式进入代码之前先把方案想清楚的场景。比如在写 PRD 之前先用它和用户走一遍设计树的每个分支。 |
| **my-grilling** | 模型调用 | 拷问引擎核心 | 模糊想法 -> 经过应力测试的共识 | **一次只问一个问题**，沿着设计树的每条分支走下去，逐步解决决策间的依赖关系。每个问题附带推荐答案，等待用户反馈后才继续，避免信息过载。如果某个问题可以通过探索代码库回答，优先探索而非提问。这是 `my-grill-with-docs` 和 `my-grill-me` 背后共用的引擎，也是 `my-improve-codebase-architecture` 和 `my-triage` 中 grilling 环节的核心。 |
| **my-handoff** | 用户调用 | 跨会话上下文交接 | 当前会话 -> handoff.md（临时目录） | 当当前会话的上下文窗口快满了、需要分支出去做原型/调研、或完成了一个阶段需要另开新会话时使用。功能：把当前对话压缩为一份交接文档，**保存到系统临时目录**（非工作区），包含"建议技能"章节指引下一个 agent 应加载哪些 skills。不重复已有工件——引用 PRD/ADR/issue/commit 替代重新描述。自动脱敏 API Key、密码、PII。 |
| **my-teach** | 用户调用 | 多会话教学系统 | 学习主题 -> MISSION + Lessons + Reference + Learning Records | 在多个会话中深入学一个技能/概念。在当前目录**有状态维护**完整教学工作区：`MISSION.md`（学习动机——所有课程围绕它设计）、`RESOURCES.md`（高质量资源清单）、`lessons/*.html`（单文件课程——Tufte 风格、可打印、有引用）、`reference/*.html`（速查表/语法/词汇表——会被反复回顾）、`learning-records/*.md`（类似 ADR 的学习决策记录——用来算最近发展区）、`assets/*`（可复用组件——样式表、测验组件、模拟器，默认复用）。**教学法**：区分流畅强度（即时检索）和存储强度（长期记忆），通过检索练习（回忆而非识别）、间隔重复、交错练习（仅限技能类）构建存储强度。每个课程紧贴使命、在最近发展区内、完成后给出一个可感知的收益。含"知识→技能→智慧"三层体系。 |
| **my-writing-great-skills** | 用户调用 | Skill 编写参考 | Skill 写作/编辑需求 -> 符合规范的 skill | **可预测性**是最高美德——agent 每次跑相同的*过程*，而非产出相同的结果。核心概念：**调用模式**——模型调用（skill 描述常驻上下文/可被其他 skill 调用）vs 用户调用（零上下文开销/需人类记忆）；**信息层次**——内联步骤 > 内联参考 > 外部参考（渐进式披露）；**分支**——不同场景走不同路径；**上下文指针**——通过措辞而非目标文件来决定何时触发引用；**引导词**——利用模型预训练中的已有概念来锚定行为（如"紧致"循环、"red"状态）；**修剪**——单一事实来源、相关性检查、无操作句测试。五种失败模式诊断：过早完成（步骤未真完成就收工）、重复（同一含义多处分说）、沉积（只加不减）、臃肿（太长即使每行都有用）、无操作句（模型默认已做的行为）。 |

---

## 主流程概览

| 场景 | 推荐路径 | 说明 |
|------|---------|------|
| **有一个新想法** | `my-grill-with-docs` → [是否多会话？→ `my-to-prd` → `my-to-issues` → 每个 issue 开新会话 `my-implement`] | 先在代码库语境下拷问打磨，然后决定是否拆分为独立 issue 实现 |
| **需要验证一个决策** | `my-handoff` → `my-prototype` → `my-handoff` 回来 | 分支出去做一次性原型（逻辑验证或 UI 探索），回来继续主线程 |
| **收到 Bug/功能请求** | `my-triage` → `my-implement` | 先经过 triage 分类验证，再实现 |
| **想学新技能** | `my-teach` | 多会话有状态学习 |
| **偶尔架构维护** | `my-improve-codebase-architecture` | 扫描浅模块、生成报告、挑选改进 |
| **不确定用哪个** | `my-guide` | 路由到正确的 skill |
| **第一次使用** | `my-init` | 配好 issue tracker / 标签 / 领域文档再开始 |

### 主流程关系图

```
                                     ┌─────────────────┐
                                     │    my-init        │ (一次性)
                                     └────────┬────────┘
                                              │
             ┌────────── my-guide ────────────┤
             │                                │
             ▼                                ▼
     ┌──────────────┐                ┌────────────────┐
     │  my-grill-me  │                │my-grill-with-docs│
     │  (无代码库)   │                │ (有代码库+文档)  │
     └──────┬───────┘                └───────┬────────┘
            │                                │
            │    ┌──────────┐               │
            └────│my-grilling│◄──────────────┘
                 │ (查问引擎)│◄──── my-improve-codebase-architecture
                 └────┬─────┘      my-triage
                      │
            ┌─────────┴─────────┐
            ▼                   ▼
     ┌──────────┐       ┌──────────┐
     │ my-to-prd │       │my-prototype│
     └────┬─────┘       │ (一次性)  │
          │             └────┬─────┘
          ▼                  │
     ┌──────────┐            │
     │my-to-issues│◄───────────┘ (验证后回来)
     └────┬─────┘
          │
          ▼
     ┌──────────┐     ┌──────────┐
     │my-implement├───►│  my-tdd   │
     └──────────┘     └──────────┘
          │
          ▼
     ┌──────────┐
     │ my-handoff│ (跨会话，通向新会话或新原型)
     └──────────┘

     工具类（被其他 skill 引用）：
     ┌──────────────────┐  ┌─────────────────┐
     │ my-codebase-      │  │ my-domain-       │
     │ design           │  │ modeling        │
     └──────────────────┘  └─────────────────┘

     独立技能：
     ┌──────────────────┐  ┌──────────────────────┐
     │ my-teach          │  │ my-writing-great-     │
     │ (多会话学习)      │  │ skills               │
     └──────────────────┘  └──────────────────────┘
```

# Skills

本项目包含 18 个为 AI 编程助手（如 Claude Code、OpenCode 等）设计的 **skills**（技能指令集），分为工程（Engineering）和通用（General）两大类。每个 skill 是一个标准化的指令文件，指导 AI 以可预测、可重复的方式完成特定任务。

> 本集源自 [mattpocock/skills](https://github.com/mattpocock/skills)。

## 目录结构

```
.apm/
└── skills/
    ├── guide/              技能路由与导航 (Engineering)
    ├── codebase-design/    深度模块设计词汇 (Engineering)
    ├── diagnosing-bugs/    Bug 诊断流程 (Engineering)
    ├── domain-modeling/    领域模型维护 (Engineering)
    ├── grill-with-docs/    带文档生成的方案拷问 (Engineering)
    ├── implement/          通用实现入口 (Engineering)
    ├── improve-codebase-architecture/ 架构改进报告 (Engineering)
    ├── init/               项目配置 (Engineering)
    ├── prototype/          快速原型 (Engineering)
    ├── tdd/                测试驱动开发 (Engineering)
    ├── to-issues/          PRD → Issues (Engineering)
    ├── to-prd/             对话 → PRD (Engineering)
    ├── triage/             Issue 分类流转 (Engineering)
    ├── grill-me/           方案拷问（无代码库版）(General)
    ├── grilling/           拷问引擎核心 (General)
    ├── handoff/            跨会话交接 (General)
    ├── teach/              多会话教学 (General)
    └── writing-great-skills/  Skill 编写指南 (General)
```

---

## 工程类 (Engineering)

| Skill | 调用方式 | 核心职责 | 输入 -> 产出 |
|-------|---------|---------|-------------|
| **guide** | 用户调用 | 技能路由与导航 | 自然语言问题 -> 推荐具体 skill/流程 |
| **codebase-design** | 模型调用 | 架构设计共享词汇 | 设计需求 -> 深度模块设计方案 |
| **diagnosing-bugs** | 模型调用 | 严谨 Bug 诊断 | 用户报告异常 -> 修复 + 回归测试 |
| **domain-modeling** | 模型调用 | 领域模型构建与打磨 | 用户讨论 -> CONTEXT.md / ADRs |
| **grill-with-docs** | 用户调用 | 方案拷问 + 文档生成 | 用户想法 -> 经过打磨的方案 + CONTEXT.md + ADRs |
| **implement** | 用户调用 | 通用功能实现 | PRD/Issues -> 已实现 + 已提交的代码 |
| **improve-codebase-architecture** | 用户调用 | 架构改进建议 | 代码库 -> HTML 架构报告 -> 选定改进项的 grilling |
| **prototype** | 用户调用 | 一次性快速原型 | 待验证问题 -> 可运行原型 + 决策记录 |
| **init** | 用户调用 | 一次性项目配置 | 裸仓库 -> 可运行工程 skills 的仓库 |
| **tdd** | 模型调用 | 测试驱动开发 | 行为需求 -> 通过测试 + 实现 |
| **to-issues** | 用户调用 | PRD → Issue 拆分 | 计划/PRD -> 一组垂直切片 issue |
| **to-prd** | 用户调用 | 对话 → PRD 合成 | 当前对话 -> PRD（已发布到 tracker） |
| **triage** | 用户调用 | Issue 分类流转 | 原始 Issue/PR -> 已标记 + 含 agent brief 的 Issue |

---

## 通用类 (General)

| Skill | 调用方式 | 核心职责 | 输入 -> 产出 |
|-------|---------|---------|-------------|
| **grill-me** | 用户调用 | 方案拷问（无代码库版） | 用户想法 -> 打磨后的清晰方案 |
| **grilling** | 模型调用 | 拷问引擎核心 | 模糊想法 -> 经过应力测试的共识 |
| **handoff** | 用户调用 | 跨会话上下文交接 | 当前会话 -> handoff.md（临时目录） |
| **teach** | 用户调用 | 多会话教学系统 | 学习主题 -> MISSION + Lessons + Reference + Learning Records |
| **writing-great-skills** | 用户调用 | Skill 编写参考 | Skill 写作/编辑需求 -> 符合规范的 skill |

---

## 主流程概览

| 场景 | 推荐路径 | 说明 |
|------|---------|------|
| **有一个新想法** | `grill-with-docs` → [是否多会话？→ `to-prd` → `to-issues` → 每个 issue 开新会话 `implement`] | 先在代码库语境下拷问打磨，然后决定是否拆分为独立 issue 实现 |
| **需要验证一个决策** | `handoff` → `prototype` → `handoff` 回来 | 分支出去做一次性原型（逻辑验证或 UI 探索），回来继续主线程 |
| **收到 Bug/功能请求** | `triage` → `implement` | 先经过 triage 分类验证，再实现 |
| **想学新技能** | `teach` | 多会话有状态学习 |
| **偶尔架构维护** | `improve-codebase-architecture` | 扫描浅模块、生成报告、挑选改进 |
| **不确定用哪个** | `guide` | 路由到正确的 skill |
| **第一次使用** | `init` | 配好 issue tracker / 标签 / 领域文档再开始 |

### 主流程关系图

```
                                     ┌─────────────────┐
                                     │    init        │ (一次性)
                                     └────────┬────────┘
                                              │
             ┌────────── guide ────────────┤
             │                                │
             ▼                                ▼
     ┌──────────────┐                ┌────────────────┐
     │  grill-me  │                │grill-with-docs│
     │  (无代码库)   │                │ (有代码库+文档)  │
     └──────┬───────┘                └───────┬────────┘
            │                                │
            │    ┌──────────┐               │
            └────│grilling│◄──────────────┘
                 │ (查问引擎)│◄──── improve-codebase-architecture
                 └────┬─────┘      triage
                      │
            ┌─────────┴─────────┐
            ▼                   ▼
     ┌──────────┐       ┌──────────┐
     │ to-prd │       │prototype│
     └────┬─────┘       │ (一次性)  │
          │             └────┬─────┘
          ▼                  │
     ┌──────────┐            │
     │to-issues│◄───────────┘ (验证后回来)
     └────┬─────┘
          │
          ▼
     ┌──────────┐     ┌──────────┐
     │implement├───►│  tdd   │
     └──────────┘     └──────────┘
          │
          ▼
     ┌──────────┐
     │ handoff│ (跨会话，通向新会话或新原型)
     └──────────┘

     工具类（被其他 skill 引用）：
     ┌──────────────────┐  ┌─────────────────┐
     │ my-codebase-      │  │ my-domain-       │
     │ design           │  │ modeling        │
     └──────────────────┘  └─────────────────┘

     独立技能：
     ┌──────────────────┐  ┌──────────────────────┐
     │ teach          │  │ my-writing-great-     │
     │ (多会话学习)      │  │ skills               │
     └──────────────────┘  └──────────────────────┘
```

---

## APM (Agent Package Manager) 使用指南

本项目现已改造为一个标准的 APM 包，你可以通过 APM 将这些技能轻松集成到各种 AI 编程助手（如 Claude Code, Cursor, Copilot 等）中。

### 1. 本地编译 (对于本仓库开发者)

如果你在当前仓库进行开发，想要编译并输出技能到本地的各个 AI 客户端配置目录：

```bash
# 编译所有本地 primitive（技能、提示等）到对应的 AI 客户端目录
apm compile --local-only
```

### 2. 作为依赖安装 (对于其他项目)

要在其他项目中使用本项目定义的技能：

1. 在你的项目根目录下初始化 APM：
   ```bash
   apm init
   ```
2. 安装本项目作为依赖（例如通过 Git 仓库）：
   ```bash
   apm install git+https://github.com/wxxxcxx/agent-package.git
   ```
3. 运行编译命令，将这些技能注入到你项目的 AI 工具链配置中：
   ```bash
   apm compile
   ```

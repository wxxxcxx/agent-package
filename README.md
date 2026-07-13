# agent-package — 技能包

21 个 AI 编程助手技能（skills），派生自 [mattpocock/skills](https://github.com/mattpocock/skills)。每个 skill 定义可复现的行为模式，通过 APM 分发。

## 技能一览

### 主流程：想法 → 交付

| Skill | 调用方 | 职责 |
|-------|--------|------|
| `woz-grill-with-docs` | 用户调用 | 拷问打磨想法，并生成 CONTEXT.md 和 ADRs |
| `woz-help` | 用户调用 | 技能路由器 — 描述你的场景，推荐路径 |
| `woz-to-spec` | `woz-help` → | 将当前对话合成为 PRD，发布到 tracker |
| `woz-to-tickets` | `woz-help` → | 将 PRD 拆为垂直切片 ticket（声明阻塞边） |
| `woz-implement` | `woz-help` → | 通用实现入口，内部驱动 `woz-tdd`，最终运行 `woz-code-review` |
| `woz-tdd` | `woz-implement` 调用 | 红-绿-重构循环 |
| `woz-code-review` | `woz-implement` 调用 | 双轴审查（规范 + 规格） |
| `woz-prototype` | 主流程分支 | 一次性原型验证设计问题（逻辑或 UI） |
| `woz-handoff` | 主流程/跨会话 | 上下文压缩，桥接会话窗口 |

### 入轨（On-ramps）

| Skill | 调用方 | 职责 |
|-------|--------|------|
| `woz-triage` | 用户调用 | Issue/PR 分类流转，输出 agent-ready brief |
| `woz-diagnosing-bugs` | 用户调用 | 严格 Bug 诊断（先建反馈环，再假设） |
| `woz-wayfinder` | 用户调用 | 探索式规划大块工作，逐步收窄 |

### 代码库健康

| Skill | 调用方 | 职责 |
|-------|--------|------|
| `woz-improve-codebase-architecture` | 用户调用 | 扫描浅模块，生成 HTML 报告，挑选改进项 |

### 底层词汇（被其他 skill 引用）

| Skill | 职责 |
|-------|------|
| `woz-codebase-design` | 深度模块设计词汇（module, seam, depth, leverage...） |
| `woz-domain-modeling` | 领域术语打磨，ADR 记录 |

### 独立工具

| Skill | 调用方 | 职责 |
|-------|--------|------|
| `woz-grill-me` | 用户调用 | 无代码库的方案拷问 |
| `woz-grilling` | 内部引擎 | 拷问核心（被 `grill-with-docs`, `triage` 等调用） |
| `woz-research` | 用户调用 | 后台代理调查问题，输出引用 Markdown |
| `woz-resolving-merge-conflicts` | 用户调用 | 解决合入/变基冲突 |
| `woz-teach` | 用户调用 | 多会话有状态教学 |
| `woz-writing-great-skills` | 用户调用 | Skill 编写指南 |
| `woz-setup-project` | 用户调用 | 一次性项目配置（issue tracker / triage labels / domain docs） |

## 调用关系

```
woz-setup-project (一次性)
       │
       ▼
woz-help ─── 路由器，推荐以下路径

═══ 新想法 ═══
                                          ┌──────────────────┐
woz-grill-with-docs ─────────► 单会话？──►   woz-implement    │
       │                              │     └── woz-tdd      │
       │                              │     └── woz-code-review
       │                              │
       │               ┌──────────────┘
       │               ▼ 多会话？
       │         woz-to-spec → woz-to-tickets
       │                     每个 ticket → woz-implement (新会话)
       │
       └── 需要验证？→ woz-handoff → woz-prototype
                           ▲                    │
                           └── woz-handoff ←────┘

═══ Bug / 请求涌入 ═══
woz-triage → woz-implement

═══ 大块模糊工作 ═══
woz-wayfinder → woz-to-spec / woz-implement

═══ 难复现 Bug ═══
woz-diagnosing-bugs
       └── 无合适 seam → woz-improve-codebase-architecture

═══ 代码库健康 ═══
woz-improve-codebase-architecture → woz-grill-with-docs (产生改进想法)

═══ 底层词汇（被以上技能引用） ═══
woz-codebase-design   ← woz-improve-codebase-architecture, woz-tdd
woz-domain-modeling   ← woz-grill-with-docs, woz-triage

═══ 独立使用 ═══
woz-grill-me      无代码库的方案拷问
woz-teach         多会话学习
woz-research      后台研究
woz-resolving-merge-conflicts  冲突解决
woz-writing-great-skills       Skill 创作指南
```

## 命名约定

所有技能以 `woz-` 前缀命名，与上游 `mattpocock/skills` 区分。以下为特殊映射：

| 上游名 | 本仓库名 |
|--------|----------|
| `ask-matt` | `woz-help` |
| `setup-matt-pocock-skills` | `woz-setup-project` |
| 其余 | `woz-` + 原名 |



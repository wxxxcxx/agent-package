# agent-package — 技能包（中文版）

27 个 AI 编程助手技能（skills），派生自 [mattpocock/skills](https://github.com/mattpocock/skills)，**正文全部译为中文**，通过 APM 分发。

- 上游同步靠 `mattpocock.lock`（记录 commit 与文件哈希）+ `scripts/sync.sh`（比对差量）
- 技能统一 `x-` 前缀，与上游区分
- 代码块、命令、路径、变量名保持原样，不翻译

## 技能一览

### 主流程：想法 → 交付

| Skill | 调用方 | 职责 |
|-------|--------|------|
| `x-grill-with-docs` | 用户调用 | 拷问打磨想法，生成术语表与 ADR |
| `x-help` | 用户调用 | 技能路由器 —— 描述场景，推荐路径 |
| `x-to-spec` | `x-help` → | 把对话合成为 spec，发布到 tracker |
| `x-to-tickets` | `x-help` → | 把 spec 拆成垂直切片 ticket（声明阻塞边） |
| `x-implement` | `x-help` → | 通用实现入口，内部驱动 `x-tdd`，收尾跑 `x-code-review` |
| `x-implement-spec` | `x-help` → | 整个 spec 在一个集成分支上并行跑多个 subagent |
| `x-tdd` | `x-implement` 调用 | 红-绿-重构循环 |
| `x-code-review` | `x-implement` 调用 | 双轴审查（规范 + 规格），并行 subagent |
| `x-pr` | 模型自调用 | PR 正文模板：最小可视化 + 前后证据 + 合并风险 |
| `x-prototype` | 主流程分支 | 一次性原型验证设计问题（逻辑或 UI） |
| `x-handoff` | 跨会话 | 上下文压缩，桥接会话窗口 |

### 入轨（On-ramps）

| Skill | 调用方 | 职责 |
|-------|--------|------|
| `x-triage` | 用户调用 | Issue/PR 分类流转，输出 agent-ready brief |
| `x-diagnosing-bugs` | 用户调用 | 严格 Bug 诊断：先建反馈环，再假设 |
| `x-wayfinder` | 用户调用 | 探索式规划大块工作，逐步收窄 |
| `x-wizard` | 模型自调用 | 生成交互式 bash 向导，带人走只有人能做的步骤 |
| `x-research` | 模型自调用 | 后台调研，输出带引用的 Markdown |

### 代码库健康

| Skill | 调用方 | 职责 |
|-------|--------|------|
| `x-improve-codebase-architecture` | 用户调用 | 扫描浅模块，生成 HTML 报告，挑选改进项 |
| `x-retro` | 用户调用 | 会话复盘：改进 agent 环境（导航/检查/规范/工具） |

### 底层词汇（被以上技能引用）

| Skill | 职责 |
|-------|------|
| `x-codebase-design` | 深模块设计词汇（module / seam / depth / leverage） |
| `x-domain-modeling` | 领域术语打磨，ADR 记录 |
| `x-grilling` | 拷问核心引擎，被多个技能复用 |

### 通用

| Skill | 调用方 | 职责 |
|-------|--------|------|
| `x-grill-me` | 用户调用 | 无代码库的方案拷问 |
| `x-teach` | 用户调用 | 多会话有状态教学 |
| `x-wait-what` | 用户调用 | 没听懂，要求换更简单的说法重讲 |
| `x-to-questionnaire` | 用户调用 | 答不了的决策 → 转成问卷给别人填 |
| `x-writing-for-agents` | 模型自调用 | 写给 agent 看的文档（skill / AGENTS.md） |
| `x-setup-project` | 用户调用 | 一次性项目配置（tracker / labels / docs 目录） |

## 调用关系

```
x-setup-project (一次性)
       │
       ▼
x-help ─── 路由器，推荐以下路径

═══ 新想法 ═══
x-grill-with-docs ──► 单会话 ──► x-implement ──► x-tdd
       │                              │            └► x-code-review
       │                              └► x-pr
       │
       └─► 多会话 ──► x-to-spec ──► x-to-tickets
                            │
                            └──► x-implement（每 ticket 新会话）
                                 或 x-implement-spec（并行 subagent）
       │
       └─► 需要验证 ──► x-handoff ──► x-prototype

═══ Bug / 请求涌入 ═══
x-triage ──► x-implement

═══ 大块模糊工作 ═══
x-wayfinder ──► x-to-spec / x-implement

═══ 难复现 Bug ═══
x-diagnosing-bugs
       └── 无合适 seam ──► x-improve-codebase-architecture

═══ 代码库健康 ═══
x-improve-codebase-architecture ──► x-grill-with-docs（产生改进想法）
x-retro ──► 改进 agent 环境本身

═══ 底层词汇（被以上技能引用） ═══
x-codebase-design   ← x-improve-codebase-architecture, x-tdd
x-domain-modeling   ← x-grill-with-docs, x-triage
x-grilling          ← x-grill-with-docs, x-triage

═══ 独立使用 ═══
x-grill-me              无代码库的方案拷问
x-teach                 多会话学习
x-wait-what             听不懂时要求重讲
x-to-questionnaire      把决策转成问卷
x-writing-for-agents    写 skill / AGENTS.md 的规范
```

## 命名与映射

所有技能以 `x-` 前缀命名。特殊映射：

| 上游名 | 本仓库名 |
|--------|----------|
| `ask-matt` | `x-help` |
| `setup-matt-pocock-skills` | `x-setup-project` |
| `writing-for-agents` | `x-writing-for-agents` |
| 其余 | `x-` + 原名 |

完整映射见 `engineering/MAPPING.md`、`general/MAPPING.md`。

## 上游同步

```bash
scripts/sync.sh            # 比对 mattpocock.lock 与上游，输出改动清单
scripts/sync.sh --stage    # 把有改动的上游文件导出到临时目录，供翻译
scripts/sync.sh --bump     # 同步完成后，更新 lock 里的 commit
```

`mattpocock.lock` 只记录：上游 commit、同步时间、每个技能的上游路径与两个 sha256（上游文件 / 本地译文）。**仓库里不保存英文原文** —— 需要旧版本时用 `git show <commit>:skills/...` 从上游取。

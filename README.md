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

## Handoff 使用详解

`woz-handoff` 是跨会话的桥梁。当上下文窗口逼近限制、或需要分支出去做原型时，用它压缩当前会话并继续。

### 典型场景：主会话 → 原型分支 → 合并回主会话

**会话 A（主线程）：** 正在打磨一个支付模块的设计。

```
用户: /woz-grill-with-docs 我想设计一个支持分期付款的支付模块...
助手: [开始 grilling session...]
      ...多轮对话后，方案逐渐清晰，但需要验证一个状态机设计...
助手: 建议先做原型验证分期状态机，再继续打磨。
      运行 /woz-handoff 将当前上下文交接出去。
```

**手顺 1 — `woz-handoff` 出：**

```
用户: /woz-handoff 验证分期付款状态机原型
```

Agent 在系统临时目录生成 `handoff-<timestamp>.md`，包含：
- 当前方案摘要（未定决策、已定约束）
- 已捕获的 CONTEXT.md 术语
- 相关 ADR 路径
- 建议技能：`woz-prototype`（逻辑分支）

**会话 B（新窗口）：** 打开新会话，引用 handoff 文档。

```
用户: [附加 handoff-<timestamp>.md] 按 handoff 的说明做原型
助手: [读取 handoff，启动 woz-prototype]
      构建一个交互式终端原型，验证分期状态转换...
      ────
      运行: pnpm prototype:payment-plan
      验证结果：状态机在"提前还款→切换分期方案"路径上有状态遗漏
      决策：需要在 Event 中添加 forceRecompute 标记
      ────
      验证完成，运行 /woz-handoff 将结论带回去。
```

**手顺 2 — `woz-handoff` 回：**

```
用户: /woz-handoff 带回分期状态机原型结论
```

Agent 生成第二个 handoff 文档，包含：
- 原型验证结论
- 新增的决策（forceRecompute 标记）
- 原型分支名和 gist 链接
- 建议技能：`woz-grill-with-docs`（继续打磨）

**会话 A（回到主线程）：** 引用 handoff 文档继续。

```
用户: [附加 handoff-回执.md] 原型做完了，继续
助手: [读取 handoff，将原型结论合并进当前方案]
      好，基于原型结果，调整状态机设计...
      [继续 grilling 会话]
```

### Handoff 规则

1. **不重复已有 artifact** — handoff 只写上下文摘要，不复制 spec/ADR/commit 内容，通过路径引用
2. **含 suggested skills** — 每个 handoff 文档末尾标注接收方应加载的技能
3. **脱敏** — API key、密码、PII 自动过滤
4. **不留在仓库里** — 写入 OS 临时目录（`$TMPDIR` / `%TEMP%`）
5. **双向引用** — 回传 handoff 保留前一个 handoff 的路径，形成链式追踪

### 用 `compact`（内置）还是 `handoff`？

| 场景 | 用 |
|------|----|
| 同一会话内阶段性总结，无需保留完整历史 | `compact` |
| 需要分支出去做原型 → 回来继续 | `handoff` → `handoff` 回传 |
| 上下文窗口即将占满，但当前阶段尚未结束 | `handoff`（开新会话） |
| 不同人/不同 Agent 接力 | `handoff` |

## 命名约定

所有技能以 `woz-` 前缀命名，与上游 `mattpocock/skills` 区分。以下为特殊映射：

| 上游名 | 本仓库名 |
|--------|----------|
| `ask-matt` | `woz-help` |
| `setup-matt-pocock-skills` | `woz-setup-project` |
| 其余 | `woz-` + 原名 |

## 使用方式

通过 [APM](https://github.com/microsoft/apm) 安装和编译：

```bash
apm install git+https://github.com/wxxxcxx/agent-package.git
apm compile
```

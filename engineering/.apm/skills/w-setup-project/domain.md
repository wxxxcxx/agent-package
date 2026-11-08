# 领域文档

工程类技能在探索代码库时，应如何使用本仓库的领域文档。

## 探索之前先读这些

- 仓库根目录的 **`GLOSSARY.md`**；或
- 根目录存在 **`GLOSSARY-MAP.md`** 时读它——它指向各上下文各自的 `GLOSSARY.md`，按话题读相关的那几个
- **`docs/adr/`**——读与即将改动的区域相关的 ADR。多上下文仓库还要看 `src/<context>/docs/adr/` 下属于该上下文的决策

任一文件不存在时，**静默继续**。不要指出缺失，也不要提议预先创建。`/w-domain-modeling`（由 `/w-grill-with-docs` 与 `/w-improve-codebase-architecture` 调起）会在术语或决策真正定下来时按需创建。

## 文件结构

单上下文仓库（多数仓库）：

```
/
├── GLOSSARY.md
├── docs/adr/
│   ├── 0001-event-sourced-orders.md
│   └── 0002-postgres-for-write-model.md
└── src/
```

多上下文仓库（根目录存在 `GLOSSARY-MAP.md`）：

```
/
├── GLOSSARY-MAP.md
├── docs/adr/                          ← 系统级决策
└── src/
    ├── ordering/
    │   ├── GLOSSARY.md
    │   └── docs/adr/                  ← 上下文内决策
    └── billing/
        ├── GLOSSARY.md
        └── docs/adr/
```

## 使用术语表的词汇

输出中要给某个领域概念命名时（issue 标题、重构提议、假设、测试名），使用 `GLOSSARY.md` 中的定义，不要漂移成术语表明确避免的同义词。

需要的概念不在术语表里时，这本身是个信号：要么你在造项目不用的说法（回头再想），要么确实有缺口（记下来交给 `/w-domain-modeling`）。

## 标注 ADR 冲突

输出与既有 ADR 相悖时，明确摆出来，而不是悄悄覆盖：

> _与 ADR-0007（订单采用事件溯源）冲突，但值得重开，理由是……_

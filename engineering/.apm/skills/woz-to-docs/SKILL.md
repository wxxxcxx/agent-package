---
name: woz-to-docs
description: Router — scan session and dispatch the right sub-skill. Use when the user says 'generate docs', 'document this', or '沉淀到文档'.
disable-model-invocation: true
---

# To Docs — Router

| Signal | Dispatch |
|--------|----------|
| Requirements, feature scope, user needs discussed | **woz-to-prd** |
| Architecture decision, trade-off, constraint accepted | **woz-to-adr** |
| System structure, component boundaries, data flow changed | **woz-to-architecture** |
| Domain terms, acronyms, new concepts introduced | **woz-to-glossary** |
| Multiple signals | Dispatch each sequentially |

**REQUIRED SUB-SKILL:** `woz-to-prd`, `woz-to-adr`, `woz-to-architecture`, `woz-to-glossary`.

Each handles its own gather → grill → generate → review. Cascade: `woz-to-adr` automatically calls `woz-to-architecture` when an ADR takes effect (Accepted). Report what was saved where.

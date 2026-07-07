---
name: woz-to-adr
description: From session or user input to an ADR changelog entry with status. Use when the session makes a decision, accepts a trade-off, or reverses a previous choice — or when the user says 'record this decision', or woz-to-docs dispatches.
---

# To ADR

**From** session or user input **to** one ADR — the **changelog of design intent**: what changed, why, and what it replaced.

## Status

`Proposed → Accepted → Deprecated / Superseded by ADR-NNNN`

New ADR superseding an old one? Update the old ADR's status to `Superseded by ADR-NEWN`.

## Workflow

1. **Gather.** Extract from session or accept user parameters (decision topic, supersedes ADR-NNNN). Template at `ADR-TEMPLATE.md` is the extraction checklist.
2. **Grill.** Ambiguous? Use `woz-grill-with-docs`.
3. **De-dup.** Scan `docs/adr/`. Decision already captured? Ask: update or supersede.
4. **Generate.** Fill template. Number sequentially — highest existing + 1.
5. **Save.** `docs/adr/NNNN-decision-title.md`.
6. **Review.** Present to user. Revise on request.
7. **Cascade.** ADR status is Accepted or changed from Accepted? System structure affected → `woz-to-architecture` now.

**Done when:** ADR saved, user approved, superseded ADRs updated, architecture doc updated if affected.

---
name: woz-to-architecture
description: From session or user input to the Architecture Design doc. Use when the session discusses component redesign, data flow changes, deployment updates — or when the user asks to write/update an arch doc, or woz-to-docs dispatches.
---

# To Architecture

**From** session or user input **to** the single global architecture doc — the current-state snapshot. Always `docs/architecture.md`. Overwrite on update; old content lives in git history.

## Status

`Draft → Current`

## Workflow

1. **Gather.** Extract from session or accept user parameters. Template at `ARCHITECTURE-TEMPLATE.md` is the extraction checklist.
2. **Grill.** Ambiguous? Use `woz-grill-with-docs`.
3. **Generate.** Fill template. If doc exists, overwrite with latest changes.
4. **Save.** `docs/architecture.md`.
5. **Review.** Present to user. Revise on request.

**Done when:** Doc saved/updated, user approved.

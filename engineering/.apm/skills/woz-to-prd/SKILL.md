---
name: woz-to-prd
description: From session or user input to Epic PRDs with User Stories. Use when the session discusses requirements, feature scope, or user needs — or when the user asks for a PRD, or woz-to-docs dispatches.
---

# To PRD — Epic & User Stories

**From** session or user input **to** one or more Epic PRDs. Each Epic covers one business domain / functional module. Each Epic contains prioritized User Stories.

Template at `PRD-TEMPLATE.md` is the extraction checklist — every section filled or marked unanswered.

## Status

`Draft → Review → Approved → Implemented → Superseded`

## Workflow

1. **Domain.** Identify the business domain / functional module the requirement belongs to.
2. **Epic.** Define the Epic. If an existing Epic in `docs/prd/` already covers this domain, extend it. If the Epic holds too much content, split — re-domain into smaller Epics.
3. **Stories.** Break the Epic into User Stories (As a… I want… So that…). Assign priority P0/P1/P2.
4. **Grill.** Ambiguous on any story or Epic boundary? Use `woz-grill-with-docs`.
5. **Generate.** Fill template per Epic.
6. **Save.** `docs/prd/<epic-name>.md`.
7. **Review.** Present all Epics. Revise on request.

**Done when:** All Epic PRDs saved, user approved, stories prioritized.

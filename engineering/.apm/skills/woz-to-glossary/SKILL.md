---
name: woz-to-glossary
description: From session or user input to the project glossary. Use when the session introduces domain-specific terms, acronyms, or concepts that need defining — or when the user says 'add term', 'define this', or woz-to-docs dispatches.
---

# To Glossary

**From** session or user input **to** the project glossary — a single `docs/glossary.md` table of every domain term, its definition, and context.

## Workflow

1. **Detect.** Session introduces domain terms, acronyms, or concepts not yet in the glossary.
2. **Define.** For each term: term name, definition, context (where/how it's used), related terms.
3. **De-dup.** Check `docs/glossary.md`. Term exists? Update definition or add nuance. Missing? Add entry.
4. **Grill.** Ambiguous definition? Use `woz-grill-with-docs`.
5. **Save.** `docs/glossary.md`. Append new terms, update existing. Template at `GLOSSARY-TEMPLATE.md` is the format reference.
6. **Review.** Present changes. Revise on request.

**Done when:** Glossary updated, user approved, all new terms defined.

## Template

See [GLOSSARY-TEMPLATE.md](GLOSSARY-TEMPLATE.md) in this directory.

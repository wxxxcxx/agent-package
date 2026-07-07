---
name: woz-research
description: Investigate a question against high-trust primary sources and capture the findings as a Markdown file in the repo. Use when the user wants a topic researched, docs or API facts gathered, or reading legwork delegated to a background agent.
disable-model-invocation: true
---

# Research

Investigate the user's question against primary sources — official docs, source code, specs, first-party APIs — not a secondary write-up of them. Follow every claim back to the source that owns it.

## Process

### 1. Scope the question

Clarify what the user wants to know. If the question is broad, break it into sub-questions. Confirm your understanding before diving in.

### 2. Delegate to a background agent

Spin up a background agent to do the research so you keep working while it reads. Give it:

- The question and sub-questions
- The primary source priority list (official docs > source code > specs > first-party APIs)
- The instruction to cite every claim to its source
- The output format: a single Markdown file

### 3. Verify and collate

When the agent returns, review its findings:

- Are claims backed by primary sources, not secondary write-ups?
- Are citations precise (URLs, line numbers, spec sections)?
- Does it answer the original question?

Fix any gaps yourself.

### 4. Write the findings

Save the findings as a single Markdown file. Follow the repo's existing convention for such notes — if the repo already keeps research notes in a `docs/research/` or similar directory, put it there. If there is no convention, put it in `docs/research/` and tell the user where it landed.

Each section should cite its source. Use this format:

```markdown
## Question

Summary answer.

## Findings

- **Claim** — source: [link or ref]
- **Claim** — source: [link or ref]
```

### 5. Report

Tell the user:
- Where the file was saved
- The key finding in 1-2 sentences
- Any sub-questions that remain unresolved

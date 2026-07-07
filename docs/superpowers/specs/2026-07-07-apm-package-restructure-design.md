# APM Package Restructure: Sub-package via Dependencies

## Status

Approved design. Awaiting user spec review before implementation.

## Summary

Restructure the agent-package APM project from a monolithic `.apm/` directory to a multi-package layout with `general` and `engineering` sub-packages managed via `dependencies.apm`.

## Current State

```
agent-package/
├── apm.yml                 # name: w, includes: auto
├── .apm/
│   ├── prompts/            # 13 prompt files (all skills mixed)
│   └── skills/             # 19 skill dirs (general + engineering mixed)
│       └── engineering/    # empty directory (orphaned)
├── general/
│   ├── apm.yml             # name: w-general, includes: [skills]
│   └── skills/             # 4 general skills (missing handoff)
└── engineering/
    └── skills/             # 13 engineering skills (no apm.yml)
```

## Target State

```
agent-package/
├── apm.yml                 # name: w, deps: [./general, ./engineering]
├── general/
│   ├── apm.yml             # name: w-general
│   ├── prompts/            # 4 general prompts
│   └── skills/             # 5 general skills (+handoff)
├── engineering/
│   ├── apm.yml             # name: w-engineering, deps: [../general]
│   ├── prompts/            # 9 engineering prompts
│   └── skills/             # 13 engineering skills
└── .apm/                   # emptied
```

## Skills Classification

| Category | Skills | Prompts |
|----------|--------|---------|
| **General** (5) | grill-me, grilling, handoff, teach, writing-great-skills | grill-me, handoff, teach, writing-great-skills |
| **Engineering** (13) | codebase-design, diagnosing-bugs, domain-modeling, grill-with-docs, guide, implement, improve-codebase-architecture, init, prototype, tdd, to-issues, to-prd, triage | guide, grill-with-docs, implement, improve-codebase-architecture, init, prototype, to-issues, to-prd, triage |

## Key Design Decisions

1. **Sub-packages own their content** — each contains `skills/` and `prompts/` dirs, declared via `includes: [skills, prompts]`. No `.apm/` sub-directory inside sub-packages.
2. **Root delegates to sub-packages** — root `apm.yml` removes `includes: auto` and uses `dependencies.apm` with local path references.
3. **engineering depends on general** — `engineering/apm.yml` declares `dependencies.apm: [{path: ../general}]`, enabling engineering skills to reference general primitives.
4. **`.apm/` cleared** — orphaned empty `engineering/` dir removed, all content migrated to sub-packages.

## apm.yml Manifests

### Root (`apm.yml`)

```yaml
name: w
version: 1.0.0
description: APM project for agent-package
author: W
targets:
  - claude
  - codex
  - copilot
  - cursor
  - gemini
  - opencode
  - windsurf
dependencies:
  apm:
    - path: ./general
    - path: ./engineering
  mcp: []
devDependencies:
  apm: []
scripts: {}
```

### General (`general/apm.yml`)

```yaml
name: w-general
version: 1.0.0
description: General skills package
author: W
targets:
  - claude
  - codex
  - copilot
  - cursor
  - gemini
  - opencode
  - windsurf
dependencies:
  apm: []
  mcp: []
includes:
  - skills
  - prompts
scripts: {}
```

### Engineering (`engineering/apm.yml`)

```yaml
name: w-engineering
version: 1.0.0
description: Engineering skills package
author: W
targets:
  - claude
  - codex
  - copilot
  - cursor
  - gemini
  - opencode
  - windsurf
dependencies:
  apm:
    - path: ../general
  mcp: []
includes:
  - skills
  - prompts
scripts: {}
```

## Migration Steps

1. Create `engineering/apm.yml`
2. Update `general/apm.yml` — add `prompts` to includes
3. Copy `handoff` skill from `.apm/skills/` to `general/skills/`
4. Copy general prompts from `.apm/prompts/` to `general/prompts/`
5. Copy engineering prompts from `.apm/prompts/` to `engineering/prompts/`
6. Remove orphaned `.apm/skills/engineering/` empty dir
7. Remove all skills from `.apm/skills/` (now in sub-packages)
8. Remove all prompts from `.apm/prompts/` (now in sub-packages)
9. Update root `apm.yml` — replace `includes: auto` with `dependencies.apm`
10. Test with `apm install` in a temp directory

## Verification

```bash
# In a temp directory:
apm init
apm install <repo-path>
apm compile
# Verify skills and prompts are installed correctly
```

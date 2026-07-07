# APM Package Restructure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Restructure agent-package from monolithic `.apm/` to sub-packages (`general`, `engineering`) managed via `dependencies.apm`.

**Architecture:** Root `apm.yml` depends on `./general` and `./engineering` via local-path `dependencies.apm`. Each sub-package owns its `skills/` and `prompts/` directories. `engineering` depends on `general`.

**Tech Stack:** APM (Agent Package Manager), YAML

## Global Constraints

- All file paths relative to project root `c:\Users\W\Workspace\Personal\agent-package`
- Root `apm.yml` must NOT use `includes: auto`
- Root `apm.yml` must use `dependencies.apm` with local path refs
- `engineering` MUST depend on `../general`
- Empty `.apm/skills/engineering/` directory must be removed
- `handoff` skill must be present in `general/skills/`

---

### Task 1: Create `engineering/apm.yml`

**Files:**
- Create: `engineering/apm.yml`

**Interfaces:**
- Consumes: N/A
- Produces: Engineering package manifest declaring skills, prompts, and dependency on general package

- [ ] **Step 1: Write `engineering/apm.yml`**

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

- [ ] **Step 2: Commit**

```bash
git add engineering/apm.yml
git commit -m "feat: create engineering APM package manifest"
```

---

### Task 2: Update `general/apm.yml` to include prompts

**Files:**
- Modify: `general/apm.yml`

**Interfaces:**
- Consumes: Existing `general/apm.yml`
- Produces: Updated manifest with `prompts` in includes

- [ ] **Step 1: Edit `general/apm.yml`**

Add `prompts` to the includes list:

```
includes:
  - skills
  - prompts
```

- [ ] **Step 2: Commit**

```bash
git add general/apm.yml
git commit -m "feat: add prompts to general package includes"
```

---

### Task 3: Copy `handoff` skill to `general/skills/`

**Files:**
- Create: `general/skills/handoff/SKILL.md`
- Source: `.apm/skills/handoff/SKILL.md`

**Interfaces:**
- Consumes: `.apm/skills/handoff/SKILL.md`
- Produces: `general/skills/handoff/SKILL.md`

- [ ] **Step 1: Create directory and copy the skill**

```bash
mkdir -p general/skills/handoff
Copy-Item ".apm/skills/handoff/SKILL.md" "general/skills/handoff/SKILL.md"
```

Verify:
```bash
ls general/skills/handoff/
# Should show: SKILL.md
```

- [ ] **Step 2: Commit**

```bash
git add general/skills/handoff/
git commit -m "feat: copy handoff skill to general package"
```

---

### Task 4: Copy general prompts to `general/prompts/`

**Files:**
- Create: `general/prompts/grill-me.prompt.md`, `general/prompts/handoff.prompt.md`, `general/prompts/teach.prompt.md`, `general/prompts/writing-great-skills.prompt.md`
- Source: `.apm/prompts/` (corresponding files)

**Interfaces:**
- Consumes: `.apm/prompts/*.prompt.md` (general subset)
- Produces: `general/prompts/*.prompt.md`

- [ ] **Step 1: Create directory and copy general prompts**

```bash
mkdir -p general/prompts
Copy-Item ".apm/prompts/grill-me.prompt.md" "general/prompts/grill-me.prompt.md"
Copy-Item ".apm/prompts/handoff.prompt.md" "general/prompts/handoff.prompt.md"
Copy-Item ".apm/prompts/teach.prompt.md" "general/prompts/teach.prompt.md"
Copy-Item ".apm/prompts/writing-great-skills.prompt.md" "general/prompts/writing-great-skills.prompt.md"
```

Verify:
```bash
ls general/prompts/
# Should show: 4 prompt files
```

- [ ] **Step 2: Commit**

```bash
git add general/prompts/
git commit -m "feat: copy general prompts to general package"
```

---

### Task 5: Copy engineering prompts to `engineering/prompts/`

**Files:**
- Create: `engineering/prompts/guide.prompt.md`, `engineering/prompts/grill-with-docs.prompt.md`, `engineering/prompts/implement.prompt.md`, `engineering/prompts/improve-codebase-architecture.prompt.md`, `engineering/prompts/init.prompt.md`, `engineering/prompts/prototype.prompt.md`, `engineering/prompts/to-issues.prompt.md`, `engineering/prompts/to-prd.prompt.md`, `engineering/prompts/triage.prompt.md`
- Source: `.apm/prompts/` (corresponding files)

- [ ] **Step 1: Create directory and copy engineering prompts**

```bash
mkdir -p engineering/prompts
Copy-Item ".apm/prompts/guide.prompt.md" "engineering/prompts/guide.prompt.md"
Copy-Item ".apm/prompts/grill-with-docs.prompt.md" "engineering/prompts/grill-with-docs.prompt.md"
Copy-Item ".apm/prompts/implement.prompt.md" "engineering/prompts/implement.prompt.md"
Copy-Item ".apm/prompts/improve-codebase-architecture.prompt.md" "engineering/prompts/improve-codebase-architecture.prompt.md"
Copy-Item ".apm/prompts/init.prompt.md" "engineering/prompts/init.prompt.md"
Copy-Item ".apm/prompts/prototype.prompt.md" "engineering/prompts/prototype.prompt.md"
Copy-Item ".apm/prompts/to-issues.prompt.md" "engineering/prompts/to-issues.prompt.md"
Copy-Item ".apm/prompts/to-prd.prompt.md" "engineering/prompts/to-prd.prompt.md"
Copy-Item ".apm/prompts/triage.prompt.md" "engineering/prompts/triage.prompt.md"
```

Verify:
```bash
ls engineering/prompts/
# Should show: 9 prompt files
```

- [ ] **Step 2: Commit**

```bash
git add engineering/prompts/
git commit -m "feat: copy engineering prompts to engineering package"
```

---

### Task 6: Update root `apm.yml`

**Files:**
- Modify: `apm.yml`

**Interfaces:**
- Consumes: Current root `apm.yml`
- Produces: Updated root manifest with dependencies instead of includes

- [ ] **Step 1: Edit `apm.yml`**

Replace the current content with:

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

- [ ] **Step 2: Commit**

```bash
git add apm.yml
git commit -m "refactor: switch root to dependencies.apm instead of includes: auto"
```

---

### Task 7: Clean up `.apm/` directory

**Files:**
- Modify: `.apm/` (remove skills, prompts, empty dirs)

- [ ] **Step 1: Remove all skills from `.apm/skills/`**

```bash
Remove-Item ".apm/skills/codebase-design" -Recurse -Force
Remove-Item ".apm/skills/diagnosing-bugs" -Recurse -Force
Remove-Item ".apm/skills/domain-modeling" -Recurse -Force
Remove-Item ".apm/skills/engineering" -Recurse -Force
Remove-Item ".apm/skills/grill-me" -Recurse -Force
Remove-Item ".apm/skills/grill-with-docs" -Recurse -Force
Remove-Item ".apm/skills/grilling" -Recurse -Force
Remove-Item ".apm/skills/guide" -Recurse -Force
Remove-Item ".apm/skills/handoff" -Recurse -Force
Remove-Item ".apm/skills/implement" -Recurse -Force
Remove-Item ".apm/skills/improve-codebase-architecture" -Recurse -Force
Remove-Item ".apm/skills/init" -Recurse -Force
Remove-Item ".apm/skills/prototype" -Recurse -Force
Remove-Item ".apm/skills/tdd" -Recurse -Force
Remove-Item ".apm/skills/teach" -Recurse -Force
Remove-Item ".apm/skills/to-issues" -Recurse -Force
Remove-Item ".apm/skills/to-prd" -Recurse -Force
Remove-Item ".apm/skills/triage" -Recurse -Force
Remove-Item ".apm/skills/writing-great-skills" -Recurse -Force
```

- [ ] **Step 2: Remove all prompts from `.apm/prompts/`**

```bash
Remove-Item ".apm/prompts/*.prompt.md" -Force
```

- [ ] **Step 3: Clean up empty directories (keep top-level `.apm/`)**

```bash
# skills and prompts dirs are now empty; leave .apm/ itself for future use
```

- [ ] **Step 4: Commit**

```bash
git add -A .apm/
git commit -m "chore: clean up .apm directory after migration to sub-packages"
```

---

### Task 8: Verify with `apm install` in a temp directory

- [ ] **Step 1: Create a temp directory and init APM**

```powershell
$tmpDir = Join-Path $env:TEMP "apm-test-$(Get-Random)"
New-Item -ItemType Directory -Path $tmpDir -Force
Set-Location $tmpDir
apm init
```

Expected: `apm.yml` created in temp dir.

- [ ] **Step 2: Install the local package**

```bash
apm install <path-to-agent-package>
```

Expected: Installs all skills and prompts from general and engineering sub-packages.

- [ ] **Step 3: Compile**

```bash
apm compile
```

Expected: Compilation succeeds. Skills and prompts appear in target AI client configs.

- [ ] **Step 4: Clean up temp directory**

```bash
Set-Location <original-project-path>
Remove-Item $tmpDir -Recurse -Force
```

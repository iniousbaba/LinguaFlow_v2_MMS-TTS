---
name: using-git-worktrees
description: Use when starting feature work that needs isolation from current workspace or before executing implementation plans - creates isolated git worktrees with smart directory selection and safety verification
---

# Using Git Worktrees

## Overview

Git worktrees create isolated workspaces sharing the same repository, allowing work on multiple branches simultaneously without switching.

**Core principle:** "Systematic directory selection + safety verification = reliable isolation."

**Announce at start:** "I'm using the using-git-worktrees skill to set up an isolated workspace."

## Directory Selection Process

Follow this priority order:

### 1. Check Existing Directories

```bash
ls -d .worktrees 2>/dev/null     # Preferred (hidden)
ls -d worktrees 2>/dev/null      # Alternative
```

**If found:** Use that directory. If both exist, `.worktrees` wins.

### 2. Check CLAUDE.md

```bash
grep -i "worktree.*director" CLAUDE.md 2>/dev/null
```

**If preference specified:** Use it without asking.

### 3. Ask User

If no directory exists and no CLAUDE.md preference:

```
No worktree directory found. Where should I create worktrees?

1. .worktrees/ (project-local, hidden)
2. ~/.config/superpowers/worktrees/<project-name>/ (global location)
```

## Safety Verification

**MUST verify directory is ignored before creating a project-local worktree:**

```bash
git check-ignore -q .worktrees 2>/dev/null || git check-ignore -q worktrees 2>/dev/null
```

**If NOT ignored:** Add to `.gitignore` and commit before creating the worktree.

**Why critical:** Prevents accidentally committing worktree contents.

For global directories (`~/.config/superpowers/worktrees`): no `.gitignore` verification needed.

## Creation Steps

```bash
# 1. Detect project name
project=$(basename "$(git rev-parse --show-toplevel)")

# 2. Create worktree with new branch
git worktree add .worktrees/$BRANCH_NAME -b $BRANCH_NAME
cd .worktrees/$BRANCH_NAME

# 3. Run project setup (auto-detect)
if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
if [ -f pyproject.toml ]; then poetry install; fi

# 4. Verify clean baseline
pytest  # For LinguaFlow
```

**If tests fail:** Report failures, ask whether to proceed or investigate.
**If tests pass:** Report ready.

## Quick Reference

| Situation | Action |
|-----------|--------|
| `.worktrees/` exists | Use it (verify ignored) |
| `worktrees/` exists | Use it (verify ignored) |
| Both exist | Use `.worktrees/` |
| Neither exists | Check CLAUDE.md → Ask user |
| Directory not ignored | Add to .gitignore + commit |
| Tests fail during baseline | Report failures + ask |

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Skipping ignore verification | Always use `git check-ignore` first |
| Assuming directory location | Follow priority: existing > CLAUDE.md > ask |
| Proceeding with failing tests | Report failures, get explicit permission |

## Integration

**Called by:**
- `subagent-driven-development` — REQUIRED before any tasks
- `executing-plans` — REQUIRED before any tasks
- `brainstorming` — after design approval

**Pairs with:**
- `finishing-a-development-branch` — REQUIRED for cleanup after work complete

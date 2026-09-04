---
name: finishing-a-development-branch
description: Use when implementation is complete, all tests pass, and you need to decide how to integrate the work - guides completion of development work by presenting structured options for merge, PR, or cleanup
---

# Finishing a Development Branch

## Overview

Guides completion of development work by presenting clear options and handling the chosen workflow.

**Core principle:** Verify tests → Present options → Execute choice → Clean up.

**Announce at start:** "I'm using the finishing-a-development-branch skill to complete this work."

## When to Use

- After all tasks in a plan are complete
- Called by `subagent-driven-development` upon task completion
- Called by `executing-plans` upon task completion

## The Process

### Step 1: Verify Tests

Run the project's test suite before proceeding:

```bash
pytest  # Python/Flask projects like LinguaFlow
```

If tests fail → display failure details and halt. Do not proceed to Step 2 with failing tests.

### Step 2: Determine Base Branch

Identify the branch to merge into (typically `main` or `master`):

```bash
git log --oneline -5
git branch
```

### Step 3: Present Options

Present exactly four choices to the user:

```
1. Merge locally into <base-branch>
2. Push and create PR
3. Keep as-is (branch stays, no merge)
4. Discard work (delete branch and worktree)
```

### Step 4: Execute Choice

**Option 1 — Merge locally:**
```bash
git checkout <base-branch>
git merge <feature-branch>
```

**Option 2 — Push and create PR:**
```bash
git push -u origin <feature-branch>
gh pr create --title "..." --body "..."
```

**Option 3 — Keep as-is:**
No git actions. Report branch location.

**Option 4 — Discard:**
Require typed confirmation: user must type `discard` before proceeding.
```bash
git worktree remove <path>
git branch -d <feature-branch>
```

### Step 5: Cleanup Worktree

For Options 1, 2, and 4: remove the worktree directory.

```bash
git worktree remove <worktree-path>
```

## Key Requirements

- **Never proceed with failing tests**
- **Always verify tests before offering options**
- **Require typed "discard" confirmation** before permanent deletion

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Offering options before tests pass | Run tests first, always |
| Deleting without confirmation | Require "discard" typed explicitly |
| Forgetting worktree cleanup | Always clean up after merge/discard |

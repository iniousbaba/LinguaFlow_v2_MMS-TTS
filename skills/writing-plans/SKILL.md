---
name: writing-plans
description: Use when creating implementation plans for multi-step development tasks - produces detailed, bite-sized task breakdowns ready for execution
---

# Writing Plans

## Overview

Generate comprehensive, bite-sized task breakdowns for implementation. Plans assume solid technical skills but minimal domain knowledge about this specific codebase.

**Announce at start:** "I'm using the writing-plans skill to create the implementation plan."

**Output location:** `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md`

## When to Use

- After `brainstorming` approves a design
- Before starting any multi-step implementation
- When a task has 3+ distinct steps

## Plan Structure

### 1. File Mapping

Show which files are responsible for what. Map boundaries clearly.

### 2. Task List

Each task must be decomposed into 2–5 minute atomic steps:
- Write failing test
- Run it (confirm it fails)
- Implement
- Run it again (confirm it passes)
- Commit

### 3. Requirements Per Step

- **Complete code** — no placeholders like "TBD" or "add validation here"
- **Exact file paths** — `utils/translate.py:45`, not "the translate file"
- **Exact commands** with expected outputs
- **Expected test output** at each verification point

## Critical Standards

**No Placeholders:** Every code step requires actual implementation. References to undefined types or functions are plan failures.

**Task Granularity:** Each step performs one atomic action. "Write failing test" and "run it" are separate steps.

**Consistency Checks:** Verify method names, types, and signatures align across tasks. Type mismatches between tasks indicate errors — fix them inline.

**Self-Review:** After drafting, scan the entire plan for:
- Coverage gaps (missing error cases)
- Placeholder red flags (TBD, TODO, ...)
- Inconsistencies between tasks

Fix inline. Do not re-review from scratch.

## Handoff Pattern

Upon completion, present two execution choices:

```
1. Subagent-Driven (recommended): Fresh subagent per task
   → invoke subagent-driven-development

2. Inline Execution: Batch execution with checkpoints
   → invoke executing-plans
```

## Principles

- DRY (Don't Repeat Yourself)
- YAGNI (You Aren't Gonna Need It)
- TDD (test before implementation)
- Frequent commits (enable rollback and progress tracking)

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Vague steps ("implement the feature") | Break into atomic 2-min actions |
| Placeholder code | Write actual implementation |
| Missing file paths | Exact paths for every file touched |
| Skipping test steps | TDD: test step before every implementation step |
| No self-review | Always scan plan before handing off |

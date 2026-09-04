---
name: executing-plans
description: Use when implementing a written plan - guides step-by-step execution with safety checkpoints and completion verification
---

# Executing Plans

## Overview

Implement written plans faithfully through a structured three-step process with mandatory safety checkpoints.

**Core principle:** Follow the plan exactly. Stop at blockers rather than improvising past them.

**REQUIRED BACKGROUND:** This skill depends on `using-git-worktrees` (for workspace isolation) and `finishing-a-development-branch` (for completion). Use `subagent-driven-development` when available for higher quality output.

## When to Use

- Executing a plan written by `writing-plans`
- Following a multi-step implementation guide
- Any task where a plan document exists

**Important:** Never start implementation on main/master branch without explicit user consent.

## The Three-Step Process

### Step 1: Load and Review

- Read the plan completely before starting
- Identify any concerns, ambiguities, or missing information
- Raise issues with the user **before** starting work
- Set up isolated workspace using `using-git-worktrees`

### Step 2: Execute Tasks

For each task in the plan:
1. Mark task as `in_progress`
2. Follow the step exactly as written
3. Run the specified verification command
4. Confirm output matches expected result
5. Mark task as `completed`
6. Commit progress

**Do not improvise.** If a step is unclear, stop and ask.

### Step 3: Complete Development

Use `finishing-a-development-branch` to:
- Verify all tests pass
- Present merge/PR/cleanup options

## Safety Checkpoints — STOP Immediately If:

- Hitting a dependency that wasn't in the plan
- Tests fail unexpectedly
- Instructions are unclear or contradictory
- Verification fails 3+ times in a row

Do not work around these. Raise them with the user.

## Integration

| Skill | When to invoke |
|-------|---------------|
| `using-git-worktrees` | REQUIRED — before executing any tasks |
| `subagent-driven-development` | RECOMMENDED — for higher quality execution |
| `finishing-a-development-branch` | REQUIRED — upon completion |
| `requesting-code-review` | After each batch of 3 tasks |

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Working on main branch | Set up worktree first |
| Improvising around a blocker | Stop and ask the user |
| Skipping verification steps | Run every verification listed in the plan |
| Continuing with failing tests | Stop and raise the issue |

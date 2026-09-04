---
name: subagent-driven-development
description: Use when executing implementation plans with independent tasks in the current session
---

# Subagent-Driven Development

## Overview

Execute implementation plans by dispatching fresh subagents per task with two-stage review (spec compliance, then code quality) after each.

**Core principle:** "Fresh subagent per task + two-stage review (spec then quality) = high quality, fast iteration."

Subagents receive isolated context rather than inheriting session history, preserving the controller's capacity for coordination.

## When to Use

- You have an implementation plan with mostly independent tasks
- You need to stay in the current session (vs. parallel sessions)
- You want automatic review checkpoints built in

## Implementation Process

1. Extract all tasks with complete text and context
2. Create a TodoWrite tracking document
3. For each task:
   - Dispatch implementer subagent
   - Handle status: `DONE`, `DONE_WITH_CONCERNS`, `NEEDS_CONTEXT`, or `BLOCKED`
   - Run spec compliance review
   - Run code quality review
   - Fix issues → re-review until approved
4. After all tasks: dispatch final code reviewer
5. Complete using `finishing-a-development-branch`

## Model Selection Strategy

Use the least powerful model that can handle each role:
- Mechanical tasks → cheaper models
- Integration tasks → standard models
- Architecture/design → most capable models

## Critical Rules

- **Never skip reviews**
- **Never proceed with unfixed issues from spec compliance**
- **Never start code quality review before spec compliance passes**
- **Answer subagent questions before implementation begins**
- **No manual fixes** — when reviewers find issues, the implementer fixes them

## Subagent Status Handling

| Status | Action |
|--------|--------|
| `DONE` | Proceed to spec review |
| `DONE_WITH_CONCERNS` | Note concerns, proceed to spec review |
| `NEEDS_CONTEXT` | Provide context, re-dispatch |
| `BLOCKED` | Raise with user before continuing |

## Advantages

**Over manual execution:**
- Subagents follow TDD naturally
- Fresh context prevents confusion
- Questions surface upfront

**Over parallel sessions:**
- Same session continuity
- Automatic review checkpoints
- Continuous progress without handoffs

## Integration

| Skill | When |
|-------|------|
| `using-git-worktrees` | REQUIRED — before executing any tasks |
| `requesting-code-review` | After each task |
| `finishing-a-development-branch` | REQUIRED — upon completion |

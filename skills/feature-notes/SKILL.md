---
name: feature-notes
description: Use when starting any feature, bugfix, or refactor to create a notes file that preserves context across session interruptions and handoffs
---

# Feature Notes

## Overview

Create and maintain a markdown notes file for every feature you work on. Notes act as your external memory — if the session is interrupted, you can resume without losing context.

**Core principle:** The notes file is your working memory. Keep it current as you work, not as a retrospective summary.

## When to Use

- At the start of every feature, bugfix, or refactor
- When resuming work after an interruption
- When a task will span multiple sessions

## Notes File Location

```
notes/features/<feature-name>.md
```

Use the same name as the feature branch. If the branch is `feature/add-igbo-tts`, the notes file is `notes/features/add-igbo-tts.md`.

## What to Put in Notes

```markdown
# <Feature Name>

## Goal
One sentence: what does this change accomplish?

## Clarifications
Answers to any questions asked before starting.

## Decisions Made
- Why approach A was chosen over approach B
- Any constraints discovered during implementation

## Current Status
What's done, what's in progress, what's next.

## Blockers
Anything that stopped progress, with context.

## Files Changed
List of files touched and why.
```

## Rules

- **Update as you go** — not at the end. Notes written after the fact are incomplete.
- **Record decisions, not steps** — the git log records steps; notes record *why*.
- **One file per feature** — don't combine multiple features in one notes file.
- **Don't delete** — leave old notes in place; they become a development log.
- Notes files are yours to edit freely — add, rearrange, delete sections as needed.

## Resuming After Interruption

When starting a new session on an existing feature:
1. Read the notes file first
2. Check git log for what was committed
3. Run tests to confirm current state
4. Update "Current Status" before continuing

## LinguaFlow Note

Add `notes/` to `.gitignore` if you don't want notes committed, or commit them if you want a development log in the repo history.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Writing notes after implementation | Notes during, not after |
| Putting implementation details in notes | Put decisions, not code |
| Forgetting to update status | Update status before ending a session |
| One notes file for multiple features | One file per feature/branch |

---
name: brainstorming
description: Use when starting any new feature, design decision, or implementation approach - requires turning ideas into fully formed designs before any implementation begins
---

# Brainstorming

## Overview

Turn ideas into fully formed designs before implementation begins.

**Core principle:** Do NOT invoke any implementation skill, write any code, scaffold any project, or take any implementation action until you have presented a design and the user has approved it. This applies universally, even to seemingly simple projects.

**Announce at start:** "I'm using the brainstorming skill to design this before we implement it."

## When to Use

- Starting any new feature (e.g. adding a new language, new translation backend)
- Making architectural decisions
- When requirements are unclear
- Before writing any implementation plan

## The Nine-Step Process

1. Explore project context — review relevant files and docs
2. Offer visual companion if needed (separate message only)
3. Ask clarifying questions one at a time
4. Propose 2–3 approaches with trade-offs
5. Present design sections with approval checkpoints
6. Write design documentation to `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md`
7. Self-review spec for placeholders, contradictions, and ambiguities
8. Request user review of the written spec
9. Invoke `writing-plans` skill (only acceptable next step post-brainstorming)

## Question Strategy

- Ask **one question per message**
- Prefer multiple-choice formats
- Focus on: purpose, constraints, and success criteria
- Never batch multiple questions

## Design Principles

- Break systems into isolated units with single purposes and well-defined interfaces
- Avoid unrelated refactoring — stay focused on current goals
- Specs should scale in complexity: brief for simple projects, up to 300 words per nuanced section
- Address: architecture, components, data flow, error handling, testing

## Hard Gate

```
NEVER proceed to implementation until:
  1. Design is written to docs/superpowers/specs/
  2. User has explicitly approved it
```

"Simple" projects are not exempt. Simple projects often harbor unexamined assumptions that cause wasted effort.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Jumping to code before design | Stop. Run brainstorming first. |
| Asking multiple questions at once | One question per message. |
| Skipping spec for "simple" tasks | All tasks need a design. |
| Writing implementation plan before user approves spec | Spec approval first. |

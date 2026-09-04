---
name: using-superpowers
description: Use this skill at the start of every task to determine which other skills apply - if there is even a 1% chance a skill might apply, you MUST invoke it
---

# Using Superpowers

## Overview

Skills override default behavior. Check for applicable skills before taking any action.

**Core principle:** "If you think there is even a 1% chance a skill might apply to what you are doing, you ABSOLUTELY MUST invoke the skill."

This is non-negotiable. It is not optional.

## Instruction Hierarchy

1. **User's explicit instructions** (highest priority)
2. **Superpowers skills** (override default behavior)
3. **Default system prompt** (lowest priority)

## Invocation Protocol

Skills must be invoked **before** any response or action — even before clarifying questions.

In Claude Code, use the `Skill` tool.

## Skill Priority When Multiple Apply

- **Process skills** (brainstorming, debugging) take precedence over implementation skills
- **Rigid skills** require exact adherence
- **Flexible skills** allow contextual adaptation

## Red Flags — You Are Rationalizing

Stop and invoke the relevant skill if you think:

- "This is just a simple question"
- "I need more context first"
- "I'll just do this one thing first"
- "The skill doesn't quite apply here"
- "I know this one without the skill"
- "This is too small to need a skill"
- "I'll check after I start"
- "The user didn't ask for the skill"
- "It would slow things down"
- "The skill is for other cases"
- "I'm already halfway through"
- "This is obvious"

**All of these mean: Invoke the skill. Now.**

## Quick Reference — Which Skill to Use

| Situation | Skill |
|-----------|-------|
| Starting any new feature or design | `brainstorming` |
| Any bug, failure, or unexpected behavior | `systematic-debugging` |
| Writing any feature or bugfix | `test-driven-development` |
| Following a written plan | `executing-plans` |
| Claiming work is complete | `verification-before-completion` |
| Creating a new plan | `writing-plans` |
| Starting feature branch work | `using-git-worktrees` |
| 2+ independent tasks | `dispatching-parallel-agents` |
| Tasks in current session | `subagent-driven-development` |
| Implementation complete | `finishing-a-development-branch` |
| Receiving review feedback | `receiving-code-review` |
| Before merging | `requesting-code-review` |
| Creating or editing a skill | `writing-skills` |

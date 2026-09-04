---
name: writing-skills
description: Use when creating new skills, editing existing skills, or verifying skills work before deployment
---

# Writing Skills

## Overview

Writing skills IS Test-Driven Development applied to process documentation.

**Core principle:** If you didn't watch an agent fail without the skill, you don't know if the skill teaches the right thing.

**REQUIRED BACKGROUND:** You MUST understand `test-driven-development` before using this skill. This skill adapts TDD to documentation.

## What is a Skill?

A **skill** is a reference guide for proven techniques, patterns, or tools. Skills help future Claude instances find and apply effective approaches.

**Skills are:** Reusable techniques, patterns, tools, reference guides

**Skills are NOT:** Narratives about how you solved a problem once, or project-specific conventions (put those in CLAUDE.md)

## TDD Mapping for Skills

| TDD Concept | Skill Creation |
|-------------|----------------|
| Test case | Pressure scenario with subagent |
| Production code | Skill document (SKILL.md) |
| Test fails (RED) | Agent violates rule without skill (baseline) |
| Test passes (GREEN) | Agent complies with skill present |
| Refactor | Close loopholes while maintaining compliance |

## The Iron Law

```
NO SKILL WITHOUT A FAILING TEST FIRST
```

Applies to NEW skills AND edits to existing skills. No exceptions — not for "simple additions," not for "just adding a section."

**Write skill before testing?** Delete it. Start over.

## SKILL.md Format

```yaml
---
name: skill-name-with-hyphens
description: Use when [specific triggering conditions and symptoms]
---
```

**Description rules:**
- Start with "Use when..."
- Describe triggering conditions ONLY — never summarize the skill's workflow
- Third person
- Max ~500 characters

**Why no workflow in description:** When descriptions summarize workflow, Claude follows the description instead of reading the full skill. The skill body becomes documentation Claude skips.

## Directory Structure

```
skills/
  skill-name/
    SKILL.md              # Main reference (required)
    supporting-file.*     # Only if needed (100+ lines of reference)
```

Flat namespace — all skills in one searchable directory.

## SKILL.md Structure

```markdown
---
name: skill-name
description: Use when [triggering conditions]
---

# Skill Name

## Overview
Core principle in 1-2 sentences.

## When to Use
Bullet list with symptoms and use cases. When NOT to use.

## Core Pattern
Step-by-step or before/after.

## Quick Reference
Table or bullets for scanning.

## Common Mistakes
What goes wrong + fixes.
```

## Token Efficiency

- Getting-started/frequently-loaded skills: <200 words
- Other skills: <500 words
- Move heavy reference (100+ lines) to separate files
- Use cross-references instead of repeating content

## RED-GREEN-REFACTOR for Skills

### RED: Baseline
Run pressure scenario WITHOUT the skill. Document exact rationalizations agents use.

### GREEN: Minimal Skill
Write skill addressing those specific rationalizations. Run same scenarios WITH skill — agents must now comply.

### REFACTOR: Close Loopholes
Agent found new rationalization? Add explicit counter. Re-test until bulletproof.

## When to Create a Skill

**Create when:**
- Technique wasn't intuitively obvious
- Pattern applies broadly across projects
- Others would benefit

**Don't create for:**
- One-off solutions
- Standard practices well-documented elsewhere
- Project-specific conventions → put in CLAUDE.md

## Deployment Checklist (Required for Each Skill)

**RED Phase:**
- [ ] Pressure scenarios created
- [ ] Baseline behavior documented without the skill

**GREEN Phase:**
- [ ] Name: letters, numbers, hyphens only
- [ ] YAML frontmatter with `name` and `description`
- [ ] Description starts with "Use when..." — no workflow summary
- [ ] Agent now complies with skill present

**REFACTOR Phase:**
- [ ] New rationalizations addressed
- [ ] Rationalization table added (for discipline skills)
- [ ] Re-tested until bulletproof

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Description summarizes workflow | Triggering conditions only |
| Skill without baseline test | Run RED phase first |
| Deploying multiple skills without testing each | Test each before moving to next |
| Narrative storytelling | Reference guide format, not story |
| Over-long skill | Target <500 words; move reference to separate files |

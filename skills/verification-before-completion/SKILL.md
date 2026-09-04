---
name: verification-before-completion
description: Use when about to claim work is complete, fixed, or passing, before committing or creating PRs - requires running verification commands and confirming output before making any success claims; evidence before assertions always
---

# Verification Before Completion

## Overview

Claiming completion without verification is dishonesty, not efficiency.

**Core principle:** Evidence before claims, always.

## The Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

Unrun verification commands cannot support success claims. Circumventing the letter of this rule violates its spirit.

## The Gate Function

Execute these five steps before any status assertion:

1. **Identify** the verification command
2. **Execute** the complete command freshly (not from memory)
3. **Review** full output and exit codes
4. **Confirm** output substantiates the claim
5. **Only then** communicate the result

Skipping steps = lying, not verifying.

## What Counts as Verification

| Claim | Required verification |
|-------|----------------------|
| "Tests passing" | Run full test suite, read output |
| "Linter clean" | Run linter, check exit code |
| "Build succeeds" | Run build command, confirm 0 exit |
| "Bug fixed" | Run regression test that reproduces bug |
| "Feature complete" | Run against requirements checklist |
| "Agent completed task" | Read agent's output, verify artifacts exist |

## Red Flags

Stop and verify before claiming if you notice:
- Speculative language: "should", "probably", "I think"
- Premature satisfaction ("looks good!")
- Pre-verification commits
- Trusting agent reports without checking
- Partial verification ("the unit tests pass" when integration tests exist)

## Common Rationalizations — All Invalid

| Excuse | Reality |
|--------|---------|
| "I'm confident" | Confidence ≠ evidence |
| "I ran it earlier" | Earlier ≠ now. Run it fresh. |
| "Linter passed" | Linter ≠ compiler ≠ tests |
| "I'm tired" | Fatigue doesn't change requirements |

## When To Apply

- Before any "done", "fixed", "passing", "complete", or "working" claim
- Before commits
- Before PRs
- Before task transitions
- Before reporting success to the user

## The Bottom Line

Execute → Read → Then assert.

No shortcuts. No exceptions.

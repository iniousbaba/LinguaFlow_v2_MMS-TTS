---
name: test-driven-development
description: Use when implementing any feature or bugfix, before writing implementation code
---

# Test-Driven Development

## Overview

Write the test first. Watch it fail. Write minimal code to pass.

**Core principle:** "If you didn't watch the test fail, you don't know if it tests the right thing."

## The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Code written before tests must be **deleted entirely** and rewritten from test specifications.

## When to Use

Apply consistently for:
- New features
- Bug fixes
- Refactoring
- Behavior changes

**Exceptions** (require explicit approval):
- Throwaway prototypes
- Generated code
- Configuration files

## Red-Green-Refactor Cycle

### RED — Write a Failing Test

- Write a minimal test demonstrating desired behavior
- Use real code rather than mocks when possible
- Run it — it must fail before you write any implementation

### GREEN — Write Minimal Implementation

- Implement only the simplest code to pass the test
- No over-engineering
- No features beyond test requirements

### REFACTOR — Clean Up

- After tests pass, clean up code
- Remove duplication, improve clarity
- All tests must continue to pass

## Test Quality Standards

Good tests:
- One behavior per test
- Clear naming that describes functionality
- Use real code rather than mock-dependent tests

## Why Order Matters

| Objection | Reality |
|-----------|---------|
| "Tests after work the same" | Tests after pass immediately — prove nothing |
| "I manually tested it" | Manual testing can't replace automated systematic verification |
| "It's too simple to test" | Simple code breaks. Test takes 30 seconds. |
| "I'll test later" | Tests-later = "what does this do?". Tests-first = "what should this do?" |

## Red Flags — Delete Code and Start Over

- Code written before tests
- Tests pass immediately without any thought
- "I already manually tested it"
- "Tests after achieve the same purpose"
- "It's about spirit not ritual"
- Any variation of "I'll test later"

**All of these mean: Delete the code. Start over with TDD.**

## Bug Fix Integration

For bugs: create a failing test that **reproduces** the bug before implementing the fix. This ensures both resolution and future regression prevention.

## Verification Checklist

Before claiming completion:
- [ ] Every function/behavior has a test
- [ ] Each test was observed failing first
- [ ] Minimal code was written to pass
- [ ] All tests pass with clean output
- [ ] Real code usage (not just mocks)

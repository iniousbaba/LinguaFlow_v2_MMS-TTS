---
name: systematic-debugging
description: Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes
---

# Systematic Debugging

## Overview

Random fixes waste time and create new bugs.

**Core principle:** ALWAYS find root cause before attempting fixes. Symptom fixes are failure.

**ABSOLUTE RULE:** NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST.

## When to Use

Apply to any technical issue including:
- Test failures
- Production bugs
- Unexpected behavior
- Performance problems
- Build failures
- Integration issues

**Especially when:** under time pressure, when a "quick fix" seems obvious, after multiple failed fix attempts, or when lacking full understanding.

## Four Mandatory Phases

### Phase 1: Root Cause Investigation

- Read error messages **completely**, including full stack traces
- Reproduce the issue consistently before proceeding
- Review recent changes via git history
- For multi-component systems (like LinguaFlow's audio pipeline): add diagnostic instrumentation at each component boundary
- Trace data flow backward through the call stack to find the origin

### Phase 2: Pattern Analysis

- Locate similar **working** code in the same codebase
- Read reference implementations completely
- List every difference between working and broken implementations
- Understand all dependencies and assumptions

### Phase 3: Hypothesis and Testing

- Form a **specific, written** hypothesis about the root cause
- Make the smallest possible change to test it
- Test **one variable at a time**
- When unsuccessful, form a new hypothesis rather than adding fixes

### Phase 4: Implementation

- Create a **failing test case** before fixing
- Implement a **single fix** addressing the root cause
- Verify the fix resolves the issue
- If 3+ fixes fail, stop and question the architecture

## Red Flags — Return to Phase 1

Stop and restart investigation if you:
- Propose a solution before understanding the issue
- Assume without verification
- Make multiple simultaneous changes
- Attempt fixes without investigation
- Find yourself saying "one more fix"

## Common Rationalizations — All Wrong

| Excuse | Reality |
|--------|---------|
| "The issue is simple" | Simple issues still have root causes |
| "There's no time" | Systematic debugging is actually faster |
| "One more fix attempt" | You're in a fix spiral — stop |
| "I know what this is" | Verify before touching anything |

## Real-World Results

- Systematic: 15–30 minute resolution, 95% first-time fix rate
- Random fixes: 2–3 hours, 40% first-time fix rate

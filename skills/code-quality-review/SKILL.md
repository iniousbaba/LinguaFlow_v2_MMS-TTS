---
name: code-quality-review
description: Use when completing a module, class, or feature implementation to assess quality before moving on - evaluates complexity, maintainability, test coverage, and documentation, then produces actionable improvement suggestions
---

# Code Quality Review

## Overview

Systematic self-assessment of code across four dimensions before marking work as done. Catches quality issues early, when they are cheap to fix.

**Core principle:** A passing test suite proves correctness, not quality. Run this after tests pass.

## When to Use

- After implementing a new module or class (e.g. a new translation backend in `utils/translate.py`)
- Before requesting code review
- After a major refactor
- When code feels "done but not quite right"

## The Four Dimensions

### 1. Complexity

- Are functions doing one thing only?
- Is cyclomatic complexity low? (branches, loops, conditions)
- Can any function be split into smaller named pieces?
- Are there nested conditionals that can be flattened?

**LinguaFlow hotspots:** `app.py:process_audio`, `listener.py:recognize_speech`, `translate.py` fallback chains

### 2. Maintainability

- Would another developer understand this without asking you?
- Are names descriptive? (`webm_to_wav` ✓, `process` ✗)
- Is there duplicated logic that should be extracted?
- Are magic values named as constants?
- Does the code follow existing patterns in the codebase?

### 3. Test Coverage

- Does every public function have at least one test?
- Are error paths tested (API failures, bad audio input, unsupported language)?
- Are edge cases covered (empty audio, unknown language code, network timeout)?
- Does each test test one behavior?

**LinguaFlow critical paths to test:**
- `LinguaFlowTranslate`: fallback chain (deep_translator → googletrans → google-cloud)
- `webm_to_wav()`: invalid/corrupt audio input
- `LinguaFlowSpeechRecognition`: each supported language code
- Flask routes: missing fields, wrong content type

### 4. Documentation

- Are non-obvious decisions explained with a comment (not what, but why)?
- Are external API behaviors documented where they're called?
- Is the function signature self-documenting via argument names?

## Process

```
1. Open the file(s) you just modified
2. Score each dimension: ✓ Good / ⚠ Needs work / ✗ Must fix
3. List specific line numbers for every ⚠ and ✗
4. Fix all ✗ items before claiming done
5. Schedule ⚠ items as follow-up tasks
6. Re-run tests after any changes
```

## Output Format

```
File: utils/translate.py

Complexity:    ⚠  translate() has 4 nested conditions (lines 45-67) — extract fallback logic
Maintainability: ✓
Test Coverage: ✗  No test for network timeout on googletrans fallback (line 58)
               ✗  No test for empty string input
Documentation: ✓

Actions:
  MUST FIX: Add test for network timeout fallback
  MUST FIX: Add test for empty string input
  TODO: Extract fallback chain to _translate_with_fallback()
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Skipping coverage dimension because "it's internal" | Every function reachable from a route needs a test |
| Marking ⚠ items as done without tracking them | Add as a TODO item before closing the session |
| Running review on untested code | Tests first, quality review second |
| Reviewing for style instead of substance | Focus on the four dimensions only |

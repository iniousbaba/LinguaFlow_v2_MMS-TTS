---
name: dispatching-parallel-agents
description: Use when facing 2+ independent tasks that can be worked on without shared state or sequential dependencies
---

# Dispatching Parallel Agents

## Overview

You delegate tasks to specialized agents with isolated context. By precisely crafting their instructions and context, you ensure they stay focused and succeed at their task. They should never inherit your session's context or history — you construct exactly what they need. This also preserves your own context for coordination work.

When you have multiple unrelated failures (different test files, different subsystems, different bugs), investigating them sequentially wastes time. Each investigation is independent and can happen in parallel.

**Core principle:** "Dispatch one agent per independent problem domain. Let them work concurrently."

## When to Use

**Use when:**
- 3+ test files failing with different root causes
- Multiple subsystems broken independently
- Each problem can be understood without context from others
- No shared state between investigations

**Don't use when:**
- Failures are related (fix one might fix others)
- Need to understand full system state
- Agents would interfere with each other

## The Pattern

### 1. Identify Independent Domains

Group failures by what's broken — each domain is independent, meaning resolving one issue doesn't affect others.

### 2. Create Focused Agent Tasks

Each agent receives:
- **Specific scope:** One test file or subsystem
- **Clear goal:** Make these tests pass
- **Constraints:** Don't change other code
- **Expected output:** Summary of what you found and fixed

### 3. Dispatch in Parallel

Multiple tasks run concurrently rather than sequentially.

### 4. Review and Integrate

When agents return: read each summary, verify fixes don't conflict, run full test suite, integrate all changes.

## Agent Prompt Structure

Good agent prompts are:
1. **Focused** — One clear problem domain
2. **Self-contained** — All context needed to understand the problem
3. **Specific about output** — What should the agent return?

## Quick Reference

| Scenario | Action |
|----------|--------|
| 3 test files with different errors | 3 agents in parallel |
| 2 subsystems broken independently | 2 agents in parallel |
| Failures share a root cause | Single investigation |
| Need full system context | Sequential, not parallel |

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Too broad scope | Specific, focused scope |
| Missing context | Include error messages and relevant code |
| No constraints | Set clear boundaries for each agent |
| Vague outputs | Specify exactly what summary to return |

## Real Example

6 test failures across 3 files → divide among 3 agents working in parallel → zero conflicts → all tests passing.

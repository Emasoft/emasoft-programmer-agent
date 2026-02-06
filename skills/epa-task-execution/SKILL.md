---
name: epa-task-execution
description: Execute programming tasks per requirements. Use when implementing assigned tasks.
license: MIT
compatibility: Requires SERENA MCP activated.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: epa-programmer-main-agent
user-invocable: false
workflow-instruction: "Step 17 - Task Execution"
procedure: "proc-execute-task"
---

# EPA Task Execution Skill

Execute programming tasks according to requirements and acceptance criteria received from the orchestrator.

## Purpose

This skill provides the complete workflow for receiving, understanding, implementing, testing, and validating programming tasks. It ensures all acceptance criteria are met before marking a task as complete.

## When to Use

Use this skill when:
- You receive a task assignment via AI Maestro message
- You need to implement code changes according to specifications
- You must validate your implementation against acceptance criteria

## Prerequisites

Before using this skill:
1. SERENA MCP must be activated for code navigation
2. Development environment must be configured for the target project
3. You must have received a valid task assignment with requirements

## Task Execution Workflow

The task execution process follows these ordered steps:

### Step 1: Receive Task Assignment
Parse and validate the incoming task from AI Maestro.
See: [op-receive-task-assignment.md](references/op-receive-task-assignment.md)
- 1.1 Read incoming AI Maestro message
- 1.2 Extract task identifier and metadata
- 1.3 Validate message format and required fields
- 1.4 Acknowledge receipt to orchestrator

### Step 2: Parse Task Requirements
Understand what needs to be implemented.
See: [op-parse-task-requirements.md](references/op-parse-task-requirements.md)
- 2.1 Extract acceptance criteria list
- 2.2 Identify dependencies on other tasks
- 2.3 Determine target files and components
- 2.4 Clarify ambiguities with orchestrator if needed

### Step 3: Setup Development Environment
Configure tooling for the specific task.
See: [op-setup-development-environment.md](references/op-setup-development-environment.md)
- 3.1 Navigate to target project directory
- 3.2 Activate required virtual environment
- 3.3 Verify dependencies are installed
- 3.4 Initialize SERENA MCP for code navigation

### Step 4: Implement Code
Write the code following requirements.
See: [op-implement-code.md](references/op-implement-code.md)
- 4.1 Analyze existing code structure with SERENA
- 4.2 Plan implementation approach
- 4.3 Write code in small, testable increments
- 4.4 Add documentation and comments

### Step 5: Write Tests
Create tests for the implementation.
See: [op-write-tests.md](references/op-write-tests.md)
- 5.1 Identify test scenarios from requirements
- 5.2 Write unit tests for new functions
- 5.3 Write integration tests if applicable
- 5.4 Run tests and fix failures

### Step 6: Validate Acceptance Criteria
Verify all criteria are met before completion.
See: [op-validate-acceptance-criteria.md](references/op-validate-acceptance-criteria.md)
- 6.1 Review each acceptance criterion
- 6.2 Verify implementation satisfies criterion
- 6.3 Document validation evidence
- 6.4 Report completion to orchestrator

## Master Checklist

Use this checklist to track task execution progress:

- [ ] Task assignment received and acknowledged
- [ ] Requirements parsed and understood
- [ ] Development environment ready
- [ ] Code implementation complete
- [ ] Tests written and passing
- [ ] All acceptance criteria validated
- [ ] Completion reported to orchestrator

## Error Handling

If any step fails:
1. Document the failure reason
2. Report the blocker to orchestrator via AI Maestro
3. Wait for guidance before proceeding
4. Do not mark task complete with failing criteria

## Related Skills

- [epa-orchestrator-communication](../epa-orchestrator-communication/SKILL.md) - For messaging the orchestrator
- [epa-handoff-management](../epa-handoff-management/SKILL.md) - For task handoffs
- [epa-github-operations](../epa-github-operations/SKILL.md) - For committing and PR operations

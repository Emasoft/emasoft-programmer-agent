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

**Reference**: [op-receive-task-assignment.md](references/op-receive-task-assignment.md)

**Contents**:
- 1.1 Read Incoming AI Maestro Message
- 1.2 Extract Task Identifier and Metadata
- 1.3 Validate Message Format and Required Fields
- 1.4 Acknowledge Receipt to Orchestrator

### Step 2: Parse Task Requirements
Understand what needs to be implemented.

**Reference**: [op-parse-task-requirements.md](references/op-parse-task-requirements.md)

**Contents**:
- 2.1 Extract Acceptance Criteria List
- 2.2 Identify Dependencies on Other Tasks
- 2.3 Determine Target Files and Components
- 2.4 Clarify Ambiguities with Orchestrator

### Step 3: Setup Development Environment
Configure tooling for the specific task.

**Reference**: [op-setup-development-environment.md](references/op-setup-development-environment.md)

**Contents**:
- 3.1 Navigate to Target Project Directory
- 3.2 Activate Required Virtual Environment
- 3.3 Verify Dependencies Are Installed
- 3.4 Initialize SERENA MCP for Code Navigation

### Step 4: Implement Code
Write the code following requirements.

**Reference**: [op-implement-code.md](references/op-implement-code.md)

**Contents**:
- 4.1 Analyze Existing Code Structure with SERENA
- 4.2 Plan Implementation Approach
- 4.3 Write Code in Small, Testable Increments
- 4.4 Add Documentation and Comments

### Step 5: Write Tests
Create tests for the implementation.

**Reference**: [op-write-tests.md](references/op-write-tests.md)

**Contents**:
- 5.1 Identify Test Scenarios from Requirements
- 5.2 Write Unit Tests for New Functions
- 5.3 Write Integration Tests if Applicable
- 5.4 Run Tests and Fix Failures

### Step 6: Validate Acceptance Criteria
Verify all criteria are met before completion.

**Reference**: [op-validate-acceptance-criteria.md](references/op-validate-acceptance-criteria.md)

**Contents**:
- 6.1 Review Each Acceptance Criterion
- 6.2 Verify Implementation Satisfies Criterion
- 6.3 Document Validation Evidence
- 6.4 Report Completion to Orchestrator

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

---
name: epa-handoff-management
description: Create and receive handoff documents. Use for work state documentation.
license: Apache-2.0
compatibility: Requires AI Maestro running.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: epa-programmer-main-agent
workflow-instruction: "support"
procedure: "support-skill"
---

# EPA Handoff Management Skill

This skill enables the Emasoft Programmer Agent to create and receive handoff documents for seamless context transfer between agents and sessions.

## Purpose

Handoff documents preserve work state across:
- Agent transitions (when EOA delegates to EPA)
- Session boundaries (when context is cleared)
- Bug discoveries (structured reporting)
- Work interruptions (save and resume)

## Operations

This skill provides four core operations for handoff management:

### 1. Read Handoff Document
**File**: [op-read-handoff-document.md](references/op-read-handoff-document.md)

**Contents**:
- 1.1 When to read a handoff document
- 1.2 Parsing handoff YAML frontmatter
- 1.3 Extracting task context and requirements
- 1.4 Identifying delegated work items
- 1.5 Resuming from checkpoints

Use this operation when receiving work from EOA or resuming from a previous session.

### 2. Create Handoff Document
**File**: [op-create-handoff-document.md](references/op-create-handoff-document.md)

**Contents**:
- 2.1 When to create a handoff document
- 2.2 Handoff document structure and format
- 2.3 Capturing current work state
- 2.4 Documenting completed and pending items
- 2.5 Writing to the handoff directory

Use this operation when transferring work to another agent or ending a session.

### 3. Write Bug Report
**File**: [op-write-bug-report.md](references/op-write-bug-report.md)

**Contents**:
- 3.1 When to write a bug report
- 3.2 Bug report structure and required fields
- 3.3 Capturing reproduction steps
- 3.4 Documenting expected versus actual behavior
- 3.5 Linking to related code and tests

Use this operation when discovering bugs during implementation work.

### 4. Document Work State
**File**: [op-document-work-state.md](references/op-document-work-state.md)

**Contents**:
- 4.1 When to document work state
- 4.2 Work state document structure
- 4.3 Capturing in-progress changes
- 4.4 Recording decision context
- 4.5 Enabling session resume

Use this operation to save current work for later continuation.

## Handoff Directory Structure

All handoff documents are stored in a standardized location:

```
$CLAUDE_PROJECT_DIR/thoughts/shared/handoffs/
├── epa-<task-name>/
│   ├── current.md           # Active handoff document
│   ├── archive/             # Previous handoff versions
│   └── bugs/                # Bug reports for this task
```

## Integration with AI Maestro

This skill integrates with AI Maestro for inter-agent messaging:
- Handoff creation triggers notification to receiving agent
- Bug reports can be escalated to EOA for triage
- Work state documents enable checkpoint-based resume

## Quick Reference

| Situation | Operation to Use |
|-----------|------------------|
| Received delegation from EOA | Read Handoff Document |
| Completing work, passing to next agent | Create Handoff Document |
| Found a bug during implementation | Write Bug Report |
| Need to pause work for later | Document Work State |
| Resuming after context clear | Read Handoff Document |

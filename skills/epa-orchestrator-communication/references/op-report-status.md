---
name: op-report-status
description: Send development status updates to EOA to keep the orchestrator informed of progress.
parent-skill: epa-orchestrator-communication
workflow-step: "Step 17"
message-type: status-update
priority: normal
---

# Operation: Report Status

This operation describes how to send "in development" status updates to the Emasoft Orchestrator Agent (EOA) to keep the orchestrator informed of your progress on assigned tasks.

## Table of Contents

- 2.1 When to Report Status
- 2.2 Status Message Format
- 2.3 Progress Indicators
- 2.4 Sending Status Updates
- 2.5 Examples

## 2.1 When to Report Status

Send status updates to EOA in these situations:

| Situation | Frequency | Priority |
|-----------|-----------|----------|
| **Starting a task** | Once at beginning | `normal` |
| **Major milestone reached** | When significant progress made | `normal` |
| **Phase transition** | Moving from one phase to another | `normal` |
| **Extended task (> 2 hours)** | Every 1-2 hours | `normal` |
| **About to go offline** | Before ending session | `high` |
| **Significant delay** | When timeline affected | `high` |

**Status Update Triggers**:

1. **Task Start**: When you begin working on a task
2. **Test Phase Complete**: When tests are written and passing/failing as expected
3. **Implementation Complete**: When code implementation is done
4. **Refactoring Complete**: When code cleanup is finished
5. **Ready for Review**: When all work is complete

## Prerequisites

Before sending a status update:

1. **Have active task**: You must be working on an assigned task
2. **Know current progress**: Assess your actual progress percentage
3. **Identify blockers**: Note any issues affecting progress
4. **Estimate completion**: Have realistic time estimate

## 2.2 Status Message Format

Structure your status update with these components:

```json
{
  "to": "orchestrator-master",
  "subject": "STATUS: [Task ID] - [Current Phase]",
  "priority": "normal",
  "content": {
    "type": "status-update",
    "message": "[Brief status summary]",
    "task_id": "[TASK-ID]",
    "phase": "[current-phase]",
    "progress_percent": [0-100],
    "completed": [
      "[Completed item 1]",
      "[Completed item 2]"
    ],
    "in_progress": "[Current work item]",
    "remaining": [
      "[Remaining item 1]",
      "[Remaining item 2]"
    ],
    "blockers": [],
    "estimated_completion": "[Time estimate]"
  }
}
```

### Message Components

| Field | Description | Required |
|-------|-------------|----------|
| `task_id` | The identifier of the task | Yes |
| `phase` | Current development phase (see section 2.3) | Yes |
| `progress_percent` | Percentage complete (0-100) | Yes |
| `completed` | Array of completed items | Yes |
| `in_progress` | Current work item | Yes |
| `remaining` | Array of remaining items | Yes |
| `blockers` | Array of blocking issues (empty if none) | Yes |
| `estimated_completion` | Time estimate to completion | No |

## 2.3 Progress Indicators

### Development Phases

Use these standardized phase names:

| Phase | Description | Typical Progress % |
|-------|-------------|-------------------|
| `planning` | Analyzing requirements, planning approach | 0-10% |
| `test-writing` | Writing failing tests (TDD) | 10-25% |
| `implementation` | Writing code to pass tests | 25-60% |
| `refactoring` | Code cleanup and optimization | 60-80% |
| `documentation` | Writing/updating documentation | 80-90% |
| `review-prep` | Preparing for review, final checks | 90-100% |

### Progress Calculation

Calculate progress based on completed items:

```
progress_percent = (completed_items / total_items) * 100
```

**Example**:
- Task has 5 items: tests, core logic, edge cases, refactoring, docs
- Completed: tests, core logic (2 items)
- Progress: (2 / 5) * 100 = 40%

## Procedure

Follow these steps to report status:

1. **Assess current state**: Determine phase, progress, and remaining work
2. **Identify blockers**: Note any issues preventing progress
3. **Estimate completion**: Calculate realistic time estimate
4. **Compose message**: Use the format specified in section 2.2
5. **Send via AI Maestro**: Execute the curl command
6. **Continue work**: Resume task after sending update

## Checklist

Use this checklist before sending a status update:

- [ ] I know the current development phase
- [ ] I have calculated the progress percentage accurately
- [ ] I have listed all completed items
- [ ] I have identified the current work item
- [ ] I have listed all remaining items
- [ ] I have noted any blockers (or confirmed none exist)
- [ ] I have a realistic completion estimate
- [ ] The message follows the required JSON format

## 2.4 Sending Status Updates

Execute this command to send a status update:

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "orchestrator-master",
    "subject": "STATUS: TASK-123 - Implementation Phase",
    "priority": "normal",
    "content": {
      "type": "status-update",
      "message": "Implementation in progress. Tests passing, working on edge cases.",
      "task_id": "TASK-123",
      "phase": "implementation",
      "progress_percent": 45,
      "completed": [
        "Unit tests written (12 tests)",
        "Core function implemented",
        "Happy path working"
      ],
      "in_progress": "Edge case handling",
      "remaining": [
        "Error handling",
        "Refactoring",
        "Documentation update"
      ],
      "blockers": [],
      "estimated_completion": "2 hours"
    }
  }'
```

### Status Update When Delayed

If progress is slower than expected:

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "orchestrator-master",
    "subject": "STATUS: TASK-123 - Implementation Delayed",
    "priority": "high",
    "content": {
      "type": "status-update",
      "message": "Implementation taking longer than expected due to complexity.",
      "task_id": "TASK-123",
      "phase": "implementation",
      "progress_percent": 35,
      "completed": [
        "Unit tests written",
        "Core function implemented"
      ],
      "in_progress": "Complex edge case handling",
      "remaining": [
        "Additional edge cases",
        "Error handling",
        "Refactoring",
        "Documentation"
      ],
      "blockers": [],
      "estimated_completion": "4 hours (revised from 2 hours)",
      "delay_reason": "Edge cases more complex than anticipated"
    }
  }'
```

## 2.5 Examples

### Example 1: Task Start Status

**Situation**: Beginning work on a new task.

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "orchestrator-master",
    "subject": "STATUS: TASK-456 - Starting Development",
    "priority": "normal",
    "content": {
      "type": "status-update",
      "message": "Starting work on TASK-456. Analyzed requirements, beginning test writing.",
      "task_id": "TASK-456",
      "phase": "test-writing",
      "progress_percent": 5,
      "completed": [
        "Requirements analysis",
        "Approach planning"
      ],
      "in_progress": "Writing unit tests",
      "remaining": [
        "Complete test suite",
        "Implementation",
        "Refactoring",
        "Documentation"
      ],
      "blockers": [],
      "estimated_completion": "3 hours"
    }
  }'
```

### Example 2: Milestone Reached

**Situation**: All tests written and passing.

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "orchestrator-master",
    "subject": "STATUS: TASK-456 - Tests Complete",
    "priority": "normal",
    "content": {
      "type": "status-update",
      "message": "All tests written and implementation complete. Moving to refactoring.",
      "task_id": "TASK-456",
      "phase": "refactoring",
      "progress_percent": 65,
      "completed": [
        "Unit tests (15 tests)",
        "Core implementation",
        "Edge case handling",
        "Error handling"
      ],
      "in_progress": "Code cleanup and refactoring",
      "remaining": [
        "Refactoring",
        "Documentation update",
        "Final review prep"
      ],
      "blockers": [],
      "estimated_completion": "1 hour"
    }
  }'
```

### Example 3: Ready for Review

**Situation**: All work complete, ready for EOA review.

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "orchestrator-master",
    "subject": "STATUS: TASK-456 - Ready for Review",
    "priority": "normal",
    "content": {
      "type": "status-update",
      "message": "Task complete. All tests passing, code refactored, documentation updated.",
      "task_id": "TASK-456",
      "phase": "review-prep",
      "progress_percent": 100,
      "completed": [
        "Unit tests (15 tests, all passing)",
        "Core implementation",
        "Edge case handling",
        "Error handling",
        "Refactoring",
        "Documentation update"
      ],
      "in_progress": "None - awaiting review",
      "remaining": [],
      "blockers": [],
      "estimated_completion": "Complete"
    }
  }'
```

### Example 4: Status with Blockers

**Situation**: Progress blocked by external dependency.

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "orchestrator-master",
    "subject": "STATUS: TASK-789 - Partially Blocked",
    "priority": "high",
    "content": {
      "type": "status-update",
      "message": "Implementation partially blocked. Completed independent work, waiting on API access.",
      "task_id": "TASK-789",
      "phase": "implementation",
      "progress_percent": 40,
      "completed": [
        "Unit tests written",
        "Local logic implemented",
        "Mock integration tests"
      ],
      "in_progress": "Blocked - cannot complete API integration",
      "remaining": [
        "Real API integration",
        "End-to-end testing",
        "Refactoring",
        "Documentation"
      ],
      "blockers": [
        "Waiting for API credentials from external team",
        "ETA for credentials: unknown"
      ],
      "estimated_completion": "Unknown until blocker resolved"
    }
  }'
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `Connection refused` | AI Maestro not running | Start AI Maestro service |
| `Message delivery failed` | Network issue | Retry after 5 seconds |
| `Invalid progress_percent` | Value outside 0-100 | Use integer between 0 and 100 |
| `Empty completed array` | No work done yet | Include at least "Task analysis" |

### Best Practices

1. **Be accurate**: Do not inflate progress percentage
2. **Be consistent**: Use standardized phase names
3. **Be honest about blockers**: Report issues early
4. **Update regularly**: Do not go silent for extended periods
5. **Include context**: Explain what "in progress" means specifically

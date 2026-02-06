---
name: op-notify-completion
description: Notify EOA when task implementation is complete and ready for review.
parent-skill: epa-orchestrator-communication
workflow-step: "Step 19"
message-type: completion-notification
priority: high
---

# Operation: Notify Completion

This operation describes how to inform the Emasoft Orchestrator Agent (EOA) when your task implementation is complete and ready for review.

## Table of Contents

- 5.1 Completion Criteria
- 5.2 Completion Notification Format
- 5.3 Deliverables Summary
- 5.4 Sending Notification
- 5.5 Examples

## 5.1 Completion Criteria

Before notifying EOA of completion, verify ALL of these criteria are met:

### Mandatory Criteria

| Criterion | Verification |
|-----------|--------------|
| **All tests pass** | Run full test suite, 100% pass rate |
| **Code implemented** | All specified functionality works |
| **Edge cases handled** | Error conditions covered |
| **No regressions** | Existing tests still pass |
| **Code formatted** | Linter passes, style consistent |
| **Type checks pass** | No type errors (if applicable) |

### Quality Criteria

| Criterion | Verification |
|-----------|--------------|
| **Code reviewed** | Self-reviewed for issues |
| **Documentation updated** | Docstrings, comments current |
| **Commits organized** | Logical commit history |
| **Branch ready** | Clean, mergeable state |

### Deliverables Ready

| Deliverable | Status |
|-------------|--------|
| Source code | Committed and pushed |
| Tests | Written and passing |
| Documentation | Updated if required |
| PR (if applicable) | Created and ready |

## Prerequisites

Before sending completion notification:

1. **All tests pass**: Run complete test suite
2. **Code formatted**: Run linter and formatter
3. **Type checks pass**: Run type checker (if applicable)
4. **Self-reviewed**: Review your own changes
5. **Commits pushed**: All changes committed and pushed
6. **PR created (if applicable)**: Pull request ready for review

## 5.2 Completion Notification Format

Structure your completion notification with these components:

```json
{
  "to": "orchestrator-master",
  "subject": "COMPLETE: [Task ID] - [Brief Description]",
  "priority": "high",
  "content": {
    "type": "completion-notification",
    "message": "[Brief completion summary]",
    "task_id": "[TASK-ID]",
    "status": "completed",
    "deliverables": {
      "code": {
        "branch": "[branch-name]",
        "commits": [number],
        "files_changed": [number],
        "lines_added": [number],
        "lines_removed": [number]
      },
      "tests": {
        "total": [number],
        "passed": [number],
        "coverage_percent": [number]
      },
      "documentation": {
        "updated": [true/false],
        "files": ["[file1]", "[file2]"]
      },
      "pr": {
        "created": [true/false],
        "url": "[PR-URL]",
        "title": "[PR-Title]"
      }
    },
    "implementation_notes": "[Any important notes about the implementation]",
    "known_limitations": ["[Limitation 1]", "[Limitation 2]"],
    "testing_notes": "[How to test the implementation]",
    "ready_for_review": true
  }
}
```

### Message Components

| Field | Description | Required |
|-------|-------------|----------|
| `task_id` | The identifier of the completed task | Yes |
| `status` | Must be "completed" | Yes |
| `deliverables` | Summary of all deliverables | Yes |
| `deliverables.code` | Code change statistics | Yes |
| `deliverables.tests` | Test results | Yes |
| `deliverables.documentation` | Documentation changes | Yes |
| `deliverables.pr` | Pull request information | If applicable |
| `implementation_notes` | Important implementation details | No |
| `known_limitations` | Any limitations or caveats | No |
| `testing_notes` | How to verify the implementation | No |
| `ready_for_review` | Confirmation ready for review | Yes |

## 5.3 Deliverables Summary

### Code Deliverables

Include these statistics:

```json
"code": {
  "branch": "feature/TASK-123-user-auth",
  "commits": 5,
  "files_changed": 8,
  "lines_added": 342,
  "lines_removed": 45
}
```

Get these values with:

```bash
# Branch name
git branch --show-current

# Commit count (from branch point)
git rev-list --count main..HEAD

# Files changed
git diff --stat main..HEAD | tail -1

# Lines added/removed
git diff --stat main..HEAD | tail -1
```

### Test Deliverables

Include test results:

```json
"tests": {
  "total": 24,
  "passed": 24,
  "coverage_percent": 92
}
```

Get these values with:

```bash
# Run tests with coverage
uv run pytest --cov=src --cov-report=term-missing -v

# Parse output for totals
```

### Documentation Deliverables

Include documentation changes:

```json
"documentation": {
  "updated": true,
  "files": [
    "docs/api/auth.md",
    "README.md"
  ]
}
```

### Pull Request Deliverables

If PR was created:

```json
"pr": {
  "created": true,
  "url": "https://github.com/org/repo/pull/123",
  "title": "feat(auth): Add user authentication module"
}
```

## Procedure

Follow these steps to notify completion:

1. **Verify all tests pass**: Run complete test suite
2. **Verify code quality**: Run linter, formatter, type checker
3. **Gather statistics**: Collect code and test metrics
4. **Create PR (if applicable)**: Open pull request
5. **Self-review**: Review your own changes one more time
6. **Compose notification**: Use the format from section 5.2
7. **Send to EOA**: Execute the curl command
8. **Wait for feedback**: Monitor for EOA response

## Checklist

Use this checklist before sending completion notification:

- [ ] All unit tests pass (100% pass rate)
- [ ] All integration tests pass (if applicable)
- [ ] Linter passes with no errors
- [ ] Type checker passes with no errors (if applicable)
- [ ] Code has been self-reviewed
- [ ] Commits are organized and have good messages
- [ ] All changes are committed and pushed
- [ ] Branch is up to date with main/base branch
- [ ] Documentation is updated (if required)
- [ ] PR is created and ready (if applicable)
- [ ] I have gathered all code and test statistics
- [ ] Known limitations are documented
- [ ] Testing notes are prepared
- [ ] The message follows the required format

## 5.4 Sending Notification

Execute this command to send the completion notification:

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "orchestrator-master",
    "subject": "COMPLETE: TASK-123 - User Authentication Module",
    "priority": "high",
    "content": {
      "type": "completion-notification",
      "message": "User authentication module implementation complete. All tests passing, PR ready for review.",
      "task_id": "TASK-123",
      "status": "completed",
      "deliverables": {
        "code": {
          "branch": "feature/TASK-123-user-auth",
          "commits": 5,
          "files_changed": 8,
          "lines_added": 342,
          "lines_removed": 45
        },
        "tests": {
          "total": 24,
          "passed": 24,
          "coverage_percent": 92
        },
        "documentation": {
          "updated": true,
          "files": ["docs/api/auth.md"]
        },
        "pr": {
          "created": true,
          "url": "https://github.com/org/repo/pull/456",
          "title": "feat(auth): Add user authentication module"
        }
      },
      "implementation_notes": "Used JWT tokens with 24-hour expiry as specified. Implemented refresh token rotation for security.",
      "known_limitations": [
        "Rate limiting not implemented (out of scope per task description)"
      ],
      "testing_notes": "Run auth tests with: uv run pytest tests/unit/test_auth.py -v",
      "ready_for_review": true
    }
  }'
```

## 5.5 Examples

### Example 1: Feature Implementation Complete

**Situation**: New feature fully implemented with tests.

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "orchestrator-master",
    "subject": "COMPLETE: TASK-456 - Order Processing Pipeline",
    "priority": "high",
    "content": {
      "type": "completion-notification",
      "message": "Order processing pipeline implementation complete with full test coverage.",
      "task_id": "TASK-456",
      "status": "completed",
      "deliverables": {
        "code": {
          "branch": "feature/TASK-456-order-pipeline",
          "commits": 8,
          "files_changed": 12,
          "lines_added": 567,
          "lines_removed": 23
        },
        "tests": {
          "total": 35,
          "passed": 35,
          "coverage_percent": 94
        },
        "documentation": {
          "updated": true,
          "files": ["docs/architecture/order-pipeline.md", "docs/api/orders.md"]
        },
        "pr": {
          "created": true,
          "url": "https://github.com/org/repo/pull/789",
          "title": "feat(orders): Add order processing pipeline"
        }
      },
      "implementation_notes": "Implemented async pipeline with retry logic. Orders processed in batches of 100 for efficiency.",
      "known_limitations": [],
      "testing_notes": "Full test suite: uv run pytest tests/ -v. Pipeline can be manually tested with: uv run python scripts/test_order_pipeline.py",
      "ready_for_review": true
    }
  }'
```

### Example 2: Bug Fix Complete

**Situation**: Bug fix implemented and verified.

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "orchestrator-master",
    "subject": "COMPLETE: TASK-789 - Fix Race Condition in Cache Update",
    "priority": "high",
    "content": {
      "type": "completion-notification",
      "message": "Race condition in cache update fixed. Added mutex lock and regression tests.",
      "task_id": "TASK-789",
      "status": "completed",
      "deliverables": {
        "code": {
          "branch": "fix/TASK-789-cache-race-condition",
          "commits": 3,
          "files_changed": 2,
          "lines_added": 45,
          "lines_removed": 12
        },
        "tests": {
          "total": 8,
          "passed": 8,
          "coverage_percent": 100
        },
        "documentation": {
          "updated": false,
          "files": []
        },
        "pr": {
          "created": true,
          "url": "https://github.com/org/repo/pull/101",
          "title": "fix(cache): Add mutex lock to prevent race condition"
        }
      },
      "implementation_notes": "Added threading.Lock() around cache write operations. Verified fix under concurrent load testing.",
      "known_limitations": [],
      "testing_notes": "Regression test: uv run pytest tests/unit/test_cache.py::test_concurrent_updates -v --count=100",
      "ready_for_review": true
    }
  }'
```

### Example 3: Refactoring Complete

**Situation**: Refactoring task completed.

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "orchestrator-master",
    "subject": "COMPLETE: TASK-101 - Refactor Payment Module",
    "priority": "high",
    "content": {
      "type": "completion-notification",
      "message": "Payment module refactored. Reduced complexity, improved testability.",
      "task_id": "TASK-101",
      "status": "completed",
      "deliverables": {
        "code": {
          "branch": "refactor/TASK-101-payment-module",
          "commits": 6,
          "files_changed": 5,
          "lines_added": 234,
          "lines_removed": 312
        },
        "tests": {
          "total": 28,
          "passed": 28,
          "coverage_percent": 96
        },
        "documentation": {
          "updated": true,
          "files": ["docs/architecture/payment-module.md"]
        },
        "pr": {
          "created": true,
          "url": "https://github.com/org/repo/pull/202",
          "title": "refactor(payment): Simplify payment processing module"
        }
      },
      "implementation_notes": "Split monolithic PaymentProcessor into PaymentValidator, PaymentExecutor, and PaymentNotifier. Reduced cyclomatic complexity from 32 to 8.",
      "known_limitations": [],
      "testing_notes": "All existing tests pass. New unit tests added for each extracted class.",
      "ready_for_review": true
    }
  }'
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `Connection refused` | AI Maestro not running | Start AI Maestro service |
| `Message delivery failed` | Network issue | Retry up to 3 times |
| `Tests failing after notification` | Regression introduced | Send correction notification |

### Post-Notification Issues

If you discover an issue after sending completion notification:

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "orchestrator-master",
    "subject": "CORRECTION: TASK-123 - Issue Found After Completion",
    "priority": "high",
    "content": {
      "type": "status-update",
      "message": "CORRECTION to previous completion notification. Issue found and being addressed.",
      "task_id": "TASK-123",
      "status": "in-progress",
      "issue_discovered": "[Description of issue]",
      "action_being_taken": "[What you are doing to fix it]",
      "revised_completion_estimate": "[New estimate]"
    }
  }'
```

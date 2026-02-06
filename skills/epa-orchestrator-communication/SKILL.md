---
name: epa-orchestrator-communication
description: Communication with EOA (Orchestrator). Use for clarifications, status updates, blockers.
license: MIT
compatibility: Requires AI Maestro running.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: epa-programmer-main-agent
user-invocable: false
workflow-instruction: "Steps 14, 15, 17, 19"
procedure: "proc-clarify-tasks, proc-handle-feedback, proc-complete-task"
---

# EPA Orchestrator Communication Skill

This skill defines all communication protocols between the Emasoft Programmer Agent (EPA) and the Emasoft Orchestrator Agent (EOA). Use this skill whenever you need to interact with the orchestrator for clarifications, status updates, blocking issues, improvement proposals, or task completion notifications.

## Overview

The EPA-EOA communication channel uses AI Maestro messaging for asynchronous inter-agent communication. All messages follow a structured format to ensure clear, actionable exchanges.

## When to Use This Skill

Use this skill in the following situations:

| Situation | Operation | Reference File |
|-----------|-----------|----------------|
| Task requirements are unclear or ambiguous | Request Clarification | [op-request-clarification.md](references/op-request-clarification.md) |
| Need to report current development status | Report Status | [op-report-status.md](references/op-report-status.md) |
| Encountered a blocking issue that prevents progress | Report Blocker | [op-report-blocker.md](references/op-report-blocker.md) |
| Have suggestions for design or task improvements | Propose Improvement | [op-propose-improvement.md](references/op-propose-improvement.md) |
| Task implementation is complete and ready for review | Notify Completion | [op-notify-completion.md](references/op-notify-completion.md) |
| Received feedback from EOA after PR review | Receive Feedback | [op-receive-feedback.md](references/op-receive-feedback.md) |

## Communication Architecture

```
EPA (Programmer Agent)          AI Maestro           EOA (Orchestrator Agent)
        |                           |                           |
        |--- Send Message --------->|                           |
        |                           |--- Deliver Message ------>|
        |                           |                           |
        |                           |<-- Response Message ------|
        |<--- Deliver Response -----|                           |
        |                           |                           |
```

## Message Priority Levels

| Priority | Use Case | Expected Response Time |
|----------|----------|------------------------|
| `urgent` | Blocking issues, critical failures | Immediate (within minutes) |
| `high` | Clarifications needed to continue, completion notifications | Within 30 minutes |
| `normal` | Status updates, improvement proposals | Within 2 hours |

## Message Types

All messages to EOA must include a `type` field in the content object:

| Type | Description |
|------|-------------|
| `clarification-request` | Asking for task clarification |
| `status-update` | Reporting development progress |
| `blocker-report` | Reporting blocking issues |
| `improvement-proposal` | Suggesting design improvements |
| `completion-notification` | Task is done, ready for review |
| `feedback-acknowledgment` | Acknowledging received feedback |

## Prerequisites

Before using any operation in this skill:

1. **AI Maestro is running**: Verify with `curl -s http://localhost:23000/health`
2. **Session is registered**: Your agent session must be registered with AI Maestro
3. **EOA is active**: The orchestrator agent session must be available

## Operations Reference

### 1. Request Clarification (Step 14)

Use when task requirements are unclear or need additional information.

**Reference**: [op-request-clarification.md](references/op-request-clarification.md)

**Contents**:
- 1.1 When to Request Clarification
- 1.2 Clarification Request Format
- 1.3 Sending the Request
- 1.4 Handling the Response
- 1.5 Examples

### 2. Report Status (Step 17)

Use to send "in development" status updates to keep EOA informed.

**Reference**: [op-report-status.md](references/op-report-status.md)

**Contents**:
- 2.1 When to Report Status
- 2.2 Status Message Format
- 2.3 Progress Indicators
- 2.4 Sending Status Updates
- 2.5 Examples

### 3. Report Blocker

Use when you encounter issues that prevent task progress.

**Reference**: [op-report-blocker.md](references/op-report-blocker.md)

**Contents**:
- 3.1 Identifying Blockers
- 3.2 Blocker Report Format
- 3.3 Severity Levels
- 3.4 Escalation Procedure
- 3.5 Examples

### 4. Propose Improvement (Step 15)

Use to suggest design or implementation improvements.

**Reference**: [op-propose-improvement.md](references/op-propose-improvement.md)

**Contents**:
- 4.1 When to Propose Improvements
- 4.2 Improvement Proposal Format
- 4.3 Justification Requirements
- 4.4 Awaiting Approval
- 4.5 Examples

### 5. Notify Completion (Step 19)

Use when task implementation is complete and ready for review.

**Reference**: [op-notify-completion.md](references/op-notify-completion.md)

**Contents**:
- 5.1 Completion Criteria
- 5.2 Completion Notification Format
- 5.3 Deliverables Summary
- 5.4 Sending Notification
- 5.5 Examples

### 6. Receive Feedback

Use to handle feedback from EOA after PR review.

**Reference**: [op-receive-feedback.md](references/op-receive-feedback.md)

**Contents**:
- 6.1 Monitoring for Feedback
- 6.2 Feedback Message Types
- 6.3 Processing Feedback
- 6.4 Acknowledgment Protocol
- 6.5 Examples

## API Quick Reference

### Send Message to EOA

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "orchestrator-master",
    "subject": "[SUBJECT]",
    "priority": "[PRIORITY]",
    "content": {
      "type": "[MESSAGE_TYPE]",
      "message": "[MESSAGE_BODY]"
    }
  }'
```

### Check for Messages from EOA

```bash
curl -s "http://localhost:23000/api/messages?agent=$SESSION_NAME&action=list&status=unread" | jq '.messages[]'
```

### Acknowledge Message

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "orchestrator-master",
    "subject": "ACK: [ORIGINAL_SUBJECT]",
    "priority": "normal",
    "content": {
      "type": "feedback-acknowledgment",
      "message": "Acknowledged and processing.",
      "original_message_id": "[MESSAGE_ID]"
    }
  }'
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `Connection refused` | AI Maestro not running | Start AI Maestro service |
| `Agent not found` | EOA session not registered | Wait for EOA to start or notify user |
| `Message delivery failed` | Network or service issue | Retry with exponential backoff |
| `Invalid message format` | Malformed JSON | Validate message structure before sending |

## Troubleshooting

### AI Maestro Connection Issues

If you cannot connect to AI Maestro:

1. Verify service is running: `curl -s http://localhost:23000/health`
2. Check if the port is in use: `lsof -i :23000`
3. Restart AI Maestro if needed

### EOA Not Responding

If EOA does not respond within expected time:

1. Check EOA session status via AI Maestro
2. Escalate to user if EOA is unavailable
3. Document the delay in status update

### Message Delivery Failures

If message delivery fails:

1. Verify message JSON is valid
2. Check session names are correct
3. Retry up to 3 times with 5-second delays
4. Report to user if all retries fail

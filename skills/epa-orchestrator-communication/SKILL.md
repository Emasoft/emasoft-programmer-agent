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

The EPA-EOA communication channel uses AMP (Agent Messaging Protocol) for asynchronous inter-agent communication. AMP provides CLI commands (`amp-send`, `amp-inbox`, `amp-read`, `amp-reply`, `amp-status`) for structured, reliable message exchange.

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

1. **AMP identity is initialized**: Verify with `cat ~/.agent-messaging/IDENTITY.md`. If not initialized, run `amp-init --auto`
2. **AMP is operational**: Verify with `amp-status`
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

## AMP Quick Reference

### Send Message to EOA

```bash
amp-send orchestrator-master "[SUBJECT]" "[MESSAGE_BODY]" --type [MESSAGE_TYPE] --priority [PRIORITY]
```

### Check for Messages from EOA

```bash
amp-inbox
```

### Read a Specific Message

```bash
amp-read <message-id>
```

### Reply to a Message (Acknowledge)

```bash
amp-reply <message-id> "Acknowledged and processing."
```

### Check AMP Status

```bash
amp-status
```

### Check AMP Identity

```bash
cat ~/.agent-messaging/IDENTITY.md
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `AMP identity not found` | AMP not initialized | Run `amp-init --auto` |
| `Recipient not found` | EOA session not registered | Wait for EOA to start or notify user |
| `Message delivery failed` | Network or service issue | Retry with `amp-send` |
| `AMP status: offline` | AMP service not running | Check with `amp-status`, restart AI Maestro service |

## Troubleshooting

### AMP Connection Issues

If AMP commands fail:

1. Check AMP status: `amp-status`
2. Verify identity: `cat ~/.agent-messaging/IDENTITY.md`
3. Re-initialize if needed: `amp-init --auto`

### EOA Not Responding

If EOA does not respond within expected time:

1. Check EOA status via `amp-status`
2. Escalate to user if EOA is unavailable
3. Document the delay in status update

### Message Delivery Failures

If message delivery fails:

1. Verify recipient name is correct
2. Check AMP status: `amp-status`
3. Retry up to 3 times with 5-second delays
4. Report to user if all retries fail

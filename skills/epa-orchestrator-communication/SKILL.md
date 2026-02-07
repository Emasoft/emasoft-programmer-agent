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

The EPA-EOA communication channel uses asynchronous inter-agent messaging provided by the globally installed `agent-messaging` skill. That skill defines the current commands and syntax for sending, receiving, reading, replying to, and checking the status of messages. Always read the `agent-messaging` skill at runtime to determine the exact commands -- never hardcode messaging command names in your workflow.

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

1. **Messaging identity is initialized**: Read the `agent-messaging` skill and follow its initialization instructions. Verify your identity is set up before sending any messages.
2. **Messaging service is operational**: Use the `agent-messaging` skill's status check operation to confirm connectivity.
3. **EOA is active**: The orchestrator agent session must be available.

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

## Messaging Quick Reference

All messaging operations below are performed using the `agent-messaging` skill. Read that skill to learn the current command syntax.

### Send Message to EOA

Send a message to the orchestrator using the `agent-messaging` skill:
- **Recipient**: your assigned orchestrator agent
- **Subject**: the subject line for this message
- **Content**: the message body text
- **Type**: the message type (see Message Types table above)
- **Priority**: the priority level (see Message Priority Levels table above)

**Verify**: confirm the message appears in your sent messages.

### Check for Messages from EOA

Check your inbox using the `agent-messaging` skill. Process all unread messages before proceeding.

### Read a Specific Message

Read the message by its ID using the `agent-messaging` skill to see its full content.

### Reply to a Message (Acknowledge)

Reply to the message using the `agent-messaging` skill, confirming receipt and stating your next action.

### Check Messaging Status

Use the `agent-messaging` skill's status check operation to verify the messaging service is running and your identity is configured.

### Verify Messaging Identity

Use the `agent-messaging` skill's identity check operation to confirm your session name is registered as your messaging identity.

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Identity not found | Messaging not initialized | Read the `agent-messaging` skill and follow its initialization instructions |
| Recipient not found | EOA session not registered | Wait for EOA to start or notify user |
| Message delivery failed | Network or service issue | Retry the send operation using the `agent-messaging` skill |
| Messaging service offline | Service not running | Use the `agent-messaging` skill's status check, restart AI Maestro service |

## Troubleshooting

### Messaging Connection Issues

If messaging operations fail:

1. Use the `agent-messaging` skill's status check operation to verify connectivity
2. Use the `agent-messaging` skill's identity check operation to verify your identity is set up
3. Re-initialize your identity following the `agent-messaging` skill's initialization instructions

### EOA Not Responding

If EOA does not respond within expected time:

1. Check the messaging service status using the `agent-messaging` skill
2. Escalate to user if EOA is unavailable
3. Document the delay in status update

### Message Delivery Failures

If message delivery fails:

1. Verify recipient name is correct
2. Check messaging service status using the `agent-messaging` skill
3. Retry up to 3 times with 5-second delays
4. Report to user if all retries fail

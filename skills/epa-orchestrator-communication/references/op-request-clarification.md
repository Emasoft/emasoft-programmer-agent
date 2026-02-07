---
name: op-request-clarification
description: Request task clarification from EOA when requirements are unclear or ambiguous.
parent-skill: epa-orchestrator-communication
workflow-step: "Step 14"
message-type: clarification-request
priority: high
---

# Operation: Request Clarification

This operation describes how to request clarification from the Emasoft Orchestrator Agent (EOA) when task requirements are unclear, ambiguous, or incomplete.

## Table of Contents

- 1.1 When to Request Clarification
- 1.2 Clarification Request Format
- 1.3 Sending the Request
- 1.4 Handling the Response
- 1.5 Examples

## 1.1 When to Request Clarification

Request clarification from EOA in these situations:

| Situation | Example |
|-----------|---------|
| **Ambiguous requirements** | Task says "improve performance" without specifying metrics or targets |
| **Missing technical details** | No API specification provided for integration task |
| **Conflicting instructions** | Task mentions two incompatible approaches |
| **Scope uncertainty** | Unclear whether refactoring should include tests |
| **Dependency questions** | Unknown if external service is available |
| **Priority conflicts** | Multiple tasks with unclear priority order |

**Do NOT request clarification for**:
- Issues you can resolve by reading existing documentation
- Standard implementation decisions within your authority
- Stylistic choices already covered by project conventions

## Prerequisites

Before requesting clarification:

1. **Read all task materials**: Ensure you have read the complete task description
2. **Check existing documentation**: Search for answers in project docs
3. **Review similar tasks**: Check if similar tasks provide context
4. **Formulate specific questions**: Prepare clear, answerable questions

## 1.2 Clarification Request Format

Structure your clarification request with these components:

```json
{
  "to": "orchestrator-master",
  "subject": "CLARIFICATION: [Task ID] - [Brief Topic]",
  "priority": "high",
  "content": {
    "type": "clarification-request",
    "message": "[Structured clarification request]",
    "task_id": "[TASK-ID]",
    "questions": [
      "[Specific question 1]",
      "[Specific question 2]"
    ],
    "context": "[What you already understand]",
    "impact": "[How this affects your progress]"
  }
}
```

### Message Components

| Field | Description | Required |
|-------|-------------|----------|
| `task_id` | The identifier of the task needing clarification | Yes |
| `questions` | Array of specific, answerable questions | Yes |
| `context` | What you already understand about the task | Yes |
| `impact` | How lack of clarity affects your work | No |

## Procedure

Follow these steps to request clarification:

1. **Identify the unclear aspect**: Pinpoint exactly what is ambiguous
2. **Formulate specific questions**: Create clear, answerable questions (not vague requests)
3. **Document your current understanding**: Show what you already know
4. **Compose the message**: Use the format specified in section 1.2
5. **Send via AMP**: Execute the `amp-send` command
6. **Wait for response**: Monitor inbox for EOA reply
7. **Acknowledge receipt**: Confirm you received the clarification
8. **Update task understanding**: Incorporate clarification into your work

## Checklist

Use this checklist before sending a clarification request:

- [ ] I have read the complete task description
- [ ] I have checked project documentation for answers
- [ ] I have formulated specific, answerable questions
- [ ] I have documented what I already understand
- [ ] The questions are not about standard implementation decisions
- [ ] The message follows the required JSON format
- [ ] The subject line includes task ID and topic
- [ ] I am prepared to wait for a response before proceeding

## 1.3 Sending the Request

Execute this command to send the clarification request:

```bash
amp-send orchestrator-master "CLARIFICATION: TASK-123 - API Authentication Method" "I need clarification on the authentication method for the external API integration. Questions: 1) Should I use OAuth2 or API key authentication? 2) Is there an existing credentials store I should use? Context: The task mentions integrating with ExternalService API but does not specify the authentication approach. I found two authentication methods in their documentation. Impact: Cannot proceed with API client implementation until authentication approach is confirmed." --type request --priority high
```

## 1.4 Handling the Response

When EOA responds to your clarification request:

1. **Read the complete response**: Do not skim; read carefully
2. **Verify understanding**: Ensure the answer addresses your questions
3. **Acknowledge receipt**: Send acknowledgment message
4. **Request follow-up if needed**: If still unclear, send follow-up questions
5. **Document the clarification**: Record the decision for future reference
6. **Resume work**: Continue with the task using the clarified requirements

### Acknowledgment Format

When you receive a clarification response, reply directly to it:

```bash
amp-reply <message-id> "Clarification received. Will proceed with OAuth2 authentication using the central credentials store."
```

Or send a new acknowledgment message:

```bash
amp-send orchestrator-master "ACK: CLARIFICATION: TASK-123 - API Authentication Method" "Clarification received. Will proceed with OAuth2 authentication using the central credentials store." --type ack
```

## 1.5 Examples

### Example 1: Unclear Performance Requirements

**Situation**: Task says "optimize database queries" without specifying targets.

```bash
amp-send orchestrator-master "CLARIFICATION: TASK-456 - Database Optimization Targets" "I need clarification on the performance targets for database query optimization. Questions: 1) What is the target query response time? 2) Which specific queries should be prioritized? 3) Are there memory usage constraints to consider? Context: The task mentions optimizing database queries but does not specify performance targets or which queries are problematic. Current slowest query takes 2.3 seconds. Impact: Cannot determine optimization success criteria or prioritization without targets." --type request --priority high
```

### Example 2: Missing Dependency Information

**Situation**: Task requires integration with a service not mentioned in project docs.

```bash
amp-send orchestrator-master "CLARIFICATION: TASK-789 - PaymentGateway Service Details" "I need details about the PaymentGateway service for integration. Questions: 1) What is the PaymentGateway API endpoint URL? 2) Is there existing client code I should reuse? 3) What test environment is available? Context: Task references PaymentGateway service but I found no documentation or existing code for it in the codebase. Impact: Cannot begin integration work without service details." --type request --priority high
```

### Example 3: Conflicting Requirements

**Situation**: Two parts of the task description contradict each other.

```bash
amp-send orchestrator-master "CLARIFICATION: TASK-101 - Conflicting Error Handling Requirements" "The task contains conflicting requirements for error handling. Questions: 1) Should errors fail fast (as stated in section 2) or be silently logged (as stated in section 4)? 2) Which requirement takes precedence? Context: Section 2 says to implement fail-fast error handling. Section 4 says errors should be logged silently without disrupting the user. These approaches are mutually exclusive. Impact: Cannot implement error handling without knowing which approach to use." --type request --priority high
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `AMP identity not found` | AMP not initialized | Run `amp-init --auto` |
| `Recipient not found: orchestrator-master` | EOA session not registered | Wait for EOA to start or notify user |
| `AMP status: offline` | AMP service not running | Check `amp-status`, restart AI Maestro |
| `No response within 30 minutes` | EOA busy or unavailable | Send reminder with `--priority urgent` |
| `Response does not answer questions` | Miscommunication | Send follow-up with specific unanswered questions |

### Retry Logic

If message delivery fails:

```bash
# Retry up to 3 times with 5-second delays
for i in 1 2 3; do
  if amp-send orchestrator-master "[SUBJECT]" "[MESSAGE]" --type request --priority high; then
    echo "Message sent successfully"
    break
  fi
  echo "Attempt $i failed, retrying in 5 seconds..."
  sleep 5
done
```

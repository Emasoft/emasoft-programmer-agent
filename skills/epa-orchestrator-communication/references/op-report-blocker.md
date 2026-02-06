---
name: op-report-blocker
description: Report blocking issues to EOA that prevent task progress.
parent-skill: epa-orchestrator-communication
workflow-step: "Escalation Path"
message-type: blocker-report
priority: urgent
---

# Operation: Report Blocker

This operation describes how to report blocking issues to the Emasoft Orchestrator Agent (EOA) when you encounter problems that prevent you from making progress on an assigned task.

## Table of Contents

- 3.1 Identifying Blockers
- 3.2 Blocker Report Format
- 3.3 Severity Levels
- 3.4 Escalation Procedure
- 3.5 Examples

## 3.1 Identifying Blockers

A blocker is an issue that completely prevents you from continuing work on a task. Blockers must be reported immediately to EOA.

### What Qualifies as a Blocker

| Type | Examples | Is Blocker? |
|------|----------|-------------|
| **Missing credentials** | API keys, database passwords, service accounts | Yes |
| **Missing access** | Repository access, server access, cloud console | Yes |
| **Missing dependency** | Required service not available, package not published | Yes |
| **Unclear requirements** | Cannot proceed without clarification | Yes (use clarification first) |
| **Technical impossibility** | Requested feature cannot be implemented as specified | Yes |
| **External dependency** | Waiting on external team or third party | Yes |
| **Environment issue** | Build system broken, CI/CD pipeline down | Yes |
| **Difficult problem** | Takes longer than expected but progress possible | No |
| **Missing documentation** | Can be discovered through code exploration | No |
| **Minor tooling issue** | Workaround available | No |

### Blocker vs. Delay

| Characteristic | Blocker | Delay |
|----------------|---------|-------|
| Can you make any progress? | No | Yes, slowly |
| Is there a workaround? | No | Possibly |
| Do you need external help? | Yes | Maybe |
| Report as | `blocker-report` | `status-update` with delay |

## Prerequisites

Before reporting a blocker:

1. **Verify it is a blocker**: Confirm no workaround exists
2. **Attempt resolution**: Try to resolve independently first
3. **Document attempts**: Note what you tried
4. **Identify root cause**: Understand why you are blocked
5. **Propose solutions**: Think of possible resolutions

## 3.2 Blocker Report Format

Structure your blocker report with these components:

```json
{
  "to": "orchestrator-master",
  "subject": "BLOCKER: [Task ID] - [Brief Description]",
  "priority": "urgent",
  "content": {
    "type": "blocker-report",
    "message": "[Brief summary of blocking issue]",
    "task_id": "[TASK-ID]",
    "severity": "[critical|high|medium]",
    "blocker_type": "[blocker-type]",
    "description": "[Detailed description of the issue]",
    "impact": "[How this affects task completion]",
    "attempted_resolutions": [
      "[What you tried]"
    ],
    "proposed_solutions": [
      "[Possible resolution 1]",
      "[Possible resolution 2]"
    ],
    "unblocking_requirements": "[What is needed to proceed]",
    "progress_before_block": "[What was completed before block]"
  }
}
```

### Message Components

| Field | Description | Required |
|-------|-------------|----------|
| `task_id` | The identifier of the blocked task | Yes |
| `severity` | Severity level (see section 3.3) | Yes |
| `blocker_type` | Category of blocker | Yes |
| `description` | Detailed description of the issue | Yes |
| `impact` | How this affects completion | Yes |
| `attempted_resolutions` | What you tried to resolve it | Yes |
| `proposed_solutions` | Possible resolutions | Yes |
| `unblocking_requirements` | What is needed to proceed | Yes |
| `progress_before_block` | Work completed before block | No |

### Blocker Types

Use these standardized blocker type values:

| Type | Description |
|------|-------------|
| `missing-credentials` | API keys, passwords, tokens |
| `missing-access` | Repository, server, or service access |
| `missing-dependency` | Required service or package unavailable |
| `unclear-requirements` | Cannot proceed without clarification |
| `technical-impossibility` | Cannot implement as specified |
| `external-dependency` | Waiting on external team |
| `environment-issue` | Build, CI/CD, or infrastructure problem |
| `resource-unavailable` | Required resource does not exist |

## 3.3 Severity Levels

### Critical Severity

**Definition**: Complete stop, no progress possible on any part of the task.

**Characteristics**:
- No workaround exists
- Cannot work on any related items
- Time-sensitive resolution needed

**Example**: Production credentials revoked, cannot deploy or test.

### High Severity

**Definition**: Major functionality blocked, but minor progress possible.

**Characteristics**:
- Some unrelated work can continue
- Core functionality blocked
- Resolution needed within hours

**Example**: API endpoint returning 500 errors, can continue writing tests but cannot verify integration.

### Medium Severity

**Definition**: Partial block, significant workaround required.

**Characteristics**:
- Workaround exists but is inefficient
- Progress significantly slowed
- Resolution needed within a day

**Example**: CI/CD pipeline slow, can test locally but deployment delayed.

## Procedure

Follow these steps to report a blocker:

1. **Confirm blocker status**: Verify no workaround exists
2. **Document the issue**: Note exact error messages, conditions
3. **Note attempted resolutions**: List what you tried
4. **Determine severity**: Use criteria from section 3.3
5. **Identify blocker type**: Use standardized types
6. **Propose solutions**: Think of possible resolutions
7. **Compose message**: Use the format from section 3.2
8. **Send with urgent priority**: Execute the curl command
9. **Wait for response**: Monitor inbox for EOA reply
10. **Continue if possible**: Work on unblocked items if any exist

## Checklist

Use this checklist before reporting a blocker:

- [ ] I have confirmed this is a blocker (no workaround exists)
- [ ] I have attempted to resolve it independently
- [ ] I have documented the exact error or issue
- [ ] I have identified the root cause
- [ ] I have categorized the blocker type
- [ ] I have assessed the severity level
- [ ] I have proposed possible solutions
- [ ] I have listed what is needed to unblock
- [ ] The message uses urgent priority
- [ ] The subject line clearly indicates BLOCKER

## 3.4 Escalation Procedure

### Escalation Timeline

| Severity | Initial Report | First Escalation | Second Escalation |
|----------|---------------|------------------|-------------------|
| Critical | Immediate | +15 minutes | +30 minutes |
| High | Immediate | +1 hour | +2 hours |
| Medium | Immediate | +4 hours | +8 hours |

### Escalation Actions

1. **First Escalation**: Resend with reminder, confirm EOA received original
2. **Second Escalation**: Request EOA to escalate to user
3. **Final Escalation**: Send direct notification to user (if configured)

### Escalation Message

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "orchestrator-master",
    "subject": "ESCALATION: BLOCKER: TASK-123 - [Description]",
    "priority": "urgent",
    "content": {
      "type": "blocker-report",
      "message": "ESCALATION: Original blocker report sent [time ago], no response received. Task remains blocked.",
      "task_id": "TASK-123",
      "severity": "critical",
      "original_report_time": "[timestamp]",
      "escalation_level": 1,
      "request": "Please acknowledge and provide resolution path."
    }
  }'
```

## 3.5 Examples

### Example 1: Missing API Credentials

**Situation**: Cannot access external API due to missing credentials.

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "orchestrator-master",
    "subject": "BLOCKER: TASK-123 - Missing PaymentGateway API Credentials",
    "priority": "urgent",
    "content": {
      "type": "blocker-report",
      "message": "Cannot proceed with PaymentGateway integration - API credentials not found.",
      "task_id": "TASK-123",
      "severity": "critical",
      "blocker_type": "missing-credentials",
      "description": "The task requires integration with PaymentGateway API. I searched the codebase, environment variables, and secrets store but found no credentials. API returns 401 Unauthorized.",
      "impact": "Cannot implement, test, or verify any API integration functionality. Task is 100% blocked.",
      "attempted_resolutions": [
        "Searched .env files for API keys",
        "Checked secrets manager (vault)",
        "Searched codebase for existing credentials",
        "Checked project documentation"
      ],
      "proposed_solutions": [
        "Provide API credentials via secrets manager",
        "Provide test/sandbox credentials for development",
        "Grant access to credentials documentation"
      ],
      "unblocking_requirements": "PaymentGateway API key and secret",
      "progress_before_block": "Unit tests written with mocks, local logic implemented, ready for real integration"
    }
  }'
```

### Example 2: External Service Down

**Situation**: Required external service is unavailable.

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "orchestrator-master",
    "subject": "BLOCKER: TASK-456 - AuthService Down",
    "priority": "urgent",
    "content": {
      "type": "blocker-report",
      "message": "AuthService is returning 503 errors. Cannot test authentication flow.",
      "task_id": "TASK-456",
      "severity": "high",
      "blocker_type": "external-dependency",
      "description": "The AuthService at auth.internal.example.com returns 503 Service Unavailable. Checked service status page - no reported outages. Issue started approximately 30 minutes ago.",
      "impact": "Cannot test any authentication functionality. Can continue writing code but cannot verify it works.",
      "attempted_resolutions": [
        "Verified service URL is correct",
        "Checked network connectivity",
        "Tried different endpoints on same service",
        "Checked service status page"
      ],
      "proposed_solutions": [
        "Wait for service recovery",
        "Use staging AuthService if available",
        "Contact infrastructure team for status"
      ],
      "unblocking_requirements": "AuthService restored to operational status",
      "progress_before_block": "Authentication module 80% complete, blocked on integration testing"
    }
  }'
```

### Example 3: Technical Impossibility

**Situation**: Requested feature cannot be implemented as specified.

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "orchestrator-master",
    "subject": "BLOCKER: TASK-789 - Technical Impossibility in Specification",
    "priority": "urgent",
    "content": {
      "type": "blocker-report",
      "message": "The specified requirement is technically impossible with the current architecture.",
      "task_id": "TASK-789",
      "severity": "critical",
      "blocker_type": "technical-impossibility",
      "description": "Task requires real-time synchronous response within 50ms, but the required data source has minimum latency of 200ms. This is a fundamental constraint of the external system that cannot be reduced.",
      "impact": "Cannot implement the feature as specified. Either the timing requirement or the data source must change.",
      "attempted_resolutions": [
        "Researched data source performance limits",
        "Tested with caching (still exceeds 50ms on cache miss)",
        "Consulted data source documentation",
        "Tested connection pooling and optimization"
      ],
      "proposed_solutions": [
        "Relax timing requirement to 250ms",
        "Use cached/stale data for real-time response",
        "Change to asynchronous pattern",
        "Use alternative data source"
      ],
      "unblocking_requirements": "Revised specification with achievable timing requirements"
    }
  }'
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `Connection refused` | AI Maestro not running | Start AI Maestro immediately |
| `EOA not responding` | EOA session inactive | Escalate to user directly |
| `Message delivery failed` | Network issue | Retry immediately, max 3 times |

### Critical Blocker Protocol

For critical severity blockers:

1. Send blocker report immediately
2. Set timer for 15 minutes
3. If no response, send escalation
4. If still no response after 30 minutes, notify user directly (if possible)
5. Document all attempts and timestamps

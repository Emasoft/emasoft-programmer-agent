---
name: op-propose-improvement
description: Propose design or task improvements to EOA during implementation.
parent-skill: epa-orchestrator-communication
workflow-step: "Step 15"
message-type: improvement-proposal
priority: normal
---

# Operation: Propose Improvement

This operation describes how to propose design or task improvements to the Emasoft Orchestrator Agent (EOA) when you identify opportunities to enhance the implementation during development.

## Table of Contents

- 4.1 When to Propose Improvements
- 4.2 Improvement Proposal Format
- 4.3 Justification Requirements
- 4.4 Awaiting Approval
- 4.5 Examples

## 4.1 When to Propose Improvements

Propose improvements to EOA in these situations:

| Situation | Appropriate Action |
|-----------|-------------------|
| **Better algorithm exists** | Propose if significantly improves performance |
| **Simpler implementation possible** | Propose if reduces complexity without losing functionality |
| **Security enhancement identified** | Always propose security improvements |
| **Code reuse opportunity** | Propose if existing code can be leveraged |
| **API design improvement** | Propose if improves usability or consistency |
| **Test coverage gap** | Propose additional test cases |
| **Documentation improvement** | Propose if unclear requirements found |
| **Architecture enhancement** | Propose if improves maintainability |

### What NOT to Propose

| Situation | Why Not |
|-----------|---------|
| **Personal preference** | Proposals must have objective justification |
| **Scope expansion** | Do not add features not requested |
| **Technology change** | Do not propose stack changes without strong justification |
| **Minor style changes** | Follow existing project conventions |
| **Changes outside task scope** | Focus on assigned task only |

### Proposal Threshold

Only propose improvements that meet these criteria:

1. **Measurable benefit**: Can quantify the improvement (performance, LOC, complexity)
2. **Low risk**: Does not introduce significant new risks
3. **Reasonable effort**: Implementation effort is justified by benefit
4. **Reversible**: Can revert if improvement does not work out

## Prerequisites

Before proposing an improvement:

1. **Complete initial analysis**: Understand the full scope of the task
2. **Identify the improvement**: Have a clear, specific proposal
3. **Assess impact**: Understand how it affects the task
4. **Prepare justification**: Have data or reasoning to support proposal
5. **Consider alternatives**: Know why this improvement is best

## 4.2 Improvement Proposal Format

Structure your improvement proposal with these components:

```json
{
  "to": "orchestrator-master",
  "subject": "PROPOSAL: [Task ID] - [Brief Description]",
  "priority": "normal",
  "content": {
    "type": "improvement-proposal",
    "message": "[Brief summary of proposed improvement]",
    "task_id": "[TASK-ID]",
    "proposal_type": "[proposal-type]",
    "current_approach": "[Description of current/specified approach]",
    "proposed_approach": "[Description of proposed improvement]",
    "justification": {
      "benefits": [
        "[Benefit 1]",
        "[Benefit 2]"
      ],
      "metrics": {
        "[metric_name]": "[before] -> [after]"
      },
      "risks": [
        "[Risk 1 and mitigation]"
      ]
    },
    "effort_estimate": "[Time to implement improvement]",
    "impact_on_timeline": "[How this affects delivery]",
    "alternatives_considered": [
      {
        "approach": "[Alternative approach]",
        "why_rejected": "[Reason not chosen]"
      }
    ],
    "approval_required": true,
    "will_proceed_if_no_response": "[yes/no]",
    "auto_proceed_after": "[time, if applicable]"
  }
}
```

### Message Components

| Field | Description | Required |
|-------|-------------|----------|
| `task_id` | The identifier of the task | Yes |
| `proposal_type` | Category of improvement | Yes |
| `current_approach` | What is currently specified | Yes |
| `proposed_approach` | What you propose instead | Yes |
| `justification` | Benefits, metrics, and risks | Yes |
| `effort_estimate` | Time to implement | Yes |
| `impact_on_timeline` | Effect on delivery | Yes |
| `alternatives_considered` | Other options evaluated | No |
| `approval_required` | Whether to wait for approval | Yes |
| `will_proceed_if_no_response` | Auto-proceed behavior | Yes |
| `auto_proceed_after` | Time before auto-proceeding | If auto-proceed is yes |

### Proposal Types

Use these standardized proposal type values:

| Type | Description |
|------|-------------|
| `algorithm-improvement` | Better algorithm for same result |
| `simplification` | Simpler implementation |
| `security-enhancement` | Security improvement |
| `code-reuse` | Leverage existing code |
| `api-improvement` | Better API design |
| `test-enhancement` | Additional test coverage |
| `documentation-improvement` | Clearer documentation |
| `architecture-enhancement` | Structural improvement |
| `performance-optimization` | Speed or resource improvement |

## 4.3 Justification Requirements

Every proposal must include strong justification:

### Quantitative Justification (Preferred)

Provide measurable data:

```json
"justification": {
  "benefits": [
    "Reduces query time from 2.3s to 0.4s (83% improvement)",
    "Reduces memory usage from 512MB to 128MB"
  ],
  "metrics": {
    "query_time": "2.3s -> 0.4s",
    "memory_usage": "512MB -> 128MB",
    "code_lines": "450 -> 280"
  },
  "risks": [
    "New algorithm requires additional testing - mitigated by comprehensive test suite"
  ]
}
```

### Qualitative Justification (When Metrics Unavailable)

Provide clear reasoning:

```json
"justification": {
  "benefits": [
    "Improves code readability by separating concerns",
    "Follows established project patterns",
    "Reduces coupling between modules"
  ],
  "metrics": {
    "cyclomatic_complexity": "15 -> 8",
    "coupling": "high -> low"
  },
  "risks": [
    "Requires updating three dependent modules - effort included in estimate"
  ]
}
```

## Procedure

Follow these steps to propose an improvement:

1. **Identify the improvement**: Note the specific enhancement opportunity
2. **Assess viability**: Confirm the improvement is feasible
3. **Gather justification**: Collect metrics or reasoning
4. **Consider alternatives**: Evaluate other approaches
5. **Estimate effort**: Calculate implementation time
6. **Compose proposal**: Use the format from section 4.2
7. **Send to EOA**: Execute the curl command
8. **Wait for response**: Do not implement until approved (unless auto-proceed)
9. **Implement if approved**: Proceed with the improvement
10. **Document the change**: Note the improvement in commit message

## Checklist

Use this checklist before sending an improvement proposal:

- [ ] The improvement has measurable benefits
- [ ] I have data or strong reasoning to justify it
- [ ] I have considered alternative approaches
- [ ] I have assessed the risks
- [ ] The effort is reasonable for the benefit
- [ ] I have estimated the implementation time
- [ ] I have noted the impact on timeline
- [ ] I have specified approval requirements
- [ ] The message follows the required format
- [ ] The subject line includes PROPOSAL prefix

## 4.4 Awaiting Approval

### Approval Required (Default)

For significant improvements, wait for EOA approval:

```json
"approval_required": true,
"will_proceed_if_no_response": "no"
```

**Behavior**: Continue with original approach if no response within 2 hours.

### Auto-Proceed for Minor Improvements

For minor, low-risk improvements:

```json
"approval_required": true,
"will_proceed_if_no_response": "yes",
"auto_proceed_after": "30 minutes"
```

**Behavior**: Proceed with improvement if no objection within specified time.

### Handling Approval

When EOA responds:

| Response | Action |
|----------|--------|
| Approved | Implement the improvement |
| Rejected | Continue with original approach |
| Modified | Implement EOA's modified version |
| Request more info | Provide additional details |

## 4.5 Examples

### Example 1: Algorithm Improvement

**Situation**: Found a more efficient algorithm.

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "orchestrator-master",
    "subject": "PROPOSAL: TASK-123 - Use Binary Search Instead of Linear Search",
    "priority": "normal",
    "content": {
      "type": "improvement-proposal",
      "message": "Proposing to use binary search instead of linear search for order lookup.",
      "task_id": "TASK-123",
      "proposal_type": "algorithm-improvement",
      "current_approach": "The task specifies iterating through the order list to find matching orders (linear search, O(n) complexity).",
      "proposed_approach": "Use binary search on the sorted order list (O(log n) complexity). The order list is already sorted by order_id.",
      "justification": {
        "benefits": [
          "Reduces search time from O(n) to O(log n)",
          "For 100,000 orders: reduces from 100,000 to 17 comparisons",
          "No additional memory required"
        ],
        "metrics": {
          "time_complexity": "O(n) -> O(log n)",
          "comparisons_100k": "100000 -> 17",
          "memory": "no change"
        },
        "risks": [
          "Requires list to remain sorted - already guaranteed by existing code"
        ]
      },
      "effort_estimate": "30 minutes",
      "impact_on_timeline": "No delay - within original estimate",
      "alternatives_considered": [
        {
          "approach": "Hash table lookup",
          "why_rejected": "Would require additional memory for hash table, binary search sufficient"
        }
      ],
      "approval_required": true,
      "will_proceed_if_no_response": "yes",
      "auto_proceed_after": "30 minutes"
    }
  }'
```

### Example 2: Code Reuse Opportunity

**Situation**: Found existing code that can be reused.

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "orchestrator-master",
    "subject": "PROPOSAL: TASK-456 - Reuse Existing Validation Module",
    "priority": "normal",
    "content": {
      "type": "improvement-proposal",
      "message": "Proposing to reuse existing InputValidator instead of writing new validation logic.",
      "task_id": "TASK-456",
      "proposal_type": "code-reuse",
      "current_approach": "Task describes implementing input validation from scratch for the new form handler.",
      "proposed_approach": "Reuse the existing InputValidator class from src/utils/validation.py. It already handles all required validation types and is well-tested.",
      "justification": {
        "benefits": [
          "Reduces implementation time by 2 hours",
          "Leverages existing, tested code",
          "Maintains consistency with rest of codebase",
          "No new code to maintain"
        ],
        "metrics": {
          "new_code_lines": "~200 -> 10 (import and usage)",
          "time_saved": "2 hours",
          "test_coverage": "Already 95% covered"
        },
        "risks": [
          "None - existing module is stable and well-tested"
        ]
      },
      "effort_estimate": "15 minutes (vs 2 hours for new implementation)",
      "impact_on_timeline": "Saves 1.75 hours",
      "approval_required": true,
      "will_proceed_if_no_response": "yes",
      "auto_proceed_after": "30 minutes"
    }
  }'
```

### Example 3: Security Enhancement

**Situation**: Identified security improvement opportunity.

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "orchestrator-master",
    "subject": "PROPOSAL: TASK-789 - Add Input Sanitization for SQL Queries",
    "priority": "high",
    "content": {
      "type": "improvement-proposal",
      "message": "Proposing to add parameterized queries to prevent SQL injection.",
      "task_id": "TASK-789",
      "proposal_type": "security-enhancement",
      "current_approach": "The task specification uses string concatenation for SQL query building.",
      "proposed_approach": "Use parameterized queries with the database library'\''s built-in escaping.",
      "justification": {
        "benefits": [
          "Prevents SQL injection attacks",
          "Industry standard security practice",
          "No performance overhead"
        ],
        "metrics": {
          "security_risk": "high -> eliminated",
          "code_change": "minor refactor"
        },
        "risks": [
          "None - parameterized queries are strictly safer"
        ]
      },
      "effort_estimate": "45 minutes",
      "impact_on_timeline": "Adds 45 minutes but strongly recommended",
      "approval_required": true,
      "will_proceed_if_no_response": "no"
    }
  }'
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `Proposal rejected` | EOA did not approve | Continue with original approach |
| `No response` | EOA busy | Follow auto-proceed setting |
| `Request for more info` | Justification insufficient | Provide additional details |

### Handling Rejection

If your proposal is rejected:

1. Acknowledge the decision
2. Continue with original approach
3. Do not re-propose the same improvement
4. Document the decision for future reference

### Handling Modification

If EOA modifies your proposal:

1. Acknowledge the modification
2. Implement the modified version
3. Report any issues with the modification

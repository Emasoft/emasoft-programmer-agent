# AGENT_OPERATIONS.md - EPA Programmer

**Single Source of Truth for Emasoft Programmer Agent (EPA) Operations**

---

## 1. Session Naming Convention

### Format
```
<project>-programmer-<number>
```

### Examples
- `svgbbox-programmer-001` - First programmer agent for svgbbox project
- `svgbbox-programmer-002` - Second programmer agent for svgbbox project
- `maestro-programmer-001` - Programmer agent for AI Maestro project
- `skillsfactory-programmer-003` - Third programmer agent for Skills Factory

### Rules
- **Project**: Use kebab-case project identifier (must match project name)
- **Type**: Always use `programmer` (identifies role)
- **Number**: Zero-padded 3-digit sequence (001, 002, 003, ...)
- **AI Maestro Identity**: Session name = registry identity for messaging
- **Chosen By**: ECOS (Chief of Staff) when spawning the programmer
- **NO `epa-` prefix**: Unlike EOA/ECOS/EIA/EAMA, EPA sessions use project-based naming

### Why This Matters
The session name is registered in AI Maestro's agent registry and becomes the messaging address for inter-agent communication. The `<project>-programmer-<number>` format allows multiple programmer agents to work on the same project without name collisions.

### Sequential Assignment
ECOS maintains a counter for each project to ensure unique numbering:
- First EPA for svgbbox → `svgbbox-programmer-001`
- Second EPA for svgbbox → `svgbbox-programmer-002`
- First EPA for maestro → `maestro-programmer-001`

---

## 2. Plugin Paths

### Environment Variables

| Variable | Value | Usage |
|----------|-------|-------|
| `${CLAUDE_PLUGIN_ROOT}` | Points to `emasoft-programmer-agent/` | Use in scripts, hooks, skill references |
| `${CLAUDE_PROJECT_DIR}` | Points to `~/agents/<session-name>/` | Project root for the programmer instance |

### Local Plugin Path Structure
```
~/agents/<project>-programmer-<number>/.claude/plugins/emasoft-programmer-agent/
```

**Example**:
```
~/agents/svgbbox-programmer-001/.claude/plugins/emasoft-programmer-agent/
```

### How Plugin is Loaded
The EPA instance is launched with `--plugin-dir` flag:
```bash
--plugin-dir ~/agents/$SESSION_NAME/.claude/plugins/emasoft-programmer-agent
```

This loads ONLY the emasoft-programmer-agent plugin into that Claude Code session.

---

## 3. Agent Directory Structure

### Complete Layout
```
~/agents/<project>-programmer-<number>/
├── .claude/
│   ├── plugins/
│   │   └── emasoft-programmer-agent/  ← Plugin loaded via --plugin-dir
│   │       ├── .claude-plugin/
│   │       │   └── plugin.json
│   │       ├── agents/
│   │       │   └── epa-programmer-main-agent.md
│   │       ├── skills/  ← Empty (uses globally installed skills)
│   │       ├── hooks/
│   │       │   └── hooks.json
│   │       └── scripts/
│   └── settings.json  ← Session-specific settings
├── work/  ← Working directory for assigned tasks
├── reports/  ← Task completion reports, blocker reports
└── logs/  ← Session logs
```

### Directory Purposes

| Directory | Purpose |
|-----------|---------|
| `.claude/plugins/` | Plugin installation location |
| `work/` | Task implementation files, scratch work |
| `reports/` | Markdown reports for EOA/ECOS (task completion, blockers, test results) |
| `logs/` | Session activity logs, AI Maestro message logs |

---

## 4. How EPA is Created

### ECOS Spawns EPA (via EOA delegation)
The ECOS (Chief of Staff) agent spawns EPA instances using the `aimaestro-agent.sh` script, typically after EOA requests implementer capacity:

```bash
SESSION_NAME="<project>-programmer-001"

aimaestro-agent.sh create $SESSION_NAME \
  --dir ~/agents/$SESSION_NAME \
  --task "Implement feature X for <project>" \
  -- --dangerously-skip-permissions --chrome --add-dir /tmp \
  --plugin-dir ~/agents/$SESSION_NAME/.claude/plugins/emasoft-programmer-agent \
  --agent epa-programmer-main-agent
```

### Breakdown

| Flag | Value | Purpose |
|------|-------|---------|
| `--dir` | `~/agents/$SESSION_NAME` | Sets working directory for the programmer |
| `--task` | Task description | Initial task prompt (from EOA or ECOS) |
| `--dangerously-skip-permissions` | - | Skip permission dialogs for automation |
| `--chrome` | - | Enable Chrome DevTools MCP |
| `--add-dir` | `/tmp` | Add /tmp as allowed working directory |
| `--plugin-dir` | `~/agents/$SESSION_NAME/.claude/plugins/emasoft-programmer-agent` | Load EPA plugin |
| `--agent` | `epa-programmer-main-agent` | Start with this agent from the plugin |

### Pre-Spawn Setup
Before spawning, ECOS must:
1. Copy the plugin to `~/agents/$SESSION_NAME/.claude/plugins/emasoft-programmer-agent/`
2. Register the session name in AI Maestro
3. Create initial task description (from EOA task breakdown)
4. Set up working directories
5. Clone project repository into `work/` directory

---

## 5. Plugin Mutual Exclusivity

### Critical Rule: One Plugin Per Agent Instance

Each EPA instance has **ONLY** the `emasoft-programmer-agent` plugin loaded.

**EPA CANNOT access**:
- `emasoft-chief-of-staff-agent` (ECOS) skills
- `emasoft-orchestrator-agent` (EOA) skills
- `emasoft-integrator-agent` (EIA) skills
- `emasoft-architect-agent` (EAA) skills
- `emasoft-assistant-manager-agent` (EAMA) skills

### Why This Matters
Each plugin defines a **role boundary**. EPA's job is to **implement tasks**, not to:
- Make architectural decisions (EAA's job)
- Orchestrate other agents (EOA's job)
- Coordinate multiple orchestrators (ECOS's job)
- Integrate and review code (EIA's job)
- Manage user communication (EAMA's job)

### Globally Installed Skills
EPA relies on **globally installed skills** (not plugin-specific skills) for implementation guidance:
- Skills installed in `~/.claude/skills/`
- Generic programming skills (TDD, refactoring, testing patterns)
- Language-specific skills (Python, TypeScript, Go, Rust)
- Tool-specific skills (Git, Docker, pytest, Jest)

**Why global skills?**
- EPA is a general-purpose implementer (not domain-specific)
- Skills are shared across all programmer instances
- Reduces plugin size and maintenance burden

### SERENA MCP for Code Navigation
EPA uses the globally configured **SERENA MCP** for code navigation and analysis:
- Symbol search
- Definition lookup
- References finding
- Call hierarchy
- Type hierarchy

**SERENA is NOT part of the EPA plugin** - it's a globally installed MCP server.

### Cross-Role Communication
All cross-role communication happens via **AI Maestro messages**, not skill sharing.

**Example**:
```
EPA encounters architectural question
→ EPA sends blocker message to EOA
→ EOA escalates to ECOS
→ ECOS delegates to EAA
→ EAA responds with architectural guidance
→ ECOS forwards to EOA
→ EOA forwards to EPA
→ EPA resumes implementation
```

---

## 6. AI Maestro Communication

### Sending Messages from EPA

#### To EOA (Orchestrator)
```bash
curl -X POST "$AIMAESTRO_API/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "svgbbox-programmer-001",
    "to": "eoa-svgbbox-orchestrator",
    "subject": "Task Completed: calculateBBox() implementation",
    "priority": "normal",
    "content": {
      "type": "completion",
      "message": "Implemented calculateBBox() with unit tests. PR #43 created. See report at ~/agents/svgbbox-programmer-001/reports/task-complete-2026-02-06.md"
    }
  }'
```

#### To ECOS (Chief of Staff) - For Blockers Only
```bash
curl -X POST "$AIMAESTRO_API/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "svgbbox-programmer-001",
    "to": "ecos-chief-of-staff-one",
    "subject": "BLOCKER: API dependency unavailable",
    "priority": "urgent",
    "content": {
      "type": "blocker",
      "message": "Cannot implement calculateBBox() - dependency on external API not available. See blocker report at ~/agents/svgbbox-programmer-001/reports/blocker-2026-02-06.md"
    }
  }'
```

#### To EIA (Integrator) - For Review Requests
```bash
curl -X POST "$AIMAESTRO_API/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "svgbbox-programmer-001",
    "to": "eia-integrator-one",
    "subject": "Review Request: PR #43",
    "priority": "high",
    "content": {
      "type": "review-request",
      "message": "PR #43 ready for review. Implements calculateBBox() with 15 unit tests. All tests passing."
    }
  }'
```

### Reading Messages (EPA Inbox)

```bash
# Check unread count
curl -s "$AIMAESTRO_API/api/messages?agent=$SESSION_NAME&action=unread-count"

# List all unread messages
curl -s "$AIMAESTRO_API/api/messages?agent=$SESSION_NAME&action=list&status=unread"

# Mark message as read
curl -X POST "$AIMAESTRO_API/api/messages" \
  -d '{"action":"mark-read","message_id":"<msg-id>"}'
```

### Message Priority Levels

| Priority | When to Use | Response Time |
|----------|-------------|---------------|
| `urgent` | Blocker, cannot proceed | Immediate |
| `high` | Clarification needed to continue | Within 5 minutes |
| `normal` | Task completion, progress update | Within 15 minutes |
| `low` | FYI, non-actionable information | When convenient |

### Content Types

| Type | Purpose | Example |
|------|---------|---------|
| `completion` | Task completed | "Implemented feature X, PR created" |
| `blocker` | Blocking issue, cannot proceed | "API dependency missing" |
| `request` | Information request | "Need clarification on requirement Y" |
| `progress` | Progress update (mid-task) | "50% complete, tests passing" |
| `report` | Detailed report | "Test results: 15/15 passing" |

---

## 7. EPA Responsibilities

### Core Responsibilities

#### 1. Receive Tasks from EOA
- EOA sends task assignment via AI Maestro message
- EPA acknowledges receipt
- EPA validates task clarity and completeness
- EPA requests clarification if task is ambiguous

#### 2. Execute Tasks (Implementation)
- Write production code per task specification
- Follow TDD workflow (tests first, implementation second)
- Use SERENA MCP for code navigation
- Use globally installed skills for implementation guidance
- Commit changes frequently with descriptive messages

#### 3. Write Tests
- Unit tests for all new functions
- Integration tests for feature workflows
- Edge case coverage
- Test coverage report (aim for >80%)

#### 4. Report Blockers Immediately
- If blocked, send blocker message to EOA within 5 minutes
- Include detailed blocker report in `reports/` directory
- Propose potential solutions if possible
- Wait for EOA/ECOS guidance (do NOT implement workarounds)

#### 5. Create Pull Requests
- Create PR when task implementation complete
- PR title: `[Project] Feature/Fix: Brief description`
- PR body: Include task reference, test results, implementation notes
- Request review from EIA via AI Maestro message
- **EPA does NOT merge PRs** - only EIA can merge

#### 6. Update Task Status
- EPA does NOT update GitHub Projects directly
- EPA reports completion to EOA
- EOA updates kanban board

### What EPA Does NOT Do

| EPA Does NOT | Who Does It | Why |
|--------------|-------------|-----|
| Assign tasks to other agents | EOA | Orchestration is orchestrator's role |
| Merge pull requests | EIA | Code integration is integrator's role |
| Make architectural decisions | EAA | Architecture is architect's role |
| Update kanban boards | EOA | Task tracking is orchestrator's role |
| Communicate with end users | EAMA | User comms is assistant manager's role |
| Spawn other programmer agents | ECOS | Capacity management is chief of staff's role |

### Workflow Pattern

```
EOA → [Task Assignment] → EPA
EPA → [Acknowledge] → EOA
    ↓ (implement)
EPA → [Progress Update] → EOA
    ↓ (tests passing)
EPA → [PR Created] → EIA (review request)
    ↓ (wait for review)
EIA → [Review Complete] → EPA (via EOA)
    ↓ (EOA merges PR)
EPA → [Task Complete] → EOA
EOA → [Kanban Updated] → GitHub
```

### Blocker Pattern

```
EOA → [Task Assignment] → EPA
EPA → [Acknowledge] → EOA
    ↓ (encounter blocker)
EPA → [BLOCKER Report] → EOA
EOA → [Escalate] → ECOS
ECOS → [Resolution] → EOA
EOA → [Unblock] → EPA
EPA → [Resume Implementation]
```

---

## 8. Wake/Hibernate/Terminate

### Session Lifecycle Management

EPA session lifecycle is managed by ECOS (or EOA delegated by ECOS) via `aimaestro-agent.sh`.

### Wake (Resume Session)

```bash
aimaestro-agent.sh wake <project>-programmer-<number>
```

**When to wake**:
- New task assigned by EOA
- Blocker resolved by ECOS/EAA
- Review feedback received from EIA

**What happens**:
- Tmux session brought to foreground
- EPA checks AI Maestro inbox
- EPA resumes implementation work

### Hibernate (Pause Session)

```bash
aimaestro-agent.sh hibernate <project>-programmer-<number>
```

**When to hibernate**:
- Task completed, waiting for review
- Blocker reported, waiting for resolution
- No active work (implementer idle)

**What happens**:
- Tmux session detached (keeps running in background)
- EPA continues monitoring via hooks
- EPA can still receive AI Maestro messages

### Terminate (End Session)

```bash
aimaestro-agent.sh terminate <project>-programmer-<number>
```

**When to terminate**:
- Task completed and PR merged
- No more tasks assigned for this programmer
- ECOS issues termination directive
- Project milestone reached

**What happens**:
- Tmux session killed
- EPA sends final completion report to EOA
- AI Maestro registry entry marked as terminated
- Working directory preserved at `~/agents/<project>-programmer-<number>/`

### Auto-Hibernate Feature

EPA can auto-hibernate after submitting PR for review:

```bash
# In EPA's configuration
AUTO_HIBERNATE_AFTER_PR=true
AUTO_HIBERNATE_TIMEOUT=600  # 10 minutes of inactivity
```

This prevents EPA from consuming resources while waiting for review feedback.

---

## 9. Troubleshooting

### Common Issues

#### Issue: EPA cannot access EOA skills
**Symptom**: `Skill 'eoa-orchestration-patterns' not found`
**Cause**: Plugin mutual exclusivity - EPA doesn't have EOA plugin loaded
**Solution**: Use AI Maestro messaging to request EOA assistance

#### Issue: AI Maestro message not received
**Symptom**: EOA didn't get task completion notification
**Cause**: Wrong session name or API endpoint
**Solution**: Verify session name in registry, check `$AIMAESTRO_API` environment variable

#### Issue: SERENA MCP not available
**Symptom**: `SERENA MCP server not found` or symbol search fails
**Cause**: SERENA MCP not configured globally, or server not running
**Solution**:
1. Check MCP server configuration in `~/.claude/mcp.json`
2. Verify SERENA server is running: `ps aux | grep serena`
3. Restart MCP server if needed

#### Issue: Globally installed skills not found
**Symptom**: `Skill 'tdd-patterns' not found`
**Cause**: Skills not installed in `~/.claude/skills/`
**Solution**:
1. Verify skills directory: `ls ~/.claude/skills/`
2. Install missing skills: `claude skill install <skill-name>`

#### Issue: Cannot commit to repository
**Symptom**: `Git authentication failed` or `Permission denied`
**Cause**: Git credentials not configured in EPA session
**Solution**:
1. Configure git: `git config --local user.name "EPA Bot"`
2. Configure email: `git config --local user.email "epa@example.com"`
3. Verify SSH key or token access

#### Issue: PR creation fails
**Symptom**: `GitHub API error: Unauthorized`
**Cause**: GitHub token not available or expired
**Solution**:
1. Verify `GITHUB_TOKEN` environment variable
2. Check token permissions (needs `repo` scope)
3. Generate new token if expired

#### Issue: EPA session terminated unexpectedly
**Symptom**: Tmux session not found
**Cause**: System restart, manual kill, or out-of-memory
**Solution**:
1. Check system logs: `journalctl -u tmux`
2. ECOS recreates session with `aimaestro-agent.sh create`
3. Restore work from `~/agents/<project>-programmer-<number>/work/`

#### Issue: EPA stuck waiting for review
**Symptom**: PR submitted but no response from EIA
**Cause**: EIA session hibernated or terminated
**Solution**:
1. EPA sends reminder message to EOA
2. EOA checks EIA status
3. EOA wakes or spawns EIA if needed

---

## 10. References

### Related Documentation
- [EOA_AGENT_OPERATIONS.md](../../emasoft-orchestrator-agent/docs/AGENT_OPERATIONS.md) - Orchestrator operations
- [EIA_AGENT_OPERATIONS.md](../../emasoft-integrator-agent/docs/AGENT_OPERATIONS.md) - Integrator operations
- [ECOS_AGENT_OPERATIONS.md](../../emasoft-chief-of-staff-agent/docs/AGENT_OPERATIONS.md) - Chief of Staff operations
- [EAA_AGENT_OPERATIONS.md](../../emasoft-architect-agent/docs/AGENT_OPERATIONS.md) - Architect operations

### External References
- [AI Maestro API Documentation](https://github.com/Emasoft/ai-maestro/blob/main/docs/API.md)
- [Claude Code Plugin System](https://docs.anthropic.com/claude/docs/plugins)
- [SERENA MCP Documentation](https://github.com/Emasoft/serena-mcp)
- [GitHub Pull Requests API](https://docs.github.com/en/rest/pulls)

---

**Document Version**: 1.0.0
**Last Updated**: 2026-02-06
**Maintained By**: claude-skills-factory

---
name: epa-github-operations
description: Git and GitHub operations. Use for branching, commits, PRs.
license: Apache-2.0
compatibility: Requires gh CLI authenticated.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: epa-programmer-main-agent
workflow-instruction: "Steps 19, 21, 22"
procedure: "proc-complete-task, proc-handle-failed-pr"
---

# EPA GitHub Operations

This skill provides procedures for Git and GitHub operations within the Emasoft Programmer Agent workflow. Use these operations for repository management, branching, commits, and pull request lifecycle.

## When to Use This Skill

- **Cloning/forking**: When starting work on a new project or task
- **Branching**: When beginning implementation of a task
- **Committing**: When saving incremental progress or completing work
- **Pull Requests**: When submitting completed work for review (Step 19)
- **Review Response**: When addressing EIA review comments (Step 21)
- **PR Updates**: When pushing fixes after PR rejection (Step 22)

## Prerequisites

1. **gh CLI installed and authenticated**: Run `gh auth status` to verify
2. **Git configured**: User name and email set
3. **Repository access**: Read/write permissions to target repository

## Operations Reference

### Repository Setup

| Operation | File | When to Use |
|-----------|------|-------------|
| Clone Repository | [op-clone-repository.md](references/op-clone-repository.md) | Initial project setup, forking upstream repos |
| Create Feature Branch | [op-create-feature-branch.md](references/op-create-feature-branch.md) | Starting work on a new task |

**Table of Contents - op-clone-repository.md:**
- 1.1 When to clone vs fork
- 1.2 Cloning with gh CLI
- 1.3 Forking upstream repositories
- 1.4 Setting up remotes for forks
- 1.5 Verifying clone success

**Table of Contents - op-create-feature-branch.md:**
- 2.1 Branch naming conventions
- 2.2 Creating branch from main
- 2.3 Switching to existing branches
- 2.4 Pushing new branch to remote

### Commit Operations

| Operation | File | When to Use |
|-----------|------|-------------|
| Commit Changes | [op-commit-changes.md](references/op-commit-changes.md) | Saving progress with meaningful messages |

**Table of Contents - op-commit-changes.md:**
- 3.1 Staging changes selectively
- 3.2 Commit message format
- 3.3 Conventional commits syntax
- 3.4 Amending commits (when safe)
- 3.5 Verifying commit success

### Pull Request Lifecycle

| Operation | File | When to Use |
|-----------|------|-------------|
| Create Pull Request | [op-create-pull-request.md](references/op-create-pull-request.md) | Submitting completed task for review (Step 19) |
| Respond to Review | [op-respond-to-review.md](references/op-respond-to-review.md) | Addressing EIA review comments (Step 21) |
| Update PR with Fixes | [op-update-pr-with-fixes.md](references/op-update-pr-with-fixes.md) | Pushing fixes after rejection (Step 22) |

**Table of Contents - op-create-pull-request.md:**
- 4.1 Preparing branch for PR
- 4.2 Writing PR title and description
- 4.3 Creating PR with gh CLI
- 4.4 Setting reviewers and labels
- 4.5 Linking to issues

**Table of Contents - op-respond-to-review.md:**
- 5.1 Reading review comments
- 5.2 Understanding rejection reasons
- 5.3 Addressing specific feedback
- 5.4 Replying to review comments
- 5.5 Requesting re-review

**Table of Contents - op-update-pr-with-fixes.md:**
- 6.1 Making requested changes
- 6.2 Committing fixes
- 6.3 Pushing updates to PR branch
- 6.4 Updating PR description
- 6.5 Notifying reviewer of updates

## Quick Reference

### Branch Naming Convention

```
<type>/<issue-number>-<short-description>
```

Examples:
- `feature/123-add-user-auth`
- `fix/456-resolve-memory-leak`
- `refactor/789-extract-utils`

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

### PR Title Format

```
<type>(<scope>): <short description>
```

Example: `feat(auth): add OAuth2 login support`

## Checklist - Full GitHub Workflow

- [ ] Clone or fork repository
- [ ] Create feature branch with proper naming
- [ ] Make changes and commit incrementally
- [ ] Push branch to remote
- [ ] Create pull request with description
- [ ] Address review comments if rejected
- [ ] Push fixes and request re-review

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `gh: command not found` | gh CLI not installed | Install with `brew install gh` |
| `gh auth login` required | Not authenticated | Run `gh auth login` |
| `Permission denied` | No write access | Request access or fork repository |
| `Branch already exists` | Branch name collision | Delete old branch or use different name |
| `Merge conflicts` | Diverged from main | Rebase or merge main into branch |

## Related Skills

- **epa-orchestrator-communication**: For messaging EIA about PR status
- **epa-code-implementation**: For making the actual code changes
- **epa-testing-validation**: For running tests before PR

## See Also

- [GitHub CLI Manual](https://cli.github.com/manual/)
- [Conventional Commits](https://www.conventionalcommits.org/)

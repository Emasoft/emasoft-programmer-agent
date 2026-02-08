---
name: epa-project-setup
description: Setup project configuration and tooling. Use when starting work on new project.
license: MIT
compatibility: Requires SERENA MCP activated.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: epa-programmer-main-agent
user-invocable: false
workflow-instruction: "Step 17 (first task)"
procedure: "proc-execute-task"
---

# EPA Project Setup Skill

This skill provides procedures for setting up project configuration and tooling when starting work on a new project. It covers language detection, package manager initialization, dependency installation, linting configuration, testing framework setup, and SERENA MCP activation.

## Supported Languages

| Language | Package Manager | Linter | Testing |
|----------|-----------------|--------|---------|
| Python | uv | ruff, mypy | pytest |
| JavaScript/TypeScript | bun, pnpm | eslint | jest, vitest |
| Rust | cargo | clippy | cargo test |
| Go | go mod | golint | go test |
| .NET | dotnet | - | dotnet test |
| C/C++ | cmake, make | clang-tidy | gtest |
| Objective-C | xcodebuild | - | XCTest |
| Swift | swift, xcodebuild | swiftlint | XCTest |

## When to Use This Skill

Use this skill when:
- Starting work on a new project for the first time
- The project lacks proper tooling configuration
- You need to set up a consistent development environment
- Onboarding to an existing project that needs tooling verification

## Prerequisites

Before using this skill:
1. Have access to the project directory
2. Have SERENA MCP available for activation
3. Know the target programming language (or be ready to detect it)

## Operations Reference

This skill provides the following operations. Read each operation file before executing its procedure.

### 1. Detect Project Language
**File**: [op-detect-project-language.md](references/op-detect-project-language.md)

Contents:
- 1.1 When to detect project language
- 1.2 File-based language detection patterns
- 1.3 Configuration file indicators
- 1.4 Fallback detection strategies
- 1.5 Multi-language project handling

### 2. Initialize Package Manager
**File**: [op-initialize-package-manager.md](references/op-initialize-package-manager.md)

Contents:
- 2.1 When to initialize package manager
- 2.2 Python: uv initialization
- 2.3 JavaScript/TypeScript: bun or pnpm initialization
- 2.4 Rust: cargo initialization
- 2.5 Go: go mod initialization
- 2.6 Other languages: initialization procedures

### 3. Install Dependencies
**File**: [op-install-dependencies.md](references/op-install-dependencies.md)

Contents:
- 3.1 When to install dependencies
- 3.2 Reading dependency files
- 3.3 Package manager specific install commands
- 3.4 Handling missing or outdated dependencies
- 3.5 Virtual environment management

### 4. Configure Linting
**File**: [op-configure-linting.md](references/op-configure-linting.md)

Contents:
- 4.1 When to configure linting
- 4.2 Python: ruff and mypy configuration
- 4.3 JavaScript/TypeScript: eslint configuration
- 4.4 Rust: clippy configuration
- 4.5 Other languages: linter setup

For ruff linter and formatter configuration, see [ruff-configuration-patterns.md](references/ruff-configuration-patterns.md):
- When to configure ruff for a new project
- Standard ruff.toml template for Emasoft projects
- What each rule set does and why it is enabled
- What each ignored rule means and why it is ignored
- Per-file ignore patterns and when to use them
- Formatter settings (quote style, indent, line endings)
- How to run ruff check and ruff format
- Customizing ruff for specific project types

### 5. Setup Testing Framework
**File**: [op-setup-testing-framework.md](references/op-setup-testing-framework.md)

Contents:
- 5.1 When to setup testing framework
- 5.2 Python: pytest configuration
- 5.3 JavaScript/TypeScript: jest or vitest configuration
- 5.4 Rust: cargo test configuration
- 5.5 Other languages: test framework setup

### 6. Activate SERENA MCP
**File**: [op-activate-serena-mcp.md](references/op-activate-serena-mcp.md)

Contents:
- 6.1 When to activate SERENA MCP
- 6.2 SERENA activation procedure
- 6.3 Verifying SERENA connection
- 6.4 SERENA tool availability check
- 6.5 Troubleshooting SERENA activation

## Standard Setup Procedure

Execute these operations in order for a complete project setup:

1. **Detect Language** - Run op-detect-project-language to identify the project language
2. **Initialize Package Manager** - Run op-initialize-package-manager for the detected language
3. **Install Dependencies** - Run op-install-dependencies to get all required packages
4. **Configure Linting** - Run op-configure-linting to enable code quality checks
5. **Setup Testing** - Run op-setup-testing-framework to enable test execution
6. **Activate SERENA** - Run op-activate-serena-mcp for code navigation

## Checklist

Use this checklist to track setup progress:

- [ ] Project language detected and confirmed
- [ ] Package manager initialized and verified
- [ ] All dependencies installed successfully
- [ ] Linting tools configured and tested
- [ ] Testing framework configured and verified
- [ ] SERENA MCP activated and responding

## Troubleshooting

### Package Manager Not Found

**Problem**: The expected package manager is not installed on the system.

**Solution**: Install the package manager first. See the specific operation file for installation instructions for each package manager.

### Dependency Installation Fails

**Problem**: Dependencies fail to install due to version conflicts or missing packages.

**Solution**: Check the op-install-dependencies.md file for troubleshooting steps specific to each package manager.

### Linter Configuration Errors

**Problem**: Linter fails to run or produces incorrect configuration errors.

**Solution**: Verify the linter configuration file format. See op-configure-linting.md for correct configuration templates.

### SERENA MCP Not Responding

**Problem**: SERENA MCP fails to activate or does not respond to commands.

**Solution**: See op-activate-serena-mcp.md for SERENA-specific troubleshooting steps.

### Multi-Language Project Setup

**Problem**: Project uses multiple languages and needs multiple toolchains.

**Solution**: Run the setup procedure for each language independently. Start with the primary language (usually the one with the entry point), then set up secondary languages.

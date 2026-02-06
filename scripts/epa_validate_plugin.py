#!/usr/bin/env python3
"""
Plugin Validator - Validate emasoft-programmer-agent plugin structure

This script validates:
1. Plugin manifest (plugin.json) structure
2. Agent definition
3. Skill structure
4. Hook configuration
5. Required files (LICENSE, README.md)
"""

import argparse
import json
import sys
from pathlib import Path
from typing import List


class ValidationResult:
    """Validation result tracker."""

    def __init__(self) -> None:
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.passed: List[str] = []

    def error(self, msg: str) -> None:
        """Add error."""
        self.errors.append(f"❌ ERROR: {msg}")

    def warning(self, msg: str) -> None:
        """Add warning."""
        self.warnings.append(f"⚠️  WARNING: {msg}")

    def success(self, msg: str) -> None:
        """Add success."""
        self.passed.append(f"✓ {msg}")

    def print_results(self, verbose: bool = False) -> int:
        """Print validation results."""
        if verbose and self.passed:
            print("\n=== PASSED CHECKS ===")
            for msg in self.passed:
                print(msg)

        if self.warnings:
            print("\n=== WARNINGS ===")
            for msg in self.warnings:
                print(msg)

        if self.errors:
            print("\n=== ERRORS ===")
            for msg in self.errors:
                print(msg)

        # Summary
        print("\n=== SUMMARY ===")
        print(f"Passed: {len(self.passed)}")
        print(f"Warnings: {len(self.warnings)}")
        print(f"Errors: {len(self.errors)}")

        # Exit code
        if self.errors:
            return 1
        elif self.warnings:
            return 2
        return 0

    def to_json(self) -> dict:
        """Return results as JSON."""
        return {
            "passed": len(self.passed),
            "warnings": len(self.warnings),
            "errors": len(self.errors),
            "details": {
                "passed": self.passed,
                "warnings": self.warnings,
                "errors": self.errors,
            },
        }


def validate_plugin(plugin_dir: Path, _verbose: bool = False) -> ValidationResult:
    """Validate plugin structure."""
    del _verbose  # Parameter kept for API compatibility
    result = ValidationResult()

    # Check plugin directory exists
    if not plugin_dir.exists():
        result.error(f"Plugin directory not found: {plugin_dir}")
        return result

    result.success(f"Plugin directory exists: {plugin_dir}")

    # Check plugin.json
    plugin_json = plugin_dir / ".claude-plugin" / "plugin.json"
    if not plugin_json.exists():
        result.error("plugin.json not found in .claude-plugin/")
        return result

    result.success("plugin.json exists")

    # Parse plugin.json
    try:
        with open(plugin_json) as f:
            manifest = json.load(f)
        result.success("plugin.json is valid JSON")
    except json.JSONDecodeError as e:
        result.error(f"plugin.json is invalid JSON: {e}")
        return result

    # Validate required fields
    required_fields = ["name", "version", "description", "author", "agents", "skills"]
    for field in required_fields:
        if field not in manifest:
            result.error(f"plugin.json missing required field: {field}")
        else:
            result.success(f"plugin.json has {field}")

    # Check name is correct
    if manifest.get("name") != "emasoft-programmer-agent":
        result.error(
            f"plugin.json name should be 'emasoft-programmer-agent', got: {manifest.get('name')}"
        )

    # Check agents field is array
    if "agents" in manifest:
        if not isinstance(manifest["agents"], list):
            result.error("plugin.json 'agents' must be an array")
        elif not manifest["agents"]:
            result.error("plugin.json 'agents' array is empty")
        else:
            result.success(f"plugin.json has {len(manifest['agents'])} agent(s)")

    # Check main agent file exists
    agent_file = plugin_dir / "agents" / "epa-programmer-main-agent.md"
    if not agent_file.exists():
        result.error("Main agent file not found: agents/epa-programmer-main-agent.md")
    else:
        result.success("Main agent file exists")

        # Validate agent frontmatter
        content = agent_file.read_text()
        if not content.startswith("---"):
            result.error("Agent file missing YAML frontmatter")
        else:
            result.success("Agent file has YAML frontmatter")

            # Check required frontmatter fields
            required_agent_fields = ["name", "description", "model", "skills"]
            for field in required_agent_fields:
                if f"{field}:" not in content.split("---")[1]:
                    result.warning(
                        f"Agent frontmatter may be missing field: {field}"
                    )

    # Check expected skill directories
    expected_skills = [
        "epa-task-execution",
        "epa-orchestrator-communication",
        "epa-github-operations",
        "epa-project-setup",
        "epa-handoff-management",
    ]

    skills_dir = plugin_dir / "skills"
    if not skills_dir.exists():
        result.error("skills/ directory not found")
    else:
        result.success("skills/ directory exists")

        for skill_name in expected_skills:
            skill_dir = skills_dir / skill_name
            if skill_dir.exists():
                result.success(f"Skill directory exists: {skill_name}")

                # Check SKILL.md
                skill_md = skill_dir / "SKILL.md"
                if skill_md.exists():
                    result.success(f"SKILL.md exists for {skill_name}")

                    # Check for frontmatter
                    content = skill_md.read_text()
                    if content.startswith("---"):
                        result.success(f"SKILL.md has frontmatter: {skill_name}")
                    else:
                        result.warning(
                            f"SKILL.md missing frontmatter: {skill_name}"
                        )
                else:
                    result.warning(f"SKILL.md not found for {skill_name}")
            else:
                result.warning(f"Skill directory not found: {skill_name}")

    # Check hooks.json
    hooks_json = plugin_dir / "hooks" / "hooks.json"
    if hooks_json.exists():
        try:
            with open(hooks_json) as f:
                json.load(f)
            result.success("hooks.json is valid JSON")
        except json.JSONDecodeError as e:
            result.error(f"hooks.json is invalid JSON: {e}")
    else:
        result.warning("hooks.json not found")

    # Check LICENSE file
    license_file = plugin_dir / "LICENSE"
    if license_file.exists():
        result.success("LICENSE file exists")
    else:
        result.warning("LICENSE file not found")

    # Check README.md
    readme_file = plugin_dir / "README.md"
    if readme_file.exists():
        result.success("README.md exists")
    else:
        result.warning("README.md not found")

    # Check scripts directory
    scripts_dir = plugin_dir / "scripts"
    if scripts_dir.exists():
        scripts = list(scripts_dir.glob("*.py"))
        result.success(f"Found {len(scripts)} Python script(s)")

        for script in scripts:
            content = script.read_text()
            if not content.startswith("#!/usr/bin/env python3"):
                result.warning(f"Script missing shebang: {script.name}")
    else:
        result.warning("scripts/ directory not found")

    return result


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Validate emasoft-programmer-agent plugin structure"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show all passed checks",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON",
    )
    parser.add_argument(
        "--plugin-dir",
        type=Path,
        help="Path to plugin directory (default: current directory's parent)",
    )

    args = parser.parse_args()

    # Determine plugin directory
    if args.plugin_dir:
        plugin_dir = args.plugin_dir
    else:
        # Assume we're running from scripts/ directory
        plugin_dir = Path(__file__).parent.parent

    if not args.json:
        print(f"Validating plugin: {plugin_dir}")
        print("=" * 60)

    result = validate_plugin(plugin_dir, args.verbose)

    if args.json:
        print(json.dumps(result.to_json(), indent=2))
        sys.exit(1 if result.errors else 0)
    else:
        exit_code = result.print_results(args.verbose)
        sys.exit(exit_code)


if __name__ == "__main__":
    main()

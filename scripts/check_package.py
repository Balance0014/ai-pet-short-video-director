#!/usr/bin/env python3
"""Check this public skill package without external dependencies or writes."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NAME = "ai-pet-short-video-director"
PLUGIN = ROOT / "plugin"
SKILL_DIR = PLUGIN / "skills" / NAME
REQUIRED = [
    "README.md",
    "LICENSE",
    ".claude-plugin/marketplace.json",
    "plugin/.claude-plugin/plugin.json",
    "plugin/README.md",
    "plugin/icon.png",
    f"plugin/skills/{NAME}/SKILL.md",
    f"plugin/skills/{NAME}/references/story.md",
    f"plugin/skills/{NAME}/references/direction.md",
    f"plugin/skills/{NAME}/references/generation.md",
    f"plugin/skills/{NAME}/references/review.md",
    f"plugin/skills/{NAME}/references/receipt.md",
    f"plugin/skills/{NAME}/examples/cat-shares-warm-mat.md",
    "evals/cases.json",
    "scripts/validate_receipt.py",
]
# The plugin folder is published on its own and must hold no executable code:
# no scripts, hooks, MCP or LSP servers, monitors, or bin/ executables.
PLUGIN_SUFFIXES = {".md", ".json", ".png"}
PLUGIN_FORBIDDEN = {"hooks", "bin", "monitors", ".mcp.json", ".lsp.json"}
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^]]+\]\(([^)]+)\)")


def load_json(relative: str, errors: list[str]) -> dict:
    try:
        data = json.loads((ROOT / relative).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        errors.append(f"invalid {relative}: {exc}")
        return {}
    if not isinstance(data, dict):
        errors.append(f"invalid {relative}: expected an object")
        return {}
    return data


def main() -> int:
    errors: list[str] = []
    for relative in REQUIRED:
        path = ROOT / relative
        if not path.is_file() or path.stat().st_size == 0:
            errors.append(f"missing or empty: {relative}")

    skill = SKILL_DIR / "SKILL.md"
    if skill.is_file():
        content = skill.read_text(encoding="utf-8")
        front = re.match(r"\A---\n(.*?)\n---\n", content, re.S)
        if not front:
            errors.append("SKILL.md needs YAML frontmatter")
        else:
            for key in ("name", "description"):
                if not re.search(rf"^{key}:\s*\S", front.group(1), re.M):
                    errors.append(f"frontmatter missing {key}")
            if not re.search(rf"^name:\s*{re.escape(SKILL_DIR.name)}\s*$", front.group(1), re.M):
                errors.append("skill name and folder name disagree")

    manifest = load_json("plugin/.claude-plugin/plugin.json", errors)
    if manifest:
        if manifest.get("name") != NAME:
            errors.append("plugin.json name and skill name disagree")
        for key in ("version", "description", "author", "license", "icon"):
            if not manifest.get(key):
                errors.append(f"plugin.json missing {key}")
        icon = manifest.get("icon")
        if isinstance(icon, str) and icon:
            icon_path = (PLUGIN / icon).resolve()
            if not icon.startswith("./") or PLUGIN.resolve() not in icon_path.parents:
                errors.append("plugin.json icon must be a ./ path inside plugin/")
            elif not icon_path.is_file() or icon_path.read_bytes()[:8] != b"\x89PNG\r\n\x1a\n":
                errors.append("plugin.json icon must point to a PNG file")

    marketplace = load_json(".claude-plugin/marketplace.json", errors)
    if marketplace:
        entries = [p for p in marketplace.get("plugins", []) if isinstance(p, dict)]
        if [(p.get("name"), p.get("source")) for p in entries] != [(NAME, "./plugin")]:
            errors.append("marketplace.json must list this plugin once with source ./plugin")

    for path in sorted(PLUGIN.rglob("*")):
        relative = path.relative_to(ROOT)
        if path.name in PLUGIN_FORBIDDEN:
            errors.append(f"plugin folder must not run code: {relative}")
        elif path.is_file() and path.name not in {".DS_Store", "LICENSE"} and path.suffix not in PLUGIN_SUFFIXES:
            errors.append(f"plugin folder may hold only Markdown, JSON, and PNG: {relative}")

    for path in ROOT.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(ROOT)
        if re.search(r"/Users/[^/]+/|[A-Za-z]:\\Users\\", text):
            errors.append(f"private absolute path in {relative}")
        for raw in MARKDOWN_LINK.findall(text):
            if raw.startswith(("http://", "https://", "#", "mailto:")):
                continue
            target = raw.split("#", 1)[0]
            if not target:
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                errors.append(f"broken local link in {relative}: {raw}")
            elif PLUGIN in path.parents and PLUGIN.resolve() not in resolved.parents:
                errors.append(f"link leaves the published plugin folder in {relative}: {raw}")

    cases_path = ROOT / "evals/cases.json"
    if cases_path.is_file():
        try:
            cases = json.loads(cases_path.read_text(encoding="utf-8"))["cases"]
            ids = [case["id"] for case in cases]
            if len(cases) < 4 or len(ids) != len(set(ids)):
                errors.append("eval cases need at least four unique IDs")
            for case in cases:
                if not case.get("prompt") or len(case.get("checks", [])) < 2:
                    errors.append(f"incomplete eval case: {case.get('id')}")
        except (ValueError, KeyError, TypeError) as exc:
            errors.append(f"invalid evals/cases.json: {exc}")

    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print("Package integrity passed. Creative behavior and media quality remain untested.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

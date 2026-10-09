#!/usr/bin/env python3
"""Check this public skill package without external dependencies or writes."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "SKILL.md",
    "README.md",
    "LICENSE",
    "references/story.md",
    "references/direction.md",
    "references/generation.md",
    "references/review.md",
    "references/receipt.md",
    "examples/cat-shares-warm-mat.md",
    "evals/cases.json",
    "scripts/validate_receipt.py",
]
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^]]+\]\(([^)]+)\)")


def main() -> int:
    errors: list[str] = []
    for relative in REQUIRED:
        path = ROOT / relative
        if not path.is_file() or path.stat().st_size == 0:
            errors.append(f"missing or empty: {relative}")

    skill = ROOT / "SKILL.md"
    if skill.is_file():
        content = skill.read_text(encoding="utf-8")
        front = re.match(r"\A---\n(.*?)\n---\n", content, re.S)
        if not front:
            errors.append("SKILL.md needs YAML frontmatter")
        else:
            for key in ("name", "description"):
                if not re.search(rf"^{key}:\s*\S", front.group(1), re.M):
                    errors.append(f"frontmatter missing {key}")
            if not re.search(r"^name:\s*ai-pet-short-video-director\s*$", front.group(1), re.M):
                errors.append("skill name and folder identity disagree")

    for path in ROOT.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(ROOT)
        if re.search(r"/Users/[^/]+/|[A-Za-z]:\\Users\\", text):
            errors.append(f"private absolute path in {relative}")
        for raw in MARKDOWN_LINK.findall(text):
            if raw.startswith(("http://", "https://", "#", "mailto:")):
                continue
            target = raw.split("#", 1)[0]
            if target and not (path.parent / target).resolve().is_file():
                errors.append(f"broken local link in {relative}: {raw}")

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

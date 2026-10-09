#!/usr/bin/env python3
"""Validate completeness and file integrity of a paid-generation receipt."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import tempfile
from datetime import datetime
from pathlib import Path


FIELDS = (
    "unit", "tool", "prompt", "story_contract", "visible_start",
    "primary_action", "visible_end", "likely_misread", "load_reason",
    "stop_condition", "remaining_risk",
)
ROLES = {"identity", "scene", "causal-state", "first-frame", "last-frame", "motion", "sound"}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def resolve(base: Path, raw: object) -> Path:
    path = Path(raw) if isinstance(raw, str) and raw else Path("/__invalid__")
    return path if path.is_absolute() else base / path


def validate(data: object, base: Path) -> list[str]:
    if not isinstance(data, dict):
        return ["receipt must be a JSON object"]
    errors: list[str] = []
    for field in FIELDS:
        if not isinstance(data.get(field), str) or len(data[field].strip()) < 8:
            errors.append(f"{field} needs a specific statement")
    if data.get("mode") not in {"compact", "rescue", "extended"}:
        errors.append("mode must be compact, rescue, or extended")
    if data.get("status") != "READY":
        errors.append("status must be READY for a paid prompt")
    prompt = data.get("prompt")
    if isinstance(prompt, str) and data.get("prompt_sha256") != sha256_bytes(prompt.encode("utf-8")):
        errors.append("prompt_sha256 does not match the current prompt")

    references = data.get("references")
    if not isinstance(references, list):
        errors.append("references must be a list")
    elif not references and not isinstance(data.get("no_reference_reason"), str):
        errors.append("no_reference_reason is required for an empty reference list")
    else:
        for number, item in enumerate(references, 1):
            if not isinstance(item, dict):
                errors.append(f"reference {number} must be an object")
                continue
            path = resolve(base, item.get("path"))
            if not path.is_file():
                errors.append(f"reference {number} file is missing")
            elif item.get("sha256") != sha256_bytes(path.read_bytes()):
                errors.append(f"reference {number} hash is stale")
            if item.get("role") not in ROLES or item.get("inspected") is not True:
                errors.append(f"reference {number} needs a valid role and actual inspection")

    if not isinstance(data.get("spatial_risk"), bool):
        errors.append("spatial_risk must be true or false")
    evidence = data.get("spatial_evidence")
    if not isinstance(evidence, list):
        errors.append("spatial_evidence must be a list")
    else:
        if data.get("spatial_risk") is True and not evidence:
            errors.append("spatial risk requires a sketch or keyframe")
        for number, raw in enumerate(evidence, 1):
            if not resolve(base, raw).is_file():
                errors.append(f"spatial evidence {number} is missing")

    checks = data.get("acceptance_checks")
    if not isinstance(checks, list) or len(checks) < 2 or any(not isinstance(x, str) or len(x.strip()) < 8 for x in checks):
        errors.append("at least two observable acceptance checks are required")
    try:
        completed = datetime.fromisoformat(data.get("completed_at", ""))
        if completed.tzinfo is None:
            raise ValueError
    except (TypeError, ValueError):
        errors.append("completed_at needs an ISO timestamp with timezone")
    return errors


def self_test() -> int:
    with tempfile.TemporaryDirectory() as folder:
        base = Path(folder)
        sample = {
            "unit": "example film / shot one", "mode": "compact", "tool": "example text to video",
            "status": "READY", "prompt": "A dog approaches a box and stops beside it.",
            "story_contract": "Show the dog discovering the box.",
            "visible_start": "The dog is two steps from the box.",
            "primary_action": "The dog approaches and sniffs the box.",
            "visible_end": "The dog stops with its nose at the box.",
            "likely_misread": "The model might put the dog inside the box.",
            "load_reason": "One dog, one location, and one simple movement.",
            "references": [], "no_reference_reason": "Text alone establishes this simple shot.",
            "spatial_risk": False, "spatial_evidence": [],
            "acceptance_checks": ["Exactly one dog is visible.", "The dog ends beside the box."],
            "stop_condition": "Stop if the dog enters the box instead.",
            "remaining_risk": "The dog may sniff too briefly to read.",
            "completed_at": "2026-01-01T12:00:00+00:00",
        }
        sample["prompt_sha256"] = sha256_bytes(sample["prompt"].encode("utf-8"))
        if validate(sample, base):
            print("FAIL: valid schema fixture rejected")
            return 1
        sample["prompt"] += " Changed after review."
        if "prompt_sha256 does not match the current prompt" not in validate(sample, base):
            print("FAIL: stale prompt was not rejected")
            return 1
        sample["prompt_sha256"] = sha256_bytes(sample["prompt"].encode("utf-8"))
        sample["spatial_risk"] = True
        if "spatial risk requires a sketch or keyframe" not in validate(sample, base):
            print("FAIL: unsupported spatial risk was not rejected")
            return 1
    print("Receipt validator self-test passed (valid schema, stale prompt, missing spatial evidence).")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("receipt", nargs="?", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    if args.receipt is None:
        parser.error("provide a receipt path or --self-test")
    try:
        data = json.loads(args.receipt.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"FAIL: cannot read receipt: {exc}")
        return 1
    errors = validate(data, args.receipt.resolve().parent)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print("Receipt evidence and hashes passed. Artistic and model outcomes remain unverified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

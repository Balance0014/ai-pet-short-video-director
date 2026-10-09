# Optional paid-generation receipt

Use this for a substantial paid generation where reproducibility and a clear stop decision matter. Save a JSON file within the user's project, never inside this skill. Run `python3 scripts/validate_receipt.py path/to/receipt.json` from the skill repository or invoke the script by its path.

The receipt is evidence of preparation, not a certificate that a model will obey. A script cannot verify artistic taste or whether `inspected: true` is honest. The producer must inspect each referenced image or clip and record the exact risk relevant to the unit.

```json
{
  "unit": "film title / source shot",
  "mode": "compact | rescue | extended",
  "tool": "tool and version checked for this unit",
  "status": "READY",
  "prompt": "one full current prompt",
  "prompt_sha256": "SHA-256 of the exact prompt string",
  "story_contract": "what the source shot must add to the film",
  "visible_start": "what the viewer sees first",
  "primary_action": "one concrete action or transformation",
  "visible_end": "what has changed and is visibly complete",
  "likely_misread": "most probable wrong literal interpretation",
  "load_reason": "why this is an appropriate unit for the chosen tool",
  "references": [
    {"path": "project-relative/or/absolute/file.png", "role": "identity | scene | causal-state | first-frame | last-frame", "sha256": "file hash", "inspected": true}
  ],
  "no_reference_reason": "required when references is empty",
  "spatial_risk": false,
  "spatial_evidence": [],
  "acceptance_checks": ["observable check 1", "observable check 2"],
  "stop_condition": "what failure stops further paid units",
  "remaining_risk": "what the model could still get wrong",
  "completed_at": "2026-01-01T12:00:00+00:00"
}
```

Resolve relative evidence paths from the receipt file's parent directory. If `spatial_risk` is true, provide at least one existing spatial sketch or keyframe in `spatial_evidence`. A complex semantic relationship, such as a leash entering a precise slot, should be visible in an inspected causal-state image when that relationship is the shot's main claim.

The prompt shown to the user must match `prompt` byte for byte. Editing the prompt invalidates the old hash and the old ready decision. If any required evidence is absent, keep the unit as `DRAFT` and say what must be fixed. Do not use this receipt to claim generation or footage review occurred.

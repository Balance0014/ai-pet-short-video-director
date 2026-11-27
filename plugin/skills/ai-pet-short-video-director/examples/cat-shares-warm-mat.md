# Worked example: The Warm Mat

**Hypothetical exercise.** No image or video was generated for this example. It illustrates directing decisions, not a measured success rate.

## Brief and pet contract

The lead is one orange tabby cat with a white chest. It walks on four legs, notices another animal's discomfort, and communicates through gaze, ears, posture, and movement rather than speech. A small brown dog is the second animal. Format: vertical pet short, about 15 seconds. Tool controls are assumed to include pet identity references and multi-shot video generation; verify those controls before use.

## Story greenlight

**Hook:** A tiny dog has fallen asleep across an entire warm floor mat while the cat stands beside it.

1. The cat reaches the mat and sees that the sleeping dog occupies all of it.
2. The cat raises one paw to reclaim space, then notices the dog shiver in a cool draft.
3. Instead of waking it, the cat grips the edge of a light cloth with its mouth and draws the cloth over the dog's back.
4. The dog wakes, shifts to one side, and leaves a dry warm patch open.
5. The cat sits in the offered space. Both settle while the cloth remains over the dog.

**Pet-only choice:** The cat gives up its first claim on the warm spot to help the dog. **Payoff:** the dog makes room in return. **Why about 15 seconds:** the cat's aborted claim, new decision, physical action, and dog's response each need a readable beat. **Main risk:** the model may teleport the cloth or make the dog's movement seem to happen before the cat acts.

## Direction and coverage

| Shot | Function and animal blocking | Camera and sound | End state |
|---|---|---|---|
| 1 | Establish one cat, one dog, mat, and folded cloth in the same room | Locked vertical view; soft room tone and draft | Dog occupies mat; cat sees it |
| 2 | Cat raises paw, notices shiver, turns toward cloth, grips its edge | Medium view; paw sound and cloth rustle | Cloth is visibly in cat's mouth |
| 3 | Cat draws cloth across dog's back; dog wakes and shifts aside | Stable two-animal view; cloth and breathing | Dog covered; space on mat open |
| 4 | Cat sits in the open spot; dog stays beside it | Brief held ending; quiet room tone | Both share the mat |

The folded cloth is visible before it is moved. The cat's mouth contact, cloth path, dog's movement, and new space on the mat must remain readable. Voice-over is unnecessary.

## Generation unit and acceptance

The cloth transfer and dog's response are two dependent actions. If the selected tool cannot control both reliably, split after the cat has gripped the cloth; use that stable image to begin the next unit. Use separate identity images for the cat and dog and a clean scene image for the mat and cloth. Reject a scene reference containing look-alike animals that could become duplicates.

**Illustrative prompt, requiring tool-specific syntax review before paid use:**

```text
Vertical pet short in one modest living room. One orange tabby cat with a white chest stands beside a warm floor mat. One small brown dog sleeps across the mat. A light folded cloth lies beside the mat.

Shot 1: Locked view of both animals and the cloth. The cat approaches the mat and pauses. The dog shivers once in a cool draft.
Shot 2: Medium view. The cat lifts one paw as if to step onto the mat, stops, looks at the shivering dog, then lowers the paw. It turns to the folded cloth and takes one edge gently in its mouth.
Shot 3: Stable view of both animals. The cat draws the cloth over the dog's back in one continuous action. The dog wakes, sees the cat, and shifts to one side, leaving an open patch on the mat.
Shot 4: The cat sits in the open patch. Hold on both animals resting together. The cloth remains over the dog.

Keep exactly one cat and one dog, their coat markings, the same room and mat, and the cloth's visible path. Natural room tone, breathing, paw movement, and cloth rustle only; no background music, captions, logos, or watermark.
```

**Accept the first take only if:** the cat's change of mind is visible; the cloth starts beside the mat and moves through visible mouth contact; the dog shifts only after the cloth action; both animals remain consistent; the final shared mat is readable.

**Stop condition:** if the cloth teleports or the dog shifts before the cat acts, do not buy a continuation. Simplify or split the cause-and-effect unit first.

## Review status

No generated footage, edit, or audience result exists for this example. The prompt has not passed a real first-take or release review.

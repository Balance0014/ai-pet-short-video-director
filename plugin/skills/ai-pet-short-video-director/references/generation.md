# Generation planning

Read when preparing stills, references, or video prompts. A prompt is a production instruction, not a guarantee of output quality.

## Identify actual tool controls

Before writing tool-specific syntax, establish whether the chosen tool supports text-to-video, image-to-video, first/last frames, multiple references, camera controls, native sound, duration, extend, and video-to-video repair. Verify current official documentation when a capability affects a paid decision. If the tool is unknown, write a capability-based prompt and mark the settings that need confirmation. Do not assume that a model supports precise internal timestamps.

## Control generation load

Define each unit as `visible start → primary action or transformation → visible end`. Count new important subjects, location changes, dependent prop actions, unfamiliar rules, and required reactions. If one stochastic unit must do all of these in order, split at a stable state or simplify the action. Give each shot one dominant camera behavior. Keep the subject's end position and the important object's final state explicit.

References have one named job each: pet identity and markings, scene geography, causal object/relationship, starting composition, ending composition, motion, or sound. State upload order and roles. Remove or crop conflicting duplicate animals before using a scene reference; “ignore the other dog” is a weak substitute for a clean image. Use a previously accepted frame for a continuation when it adequately locks the scene.

## Prompt forms

**Text-to-video:** `format → character identity → location and light → visible start → one primary action → camera → visible end → necessary sound → targeted constraints`.

**Image-to-video:** The image already provides appearance and scene. Write `camera behavior → subject movement and pace → environmental response → final pose/composition → invariants and likely failure to avoid`.

**First/last frame:** Describe the motion between the approved images, what changes, and what must stay fixed. Do not contradict the images with a second visual description.

**Multi-shot generation:** Use numbered shots only when the chosen tool supports them. Each shot adds a distinct state change, with one camera instruction and one primary action. Manage exact cut timing in the edit unless the tool demonstrably offers reliable shot timing.

Use observable wording: “the cat stops, looks from the sleeping dog to the empty half of the mat, then settles beside the dog” is actionable; “the cat creates a cinematic moment of friendship” is not. Name only negatives matching this unit's real failure risks, including extra pets, changed coat markings, or human-like limbs when relevant.

## Paid prompt gate

Before asking the user to spend credits, record:

`approved story and unit | tool/control assumptions | ordered references and roles | visible start/action/end | main misread risk | continuity from actual accepted footage | expected sound | first-take acceptance checks | stop condition`

Inspect the actual reference assets before claiming they are clean. A filled gate shows the preparation was done; it does not establish that the model will comply. Deliver one complete copyable prompt, not fragments or several competing versions. Any revision replaces the previous prompt in full.

If the user asks only for a draft, label it as a draft. Do not run paid generation, alter an account, or publish without the required authorization.

# Chloe Identity LoRA v1

Status: Draft training plan
Purpose: Local still-image identity control for Chloe Katastrophe

## Objective

Train a small identity LoRA so local SDXL-family models understand Chloe as a
stable person instead of rebuilding her from a long descriptive prompt each
time.

The target behavior is:

```text
photo of chloe_katastrophe_v1, Chloe in a corset, standing in a gothic castle
```

The model should preserve Chloe Model v1 facial identity, build, age, skin
texture, eyes, hair, and emotional presence while allowing wardrobe, setting,
lighting, pose, and genre to remain prompt-controlled.

## Trigger

Primary training token:

```text
chloe_katastrophe_v1
```

Human-readable alias:

```text
Chloe Katastrophe
```

Do not train only on the plain token `Chloe`. It is too common and will inherit
unwanted model priors. Use `chloe_katastrophe_v1` for reliable generation, then
write prompts naturally around it.

## Identity Scope

This LoRA should learn who Chloe is, not what she is wearing.

Include:

- approved Chloe Model v1 headshots
- approved three-quarter and profile views
- approved full-body turnaround references
- approved expression and performance references
- carefully curated synthetic identity expansions

Avoid baking in:

- corsets, lingerie, gothic wardrobe, heels, castle interiors, boudoir sets
- one-off music-video styling
- SDXL/Juggernaut test renders that drift from canon
- old marketing visuals that conflict with Chloe Model v1

Wardrobe and setting belong in the generation prompt after the identity LoRA is
loaded.

## Source Hierarchy

Use these as hard sources:

```text
studio/chloe-model/appearance.md
studio/reference-packs/chloe_model_v1/MODEL_CARD.md
studio/milestones/chloe_model_v1.json
```

Use these as the first dataset pool:

```text
studio/reference-decks/approved/001_identity_lock/
studio/reference-decks/approved/002_anatomical_reference/
studio/reference-decks/approved/002_character_turnaround/
studio/reference-decks/approved/003_expression_core/
studio/reference-decks/approved/004_cinematic_performance/
```

Synthetic expansion images may be added only after human approval. Store them
as generated artifacts, not recovered canon.

## Caption Rules

Captions should be short, factual, and identity-forward.

Every caption starts with:

```text
photo of chloe_katastrophe_v1, adult woman
```

Then add only what is visible and useful:

```text
gray-green eyes, dark wavy chestnut hair, fair textured skin, light freckles,
subtle Slavic facial structure, restrained expression
```

For full-body references, include:

```text
natural feminine hourglass silhouette, realistic proportions, quiet posture
```

Do not caption temporary wardrobe as identity unless it is deliberately neutral.
Avoid sexualized wording in the identity dataset. We can make the final prompts
sensual later without teaching the LoRA that sensuality is the identity.

## Acceptance Tests

A useful identity LoRA should pass these prompts without repeating Chloe's full
visual canon:

```text
photo of chloe_katastrophe_v1, simple black dress, standing in a plain studio
photo of chloe_katastrophe_v1, Chloe in a corset, standing in a gothic castle
photo of chloe_katastrophe_v1, archive portrait, soft window light
photo of chloe_katastrophe_v1, futuristic rain street, cinematic still
```

Reject a trained LoRA if it consistently produces:

- generic fashion-model faces
- porcelain skin or plastic smoothing
- over-glamourized makeup as a default
- a younger or more doll-like Chloe
- exaggerated body proportions
- locked wardrobe or locked boudoir posing
- severe hand, limb, or torso artifacts at ordinary settings

## Local Dataset Assembly

Build the local training folder with:

```bash
python3 scripts/prepare_chloe_lora_identity_dataset.py
```

The script writes into ignored local storage:

```text
tools/lora_datasets/chloe_lora_v1/
```

That keeps large duplicated image/caption training folders out of git while the
manifest, rules, and prompt set remain versioned.


# Chloe Photoshoot Foundation

Purpose: define the still-image ladder for Chloe photoshoots before using any
still as a video source.

## Principle

Photoshoot images should be built in layers. Do not ask the model to solve
identity, wardrobe, body continuity, pose, lighting, and setting all at once
until each earlier layer is stable.

## Stage 1: Model

Goal: prove the local model can preserve Chloe Model v1.

Use current visual canon and reference images to preserve:

- exact Chloe Model v1 face identity
- gray-green eyes with amber flecks
- dark chestnut near-black wavy hair
- fair textured skin with subtle freckles
- adult apparent age, mid-twenties
- natural feminine hourglass build
- realistic body proportions
- Slavic/Eastern European facial structure

Keep wardrobe simple and non-distracting. The output is useful only if Chloe is
recognizable before styling pressure is added.

## Stage 2: Model + Wardrobe

Goal: prove wardrobe control without identity drift.

Preserve all Stage 1 identity traits. Change only wardrobe and fashion styling:

- confident gothic boudoir fashion
- black lace corset bodysuit or structured corset
- fishnet stockings
- unique gothic heels
- subtle silver hardware
- sheer black robe, lace sleeves, or similar editorial layer
- tasteful sensuality, non-explicit
- no nudity

Evaluate face, skin texture, eye color, body proportions, hands, feet, posture,
and whether the outfit reads as intentional fashion instead of costume noise.

## Stage 3: Model + Wardrobe + Setting

Goal: prove setting control after identity and wardrobe are stable.

Preserve the approved Stage 2 Chloe and wardrobe. Add a setting such as:

- bright professional gothic boudoir studio
- softbox lighting
- dark velvet chaise
- antique mirror
- black lacquer vanity
- subtle red practical lights
- clean editorial composition
- tasteful sensual atmosphere

The setting should support Chloe, not overwrite her. No other participants.

## Promotion Rule

Only promote a still to video-source status when it passes:

- Chloe remains recognizable as Model v1
- wardrobe matches the intended shoot
- body proportions remain realistic
- skin texture is natural, not plastic
- pose and expression feel confident
- setting does not introduce unwanted people or identity drift

## Current Local Workflow

First local Mac-compatible test workflow:

```text
studio/workflows/comfyui_templates/sdxl_ipadapter_chloe_gothic_wardrobe_still.json
```

First result note: the v1 SDXL/IPAdapter output preserved a plausible Chloe-like
face, green eyes, natural skin texture, and dark hair better than expected, but
it read as a soft cropped portrait rather than a confident full photoshoot. It
missed the visible corset/fishnets/unique heels requirement and did not provide
enough body or shoe visibility for Stage 2 approval.

Use the v2 full-body workflow for the next wardrobe test:

```text
studio/workflows/comfyui_templates/sdxl_ipadapter_chloe_gothic_wardrobe_still_v2_full_body.json
```

Second result note: v2 improved facial continuity, skin texture, hair, and
gothic wardrobe styling, but it remained a seated cropped portrait. It did not
solve Stage 2 because the full body, fishnet continuity, and unique heels were
not visible. The likely cause is the `PLUS FACE (portraits)` adapter preset
combined with the headshot reference.

Use the v3 standing full-length workflow to test whether the general SDXL
IPAdapter preset and full-body reference can preserve enough identity while
allowing head-to-toe wardrobe control:

```text
studio/workflows/comfyui_templates/sdxl_ipadapter_chloe_gothic_wardrobe_still_v3_standing_full_length.json
```

Third result note: v3 improved standing full-body composition and shoe
visibility, but failed Chloe identity. The general `PLUS (high strength)`
adapter with the full-body reference produced a different woman with darker
eyes, different facial structure, and a sporty bodysuit silhouette. This path
is not acceptable for Chloe Model v1 continuity without stronger face locking.

Use the v4 face-locked standing workflow to return to the `PLUS FACE
(portraits)` adapter and headshot reference while lowering adapter strength and
forcing standing/full-length composition through prompt and negatives:

```text
studio/workflows/comfyui_templates/sdxl_ipadapter_chloe_gothic_wardrobe_still_v4_face_locked_standing.json
```

Fourth result note: v4 is the best Chloe identity result so far. It restores
gray-green eyes, dark chestnut near-black hair, pale textured skin, slim angular
build, and a recognizable Chloe-like face. It also moves wardrobe toward the
black gothic corset and lace direction. It is not yet a Stage 2 pass because the
image remains cropped above the knees and does not show fishnet continuity or
the unique heels.

Use the v5 face-locked catalog workflow to keep the v4 identity strategy while
pushing the camera farther back through full-length fashion catalog language,
more negative crop terms, a taller latent, and slightly lower/shorter IPAdapter
influence:

```text
studio/workflows/comfyui_templates/sdxl_ipadapter_chloe_gothic_wardrobe_still_v5_face_locked_catalog_full_length.json
```

Fifth result note: v5 moved farther away again. Lowering IPAdapter influence
did not solve full-body framing; it produced another cropped portrait and began
to idealize the face away from Chloe Model v1. This closes the prompt-only SDXL
branch for Stage 2. The next local branch should keep `PLUS FACE (portraits)`
for identity and add OpenPose/ControlNet for composition.

Next technical setup:

```text
scripts/download_comfyui_sdxl_openpose_controlnet.sh
```

Before adding OpenPose, test a stronger photoreal base checkpoint. The SDXL base
model may be part of the identity/composition tradeoff. Juggernaut XL v9 is the
next local photoshoot candidate because it is a photoreal SDXL finetune with
strong portrait/fashion tendencies.

Setup:

```text
scripts/download_comfyui_juggernaut_xl_models.sh
```

First workflow:

```text
studio/workflows/comfyui_templates/juggernaut_xl_ipadapter_chloe_gothic_wardrobe_face_locked.json
```

First Juggernaut result note: Juggernaut XL improved full-body framing and
gothic fashion wardrobe control compared with plain SDXL, but the output did
not preserve Chloe identity strongly enough. The face became a generic fashion
model version of Chloe, and the lower body, heels, hands, and dangling garment
details showed visible rendering artifacts. The crossed-leg pose and ornate
lace/strap prompt likely increased malformed anatomy and wardrobe clutter.

Use the v2 clean full-body workflow to test simpler wardrobe geometry, a stable
feet-apart stance, relaxed arms, fewer dangling details, and slightly stronger
IPAdapter identity pressure:

```text
studio/workflows/comfyui_templates/juggernaut_xl_ipadapter_chloe_gothic_wardrobe_face_locked_v2_clean_full_body.json
```

Flux Kontext remains a higher-fidelity image-edit candidate, but the current
FP8 ComfyUI repack does not run on Apple MPS. Use it on CUDA/RunPod or replace
it with a non-FP8 Kontext-compatible model before retrying locally.

Kontext workflow:

```text
studio/workflows/comfyui_templates/flux_kontext_chloe_gothic_wardrobe_still.json
```

Reference inputs:

```text
tools/ComfyUI/input/chloe_kontext_identity_headshot.png
tools/ComfyUI/input/chloe_kontext_identity_full_body.png
```

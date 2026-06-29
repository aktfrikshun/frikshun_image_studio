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

First local test workflow:

```text
studio/workflows/comfyui_templates/flux_kontext_chloe_gothic_wardrobe_still.json
```

Reference inputs:

```text
tools/ComfyUI/input/chloe_kontext_identity_headshot.png
tools/ComfyUI/input/chloe_kontext_identity_full_body.png
```

# Chloe v0.2 Eye Repair Round 4

Status: generated candidate batch, pending Allen review

Generated: 2026-07-01

## Purpose

Round three showed that eye shape is the main failure point in otherwise close
Chloe identity references. This round tests whether direct-gaze, face-dominant
prompts with stronger eye-specific negative constraints can reduce drift.

## Method

- Used direct-gaze prompts only.
- Required both eyes to be visible and unobstructed.
- Avoided narrative settings, props, jewelry, and scene complexity.
- Kept wardrobe secondary to face and eye evaluation.
- Added negative constraints for asymmetrical eyes, mismatched iris size,
  misaligned pupils, distorted eyelids, glassy eyes, and doll-like eyes.
- Generated two seed variants per wardrobe direction.

## Contents

- `001` and `002`: black tank direct-gaze test
- `003` and `004`: charcoal sweater direct-gaze test
- `005` and `006`: blue shirt direct-gaze test
- `007` and `008`: corset direct-gaze test
- `009` and `010`: leather jacket direct-gaze test
- `011` and `012`: black long-sleeve direct-gaze test
- `contact_sheet.jpg`: quick visual review sheet
- `manifest.json`: source prompts, seeds, model settings, and outputs

## Preliminary Chloe Read

The strongest preliminary candidates appear to be `005`, `010`, and `011`,
with `011` likely the strongest face-forward identity read. Some outputs still
ignore the direct-gaze instruction or place the face too far away for confident
eye evaluation. Do not treat any image in this folder as approved training data
until Allen reviews it.

## Review Focus

- Are both eyes recognizably Chloe?
- Are the pupils, iris size, and eyelids natural and symmetrical?
- Does the face still preserve Chloe Model v1 lips, cheekbones, skin texture,
  and hair?
- Is the image close enough to promote into the approved v0.2 training pool?

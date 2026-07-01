# Chloe v0.2 Anatomy Repair Round 5

Status: generated candidate batch, pending Allen review

Generated: 2026-07-01

## Purpose

Round four improved some eye reads but introduced a stretched-neck / mannequin
upper-body failure. Round five keeps the eye constraints while adding explicit
normal-neck, shoulder, trapezius, collarbone, and proportional head/body
constraints.

## Method

- Reduced the batch to eight images for faster iteration.
- Used four wardrobe directions with two variants each.
- Prompted for chest-up framing, direct gaze, natural shoulders, realistic
  collarbone spacing, relaxed trapezius, and normal neck length.
- Added negative constraints for long neck, swan neck, stretched throat, tiny
  shoulders, narrow shoulders, mannequin body, and disproportionate head.
- Kept background plain and wardrobe secondary to identity/anatomy.

## Contents

- `001` and `002`: black tank anatomy repair
- `003` and `004`: charcoal sweater anatomy repair
- `005` and `006`: blue shirt anatomy repair
- `007` and `008`: corset anatomy repair
- `contact_sheet.jpg`: quick visual review sheet
- `manifest.json`: source prompts, seeds, model settings, and outputs

## Preliminary Chloe Read

The long-neck problem is reduced compared with round four, but the model still
drifts toward wider framing than requested. The strongest preliminary
face/anatomy balance appears to be `005`. `003` and `007` may be plausible but
need close review. `006` falls back into side-gaze, and `008` is too distant for
confident identity evaluation.

Do not treat any image in this folder as approved training data until Allen
reviews it.

## Review Focus

- Is the neck normal human length?
- Are shoulders, collarbones, and upper torso proportional?
- Do both eyes still read as Chloe?
- Does the face preserve Chloe Model v1 lips, cheekbones, skin texture, and hair?

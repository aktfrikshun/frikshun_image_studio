# Chloe v0.2 Wardrobe Identity Refinement Round 3

Status: generated candidate batch, pending Allen review

Generated: 2026-07-01

## Purpose

This round narrows the v0.2 wardrobe identity work after Allen's round two
review. The goal is not setting diversity yet. It is to test whether the local
Chloe LoRA can hold facial identity, skin texture, lips, cheekbone structure,
eyes, hair, and body proportions across simple wardrobe changes on blank or
plain backgrounds.

## Method

- Used the Chloe v0.1 LoRA with stronger identity weighting.
- Kept backgrounds plain or minimally textured.
- Avoided narrative settings, props, and complex scene composition.
- Used mostly chest-up, half-body, and simple full-body framing.
- Reduced prompt complexity so wardrobe changes do not overpower identity.
- Generated two seed variants per wardrobe direction.

## Contents

- `001` and `002`: black tank identity calibration
- `003` and `004`: charcoal sweater identity calibration
- `005` and `006`: blue shirt identity calibration
- `007` and `008`: black corset identity calibration
- `009` and `010`: dark layered top / jacket identity calibration
- `011` and `012`: black top side-profile identity calibration
- `contact_sheet.jpg`: quick visual review sheet
- `manifest.json`: source prompts, seeds, model settings, and outputs

## Preliminary Read

This round appears more internally consistent than round two, especially in the
face-dominant images. The strongest preliminary identity candidates are `007`,
`009`, `011`, and `012`, though side-profile views should not dominate a training
set. Full-body candidates remain useful for body continuity, but some faces are
soft at distance and need Allen approval before promotion.

Do not treat any image in this folder as approved training data until reviewed.

## Next Review Questions

- Which faces read immediately as Chloe without explanation?
- Are the lips, cheekbones, and eye shape close enough to Chloe Model v1?
- Are any wardrobe/body variants useful enough to keep despite softer facial
  detail?
- Should the next round focus on fewer full-body images and more face-dominant
  half-body references?

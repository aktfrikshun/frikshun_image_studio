# Chloe v0.2 Wardrobe Identity Refinement Round 3

Status: reviewed candidate batch

Generated: 2026-07-01
Reviewed: 2026-07-01

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

## Allen Review

Approved for Chloe v0.2 identity reference consideration:

- `007_corset_identity_calibration_v01`
- `009_leather_jacket_identity_calibration_v01`
- `011_black_top_identity_calibration_v01`
- `012_black_top_identity_calibration_v02`

Close but not approved because the eyes still feel slightly off:

- `002_black_tank_identity_calibration_v02`
- `006_blue_shirt_identity_calibration_v02`
- `008_corset_identity_calibration_v02`
- `010_leather_jacket_identity_calibration_v02`

Rejected for misshapen eyes / identity drift:

- `001_black_tank_identity_calibration_v01`
- `003_charcoal_sweater_identity_calibration_v01`
- `004_charcoal_sweater_identity_calibration_v02`
- `005_blue_shirt_identity_calibration_v01`

## Notes

This round is more internally consistent than round two, but eye shape remains
the main failure point. The strongest keepers are mostly face-dominant images,
which supports the next refinement direction: fewer distant full-body frames,
more direct eye contact, and stronger eye-shape constraints before expanding
into settings.

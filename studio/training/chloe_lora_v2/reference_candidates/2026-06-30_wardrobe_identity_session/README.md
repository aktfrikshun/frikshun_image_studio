# Chloe LoRA v0.2 Wardrobe Identity Session

Date: 2026-06-30
Generator: local ComfyUI API runner
Base workflow: `studio/workflows/comfyui_templates/chloe_lora_v0_1_plain_lingerie_texture_tuned_reference.json`
Session runner: `scripts/run_chloe_v2_wardrobe_session.py`
Base LoRA: `chloe_katastrophe_v1_sdxl_lora_v0_1.safetensors`
Base checkpoint: `Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors`

## Purpose

Generate Chloe LoRA v0.2 reference candidates focused on identity preservation
across wardrobe, jewelry, framing, and body position.

This batch intentionally avoids complex settings. Backgrounds are blank or
plain studio walls so evaluation can focus on:

- recognizable Chloe facial identity
- gray-green eyes and natural skin texture
- canon-consistent body proportions
- wardrobe/accessory variation without environment complexity

## Review Contact Sheet

`contact_sheet.jpg`

## Allen Review

Allen reviewed this batch and rejected all images for v0.2 identity training.

Overall decision: `rejected_identity_drift`

Reason: none of the faces look recognizably enough like Chloe. Image `010` is
the closest, but even that image has strange eyes and should not be used for
identity training.

Several images remain useful as wardrobe or costume references only. Do not
promote any image from this batch into a Chloe identity training dataset.

| File | Wardrobe / Framing | Review Status | Notes |
| --- | --- | --- | --- |
| `001_black_tank_close_portrait_00001_.png` | black tank, upper-body | rejected_identity_drift | Costume/basic wardrobe idea may be useful, but the face does not look like Chloe. |
| `002_charcoal_sweater_waist_up_00001_.png` | charcoal sweater, full/three-quarter body | rejected_identity_drift | Useful daily wardrobe idea only. Reject for identity training. |
| `003_gray_hoodie_three_quarter_00001_.png` | hoodie and tank, three-quarter | rejected_identity_drift | Casual wardrobe idea may be useful, but the face drifts away from Chloe. |
| `004_black_lace_camisole_upper_thigh_00001_.png` | intimate black wardrobe, upper-thigh | rejected_identity_drift | Costume/body framing may be useful, but identity does not hold. |
| `005_gothic_corset_full_body_00001_.png` | gothic corset, full body | rejected_identity_drift | Useful gothic wardrobe silhouette only. Face is not Chloe. |
| `006_black_slip_dress_three_quarter_00001_.png` | black slip dress, seated | rejected_identity_drift | Seated pose and wardrobe may be useful, but reject for identity. |
| `007_leather_jacket_full_body_00001_.png` | leather jacket, full body | rejected_identity_drift | Daily wardrobe idea only. Face drifts generic. |
| `008_blue_shirt_waist_up_00001_.png` | muted blue shirt, waist-up | rejected_identity_drift | Non-black wardrobe idea may be useful, but face does not preserve Chloe identity. |
| `009_athletic_wear_full_body_00001_.png` | athletic wear, full body | rejected_identity_drift | Sports wardrobe idea only. Reject for identity training. |
| `010_ruby_memory_close_portrait_00001_.png` | black top, close portrait | rejected_identity_drift | Closest of the batch, but the eyes seem strange and the face is still not canon-safe. |

## Next Prompt Adjustments

- Generate closer variants for corset and leather-jacket references.
- Keep full-body prompts, but also pair each full-body wardrobe with a waist-up
  or chest-up variant so identity remains reviewable.
- Jewelry prompts need stronger small-scale control; the ruby and wolf pendant
  did not reliably appear in this run.
- Avoid letting athletic references become fitness-model or elongated-body
  references.
- Before generating another wardrobe batch, improve identity locking. This batch
  shows that wardrobe variation alone still pulls the face away from Chloe.

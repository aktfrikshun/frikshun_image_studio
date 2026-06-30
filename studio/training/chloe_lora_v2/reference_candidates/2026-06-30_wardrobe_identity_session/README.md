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

## Preliminary Review

These are candidate references only. Do not promote into v0.2 training until
Allen reviews them.

| File | Wardrobe / Framing | Preliminary Status | Notes |
| --- | --- | --- | --- |
| `001_black_tank_close_portrait_00001_.png` | black tank, upper-body | strong_candidate_pending_review | Strong face, skin texture, and body read. Prompt asked for close portrait but output is closer to upper-body; still useful. |
| `002_charcoal_sweater_waist_up_00001_.png` | charcoal sweater, full/three-quarter body | candidate_pending_review | Useful daily wardrobe. Face is a little smaller than ideal but still reviewable. |
| `003_gray_hoodie_three_quarter_00001_.png` | hoodie and tank, three-quarter | candidate_pending_review | Good plain-background casual reference. Watch for slight generic-model drift. |
| `004_black_lace_camisole_upper_thigh_00001_.png` | intimate black wardrobe, upper-thigh | strong_candidate_pending_review | Strong body and face continuity. Wardrobe simplified away from lace/camisole details, but the identity holds well. |
| `005_gothic_corset_full_body_00001_.png` | gothic corset, full body | candidate_with_scale_caution | Useful wardrobe silhouette. Face is small, so identity confidence is lower; may need a closer corset variant. |
| `006_black_slip_dress_three_quarter_00001_.png` | black slip dress, seated | candidate_pending_review | Useful seated body-position reference. Face is decent, but pose/stool should not become overrepresented. |
| `007_leather_jacket_full_body_00001_.png` | leather jacket, full body | candidate_with_identity_caution | Useful daily wardrobe and full-body stance. Face may be drifting more generic than the strongest candidates. |
| `008_blue_shirt_waist_up_00001_.png` | muted blue shirt, waist-up | strong_candidate_pending_review | Strong face, hair, and skin read. Good non-black wardrobe variation. |
| `009_athletic_wear_full_body_00001_.png` | athletic wear, full body | candidate_with_body_caution | Useful sports wardrobe on plain background. Watch for athletic/elongated body drift. |
| `010_ruby_memory_close_portrait_00001_.png` | black top, close portrait | strong_candidate_pending_review | Strong close identity candidate. Ruby ring prompt did not clearly render, but face and skin are useful. |

## Next Prompt Adjustments

- Generate closer variants for corset and leather-jacket references.
- Keep full-body prompts, but also pair each full-body wardrobe with a waist-up
  or chest-up variant so identity remains reviewable.
- Jewelry prompts need stronger small-scale control; the ruby and wolf pendant
  did not reliably appear in this run.
- Avoid letting athletic references become fitness-model or elongated-body
  references.

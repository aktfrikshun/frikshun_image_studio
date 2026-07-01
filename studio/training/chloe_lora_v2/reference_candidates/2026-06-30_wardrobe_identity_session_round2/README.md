# Chloe LoRA v0.2 Wardrobe Identity Session Round 2

Date: 2026-06-30
Generator: local ComfyUI API runner
Session runner: `scripts/run_chloe_v2_identity_locked_wardrobe_session.py`
Base workflow: `studio/workflows/comfyui_templates/chloe_lora_v0_1_plain_lingerie_texture_tuned_reference.json`
Base LoRA: `chloe_katastrophe_v1_sdxl_lora_v0_1.safetensors`
Base checkpoint: `Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors`

## Purpose

Generate a second wardrobe/accessory identity round after Allen rejected the
first wardrobe session for identity drift.

This round attempts to minimize drift by using:

- chest-up and waist-up framing instead of full-body-first framing
- direct eye contact
- larger faces
- stricter "wardrobe swap only" identity language
- stronger LoRA weights
- plain backgrounds only

## Review Contact Sheet

`contact_sheet.jpg`

## Preliminary Review

These are candidate references only. Allen has not approved them.

Compared with round 1, this batch is more consistent and the faces are less
chaotic. However, identity still needs careful review. Do not promote any image
from this batch into the v0.2 identity dataset without explicit approval.

| File | Wardrobe / Framing | Preliminary Status | Notes |
| --- | --- | --- | --- |
| `001_black_tank_chest_up_identity_00001_.png` | black tank, chest-up | candidate_pending_review | Better body/wardrobe control than round 1, but face still needs Allen review. |
| `002_charcoal_sweater_chest_up_identity_00001_.png` | charcoal sweater, chest-up | candidate_pending_review | One of the more stable daily-wardrobe candidates; check eye shape and facial geometry. |
| `003_blue_shirt_chest_up_identity_00001_.png` | muted blue shirt, chest-up | candidate_pending_review | Useful non-black wardrobe variation; face is clear enough for review. |
| `004_gray_hoodie_waist_up_identity_00001_.png` | gray hoodie, waist-up | candidate_pending_review | Casual wardrobe reference with clear body framing; face may still read generic. |
| `005_black_lace_chest_up_identity_00001_.png` | black intimate wardrobe, chest-up | candidate_pending_review | Useful simple intimate wardrobe reference; identity requires close review. |
| `006_corset_waist_up_identity_00001_.png` | gothic corset, waist-up | candidate_pending_review | Strong wardrobe shape, but side gaze and stylized costume may reduce identity confidence. |
| `007_leather_jacket_waist_up_identity_00001_.png` | leather jacket, waist-up | candidate_pending_review | Useful jacket styling; face and expression may be drifting. |
| `008_ruby_ring_close_identity_00001_.png` | black top / ruby prompt, close portrait | candidate_pending_review | Face is large and reviewable; ruby did not clearly render. |

## Next Prompt Adjustments

- If Allen rejects this round, switch from text/LoRA-only generation to stronger
  identity conditioning such as IPAdapter/InstantID or a curated v0.2 retrain
  using approved Chloe identity images only.
- Keep the larger face and simple background strategy.
- Generate fewer variants per batch and review faster, before spending time on
  full wardrobe coverage.

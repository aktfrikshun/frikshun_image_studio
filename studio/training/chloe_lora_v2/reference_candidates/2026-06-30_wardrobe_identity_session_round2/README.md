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

## Allen Review

Allen reviewed this batch on 2026-07-01.

Compared with round 1, this batch is much closer. Allen rejected `004` for
identity drift and `005` for the eyes. The remaining six images seem very close
and should be held as strong candidates pending final training approval.

Do not automatically promote the strong candidates into the v0.2 identity
dataset without final approval.

| File | Wardrobe / Framing | Review Status | Notes |
| --- | --- | --- | --- |
| `001_black_tank_chest_up_identity_00001_.png` | black tank, chest-up | strong_candidate_pending_final_review | Allen reviewed as very close. Hold for final training approval. |
| `002_charcoal_sweater_chest_up_identity_00001_.png` | charcoal sweater, chest-up | strong_candidate_pending_final_review | Allen reviewed as very close. Hold for final training approval. |
| `003_blue_shirt_chest_up_identity_00001_.png` | muted blue shirt, chest-up | strong_candidate_pending_final_review | Allen reviewed as very close. Useful non-black wardrobe variation. |
| `004_gray_hoodie_waist_up_identity_00001_.png` | gray hoodie, waist-up | rejected_identity_drift | Rejected by Allen for identity drift. Do not train. |
| `005_black_lace_chest_up_identity_00001_.png` | black intimate wardrobe, chest-up | rejected_eye_artifacts | Rejected by Allen because the eyes are not acceptable. Do not train. |
| `006_corset_waist_up_identity_00001_.png` | gothic corset, waist-up | strong_candidate_pending_final_review | Allen reviewed as very close. Hold for final training approval. |
| `007_leather_jacket_waist_up_identity_00001_.png` | leather jacket, waist-up | strong_candidate_pending_final_review | Allen reviewed as very close. Hold for final training approval. |
| `008_ruby_ring_close_identity_00001_.png` | black top / ruby prompt, close portrait | strong_candidate_pending_final_review | Allen reviewed as very close. Ruby did not clearly render, but identity is promising. |

## Next Prompt Adjustments

- If Allen rejects this round, switch from text/LoRA-only generation to stronger
  identity conditioning such as IPAdapter/InstantID or a curated v0.2 retrain
  using approved Chloe identity images only.
- Keep the larger face and simple background strategy.
- Generate fewer variants per batch and review faster, before spending time on
  full wardrobe coverage.

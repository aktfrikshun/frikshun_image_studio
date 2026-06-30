# Chloe LoRA v0.2 Reference Candidates: API Refset Probe

Date: 2026-06-30
Generator: local ComfyUI API runner
Base LoRA: `chloe_katastrophe_v1_sdxl_lora_v0_1.safetensors`
Base checkpoint: `Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors`

## Purpose

Build a setting-diverse candidate pool for Chloe LoRA v0.2 so the next model
learns that Chloe's identity should survive wardrobe, pose, and environment
changes without re-describing her face every time.

These are candidates, not final training approvals. They should be reviewed
against Chloe Model v1 canon before being copied into a training dataset.

## Candidates

| File | Setting | Status | Notes |
| --- | --- | --- | --- |
| `001_gothic_cemetery_identity_candidate.png` | gothic cemetery | approved | Allen approved for v0.2 reference use. Strong cemetery pressure test: identity, hair, skin, and mood hold well. Side-angle gaze ignored direct-gaze prompt, but the result is useful for angle/setting diversity. |
| `002_sports_training_identity_candidate.png` | sports / athletic training | rejected | Allen rejected for identity drift: the sports context is useful, but the subject does not look like Chloe. Do not include in v0.2 training. |
| `003_archive_desk_camera_photos_identity_candidate.png` | archive desk with camera/photos | quarantine_repair_or_regenerate | Setting and archive-world context are useful, but Allen flagged the eyes as malformed. Do not include directly in v0.2 training; regenerate or repair the eye region first. |

## Caption Drafts

```text
photo of chloe_katastrophe_v1, adult woman, gothic cemetery environmental portrait, dark wavy hair, gray-green eyes, fair textured skin with light freckles, subtle Slavic facial structure, black wool coat, weathered headstones, overcast natural light, quiet observant expression
```

```text
photo of chloe_katastrophe_v1, adult woman, sports training reference, full-body athletic portrait, practical black athletic tank top and charcoal leggings, gray-green eyes, dark wavy hair, fair textured skin, natural feminine hourglass silhouette, relaxed neutral posture, outdoor track
```

```text
photo of chloe_katastrophe_v1, adult woman, archive desk portrait, gray-green eyes, dark wavy hair, fair textured skin with freckles, subtle Slavic facial structure, seated at wooden desk, vintage camera, recovered photographs, handwritten notes, warm practical light, quiet searching expression
```

## v0.2 Training Guidance

- Do not train on every generated image automatically.
- Prefer candidates where Chloe remains immediately recognizable.
- Include setting diversity only when identity remains strong.
- Preserve multiple framings: close portrait, upper-body, three-quarter, and
  full-body.
- Avoid overrepresenting lingerie/corset imagery in v0.2; the goal is robust
  identity across normal and stylized shoots.
- Add more candidates for cemetery, sports, archive desk, and other practical
  settings before retraining.

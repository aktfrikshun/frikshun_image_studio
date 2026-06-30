# Chloe LoRA v0.2 Reference Candidates: API Refset Probe

Date: 2026-06-30
Generator: local ComfyUI API runner
Base LoRA: `chloe_katastrophe_v1_sdxl_lora_v0_1.safetensors`
Base checkpoint: `Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors`

## Purpose

This batch was an early setting-diversity probe. After Allen's review, v0.2 has
been narrowed to identity plus wardrobe/accessory robustness on blank or simple
backgrounds. Setting-heavy candidates from this batch should not define v0.2;
they are retained as review evidence and possible v0.3 planning material.

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

## v0.2 / v0.3 Training Guidance

- Do not train on every generated image automatically.
- Prefer candidates where Chloe remains immediately recognizable.
- Preserve multiple framings: close portrait, upper-body, three-quarter, and
  full-body.
- For v0.2, use blank or simple backgrounds and vary wardrobe/accessories first.
- Hold complex settings for v0.3 after v0.2 can preserve identity reliably.
- Avoid overrepresenting lingerie/corset imagery in v0.2; the goal is robust
  identity across normal and stylized wardrobe, not a single visual lane.
- Regenerate sports and archive-desk ideas later as v0.3 setting tests.

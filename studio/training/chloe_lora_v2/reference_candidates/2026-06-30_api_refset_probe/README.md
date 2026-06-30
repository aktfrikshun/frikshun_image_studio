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
| `001_gothic_cemetery_identity_candidate.png` | gothic cemetery | candidate | Strong cemetery pressure test. Identity, hair, skin, and mood hold well. Side-angle gaze ignored direct-gaze prompt, but the result is useful for angle/setting diversity. |
| `002_sports_training_identity_candidate.png` | sports / athletic training | candidate | Useful full-body/body-shape candidate. Face is recognizable, posture is neutral, and sportswear stays practical rather than exaggerated fitness-model styling. |
| `003_archive_desk_camera_photos_identity_candidate.png` | archive desk with camera/photos | strong candidate | Best identity result in this batch. Strong eyes, skin texture, hair, and archive-world context. Good candidate for v0.2 if Allen approves. |

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

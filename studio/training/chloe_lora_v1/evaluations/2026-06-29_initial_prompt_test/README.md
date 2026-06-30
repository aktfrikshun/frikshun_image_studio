# Chloe LoRA v0.1 Initial Prompt Evaluation

Date: 2026-06-29
Model: `chloe_katastrophe_v1_sdxl_lora_v0_1.safetensors`
Base checkpoint: `Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors`

## Outputs

| File | Prompt Class | Result |
| --- | --- | --- |
| `001_simple_studio_prompt.png` | simple studio identity prompt | Strong face match. Hair, eyes, skin texture, and general presence are close to Chloe Model v1. |
| `002_gothic_castle_prompt_identity_drift.png` | gothic castle full-body corset prompt | Identity drift. Costume and setting are successful, but face, build, and age read as a different woman. |
| `003_combined_prompt_stronger_identity_cropped.png` | combined identity + gothic castle/corset prompt | Stronger identity bridge. Face, hair, eyes, skin texture, and fuller corset silhouette are much closer to canon, but the image crops to upper body. |

## Diagnosis

Chloe LoRA v0.1 learned the core face well in a neutral/portrait-like domain.
It does not yet reliably hold identity when the prompt asks for a high-pressure
combination of full body, gothic wardrobe, corset, and castle setting.

The third output shows that the LoRA can bridge identity and gothic styling when
the prompt carries enough Chloe-specific face, hair, skin, and build language.
The useful failure moved from identity drift to camera/framing: the image is
stronger, but it is not full body.

Likely causes:

- The training set is identity-forward and neutral by design.
- The dataset has fewer full-body identity anchors than face anchors.
- The prompt phrase `Chloe in a corset, standing in a gothic castle` gives the
  base model strong prior imagery for a generic gothic woman.
- LoRA strength `0.75` is too weak for high-costume/high-setting tests.

## Next Test

Use the identity-weighted gothic castle workflow:

```text
studio/workflows/comfyui_templates/chloe_lora_v0_1_gothic_castle_identity_weighted.json
```

Changes from the first simple workflow:

- LoRA model strength: `1.15`
- LoRA CLIP strength: `1.0`
- identity traits placed before costume and setting
- stronger negative prompt against wrong face, stocky build, brown eyes, and
  generic gothic model drift
- sampler raised to 34 steps / CFG 6.0

If identity holds but the body is cropped, use the full-body locked variant:

```text
studio/workflows/comfyui_templates/chloe_lora_v0_1_gothic_castle_full_body_locked.json
```

That workflow moves composition to the front of the prompt: head-to-toe,
camera pulled back, feet visible, and full-length fashion catalogue framing.

## Possible v0.2 Direction

If the weighted workflow still drifts, train v0.2 with approved synthetic
augmentation that keeps Chloe identity while varying:

- full-body studio poses
- three-quarter full-body poses
- simple black dress/corset-neutral silhouettes
- gothic architecture backgrounds without changing identity
- restrained fashion poses that preserve Chloe's build canon

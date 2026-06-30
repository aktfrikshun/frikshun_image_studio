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
| `004_full_body_locked_face_degraded.png` | full-body locked gothic castle prompt | Framing improved, but face quality and identity degraded. The subject is too small in frame and the castle consumes too much detail budget. |
| `005_plain_lingerie_wardrobe_face_drift.png` | plain-background lingerie wardrobe prompt | Wardrobe, pose, and body proportions are useful, but the side-glance catalogue pose drifts into a generic model face rather than Chloe. |
| `006_plain_lingerie_face_locked_partial_win.png` | plain-background lingerie face-locked prompt | Clear improvement. Direct gaze, wardrobe, and body proportions are usable; remaining issue is a slightly polished/generic face texture. |
| `007_plain_lingerie_texture_tuned_reference_win.png` | plain-background lingerie texture-tuned prompt | Current wardrobe reference win. Stronger Chloe identity, better skin texture, direct gaze, and usable gothic lingerie styling. |

## Diagnosis

Chloe LoRA v0.1 learned the core face well in a neutral/portrait-like domain.
It does not yet reliably hold identity when the prompt asks for a high-pressure
combination of full body, gothic wardrobe, corset, and castle setting.

The third output shows that the LoRA can bridge identity and gothic styling when
the prompt carries enough Chloe-specific face, hair, skin, and build language.
The useful failure moved from identity drift to camera/framing: the image is
stronger, but it is not full body.

The fourth output confirms that forcing full body in a detailed castle solves
the crop at the expense of face fidelity. The next step should isolate wardrobe
on a plain background before reintroducing complex settings.

The fifth output confirms that removing the castle helps the wardrobe and body
reference, but side-glance fashion posing still weakens identity. The next
variant should keep the plain background while forcing direct eye contact,
centered face, and a face large enough for identity fidelity.

The sixth output is the first usable plain lingerie wardrobe reference. It holds
direct gaze and proportions well enough to tune from. The next iteration should
keep the recipe stable while reducing catalogue polish and restoring more
natural Chloe skin/face texture.

The seventh output is the current wardrobe reference winner. It keeps identity,
texture, hair, eyes, and black lace styling in a usable balance. The next step
should not return directly to a castle corridor; instead, add only a minimal
gothic setting cue while preserving the winning subject/wardrobe recipe.

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

After the first full-body locked result degraded the face, shift to a simpler
wardrobe reference workflow:

```text
studio/workflows/comfyui_templates/chloe_lora_v0_1_plain_lingerie_wardrobe_reference.json
```

This keeps the background plain and tests only whether Chloe identity survives
an elegant black lace gothic lingerie/corset wardrobe change.

The first plain lingerie result held the wardrobe but not the face. Use the
face-locked variant next:

```text
studio/workflows/comfyui_templates/chloe_lora_v0_1_plain_lingerie_face_locked_reference.json
```

This variant uses stronger LoRA weights, direct eye contact, centered
front-facing geometry, and a negative prompt against side-glance/profile drift.

The face-locked result is usable but a little too polished. Use this texture
tuned variant next:

```text
studio/workflows/comfyui_templates/chloe_lora_v0_1_plain_lingerie_texture_tuned_reference.json
```

This keeps the same plain-background wardrobe setup while adding natural skin
texture, subtle asymmetry, and negative prompts against beauty-filter/catalogue
model drift.

The texture-tuned result is the current wardrobe reference win. Use this bridge
workflow to introduce a simple gothic setting without overloading identity:

```text
studio/workflows/comfyui_templates/chloe_lora_v0_1_lingerie_simple_gothic_setting_bridge.json
```

This adds only a plain charcoal wall, subtle stone texture, and a soft arched
window hint while explicitly avoiding castle/cathedral background dominance.

## Possible v0.2 Direction

If the weighted workflow still drifts, train v0.2 with approved synthetic
augmentation that keeps Chloe identity while varying:

- full-body studio poses
- three-quarter full-body poses
- simple black dress/corset-neutral silhouettes
- gothic architecture backgrounds without changing identity
- restrained fashion poses that preserve Chloe's build canon

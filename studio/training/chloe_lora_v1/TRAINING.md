# Chloe Identity LoRA v0.1 Training

Status: Local trainer route prepared

## Goal

Train the trigger token:

```text
chloe_katastrophe_v1
```

against the approved 22-reference identity set so local SDXL-family models can
generate Chloe without rewriting her full canon in every prompt.

## Local Route

The first local route uses Kohya `sd-scripts` because it can train against the
local SDXL `.safetensors` checkpoints already downloaded for ComfyUI.

Install or update the trainer:

```bash
scripts/setup_kohya_sdxl_lora_trainer.sh
```

Run preflight:

```bash
scripts/preflight_chloe_lora_trainer.sh
```

Start the first training run:

```bash
scripts/train_chloe_lora_sdxl_local.sh
```

The default full run is 800 steps. A 20-step smoke test on the local M1 Max
completed successfully on 2026-06-29 using Apple MPS. The first full 800-step
run completed in 1:42:39 and produced the run record:

```text
studio/training/chloe_lora_v1/runs/2026-06-29_sdxl_juggernaut_v0_1.md
```

Run a short smoke test:

```bash
CHLOE_LORA_MAX_STEPS=20 scripts/train_chloe_lora_sdxl_local.sh
```

By default the training launcher uses:

```text
tools/ComfyUI/models/checkpoints/Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors
```

Override the base model if needed:

```bash
CHLOE_LORA_BASE_MODEL=/absolute/path/to/model.safetensors scripts/train_chloe_lora_sdxl_local.sh
```

## Outputs

Training files are written under ignored local storage:

```text
tools/lora_training/chloe_lora_v1/
```

Expected LoRA file:

```text
tools/lora_training/chloe_lora_v1/output/chloe_katastrophe_v1_sdxl_lora_v0_1.safetensors
```

Copy the finished LoRA into ComfyUI after review:

```text
tools/ComfyUI/models/loras/
```

## First Test Prompts

Open this ready-to-run ComfyUI workflow:

```text
studio/workflows/comfyui_templates/chloe_lora_v0_1_simple_prompt_test.json
```

It includes:

```text
checkpoint: Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors
LoRA: chloe_katastrophe_v1_sdxl_lora_v0_1.safetensors
positive prompt: simple Chloe studio test
negative prompt: basic identity/artifact guardrails
sampler: dpmpp_2m karras, 30 steps, CFG 5.5
latent size: 832x1216
```

Initial visual evaluation:

```text
studio/training/chloe_lora_v1/evaluations/2026-06-29_initial_prompt_test/
```

The simple studio prompt held identity well. The first gothic castle/corset test
lost identity, so use this stronger identity-weighted workflow for the next
round:

```text
studio/workflows/comfyui_templates/chloe_lora_v0_1_gothic_castle_identity_weighted.json
```

The combined identity + gothic castle/corset prompt held identity much better
and preserved the fuller corset silhouette, but cropped to upper body. Use this
full-body locked workflow when the next failure mode is framing rather than
identity:

```text
studio/workflows/comfyui_templates/chloe_lora_v0_1_gothic_castle_full_body_locked.json
```

The first full-body locked castle result improved framing but degraded the face,
so use this plain-background wardrobe reference before adding complex settings:

```text
studio/workflows/comfyui_templates/chloe_lora_v0_1_plain_lingerie_wardrobe_reference.json
```

If the wardrobe holds but the face drifts into a generic catalogue model, use
the face-locked variant:

```text
studio/workflows/comfyui_templates/chloe_lora_v0_1_plain_lingerie_face_locked_reference.json
```

If the face-locked result is usable but too polished, use the texture-tuned
variant:

```text
studio/workflows/comfyui_templates/chloe_lora_v0_1_plain_lingerie_texture_tuned_reference.json
```

The texture-tuned output is the current plain lingerie wardrobe reference win.
Use this bridge workflow to add only a minimal gothic setting cue before trying
complex architecture again:

```text
studio/workflows/comfyui_templates/chloe_lora_v0_1_lingerie_simple_gothic_setting_bridge.json
```

If that bridge drifts into a close side-glance portrait or loses the setting,
use the stricter direct-gaze arch-wall bridge:

```text
studio/workflows/comfyui_templates/chloe_lora_v0_1_lingerie_arch_wall_direct_gaze_bridge.json
```

If the direct-gaze bridge improves framing but loses the arch and turns lingerie
into leggings, use the three-quarter boudoir bridge:

```text
studio/workflows/comfyui_templates/chloe_lora_v0_1_lingerie_arch_boudoir_three_quarter_bridge.json
```

The current test ladder is: hold identity, hold identity with wardrobe, then
hold identity + wardrobe inside a setting.

## API-Driven ComfyUI Runs

ComfyUI can be driven without the browser UI. Start the local server:

```text
scripts/run_comfyui_local.sh
```

Then submit any supported Chloe LoRA workflow through the API runner:

```text
python3 scripts/run_comfyui_workflow.py \
  studio/workflows/comfyui_templates/chloe_lora_v0_1_lingerie_arch_boudoir_three_quarter_bridge.json \
  --runs 4 \
  --outdir studio/outputs/comfyui_api/chloe_lora_v0_1_arch_boudoir_three_quarter
```

The runner converts the UI workflow JSON into ComfyUI's `/prompt` API format,
queues each run, polls `/history/{prompt_id}`, downloads generated images from
`/view`, and writes a manifest with prompt ids, seeds, and output paths.

Use `--dry-run` to inspect the converted API graph without generating:

```text
python3 scripts/run_comfyui_workflow.py \
  studio/workflows/comfyui_templates/chloe_lora_v0_1_lingerie_arch_boudoir_three_quarter_bridge.json \
  --dry-run \
  --outdir /tmp/comfyui-api-dry-run
```

Use these after the LoRA is available in ComfyUI:

```text
photo of chloe_katastrophe_v1, simple black dress, standing in a plain studio
photo of chloe_katastrophe_v1, Chloe in a corset, standing in a gothic castle
photo of chloe_katastrophe_v1, archive portrait, soft window light
photo of chloe_katastrophe_v1, futuristic rain street, cinematic still
```

## Notes

The local Mac may still reject or crawl through training because SDXL training is
heavy and Apple MPS support varies by tool. That is useful information. If the
local route fails at runtime, preserve the dataset and config and move the same
training folder to a CUDA host.

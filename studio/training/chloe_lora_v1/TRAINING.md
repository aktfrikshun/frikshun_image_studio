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

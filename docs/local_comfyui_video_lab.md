# Local ComfyUI Video Lab

This lab is for testing whether Chloe image-to-video can work locally before we
move serious rendering to RunPod. The goal is not speed; the goal is to learn
identity consistency, local restrictions, and model behavior without burning
hosted API credit.

## Machine Baseline

Current local target:

- MacBook Pro, Apple M1 Max
- 32 GB unified memory
- 24-core Apple GPU / Metal
- Recommended role: workflow editor, prompt lab, low-resolution diagnostics,
  and short LTX tests

Use RunPod later for longer Wan/LTX generations, 720p+ output, batches, and
anything that needs CUDA VRAM.

## Install ComfyUI

The setup script installs ComfyUI into `tools/ComfyUI`, which is ignored by git.
It prefers the bundled Codex Python 3.12 runtime because macOS system Python is
3.9 on this machine.

```bash
scripts/setup_comfyui_local.sh
```

If you want to use a different Python:

```bash
PYTHON_BIN=/opt/homebrew/bin/python3.12 scripts/setup_comfyui_local.sh
```

Launch ComfyUI:

```bash
scripts/run_comfyui_local.sh
```

Then open:

```text
http://127.0.0.1:8188
```

Important local note: the Codex sandbox could not see Apple MPS, but the same
environment launched correctly with normal terminal permissions. If ComfyUI
crashes with `Torch not compiled with CUDA enabled`, launch it from Terminal
with `scripts/run_comfyui_local.sh`.

## First Test Target

Use the first diagnostic prompt:

```text
studio/workflows/comfyui_ltx_identity_motion_test.md
```

Use the primary Chloe Model v1 headshot as the source image:

```text
studio/reference-packs/chloe_model_v1/packs/character_turnaround_v1/001/001_front_headshot_v1.png
```

Keep the first clip intentionally conservative:

- 9:16 vertical
- 480p or lower if memory is tight
- 3-5 seconds
- low motion
- no dialogue/lip-sync yet
- fully covered wardrobe

This gives us a clean read on whether the local model preserves identity before
we add sexuality, platform framing, dialogue, or complex camera movement.

## Model Notes

ComfyUI 0.26.0 launched successfully on this Mac with:

- PyTorch 2.12.1
- device: `mps`
- memory mode: shared
- reported memory: 32768 MB

Start with LTXV locally because the built-in workflow is simple and has concrete
model filenames. Treat Wan as a hosted-GPU candidate unless a small quantized
local workflow proves itself.

The first local LTXV image-to-video workflow is built into ComfyUI as
`ltxv_image_to_video`. It expects:

```text
tools/ComfyUI/models/checkpoints/ltx-video-2b-v0.9.5.safetensors
tools/ComfyUI/models/text_encoders/t5xxl_fp16.safetensors
```

Download them with:

```bash
scripts/download_comfyui_ltxv_models.sh
```

Confirmed local install:

```text
5.9G tools/ComfyUI/models/checkpoints/ltx-video-2b-v0.9.5.safetensors
9.1G tools/ComfyUI/models/text_encoders/t5xxl_fp16.safetensors
```

The installed ComfyUI package also includes newer LTX2 and Wan templates. To
copy the useful templates into this repo for inspection/import:

```bash
scripts/export_comfyui_video_templates.sh
```

The first exported templates are:

```text
studio/workflows/comfyui_templates/ltxv_image_to_video.json
studio/workflows/comfyui_templates/video_ltx2_i2v_distilled.json
studio/workflows/comfyui_templates/image_to_video_wan.json
```

## First LTXV Result

The first Chloe LTXV test produced a deformed face. Likely causes:

- the stock workflow used landscape `768x512` against a portrait headshot
- `LTXVImgToVideo` strength was `0.15`, which preserves very little of the
  source image according to the embedded node docs
- the prompt asked for a push-in and expression shift before proving identity
  stability

Use the lower-motion portrait diagnostic next:

```text
studio/workflows/comfyui_templates/ltxv_chloe_identity_motion_test_portrait_low_motion.json
```

Key settings:

```text
width: 512
height: 768
frames: 49
fps: 12
strength: 0.95
```

Expected local limitations:

- first generation may be slow
- model downloads are large
- some custom nodes may assume CUDA and fail on MPS
- high resolution or long clips may run out of memory
- identity may drift without an IP/reference workflow or LoRA-style identity
  conditioning

## Decision Gate

Local testing is successful enough to move to RunPod when:

- at least one local image-to-video workflow runs without hosted moderation
- Chloe remains recognizable for a short low-motion clip
- the workflow can be saved and repeated
- failures are model quality or speed problems, not policy/provider blocks

If local generation works but is slow, move the saved ComfyUI workflow to
RunPod and use a CUDA GPU for real output.

## Still Image First

After the first usable low-motion LTXV result, move one step earlier in the
pipeline: validate still-image identity and wardrobe before spending time on
motion. The first local still workflow uses Flux Kontext because Kontext is
designed for image editing with explicit preservation instructions.

The photoshoot ladder is tracked here:

```text
studio/workflows/chloe_photoshoot_foundation.md
```

Prepare the required model files:

```bash
scripts/download_comfyui_flux_kontext_models.sh
```

Prepare the Chloe reference images in ComfyUI's input folder:

```bash
scripts/prepare_comfyui_chloe_kontext_inputs.sh
```

Then open this workflow in ComfyUI:

```text
studio/workflows/comfyui_templates/flux_kontext_chloe_gothic_wardrobe_still.json
```

This workflow uses:

```text
image 1: chloe_kontext_identity_headshot.png
image 2: chloe_kontext_identity_full_body.png
model: flux1-dev-kontext_fp8_scaled.safetensors
clip: clip_l.safetensors
t5: t5xxl_fp16.safetensors
vae: ae.safetensors
```

The prompt asks for a tasteful gothic boudoir fashion still while preserving
Chloe Model v1 face, build, age, eye color, hair color, skin texture, and body
proportions.

### Current Flux Kontext Finding

The local Flux Kontext FP8 workflow does not run on Apple MPS as configured.
The KSampler fails with:

```text
TypeError: Trying to convert Float8_e4m3fn to the MPS backend but it does not have support for that dtype.
```

This is a runtime/model-format issue, not a prompt or input-image issue. Treat
`flux1-dev-kontext_fp8_scaled.safetensors` as a CUDA/RunPod candidate unless we
replace it with non-FP8 weights that PyTorch MPS can execute.

Next still-image options:

- use RunPod/CUDA for Flux Kontext identity + wardrobe tests
- find and test a non-FP8 Kontext-compatible local workflow
- switch local still testing to a Mac-compatible SDXL identity workflow

## Local SDXL + IPAdapter Still Test

The first Mac-friendly still-image path is SDXL plus IPAdapter, using Chloe's
approved headshot as the identity reference. This is not as surgically faithful
as Kontext image editing, but it avoids FP8 and CUDA-only assumptions.

Install the IPAdapter custom node:

```bash
git clone https://github.com/cubiq/ComfyUI_IPAdapter_plus.git tools/ComfyUI/custom_nodes/ComfyUI_IPAdapter_plus
```

Prepare the model files:

```bash
scripts/download_comfyui_sdxl_ipadapter_models.sh
```

Prepare the Chloe reference images in ComfyUI's input folder if needed:

```bash
scripts/prepare_comfyui_chloe_kontext_inputs.sh
```

Then restart ComfyUI and open:

```text
studio/workflows/comfyui_templates/sdxl_ipadapter_chloe_gothic_wardrobe_still.json
```

This workflow uses:

```text
checkpoint: sd_xl_base_1.0.safetensors
clip vision: CLIP-ViT-H-14-laion2B-s32B-b79K.safetensors
ipadapter: ip-adapter-plus-face_sdxl_vit-h.safetensors
ipadapter full-length option: ip-adapter-plus_sdxl_vit-h.safetensors
reference: chloe_kontext_identity_headshot.png
latent: 768x1024
```

Evaluation rule: do not promote this path to setting or video until the output
preserves Chloe Model v1 face shape, green eyes, dark auburn-black hair,
adult build, skin texture, and overall presence while changing wardrobe.

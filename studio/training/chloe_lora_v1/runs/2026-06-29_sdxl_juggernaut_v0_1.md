# Chloe Identity LoRA v0.1 Run

Date: 2026-06-29
Status: Complete

## Summary

Local SDXL LoRA training completed successfully on Allen's MacBook Pro using
Apple MPS.

Trigger token:

```text
chloe_katastrophe_v1
```

Base model:

```text
tools/ComfyUI/models/checkpoints/Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors
```

Dataset:

```text
tools/lora_datasets/chloe_lora_v1/images
```

Dataset count:

```text
22 PNG images
22 TXT captions
```

Training command:

```bash
scripts/train_chloe_lora_sdxl_local.sh
```

## Training Settings

```text
max_train_steps: 800
network_dim: 16
network_alpha: 8
learning_rate: 0.0001
optimizer: AdamW
resolution: 1024x1024 buckets
batch_size: 1
repeats: 10
mixed_precision: no
device: mps
```

Observed elapsed training time:

```text
1:42:39
```

Final average loss:

```text
0.133
```

## Outputs

Primary final LoRA:

```text
tools/lora_training/chloe_lora_v1/output/chloe_katastrophe_v1_sdxl_lora_v0_1.safetensors
```

Installed ComfyUI copy:

```text
tools/ComfyUI/models/loras/chloe_katastrophe_v1_sdxl_lora_v0_1.safetensors
```

Checkpoints:

```text
tools/lora_training/chloe_lora_v1/output/chloe_katastrophe_v1_sdxl_lora_v0_1-step00000200.safetensors
tools/lora_training/chloe_lora_v1/output/chloe_katastrophe_v1_sdxl_lora_v0_1-step00000400.safetensors
tools/lora_training/chloe_lora_v1/output/chloe_katastrophe_v1_sdxl_lora_v0_1-step00000600.safetensors
tools/lora_training/chloe_lora_v1/output/chloe_katastrophe_v1_sdxl_lora_v0_1-step00000800.safetensors
```

## SHA-256

```text
e7295d6d917bb21f548bfebe14baf08b533dd237310a6783a18524cdabe70efc  chloe_katastrophe_v1_sdxl_lora_v0_1-step00000200.safetensors
cf5f16a5297cdb277daed6930be26ab189b5092ca23e96c78df5fb7a000425ee  chloe_katastrophe_v1_sdxl_lora_v0_1-step00000400.safetensors
57c2ab9eda25734b8dde536882cb9fd35d50653bf5a6755f2900ded87bab2ef1  chloe_katastrophe_v1_sdxl_lora_v0_1-step00000600.safetensors
8a7fd3818db0c2837e2de16f2bf3f93da171ae2b2d68b875c1ba2490689ee114  chloe_katastrophe_v1_sdxl_lora_v0_1-step00000800.safetensors
80f6a99e1bb379ac62c2003825037f8c56489c90929996195c8f0716a11b291d  chloe_katastrophe_v1_sdxl_lora_v0_1.safetensors
```

## First Test Prompts

```text
photo of chloe_katastrophe_v1, simple black dress, standing in a plain studio
photo of chloe_katastrophe_v1, Chloe in a corset, standing in a gothic castle
photo of chloe_katastrophe_v1, archive portrait, soft window light
photo of chloe_katastrophe_v1, futuristic rain street, cinematic still
```

## Notes

The run had a few temporary MPS stalls but recovered without intervention.
Checkpoint files were written at steps 200, 400, 600, and 800.

The final model has not yet been visually evaluated. Next step is a ComfyUI
test workflow using the installed LoRA.


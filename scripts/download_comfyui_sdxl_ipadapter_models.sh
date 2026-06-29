#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
COMFY_DIR="${ROOT_DIR}/tools/ComfyUI"

if [ ! -d "${COMFY_DIR}" ]; then
  echo "ComfyUI is not installed yet. Run scripts/setup_comfyui_local.sh first." >&2
  exit 1
fi

download() {
  local url="$1"
  local out="$2"
  mkdir -p "$(dirname "${out}")"
  if [ -f "${out}" ]; then
    echo "Already present: ${out}"
    return
  fi
  echo "Downloading: ${out}"
  curl -L --fail --continue-at - --output "${out}" "${url}"
}

download \
  "https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/sd_xl_base_1.0.safetensors" \
  "${COMFY_DIR}/models/checkpoints/sd_xl_base_1.0.safetensors"

download \
  "https://huggingface.co/h94/IP-Adapter/resolve/main/models/image_encoder/model.safetensors" \
  "${COMFY_DIR}/models/clip_vision/CLIP-ViT-H-14-laion2B-s32B-b79K.safetensors"

download \
  "https://huggingface.co/h94/IP-Adapter/resolve/main/sdxl_models/ip-adapter-plus-face_sdxl_vit-h.safetensors" \
  "${COMFY_DIR}/models/ipadapter/ip-adapter-plus-face_sdxl_vit-h.safetensors"

download \
  "https://huggingface.co/h94/IP-Adapter/resolve/main/sdxl_models/ip-adapter-plus_sdxl_vit-h.safetensors" \
  "${COMFY_DIR}/models/ipadapter/ip-adapter-plus_sdxl_vit-h.safetensors"

echo
echo "SDXL + IPAdapter model files are in place for local Chloe still-image tests."

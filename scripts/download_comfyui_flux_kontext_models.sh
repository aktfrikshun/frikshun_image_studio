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
  "https://huggingface.co/Comfy-Org/flux1-kontext-dev_ComfyUI/resolve/main/split_files/diffusion_models/flux1-dev-kontext_fp8_scaled.safetensors" \
  "${COMFY_DIR}/models/diffusion_models/flux1-dev-kontext_fp8_scaled.safetensors"

download \
  "https://huggingface.co/Comfy-Org/Lumina_Image_2.0_Repackaged/resolve/main/split_files/vae/ae.safetensors" \
  "${COMFY_DIR}/models/vae/ae.safetensors"

download \
  "https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/clip_l.safetensors" \
  "${COMFY_DIR}/models/text_encoders/clip_l.safetensors"

if [ ! -f "${COMFY_DIR}/models/text_encoders/t5xxl_fp16.safetensors" ]; then
  download \
    "https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/t5xxl_fp16.safetensors" \
    "${COMFY_DIR}/models/text_encoders/t5xxl_fp16.safetensors"
fi

echo
echo "Flux Kontext model files are in place for local image-edit tests."

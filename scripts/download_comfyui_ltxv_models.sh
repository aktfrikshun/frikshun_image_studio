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
  "https://huggingface.co/Lightricks/LTX-Video/resolve/main/ltx-video-2b-v0.9.5.safetensors" \
  "${COMFY_DIR}/models/checkpoints/ltx-video-2b-v0.9.5.safetensors"

download \
  "https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/t5xxl_fp16.safetensors" \
  "${COMFY_DIR}/models/text_encoders/t5xxl_fp16.safetensors"

echo
echo "LTXV v0.9.5 model files are in place for the built-in ltxv_image_to_video workflow."

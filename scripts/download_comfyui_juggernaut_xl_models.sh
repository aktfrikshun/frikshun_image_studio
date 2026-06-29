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
  "https://huggingface.co/RunDiffusion/Juggernaut-XL-v9/resolve/main/Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors" \
  "${COMFY_DIR}/models/checkpoints/Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors"

echo
echo "Juggernaut XL v9 is in place for local photoreal photoshoot tests."

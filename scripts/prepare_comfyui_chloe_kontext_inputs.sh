#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
COMFY_INPUT_DIR="${ROOT_DIR}/tools/ComfyUI/input"

mkdir -p "${COMFY_INPUT_DIR}"

cp \
  "${ROOT_DIR}/studio/reference-packs/chloe_model_v1/packs/character_turnaround_v1/001/001_front_headshot_v1.png" \
  "${COMFY_INPUT_DIR}/chloe_kontext_identity_headshot.png"

cp \
  "${ROOT_DIR}/studio/reference-packs/chloe_model_v1/packs/character_turnaround_v1/005/005_full_body_front_v3.png" \
  "${COMFY_INPUT_DIR}/chloe_kontext_identity_full_body.png"

echo "Prepared Chloe Kontext input images:"
echo "${COMFY_INPUT_DIR}/chloe_kontext_identity_headshot.png"
echo "${COMFY_INPUT_DIR}/chloe_kontext_identity_full_body.png"

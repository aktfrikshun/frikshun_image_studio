#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
COMFY_DIR="${ROOT_DIR}/tools/ComfyUI"
OUT_DIR="${ROOT_DIR}/studio/workflows/comfyui_templates"

if [ ! -d "${COMFY_DIR}/.venv" ]; then
  echo "ComfyUI is not installed yet. Run scripts/setup_comfyui_local.sh first." >&2
  exit 1
fi

mkdir -p "${OUT_DIR}"

cp \
  "${COMFY_DIR}/.venv/lib/python3.12/site-packages/comfyui_workflow_templates_media_video/templates/ltxv_image_to_video.json" \
  "${OUT_DIR}/ltxv_image_to_video.json"

cp \
  "${COMFY_DIR}/.venv/lib/python3.12/site-packages/comfyui_workflow_templates_media_image/templates/video_ltx2_i2v_distilled.json" \
  "${OUT_DIR}/video_ltx2_i2v_distilled.json"

cp \
  "${COMFY_DIR}/.venv/lib/python3.12/site-packages/comfyui_workflow_templates_media_video/templates/image_to_video_wan.json" \
  "${OUT_DIR}/image_to_video_wan.json"

echo "Exported ComfyUI templates to ${OUT_DIR}"

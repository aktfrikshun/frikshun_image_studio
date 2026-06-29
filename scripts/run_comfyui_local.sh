#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
COMFY_DIR="${ROOT_DIR}/tools/ComfyUI"

if [ ! -d "${COMFY_DIR}/.venv" ]; then
  echo "ComfyUI is not installed yet. Run scripts/setup_comfyui_local.sh first." >&2
  exit 1
fi

# shellcheck disable=SC1091
source "${COMFY_DIR}/.venv/bin/activate"
cd "${COMFY_DIR}"

exec python main.py --listen 127.0.0.1 --port "${COMFYUI_PORT:-8188}"

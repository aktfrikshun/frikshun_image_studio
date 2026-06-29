#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TOOLS_DIR="${ROOT_DIR}/tools"
COMFY_DIR="${TOOLS_DIR}/ComfyUI"
PYTHON_BIN="${PYTHON_BIN:-/Users/allentaylor/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3}"

if ! command -v git >/dev/null 2>&1; then
  echo "git is required but was not found on PATH." >&2
  exit 1
fi

if [ ! -x "${PYTHON_BIN}" ]; then
  PYTHON_BIN="$(command -v python3 || true)"
fi

if [ -z "${PYTHON_BIN}" ] || ! "${PYTHON_BIN}" - <<'PY'
import sys
raise SystemExit(0 if sys.version_info >= (3, 10) else 1)
PY
then
  echo "ComfyUI needs Python 3.10+. Set PYTHON_BIN=/path/to/python3.10+ and rerun." >&2
  exit 1
fi

mkdir -p "${TOOLS_DIR}"

if [ ! -d "${COMFY_DIR}/.git" ]; then
  git clone https://github.com/comfyanonymous/ComfyUI.git "${COMFY_DIR}"
else
  git -C "${COMFY_DIR}" pull --ff-only
fi

"${PYTHON_BIN}" -m venv "${COMFY_DIR}/.venv"
# shellcheck disable=SC1091
source "${COMFY_DIR}/.venv/bin/activate"
python -m pip install --upgrade pip
pip install -r "${COMFY_DIR}/requirements.txt"

echo
echo "ComfyUI installed at ${COMFY_DIR}"
echo "Launch with: scripts/run_comfyui_local.sh"

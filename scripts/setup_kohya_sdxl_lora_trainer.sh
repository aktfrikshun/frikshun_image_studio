#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TOOLS_DIR="${ROOT_DIR}/tools"
SD_SCRIPTS_DIR="${TOOLS_DIR}/sd-scripts"
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
  echo "Kohya sd-scripts needs Python 3.10+. Set PYTHON_BIN=/path/to/python3.10+ and rerun." >&2
  exit 1
fi

mkdir -p "${TOOLS_DIR}"

if [ ! -d "${SD_SCRIPTS_DIR}/.git" ]; then
  git clone https://github.com/kohya-ss/sd-scripts.git "${SD_SCRIPTS_DIR}"
else
  git -C "${SD_SCRIPTS_DIR}" pull --ff-only
fi

"${PYTHON_BIN}" -m venv "${SD_SCRIPTS_DIR}/.venv"
# shellcheck disable=SC1091
source "${SD_SCRIPTS_DIR}/.venv/bin/activate"

python -m pip install --upgrade pip setuptools wheel

cd "${SD_SCRIPTS_DIR}"

if [ -f "${SD_SCRIPTS_DIR}/requirements_macos.txt" ]; then
  pip install -r requirements_macos.txt
else
  pip install -r requirements.txt
fi

pip install toml torchvision

echo
echo "Kohya sd-scripts installed at ${SD_SCRIPTS_DIR}"
echo "Run preflight with: scripts/preflight_chloe_lora_trainer.sh"

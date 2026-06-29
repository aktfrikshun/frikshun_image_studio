#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SD_SCRIPTS_DIR="${ROOT_DIR}/tools/sd-scripts"
VENV_PYTHON="${SD_SCRIPTS_DIR}/.venv/bin/python"
DATASET_DIR="${ROOT_DIR}/tools/lora_datasets/chloe_lora_v1/images"
MODEL_PATH="${CHLOE_LORA_BASE_MODEL:-${ROOT_DIR}/tools/ComfyUI/models/checkpoints/Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors}"

if [ ! -x "${VENV_PYTHON}" ]; then
  echo "Missing Kohya trainer venv. Run scripts/setup_kohya_sdxl_lora_trainer.sh first." >&2
  exit 1
fi

if [ ! -f "${SD_SCRIPTS_DIR}/sdxl_train_network.py" ]; then
  echo "Missing sdxl_train_network.py in ${SD_SCRIPTS_DIR}." >&2
  exit 1
fi

if [ ! -d "${DATASET_DIR}" ]; then
  echo "Missing local dataset. Run python3 scripts/prepare_chloe_lora_identity_dataset.py first." >&2
  exit 1
fi

if [ ! -f "${MODEL_PATH}" ]; then
  echo "Missing base model: ${MODEL_PATH}" >&2
  exit 1
fi

PNG_COUNT="$(find "${DATASET_DIR}" -maxdepth 1 -type f -name '*.png' | wc -l | tr -d ' ')"
TXT_COUNT="$(find "${DATASET_DIR}" -maxdepth 1 -type f -name '*.txt' | wc -l | tr -d ' ')"

echo "Base model: ${MODEL_PATH}"
echo "Dataset images: ${PNG_COUNT}"
echo "Dataset captions: ${TXT_COUNT}"

if [ "${PNG_COUNT}" != "${TXT_COUNT}" ]; then
  echo "Image/caption count mismatch." >&2
  exit 1
fi

"${VENV_PYTHON}" - <<'PY'
import importlib.util
import torch

required = ["accelerate", "safetensors", "toml", "torchvision", "transformers"]
missing = [name for name in required if importlib.util.find_spec(name) is None]
print(f"torch: {torch.__version__}")
print(f"mps built: {torch.backends.mps.is_built()}")
print(f"mps available: {torch.backends.mps.is_available()}")
if missing:
    raise SystemExit(f"Missing packages: {', '.join(missing)}")
PY

echo "Preflight passed."

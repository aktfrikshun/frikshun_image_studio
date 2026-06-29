#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SD_SCRIPTS_DIR="${ROOT_DIR}/tools/sd-scripts"
VENV_DIR="${SD_SCRIPTS_DIR}/.venv"
TRAIN_ROOT="${ROOT_DIR}/tools/lora_training/chloe_lora_v1"
DATASET_DIR="${ROOT_DIR}/tools/lora_datasets/chloe_lora_v1/images"
OUTPUT_DIR="${TRAIN_ROOT}/output"
LOG_DIR="${TRAIN_ROOT}/logs"
CONFIG_FILE="${TRAIN_ROOT}/kohya_sdxl_lora_config.local.toml"
DATASET_CONFIG_FILE="${TRAIN_ROOT}/kohya_dataset_config.local.toml"
BASE_MODEL="${CHLOE_LORA_BASE_MODEL:-${ROOT_DIR}/tools/ComfyUI/models/checkpoints/Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors}"
MAX_STEPS="${CHLOE_LORA_MAX_STEPS:-800}"
NETWORK_DIM="${CHLOE_LORA_NETWORK_DIM:-16}"
NETWORK_ALPHA="${CHLOE_LORA_NETWORK_ALPHA:-8}"
LEARNING_RATE="${CHLOE_LORA_LEARNING_RATE:-0.0001}"
REPEATS="${CHLOE_LORA_REPEATS:-10}"

if [ ! -d "${VENV_DIR}" ]; then
  echo "Missing Kohya trainer. Run scripts/setup_kohya_sdxl_lora_trainer.sh first." >&2
  exit 1
fi

python3 "${ROOT_DIR}/scripts/prepare_chloe_lora_identity_dataset.py"
"${ROOT_DIR}/scripts/preflight_chloe_lora_trainer.sh"

mkdir -p "${TRAIN_ROOT}" "${OUTPUT_DIR}" "${LOG_DIR}"

cat > "${DATASET_CONFIG_FILE}" <<EOF
[general]
caption_extension = ".txt"
shuffle_caption = false
keep_tokens = 1

[[datasets]]
resolution = [1024, 1024]
batch_size = 1
enable_bucket = true
bucket_no_upscale = false
bucket_reso_steps = 64

  [[datasets.subsets]]
  image_dir = "${DATASET_DIR}"
  num_repeats = ${REPEATS}
EOF

cat > "${CONFIG_FILE}" <<EOF
pretrained_model_name_or_path = "${BASE_MODEL}"
dataset_config = "${DATASET_CONFIG_FILE}"
output_dir = "${OUTPUT_DIR}"
output_name = "chloe_katastrophe_v1_sdxl_lora_v0_1"
logging_dir = "${LOG_DIR}"

network_module = "networks.lora"
network_dim = ${NETWORK_DIM}
network_alpha = ${NETWORK_ALPHA}

max_train_steps = ${MAX_STEPS}
learning_rate = ${LEARNING_RATE}
unet_lr = ${LEARNING_RATE}
text_encoder_lr = 0.000005
optimizer_type = "AdamW"
lr_scheduler = "constant"
lr_warmup_steps = 0

train_batch_size = 1
max_data_loader_n_workers = 0
persistent_data_loader_workers = false
gradient_checkpointing = true
cache_latents = true
cache_latents_to_disk = true
lowram = true

mixed_precision = "no"
save_precision = "float"
save_model_as = "safetensors"
save_every_n_steps = 200
seed = 1203
max_token_length = 225

caption_dropout_rate = 0.0
caption_tag_dropout_rate = 0.0
clip_skip = 1
EOF

# shellcheck disable=SC1091
source "${VENV_DIR}/bin/activate"
cd "${SD_SCRIPTS_DIR}"

accelerate launch \
  --num_processes 1 \
  --num_machines 1 \
  --mixed_precision no \
  --dynamo_backend no \
  --num_cpu_threads_per_process 2 \
  sdxl_train_network.py \
  --config_file "${CONFIG_FILE}"

echo
echo "LoRA outputs written to ${OUTPUT_DIR}"

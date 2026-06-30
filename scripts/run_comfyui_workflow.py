#!/usr/bin/env python3
"""Run a ComfyUI workflow JSON through the local ComfyUI HTTP API.

The ComfyUI UI exports graph/workflow JSON, while the `/prompt` endpoint expects
an API prompt keyed by node id. This script converts the simple built-in node
workflows we use for Chloe LoRA still-image tests and copies generated outputs
into a chosen experiment folder.
"""

from __future__ import annotations

import argparse
import json
import random
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path
from typing import Any


WIDGET_INPUTS: dict[str, list[str]] = {
    "CheckpointLoaderSimple": ["ckpt_name"],
    "LoraLoader": ["lora_name", "strength_model", "strength_clip"],
    "CLIPTextEncode": ["text"],
    "EmptyLatentImage": ["width", "height", "batch_size"],
    "KSampler": [
        "seed",
        "control_after_generate",
        "steps",
        "cfg",
        "sampler_name",
        "scheduler",
        "denoise",
    ],
    "SaveImage": ["filename_prefix"],
}

EXECUTABLE_NODE_TYPES = set(WIDGET_INPUTS) | {"VAEDecode"}


def load_workflow(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def build_link_index(workflow: dict[str, Any]) -> dict[int, list[Any]]:
    return {int(link[0]): link for link in workflow.get("links", [])}


def node_widget_inputs(node: dict[str, Any]) -> dict[str, Any]:
    names = WIDGET_INPUTS.get(node["type"], [])
    values = node.get("widgets_values", [])
    inputs: dict[str, Any] = {}
    for name, value in zip(names, values):
        if name == "control_after_generate":
            continue
        inputs[name] = value
    return inputs


def convert_ui_workflow_to_api(workflow: dict[str, Any]) -> dict[str, Any]:
    link_index = build_link_index(workflow)
    api_prompt: dict[str, Any] = {}

    for node in workflow.get("nodes", []):
        node_type = node["type"]
        if node_type not in EXECUTABLE_NODE_TYPES:
            continue

        node_id = str(node["id"])
        inputs = node_widget_inputs(node)

        for input_slot in node.get("inputs", []):
            link_id = input_slot.get("link")
            if link_id is None:
                continue
            link = link_index[int(link_id)]
            origin_node_id = str(link[1])
            origin_slot = int(link[2])
            inputs[input_slot["name"]] = [origin_node_id, origin_slot]

        api_prompt[node_id] = {
            "class_type": node_type,
            "inputs": inputs,
        }

    return api_prompt


def find_nodes_by_type(api_prompt: dict[str, Any], class_type: str) -> list[dict[str, Any]]:
    return [node for node in api_prompt.values() if node["class_type"] == class_type]


def set_run_values(api_prompt: dict[str, Any], workflow_stem: str, run_index: int, seed: int | None) -> int:
    resolved_seed = seed if seed is not None else random.randint(1, 2**48 - 1)

    for node in find_nodes_by_type(api_prompt, "KSampler"):
        node["inputs"]["seed"] = resolved_seed

    for node in find_nodes_by_type(api_prompt, "SaveImage"):
        prefix = node["inputs"].get("filename_prefix") or workflow_stem
        node["inputs"]["filename_prefix"] = f"{prefix}_api_{run_index:03d}"

    return resolved_seed


def post_json(server: str, path: str, payload: dict[str, Any]) -> dict[str, Any]:
    request = urllib.request.Request(
        f"http://{server}{path}",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def get_json(server: str, path: str) -> dict[str, Any]:
    with urllib.request.urlopen(f"http://{server}{path}", timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def download_image(server: str, image_info: dict[str, Any], outdir: Path) -> Path:
    params = urllib.parse.urlencode(
        {
            "filename": image_info["filename"],
            "subfolder": image_info.get("subfolder", ""),
            "type": image_info.get("type", "output"),
        }
    )
    url = f"http://{server}/view?{params}"
    target = outdir / image_info["filename"]
    with urllib.request.urlopen(url, timeout=60) as response:
        target.write_bytes(response.read())
    return target


def wait_for_history(server: str, prompt_id: str, timeout_seconds: int, poll_seconds: float) -> dict[str, Any]:
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        history = get_json(server, f"/history/{prompt_id}")
        if prompt_id in history:
            return history[prompt_id]
        time.sleep(poll_seconds)
    raise TimeoutError(f"Timed out waiting for ComfyUI prompt {prompt_id}")


def queue_prompt(server: str, api_prompt: dict[str, Any], client_id: str) -> str:
    response = post_json(
        server,
        "/prompt",
        {
            "prompt": api_prompt,
            "client_id": client_id,
        },
    )
    return response["prompt_id"]


def collect_outputs(server: str, history: dict[str, Any], outdir: Path) -> list[Path]:
    saved: list[Path] = []
    outdir.mkdir(parents=True, exist_ok=True)
    for node_output in history.get("outputs", {}).values():
        for image in node_output.get("images", []):
            saved.append(download_image(server, image, outdir))
    return saved


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workflow", type=Path, help="ComfyUI UI workflow JSON to run")
    parser.add_argument("--server", default="127.0.0.1:8188", help="ComfyUI server host:port")
    parser.add_argument("--outdir", type=Path, default=Path("studio/outputs/comfyui_api"))
    parser.add_argument("--runs", type=int, default=1)
    parser.add_argument("--seed", type=int, default=None, help="Base seed. Each run increments from this seed.")
    parser.add_argument("--timeout", type=int, default=1800, help="Seconds to wait per run")
    parser.add_argument("--poll", type=float, default=2.0, help="Seconds between history polls")
    parser.add_argument("--dry-run", action="store_true", help="Write converted API prompt and do not call ComfyUI")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    workflow = load_workflow(args.workflow)
    api_prompt = convert_ui_workflow_to_api(workflow)
    workflow_stem = args.workflow.stem
    args.outdir.mkdir(parents=True, exist_ok=True)

    if args.dry_run:
        dry_run_path = args.outdir / f"{workflow_stem}.api.json"
        dry_run_path.write_text(json.dumps(api_prompt, indent=2) + "\n", encoding="utf-8")
        print(dry_run_path)
        return

    client_id = str(uuid.uuid4())
    manifest: list[dict[str, Any]] = []

    for run_index in range(1, args.runs + 1):
        run_prompt = json.loads(json.dumps(api_prompt))
        seed = None if args.seed is None else args.seed + run_index - 1
        resolved_seed = set_run_values(run_prompt, workflow_stem, run_index, seed)
        prompt_id = queue_prompt(args.server, run_prompt, client_id)
        print(f"queued run={run_index} prompt_id={prompt_id} seed={resolved_seed}")
        history = wait_for_history(args.server, prompt_id, args.timeout, args.poll)
        outputs = collect_outputs(args.server, history, args.outdir)
        for output in outputs:
            print(output)
        manifest.append(
            {
                "run": run_index,
                "prompt_id": prompt_id,
                "seed": resolved_seed,
                "outputs": [str(path) for path in outputs],
            }
        )

    manifest_path = args.outdir / f"{workflow_stem}.manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(manifest_path)


if __name__ == "__main__":
    try:
        main()
    except urllib.error.URLError as exc:
        raise SystemExit(
            "Could not reach ComfyUI. Start it with `scripts/run_comfyui_local.sh` "
            "or pass --server host:port."
        ) from exc

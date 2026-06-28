from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


API_BASE = "https://api.replicate.com/v1"


def load_env_file(path: Path) -> None:
    if not path.exists():
        return

    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def read_text(path: Path | None, fallback: str) -> str:
    if path:
        return path.read_text(encoding="utf-8").strip()
    return fallback.strip()


def image_data_url(path: Path) -> str:
    mime_type = mimetypes.guess_type(path.name)[0] or "image/png"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def parse_value(value: str) -> Any:
    lowered = value.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if lowered == "null":
        return None
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        return value


def parse_key_value(raw: str) -> tuple[str, Any]:
    if "=" not in raw:
        raise argparse.ArgumentTypeError("Expected KEY=VALUE.")
    key, value = raw.split("=", 1)
    if not key.strip():
        raise argparse.ArgumentTypeError("Input key cannot be empty.")
    return key.strip(), parse_value(value.strip())


def parse_image_key_value(raw: str) -> tuple[str, str]:
    if "=" not in raw:
        raise argparse.ArgumentTypeError("Expected KEY=PATH.")
    key, value = raw.split("=", 1)
    if not key.strip():
        raise argparse.ArgumentTypeError("Image input key cannot be empty.")
    path = Path(value.strip())
    if not path.exists():
        raise argparse.ArgumentTypeError(f"Image input path does not exist: {path}")
    return key.strip(), image_data_url(path)


def request_json(method: str, url: str, token: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = None
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Prefer"] = "wait=60"

    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=90) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Replicate API error {error.code}: {body}") from error


def create_prediction(model: str, token: str, model_input: dict[str, Any]) -> dict[str, Any]:
    owner, name = model.split("/", 1)
    url = f"{API_BASE}/models/{urllib.parse.quote(owner)}/{urllib.parse.quote(name)}/predictions"
    return request_json("POST", url, token, {"input": model_input})


def poll_prediction(prediction: dict[str, Any], token: str) -> dict[str, Any]:
    status = prediction.get("status")
    get_url = prediction.get("urls", {}).get("get")
    while status not in {"succeeded", "failed", "canceled"}:
        if not get_url:
            raise RuntimeError("Replicate response did not include a polling URL.")
        time.sleep(2)
        prediction = request_json("GET", get_url, token)
        status = prediction.get("status")
    return prediction


def output_urls(output: Any) -> list[str]:
    if isinstance(output, str):
        return [output]
    if isinstance(output, list):
        urls: list[str] = []
        for item in output:
            if isinstance(item, str):
                urls.append(item)
            elif isinstance(item, dict):
                url = item.get("url") or item.get("file") or item.get("image")
                if isinstance(url, str):
                    urls.append(url)
        return urls
    if isinstance(output, dict):
        url = output.get("url") or output.get("file") or output.get("image")
        return [url] if isinstance(url, str) else []
    return []


def download(url: str, output_path: Path) -> None:
    with urllib.request.urlopen(url, timeout=120) as response:
        output_path.write_bytes(response.read())


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a single image with Replicate.")
    parser.add_argument("--prompt", default="", help="Prompt text. Ignored when --prompt-file is present.")
    parser.add_argument("--prompt-file", type=Path, help="Path to a prompt text or markdown file.")
    parser.add_argument("--outdir", type=Path, default=Path("studio/outputs/replicate"))
    parser.add_argument("--basename", default="chloe-replicate-test")
    parser.add_argument("--model", default="black-forest-labs/flux-schnell")
    parser.add_argument("--aspect-ratio", default="2:3")
    parser.add_argument("--output-format", default="png", choices=["webp", "jpg", "png"])
    parser.add_argument("--seed", type=int)
    parser.add_argument("--steps", type=int, default=4)
    parser.add_argument(
        "--input",
        action="append",
        default=[],
        type=parse_key_value,
        metavar="KEY=VALUE",
        help="Additional model input field. Can be supplied more than once.",
    )
    parser.add_argument(
        "--image-input",
        action="append",
        default=[],
        type=parse_image_key_value,
        metavar="KEY=PATH",
        help="Additional model image input field encoded as a data URL. Can be supplied more than once.",
    )
    args = parser.parse_args()

    load_env_file(Path(".env"))
    token = os.environ.get("REPLICATE_API_TOKEN")
    if not token:
        raise SystemExit("Set REPLICATE_API_TOKEN in the environment before running this script.")

    prompt = read_text(args.prompt_file, args.prompt)
    if not prompt:
        raise SystemExit("Provide --prompt or --prompt-file.")

    model_input: dict[str, Any] = {
        "prompt": prompt,
        "aspect_ratio": args.aspect_ratio,
        "output_format": args.output_format,
        "num_outputs": 1,
        "num_inference_steps": args.steps,
    }
    if args.seed is not None:
        model_input["seed"] = args.seed
    for key, value in args.input:
        model_input[key] = value
    for key, value in args.image_input:
        model_input[key] = value

    args.outdir.mkdir(parents=True, exist_ok=True)
    prediction = poll_prediction(create_prediction(args.model, token, model_input), token)
    if prediction.get("status") != "succeeded":
        raise RuntimeError(f"Replicate prediction ended with status {prediction.get('status')}: {prediction.get('error')}")

    urls = output_urls(prediction.get("output"))
    if not urls:
        raise RuntimeError(f"Replicate prediction succeeded but no output URLs were found: {prediction.get('output')}")

    image_path = args.outdir / f"{args.basename}.{args.output_format}"
    metadata_path = args.outdir / f"{args.basename}.json"
    download(urls[0], image_path)
    metadata = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "model": args.model,
        "prediction_id": prediction.get("id"),
        "status": prediction.get("status"),
        "prompt": prompt,
        "input": model_input,
        "output_path": str(image_path),
        "replicate_output": prediction.get("output"),
    }
    metadata_path.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    print(image_path)
    print(metadata_path)


if __name__ == "__main__":
    main()

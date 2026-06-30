#!/usr/bin/env python3
"""Generate Chloe LoRA v0.2 wardrobe/accessory identity candidates.

This session keeps backgrounds plain and varies wardrobe, jewelry, framing, and
body position. The goal is reference candidates for identity robustness, not
finished promotional images.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

sys.path.append(str(Path(__file__).resolve().parent))

from run_comfyui_workflow import (  # noqa: E402
    collect_outputs,
    convert_ui_workflow_to_api,
    find_nodes_by_type,
    load_workflow,
    queue_prompt,
    wait_for_history,
)


BASE_IDENTITY = (
    "photo of chloe_katastrophe_v1, Chloe Katastrophe, same recognizable woman "
    "from Chloe Model v1, adult woman age 24-26, delicate Slavic facial "
    "structure, high cheekbones, soft jawline, straight nose, naturally full "
    "lips, gray-green eyes with subtle amber flecks, dark chestnut nearly black "
    "naturally wavy hair, fair skin with light freckles, visible pores, slight "
    "natural redness, subtle under-eye texture, natural feminine hourglass "
    "silhouette, moderately full bust consistent with canon, gently defined "
    "waist, naturally rounded hips, realistic skin texture, quiet intelligent "
    "restrained expression, slight human asymmetry, real person not retouched"
)


BASE_STYLE = (
    "plain neutral seamless studio background, blank wall, simple floor, soft "
    "natural studio lighting, photorealistic wardrobe reference photograph, "
    "identity reference, face sharp, eyes sharp, natural perspective, no complex "
    "setting, no props, no text, no logos"
)


NEGATIVE = (
    "different woman, different face, generic model face, fashion model face, "
    "stock photo face, childlike, teenager, doll face, plastic skin, wax skin, "
    "porcelain skin, airbrushed skin, beauty filter, heavy glamour makeup, "
    "distorted eyes, malformed eyes, asymmetrical eyes, cross eyed, lazy eye, "
    "black eyes, brown eyes, glowing eyes, blurry face, small face, deformed "
    "hands, extra fingers, missing fingers, distorted body, extra limbs, "
    "cropped head, cropped feet, overly muscular, bodybuilder, overly thin, "
    "exaggerated hourglass, exaggerated bust, exaggerated hips, oversized "
    "jewelry, huge pendant, statement necklace, luxury branding, text, "
    "watermark, busy background, city, cemetery, archive desk, car interior, "
    "beach, ruins, dramatic fantasy setting, low quality, jpeg artifacts"
)


PROMPTS: list[dict[str, Any]] = [
    {
        "slug": "black_tank_close_portrait",
        "framing": "close portrait from upper chest up, direct calm eye contact",
        "wardrobe": "simple fitted black cotton tank top, delicate silver chain with small silver wolf pendant",
        "pose": "standing naturally, shoulders relaxed, head level",
    },
    {
        "slug": "charcoal_sweater_waist_up",
        "framing": "waist-up portrait, face large enough for identity review",
        "wardrobe": "soft charcoal wool sweater, small silver compass charm on a fine chain",
        "pose": "standing with one hand relaxed near waist, quiet attentive posture",
    },
    {
        "slug": "gray_hoodie_three_quarter",
        "framing": "three-quarter body portrait from head to mid-thigh",
        "wardrobe": "plain gray zip hoodie over white ribbed tank top, dark fitted shorts, no visible logos",
        "pose": "standing with relaxed weight shift, one hand lightly holding hoodie edge",
    },
    {
        "slug": "black_lace_camisole_upper_thigh",
        "framing": "upper-thigh wardrobe portrait, face and torso both clearly visible",
        "wardrobe": "black lace camisole and high-waisted black briefs, tasteful intimate wardrobe, delicate silver wolf pendant",
        "pose": "standing upright, shoulders relaxed, confident calm posture",
    },
    {
        "slug": "gothic_corset_full_body",
        "framing": "full-body reference photograph, head to feet visible",
        "wardrobe": "fitted black gothic corset over matte black skirt, black tights, simple black ankle boots, tiny ruby ring",
        "pose": "standing naturally with arms relaxed, feet comfortable beneath hips",
    },
    {
        "slug": "black_slip_dress_three_quarter",
        "framing": "three-quarter body portrait, head to knees visible",
        "wardrobe": "simple black slip dress, delicate silver chain with small wolf pendant",
        "pose": "seated on a plain studio stool, upright posture, knees angled slightly, hands resting naturally",
    },
    {
        "slug": "leather_jacket_full_body",
        "framing": "full-body reference photograph, head to feet visible",
        "wardrobe": "worn black leather jacket over plain black tee, dark jeans, black boots, no large accessories",
        "pose": "standing with one hand in jacket pocket, grounded relaxed stance",
    },
    {
        "slug": "blue_shirt_waist_up",
        "framing": "waist-up portrait, direct eye contact, face centered and sharp",
        "wardrobe": "muted blue button-down shirt with rolled sleeves, small ruby stud earrings",
        "pose": "standing with slight head angle, calm listening expression",
    },
    {
        "slug": "athletic_wear_full_body",
        "framing": "full-body reference photograph, head to feet visible",
        "wardrobe": "practical black athletic tank top and charcoal leggings, no logos, no jewelry",
        "pose": "standing neutral front view, arms relaxed, everyday movement body not fitness-model posing",
    },
    {
        "slug": "ruby_memory_close_portrait",
        "framing": "close portrait from upper chest up, face dominant in frame",
        "wardrobe": "plain black long-sleeve top, delicate silver wolf pendant, small bright red ruby ring visible on one hand",
        "pose": "one hand lightly near collarbone so the ruby ring is visible but not dominant",
    },
]


def set_text_nodes(api_prompt: dict[str, Any], positive: str, negative: str) -> None:
    text_nodes = find_nodes_by_type(api_prompt, "CLIPTextEncode")
    if len(text_nodes) < 2:
        raise RuntimeError("Expected at least two CLIPTextEncode nodes")
    text_nodes[0]["inputs"]["text"] = positive
    text_nodes[1]["inputs"]["text"] = negative


def set_sampler(api_prompt: dict[str, Any], seed: int, steps: int, cfg: float) -> None:
    for node in find_nodes_by_type(api_prompt, "KSampler"):
        node["inputs"]["seed"] = seed
        node["inputs"]["steps"] = steps
        node["inputs"]["cfg"] = cfg


def set_output_prefix(api_prompt: dict[str, Any], prefix: str) -> None:
    for node in find_nodes_by_type(api_prompt, "SaveImage"):
        node["inputs"]["filename_prefix"] = prefix


def set_latent(api_prompt: dict[str, Any], width: int, height: int) -> None:
    for node in find_nodes_by_type(api_prompt, "EmptyLatentImage"):
        node["inputs"]["width"] = width
        node["inputs"]["height"] = height
        node["inputs"]["batch_size"] = 1


def build_positive_prompt(spec: dict[str, Any]) -> str:
    parts = [
        BASE_IDENTITY,
        spec["framing"],
        spec["wardrobe"],
        spec["pose"],
        BASE_STYLE,
    ]
    return ", ".join(parts)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--workflow",
        type=Path,
        default=Path("studio/workflows/comfyui_templates/chloe_lora_v0_1_plain_lingerie_texture_tuned_reference.json"),
    )
    parser.add_argument("--server", default="127.0.0.1:8188")
    parser.add_argument(
        "--outdir",
        type=Path,
        default=Path("studio/training/chloe_lora_v2/reference_candidates/2026-06-30_wardrobe_identity_session"),
    )
    parser.add_argument("--seed", type=int, default=22063001)
    parser.add_argument("--steps", type=int, default=32)
    parser.add_argument("--cfg", type=float, default=6.0)
    parser.add_argument("--width", type=int, default=832)
    parser.add_argument("--height", type=int, default=1216)
    parser.add_argument("--timeout", type=int, default=1800)
    parser.add_argument("--poll", type=float, default=2.0)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    workflow = load_workflow(args.workflow)
    base_prompt = convert_ui_workflow_to_api(workflow)
    args.outdir.mkdir(parents=True, exist_ok=True)

    prompt_specs = PROMPTS[: args.limit] if args.limit else PROMPTS
    manifest: dict[str, Any] = {
        "batch": args.outdir.name,
        "purpose": "Chloe LoRA v0.2 wardrobe/accessory identity reference candidates on plain backgrounds.",
        "base_workflow": str(args.workflow),
        "evaluation_focus": [
            "recognizable Chloe facial identity",
            "gray-green eyes and natural skin texture",
            "canon-consistent body proportions",
            "wardrobe/accessory variation without setting complexity",
        ],
        "items": [],
    }

    for index, spec in enumerate(prompt_specs, start=1):
        run_prompt = json.loads(json.dumps(base_prompt))
        seed = args.seed + index - 1
        positive = build_positive_prompt(spec)
        set_text_nodes(run_prompt, positive, NEGATIVE)
        set_sampler(run_prompt, seed, args.steps, args.cfg)
        set_latent(run_prompt, args.width, args.height)
        prefix = f"{index:03d}_{spec['slug']}"
        set_output_prefix(run_prompt, prefix)

        item: dict[str, Any] = {
            "index": index,
            "slug": spec["slug"],
            "seed": seed,
            "status": "candidate_pending_review",
            "framing": spec["framing"],
            "wardrobe": spec["wardrobe"],
            "pose": spec["pose"],
            "positive_prompt": positive,
            "negative_prompt": NEGATIVE,
            "outputs": [],
        }

        if args.dry_run:
            api_path = args.outdir / f"{prefix}.api.json"
            api_path.write_text(json.dumps(run_prompt, indent=2) + "\n", encoding="utf-8")
            item["api_prompt"] = str(api_path)
        else:
            prompt_id = queue_prompt(args.server, run_prompt, "chloe-v2-wardrobe-session")
            print(f"queued {prefix} prompt_id={prompt_id} seed={seed}")
            history = wait_for_history(args.server, prompt_id, args.timeout, args.poll)
            outputs = collect_outputs(args.server, history, args.outdir)
            for output in outputs:
                print(output)
            item["prompt_id"] = prompt_id
            item["outputs"] = [str(path) for path in outputs]

        manifest["items"].append(item)

    manifest_path = args.outdir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(manifest_path)


if __name__ == "__main__":
    main()

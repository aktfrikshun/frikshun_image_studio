#!/usr/bin/env python3
"""Generate a stricter Chloe v0.2 wardrobe identity-lock session.

Round 1 showed that wardrobe variation pulled the face away from Chloe. This
round makes the face larger, keeps poses calmer, avoids full-body-first
composition, and uses stronger identity language plus stronger LoRA weights.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

sys.path.append(str(Path(__file__).resolve().parent))

from run_chloe_v2_wardrobe_session import (  # noqa: E402
    BASE_STYLE,
    NEGATIVE,
    build_positive_prompt,
    set_latent,
    set_output_prefix,
    set_sampler,
    set_text_nodes,
)
from run_comfyui_workflow import (  # noqa: E402
    collect_outputs,
    convert_ui_workflow_to_api,
    find_nodes_by_type,
    load_workflow,
    queue_prompt,
    wait_for_history,
)


IDENTITY_LOCK = (
    "photo of chloe_katastrophe_v1, exact same Chloe Katastrophe identity as "
    "approved Chloe Model v1, wardrobe swap only, do not redesign her face, do "
    "not change facial structure, same gray-green eyes with subtle amber flecks, "
    "same eye shape and spacing, same delicate Slavic facial geometry, high "
    "cheekbones, soft jawline, straight nose, naturally full lips, same fair "
    "skin with freckles and visible pores, same dark chestnut nearly black "
    "naturally wavy hair, adult woman age 24-26, quiet restrained expression, "
    "natural feminine hourglass body, moderately full bust, gently defined "
    "waist, naturally rounded hips, real person, natural imperfections"
)


STRICT_STYLE = (
    "plain neutral gray seamless background, soft even studio light, identity "
    "reference photograph, face large in frame, eyes sharp and natural, skin "
    "texture visible, natural 70mm portrait lens, no environment, no props, no "
    "dramatic styling, no retouching, no glamour face, no beauty filter"
)


STRICT_NEGATIVE = (
    NEGATIVE
    + ", changed face, redesigned face, new person, influencer face, "
    "instagram model, fox-eye makeup, overdone eyebrows, heavy eyeliner, "
    "catwalk pose, sultry beauty pose, open mouth, vacant stare, dead eyes, "
    "strange eyes, glassy eyes, oversized head, tiny head, long neck"
)


PROMPTS: list[dict[str, Any]] = [
    {
        "slug": "black_tank_chest_up_identity",
        "framing": "chest-up portrait, direct calm eye contact, face centered and dominant",
        "wardrobe": "simple fitted black cotton tank top, no visible jewelry",
        "pose": "standing still, shoulders relaxed, head level, neutral documentary posture",
    },
    {
        "slug": "charcoal_sweater_chest_up_identity",
        "framing": "chest-up portrait, direct calm eye contact, face centered and dominant",
        "wardrobe": "soft charcoal wool sweater, delicate silver chain with very small wolf pendant inherited from Gregor",
        "pose": "standing still, relaxed shoulders, quiet attentive expression",
    },
    {
        "slug": "blue_shirt_chest_up_identity",
        "framing": "chest-up portrait, direct eye contact, face centered and sharp",
        "wardrobe": "muted blue button-down shirt with open collar, no logos, no earrings",
        "pose": "standing still with a slight natural head angle, restrained expression",
    },
    {
        "slug": "gray_hoodie_waist_up_identity",
        "framing": "waist-up portrait, face large enough for identity review",
        "wardrobe": "plain gray zip hoodie over black tank top, no visible logos",
        "pose": "standing front-facing, hands outside frame, calm neutral posture",
    },
    {
        "slug": "black_lace_chest_up_identity",
        "framing": "chest-up portrait, face centered and dominant",
        "wardrobe": "black lace camisole, tasteful intimate wardrobe, no necklace",
        "pose": "standing still, shoulders relaxed, direct calm eye contact",
    },
    {
        "slug": "corset_waist_up_identity",
        "framing": "waist-up portrait, face large and sharp, torso visible for wardrobe reference",
        "wardrobe": "fitted black gothic corset, matte fabric, minimal lace, no jewelry",
        "pose": "standing front-facing, arms relaxed outside frame, documentary reference posture",
    },
    {
        "slug": "leather_jacket_waist_up_identity",
        "framing": "waist-up portrait, direct eye contact, face centered",
        "wardrobe": "worn black leather jacket over plain black tee, no large accessories",
        "pose": "standing still, shoulders relaxed, quiet observant expression",
    },
    {
        "slug": "ruby_ring_close_identity",
        "framing": "close portrait from upper chest up, face dominant in frame",
        "wardrobe": "plain black long-sleeve top, small bright red ruby ring from her mother visible near collarbone",
        "pose": "one hand lightly near collarbone, ring small and secondary, direct calm eye contact",
    },
]


def strict_positive_prompt(spec: dict[str, Any]) -> str:
    return ", ".join(
        [
            IDENTITY_LOCK,
            spec["framing"],
            spec["wardrobe"],
            spec["pose"],
            STRICT_STYLE,
        ]
    )


def set_lora_strength(api_prompt: dict[str, Any], model_strength: float, clip_strength: float) -> None:
    for node in find_nodes_by_type(api_prompt, "LoraLoader"):
        node["inputs"]["strength_model"] = model_strength
        node["inputs"]["strength_clip"] = clip_strength


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
        default=Path("studio/training/chloe_lora_v2/reference_candidates/2026-06-30_wardrobe_identity_session_round2"),
    )
    parser.add_argument("--seed", type=int, default=22063101)
    parser.add_argument("--steps", type=int, default=34)
    parser.add_argument("--cfg", type=float, default=5.2)
    parser.add_argument("--width", type=int, default=832)
    parser.add_argument("--height", type=int, default=1216)
    parser.add_argument("--lora-model-strength", type=float, default=1.45)
    parser.add_argument("--lora-clip-strength", type=float, default=1.15)
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
        "purpose": "Second Chloe LoRA v0.2 wardrobe identity session with stricter identity locking and larger faces.",
        "base_workflow": str(args.workflow),
        "identity_strategy": [
            "chest-up and waist-up framing over full-body framing",
            "plain backgrounds only",
            "stronger LoRA weights",
            "wardrobe swap only language",
            "direct eye contact and face-centered composition",
        ],
        "lora_model_strength": args.lora_model_strength,
        "lora_clip_strength": args.lora_clip_strength,
        "items": [],
    }

    for index, spec in enumerate(prompt_specs, start=1):
        run_prompt = json.loads(json.dumps(base_prompt))
        seed = args.seed + index - 1
        positive = strict_positive_prompt(spec)
        set_lora_strength(run_prompt, args.lora_model_strength, args.lora_clip_strength)
        set_text_nodes(run_prompt, positive, STRICT_NEGATIVE)
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
            "negative_prompt": STRICT_NEGATIVE,
            "outputs": [],
        }

        if args.dry_run:
            api_path = args.outdir / f"{prefix}.api.json"
            api_path.write_text(json.dumps(run_prompt, indent=2) + "\n", encoding="utf-8")
            item["api_prompt"] = str(api_path)
        else:
            prompt_id = queue_prompt(args.server, run_prompt, "chloe-v2-identity-locked-wardrobe-session")
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

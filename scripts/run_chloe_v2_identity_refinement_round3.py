#!/usr/bin/env python3
"""Generate Chloe v0.2 wardrobe identity refinement round 3.

Round 2 produced six near-miss candidates. This round keeps only those wardrobe
directions, generates two seeds per prompt, and further narrows the evaluation
to face geometry, skin texture, lips, cheekbones, and eyes.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

sys.path.append(str(Path(__file__).resolve().parent))

from run_chloe_v2_identity_locked_wardrobe_session import (  # noqa: E402
    IDENTITY_LOCK,
    STRICT_NEGATIVE,
    set_lora_strength,
)
from run_chloe_v2_wardrobe_session import (  # noqa: E402
    set_latent,
    set_output_prefix,
    set_sampler,
    set_text_nodes,
)
from run_comfyui_workflow import (  # noqa: E402
    collect_outputs,
    convert_ui_workflow_to_api,
    load_workflow,
    queue_prompt,
    wait_for_history,
)


ROUND3_IDENTITY = (
    IDENTITY_LOCK
    + ", exact approved Chloe face, preserve the same cheekbone structure, "
    "preserve the same mouth and lip shape, preserve natural skin texture and "
    "subtle freckles, skin not too smooth, no cosmetic model smoothing, eyes "
    "must look human and gray-green, expression quiet and intelligent, not "
    "glamorous, not a different pretty woman"
)


ROUND3_STYLE = (
    "plain matte neutral gray background, soft even windowlike studio light, "
    "face is the main subject, face occupies large portion of frame, eyes sharp, "
    "lips and cheekbones clearly visible, natural skin detail visible, "
    "photorealistic identity calibration image, 85mm portrait lens, no props, "
    "no environment, wardrobe secondary to identity"
)


ROUND3_NEGATIVE = (
    STRICT_NEGATIVE
    + ", smooth model skin, generic cheekbones, generic lips, plumped lips, "
    "overfilled lips, sharpened jawline, gaunt cheeks, harsh cheek contour, "
    "makeup transformation, face transplant, different mouth, different nose"
)


PROMPTS: list[dict[str, Any]] = [
    {
        "slug": "black_tank_identity_calibration",
        "framing": "tight chest-up portrait, direct calm eye contact, face centered",
        "wardrobe": "simple fitted black cotton tank top, no visible jewelry",
        "pose": "standing still, shoulders relaxed, head level, neutral documentary posture",
    },
    {
        "slug": "charcoal_sweater_identity_calibration",
        "framing": "tight chest-up portrait, direct calm eye contact, face centered",
        "wardrobe": "soft charcoal wool sweater, no visible jewelry",
        "pose": "standing still, relaxed shoulders, quiet attentive expression",
    },
    {
        "slug": "blue_shirt_identity_calibration",
        "framing": "tight chest-up portrait, direct eye contact, face centered",
        "wardrobe": "muted blue button-down shirt with open collar, no logos, no earrings",
        "pose": "standing still, restrained expression, slight natural head angle",
    },
    {
        "slug": "corset_identity_calibration",
        "framing": "upper-torso portrait, face large and sharp, corset only partially visible",
        "wardrobe": "fitted black gothic corset, matte fabric, minimal lace, no jewelry",
        "pose": "standing front-facing, documentary reference posture, calm direct gaze",
    },
    {
        "slug": "leather_jacket_identity_calibration",
        "framing": "tight waist-up portrait, direct eye contact, face centered",
        "wardrobe": "worn black leather jacket over plain black tee, no large accessories",
        "pose": "standing still, shoulders relaxed, quiet observant expression",
    },
    {
        "slug": "black_top_identity_calibration",
        "framing": "close portrait from upper chest up, face dominant in frame",
        "wardrobe": "plain black long-sleeve top, no visible jewelry",
        "pose": "standing still, direct calm eye contact, hand outside frame",
    },
]


def round3_positive_prompt(spec: dict[str, Any]) -> str:
    return ", ".join(
        [
            ROUND3_IDENTITY,
            spec["framing"],
            spec["wardrobe"],
            spec["pose"],
            ROUND3_STYLE,
        ]
    )


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
        default=Path("studio/training/chloe_lora_v2/reference_candidates/2026-07-01_wardrobe_identity_refinement_round3"),
    )
    parser.add_argument("--seed", type=int, default=22070101)
    parser.add_argument("--variants", type=int, default=2)
    parser.add_argument("--steps", type=int, default=36)
    parser.add_argument("--cfg", type=float, default=4.8)
    parser.add_argument("--width", type=int, default=832)
    parser.add_argument("--height", type=int, default=1216)
    parser.add_argument("--lora-model-strength", type=float, default=1.55)
    parser.add_argument("--lora-clip-strength", type=float, default=1.2)
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
        "purpose": "Chloe LoRA v0.2 wardrobe identity refinement round 3: two seeds per near-miss wardrobe direction, evaluated for face/skin/lips/cheekbones.",
        "base_workflow": str(args.workflow),
        "identity_strategy": [
            "two seeds per near-miss wardrobe direction",
            "tight chest-up or face-dominant framing",
            "wardrobe secondary to identity",
            "explicit cheekbone, lip, skin texture, and eye constraints",
            "stronger LoRA weights with lower CFG",
        ],
        "lora_model_strength": args.lora_model_strength,
        "lora_clip_strength": args.lora_clip_strength,
        "items": [],
    }

    run_index = 0
    for spec in prompt_specs:
        for variant in range(1, args.variants + 1):
            run_index += 1
            run_prompt = json.loads(json.dumps(base_prompt))
            seed = args.seed + run_index - 1
            positive = round3_positive_prompt(spec)
            set_lora_strength(run_prompt, args.lora_model_strength, args.lora_clip_strength)
            set_text_nodes(run_prompt, positive, ROUND3_NEGATIVE)
            set_sampler(run_prompt, seed, args.steps, args.cfg)
            set_latent(run_prompt, args.width, args.height)
            prefix = f"{run_index:03d}_{spec['slug']}_v{variant:02d}"
            set_output_prefix(run_prompt, prefix)

            item: dict[str, Any] = {
                "index": run_index,
                "slug": spec["slug"],
                "variant": variant,
                "seed": seed,
                "status": "candidate_pending_review",
                "framing": spec["framing"],
                "wardrobe": spec["wardrobe"],
                "pose": spec["pose"],
                "positive_prompt": positive,
                "negative_prompt": ROUND3_NEGATIVE,
                "outputs": [],
            }

            if args.dry_run:
                api_path = args.outdir / f"{prefix}.api.json"
                api_path.write_text(json.dumps(run_prompt, indent=2) + "\n", encoding="utf-8")
                item["api_prompt"] = str(api_path)
            else:
                prompt_id = queue_prompt(args.server, run_prompt, "chloe-v2-identity-refinement-round3")
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

#!/usr/bin/env python3
"""Generate Chloe v0.2 eye-repair identity refinement round 4.

Round 3 showed that the local LoRA can preserve Chloe in some close portraits,
but eye shape remains the main failure point. This round avoids side profiles
and distant full-body framing so every output can be judged primarily on
recognizable Chloe eyes, lips, cheekbones, skin texture, and hair.
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


ROUND4_IDENTITY = (
    IDENTITY_LOCK
    + ", exact approved Chloe face from accepted v0.2 references, direct gaze, "
    "both eyes clearly visible and symmetrical, gray-green human eyes, natural "
    "eyelids, aligned pupils, matching iris size, preserve exact mouth and lip "
    "shape, preserve cheekbone structure, natural skin texture, subtle freckles, "
    "not cosmetic model skin, quiet intelligent expression"
)


ROUND4_STYLE = (
    "plain matte neutral gray studio wall, soft even daylight, photorealistic "
    "identity reference photo, 85mm portrait lens, face sharp, eyes are the "
    "primary focus, lips and cheekbones clearly visible, wardrobe secondary, "
    "no props, no jewelry, no environment, no dramatic styling"
)


ROUND4_NEGATIVE = (
    STRICT_NEGATIVE
    + ", misshapen eyes, mismatched eyes, asymmetrical eyes, distorted eyelids, "
    "drooping eyelid, crossed eyes, lazy eye, wandering eye, glassy eyes, doll "
    "eyes, dead eyes, oversized iris, tiny iris, mismatched iris size, misaligned "
    "pupils, blurry eyes, extra eyelid folds, warped eyelashes, overdone eye "
    "makeup, different eye color, generic fashion model face, generic lips, "
    "plumped lips, overfilled lips, sharpened jawline, gaunt cheeks, face "
    "transplant, different nose, different mouth"
)


PROMPTS: list[dict[str, Any]] = [
    {
        "slug": "black_tank_direct_gaze",
        "framing": "tight chest-up portrait, direct eye contact, face centered, both eyes unobstructed",
        "wardrobe": "simple fitted black cotton tank top",
        "pose": "standing still, shoulders relaxed, head level, neutral documentary posture",
    },
    {
        "slug": "charcoal_sweater_direct_gaze",
        "framing": "tight chest-up portrait, direct eye contact, face centered, both eyes unobstructed",
        "wardrobe": "soft charcoal wool sweater",
        "pose": "standing still, relaxed shoulders, quiet attentive expression",
    },
    {
        "slug": "blue_shirt_direct_gaze",
        "framing": "tight chest-up portrait, direct eye contact, face centered, both eyes unobstructed",
        "wardrobe": "muted blue button-down shirt with open collar, no logos",
        "pose": "standing still, restrained expression, slight natural head angle",
    },
    {
        "slug": "corset_direct_gaze",
        "framing": "upper-torso portrait, direct eye contact, face large and sharp, both eyes unobstructed",
        "wardrobe": "fitted black gothic corset, matte fabric, minimal lace",
        "pose": "standing front-facing, calm direct gaze, documentary reference posture",
    },
    {
        "slug": "leather_jacket_direct_gaze",
        "framing": "tight waist-up portrait, direct eye contact, face centered, both eyes unobstructed",
        "wardrobe": "worn black leather jacket over plain black tee",
        "pose": "standing still, shoulders relaxed, quiet observant expression",
    },
    {
        "slug": "black_long_sleeve_direct_gaze",
        "framing": "close portrait from upper chest up, direct eye contact, face dominant in frame",
        "wardrobe": "plain black long-sleeve top",
        "pose": "standing still, direct calm eye contact, head level",
    },
]


def round4_positive_prompt(spec: dict[str, Any]) -> str:
    return ", ".join(
        [
            ROUND4_IDENTITY,
            spec["framing"],
            spec["wardrobe"],
            spec["pose"],
            ROUND4_STYLE,
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
        default=Path("studio/training/chloe_lora_v2/reference_candidates/2026-07-01_eye_repair_round4"),
    )
    parser.add_argument("--seed", type=int, default=22070201)
    parser.add_argument("--variants", type=int, default=2)
    parser.add_argument("--steps", type=int, default=38)
    parser.add_argument("--cfg", type=float, default=4.5)
    parser.add_argument("--width", type=int, default=832)
    parser.add_argument("--height", type=int, default=1216)
    parser.add_argument("--lora-model-strength", type=float, default=1.6)
    parser.add_argument("--lora-clip-strength", type=float, default=1.25)
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
        "purpose": "Chloe LoRA v0.2 eye-repair refinement round 4: direct-gaze wardrobe references evaluated primarily for eye stability.",
        "base_workflow": str(args.workflow),
        "identity_strategy": [
            "direct gaze only",
            "both eyes clearly visible",
            "no side profiles",
            "no distant full-body framing",
            "wardrobe secondary to face and eyes",
            "stronger negative constraints for eye asymmetry and pupil/eyelid distortion",
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
            positive = round4_positive_prompt(spec)
            set_lora_strength(run_prompt, args.lora_model_strength, args.lora_clip_strength)
            set_text_nodes(run_prompt, positive, ROUND4_NEGATIVE)
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
                "negative_prompt": ROUND4_NEGATIVE,
                "outputs": [],
            }

            if args.dry_run:
                api_path = args.outdir / f"{prefix}.api.json"
                api_path.write_text(json.dumps(run_prompt, indent=2) + "\n", encoding="utf-8")
                item["api_prompt"] = str(api_path)
            else:
                prompt_id = queue_prompt(args.server, run_prompt, "chloe-v2-eye-repair-round4")
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

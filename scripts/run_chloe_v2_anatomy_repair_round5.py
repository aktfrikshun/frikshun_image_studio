#!/usr/bin/env python3
"""Generate Chloe v0.2 anatomy-repair identity refinement round 5.

Round 4 improved some eye reads but introduced a stretched-neck / mannequin
upper-body failure. This round keeps eye constraints while adding normal
neck, shoulder, trapezius, and collarbone anatomy constraints.
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


ROUND5_IDENTITY = (
    IDENTITY_LOCK
    + ", exact approved Chloe face from accepted v0.2 references, direct gaze, "
    "both eyes clearly visible and symmetrical, gray-green human eyes, natural "
    "eyelids, aligned pupils, matching iris size, preserve exact mouth and lip "
    "shape, preserve cheekbone structure, natural skin texture, subtle freckles, "
    "normal human neck length, realistic shoulder width, natural shoulder slope, "
    "relaxed trapezius, realistic collarbone spacing, head proportional to body, "
    "quiet intelligent expression"
)


ROUND5_STYLE = (
    "plain matte neutral gray studio wall, soft even daylight, photorealistic "
    "identity reference photo, natural 85mm portrait lens, chest-up framing, "
    "head and shoulders proportional, eyes sharp, lips and cheekbones visible, "
    "wardrobe secondary, no props, no jewelry, no environment, no dramatic styling"
)


ROUND5_NEGATIVE = (
    STRICT_NEGATIVE
    + ", long neck, giraffe neck, swan neck, stretched neck, elongated throat, "
    "overlong throat, tiny shoulders, narrow shoulders, sloped mannequin shoulders, "
    "pinched shoulders, missing trapezius, stretched torso, mannequin body, doll "
    "body, disproportionate head, tiny head, misshapen eyes, mismatched eyes, "
    "asymmetrical eyes, distorted eyelids, drooping eyelid, crossed eyes, lazy eye, "
    "wandering eye, glassy eyes, doll eyes, dead eyes, oversized iris, tiny iris, "
    "mismatched iris size, misaligned pupils, blurry eyes, warped eyelashes, "
    "generic fashion model face, generic lips, plumped lips, overfilled lips, "
    "sharpened jawline, gaunt cheeks, face transplant, different nose, different mouth"
)


PROMPTS: list[dict[str, Any]] = [
    {
        "slug": "black_tank_chest_up_anatomy",
        "framing": "chest-up portrait including natural shoulders and collarbones, direct eye contact, face centered",
        "wardrobe": "simple fitted black cotton tank top",
        "pose": "standing still, shoulders relaxed and level, head upright, normal neck length",
    },
    {
        "slug": "charcoal_sweater_chest_up_anatomy",
        "framing": "chest-up portrait including natural shoulders and collarbones, direct eye contact, face centered",
        "wardrobe": "soft charcoal wool sweater",
        "pose": "standing still, shoulders relaxed and level, head upright, normal neck length",
    },
    {
        "slug": "blue_shirt_chest_up_anatomy",
        "framing": "chest-up portrait including natural shoulders and collarbones, direct eye contact, face centered",
        "wardrobe": "muted blue button-down shirt with open collar, no logos",
        "pose": "standing still, shoulders relaxed and level, slight natural head angle, normal neck length",
    },
    {
        "slug": "corset_chest_up_anatomy",
        "framing": "chest-up portrait including natural shoulders and collarbones, direct eye contact, face centered",
        "wardrobe": "fitted black gothic corset, matte fabric, minimal lace",
        "pose": "standing front-facing, shoulders relaxed and level, head upright, normal neck length",
    },
]


def round5_positive_prompt(spec: dict[str, Any]) -> str:
    return ", ".join(
        [
            ROUND5_IDENTITY,
            spec["framing"],
            spec["wardrobe"],
            spec["pose"],
            ROUND5_STYLE,
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
        default=Path("studio/training/chloe_lora_v2/reference_candidates/2026-07-01_anatomy_repair_round5"),
    )
    parser.add_argument("--seed", type=int, default=22070301)
    parser.add_argument("--variants", type=int, default=2)
    parser.add_argument("--steps", type=int, default=36)
    parser.add_argument("--cfg", type=float, default=4.35)
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
        "purpose": "Chloe LoRA v0.2 anatomy repair round 5: direct-gaze chest-up references evaluated for eyes plus normal neck/shoulder anatomy.",
        "base_workflow": str(args.workflow),
        "identity_strategy": [
            "direct gaze only",
            "chest-up framing with natural shoulders and collarbones",
            "normal neck length and proportional head/shoulders",
            "no side profiles",
            "no full-body distance",
            "wardrobe secondary to face, eyes, and upper-body anatomy",
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
            positive = round5_positive_prompt(spec)
            set_lora_strength(run_prompt, args.lora_model_strength, args.lora_clip_strength)
            set_text_nodes(run_prompt, positive, ROUND5_NEGATIVE)
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
                "negative_prompt": ROUND5_NEGATIVE,
                "outputs": [],
            }

            if args.dry_run:
                api_path = args.outdir / f"{prefix}.api.json"
                api_path.write_text(json.dumps(run_prompt, indent=2) + "\n", encoding="utf-8")
                item["api_prompt"] = str(api_path)
            else:
                prompt_id = queue_prompt(args.server, run_prompt, "chloe-v2-anatomy-repair-round5")
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

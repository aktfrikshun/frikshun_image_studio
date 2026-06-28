# FrikShun Image Studio

FrikShun Image Studio is a local Python pipeline for generating, reviewing,
approving, rejecting, and iterating AI-generated character images for virtual
artists. It ships with a mock Pillow generator, so it works without external APIs.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

The default studio root is `./studio`. You can override it with:

1. CLI option: `--studio-root /path/to/studio`
2. Environment variable: `FRIKSHUN_STUDIO_ROOT`
3. Config file: `frikshun_image_studio.yaml`
4. Default: `./studio`

## Create A Session

```bash
python app.py create-session --name 001_identity_lock --character "Chloe Katastrophe"
```

Session manifests live under `studio/sessions`. They may reference canon and
directive files with absolute paths or paths relative to the studio root:

```yaml
visual_canon_file: chloe-model/appearance.md
image_directives_file: workflows/model-v1-shot-list.md
negative_canon_file: chloe-model/negative-canon.md
```

An example is included at `studio/sessions/examples/chloe_identity_lock.yaml`.

Each image task should include a Creative Brief instead of a bare prompt:

```yaml
images:
  - id: "003"
    filename: 003_right_profile.png
    creative_brief:
      asset_id: "003"
      purpose: Establish Chloe's right profile identity.
      success_criteria: Chloe remains immediately recognizable from approved identity-core references.
      generation_guidance: right profile close-up portrait, natural skin texture, soft window light
      review_focus: nose profile, jawline, eye shape, hairline, and continuity with identity-core images
    status: pending
```

## Generate Mock Images

```bash
python app.py generate --session studio/sessions/examples/chloe_identity_lock.yaml
```

Generated candidates are written to:

```text
studio/outputs/<session_id>/<asset_id>/v001/
```

Each version includes the image, a JSON metadata file, and `prompt_audit.md`
showing how the Creative Brief was grounded in canon and review feedback.

## Review UI

```bash
streamlit run frikshun/ui.py
```

Or launch through the CLI:

```bash
python app.py review
```

The UI lets you select a manifest, inspect generated candidates, approve,
reject with required feedback, or regenerate.

Approved files move to:

```text
studio/reference-decks/approved/<session_id>/
```

Rejected files move to:

```text
studio/reference-decks/rejected/<session_id>/
```

## Rejection Feedback Loop

Rejecting an image stores the reason in the image metadata and appends it to:

```text
studio/rejection-feedback/<session_id>/<asset_id>.md
```

Future regenerations for the same asset include that accumulated feedback as
explicit avoidance guidance:

```text
Previous rejected attempts failed for these reasons. Avoid repeating them:
- face too young
- hair too polished
- too cyberpunk
```

## Approval Metadata

Approved references can carry identity-focused review scores:

```json
{
  "identity_score": 9.6,
  "canon_confidence": 9.4,
  "appearance_score": 9.7,
  "expression_score": 9.5,
  "technical_score": 9.8,
  "continuity_score": 9.6,
  "reference_score": 9.61,
  "reference_priority": "primary",
  "model_status": "identity_core",
  "approved": true,
  "notes": "Why this image should or should not anchor future generations."
}
```

`reference_score` is computed as:

```text
40% identity_score + 30% continuity_score + 20% canon_confidence + 10% technical_score
```

`ReviewStore.approved_references(...)` returns approved references ranked by
that score so future reference packs can prefer stable identity-core images over
merely recent or technically polished ones.

## Creative Brief Composition

`PromptBuilder` always grounds generation in the available character visual
canon, global image creation directives, session description, the asset Creative
Brief, prior rejection feedback, and negative canon. Missing files are reported
as warnings in `prompt_audit.md`, but generation continues when possible.

## Plugging In Real Image APIs

`frikshun/generator.py` defines the `ImageGenerator` interface. The
`OpenAIImageGenerator` class is a stub with TODO comments for API integration.
You can add OpenAI, Flux, or another provider by implementing `generate(...)`
and returning the same `GeneratedImage` metadata contract used by
`MockImageGenerator`.

## Replicate Prototype

The repository includes a small Replicate HTTP prototype for one-off model
tests without storing API tokens in git.

1. Copy `.env.example` to `.env`.
2. Set `REPLICATE_API_TOKEN` in `.env`.
3. Run a prompt file:

```bash
python3 scripts/replicate_image.py \
  --prompt-file studio/workflows/heygen_intro_gothic_glamour_prompt.md \
  --outdir studio/outputs/replicate/heygen_intro_gothic_glamour \
  --basename chloe-heygen-gothic-glamour-001 \
  --model black-forest-labs/flux-schnell \
  --aspect-ratio 2:3 \
  --output-format png
```

Generated prototype images and metadata are written under `studio/outputs`,
which is ignored by git.

Some Replicate models accept reference images or edit targets. The prototype can
send local images as data URLs with `--image-input KEY=PATH` and arbitrary model
settings with `--input KEY=VALUE`:

```bash
python3 scripts/replicate_image.py \
  --prompt-file studio/workflows/heygen_intro_identity_reference_prompt.md \
  --outdir studio/outputs/replicate/heygen_intro_gothic_glamour \
  --basename chloe-heygen-gothic-glamour-reference-001 \
  --model black-forest-labs/flux-kontext-pro \
  --aspect-ratio 2:3 \
  --output-format png \
  --image-input input_image=studio/reference-packs/chloe_model_v1/packs/character_turnaround_v1/001/001_front_headshot_v1.png
```

Only run reference-image tests when it is acceptable to upload that local image
to the selected external provider.

Build a Python app called FrikShun Image Studio.

Purpose:
A local studio pipeline for generating, reviewing, approving, rejecting, and iterating AI-generated character images for virtual artists like Chloe Katastrophe.

Core requirements:

1. Project structure

Create:

frikshun_image_studio/
  app.py
  requirements.txt
  README.md
  studio/
    sessions/
    reference-decks/
      approved/
      rejected/
    outputs/
    logs/
  frikshun/
    __init__.py
    models.py
    session_loader.py
    prompt_builder.py
    generator.py
    review_store.py
    ui.py

2. Session manifest

Use YAML session manifests like:

session_id: 001_identity_lock
character: Chloe Katastrophe
description: Identity lock portraits
base_prompt_file: studio/chloe-model/BASE_CHARACTER_PROMPT.md
negative_prompt_file: studio/chloe-model/negative-canon.md
images:
  - id: 001
    filename: 001_front_neutral_headshot.png
    purpose: Front neutral headshot
    prompt: front-facing portrait, neutral expression, studio lighting
    status: pending
  - id: 002
    filename: 002_three_quarter_left.png
    purpose: Three-quarter left portrait
    prompt: three-quarter left portrait, calm expression
    status: pending

3. Data model

Use Pydantic models for:
- SessionManifest
- ImageTask
- GeneratedImage
- ReviewDecision

Each generated image should have a JSON metadata file beside it:

{
  "asset_id": "001",
  "session_id": "001_identity_lock",
  "filename": "001_front_neutral_headshot.png",
  "prompt": "...",
  "negative_prompt": "...",
  "generation_model": "...",
  "status": "candidate|approved|rejected",
  "rejection_reason": "",
  "created_at": ""
}

4. Prompt builder

PromptBuilder is the heart of the application. It must never send only the asset prompt. Every generation must be grounded in the current canon, visual directives, negative canon, and accumulated rejection feedback.

Combine:
- base character prompt
- task-specific prompt
- rejection feedback from previous rejected versions of the same asset
- negative prompt

When an image is rejected, future generations for the same asset should include a concise avoidance note, for example:

Previous rejection feedback:
- face looked too young
- hair too polished
- too cyberpunk

Revise the next prompt to avoid those issues.

5. Image generation abstraction

Create a generator interface:

class ImageGenerator:
    def generate(self, prompt: str, negative_prompt: str, output_path: Path) -> GeneratedImage:
        ...

Implement:
- MockImageGenerator that creates placeholder PNGs using Pillow with prompt text embedded.
- OpenAIImageGenerator stub with clear TODO comments for API integration.

The app must run fully with MockImageGenerator without external APIs.

6. Review UI

Use Streamlit for the UI.

Features:
- Select session manifest.
- Display pending/candidate images in a gallery.
- Show image metadata and prompt.
- Buttons:
  - Approve
  - Reject
  - Regenerate
- If Reject is clicked:
  - require rejection reason text
  - move image to studio/reference-decks/rejected/<session_id>/
  - update metadata status to rejected
  - save rejection reason
- If Approve is clicked:
  - move image to studio/reference-decks/approved/<session_id>/
  - update metadata status to approved
- Regenerate:
  - use prior rejection reasons for that asset
  - generate a new version with incremented version number

7. File organization

Generated candidates go to:

studio/outputs/<session_id>/<asset_id>/v001/

Approved:

studio/reference-decks/approved/<session_id>/

Rejected:

studio/reference-decks/rejected/<session_id>/

Each image should be stored with matching JSON metadata.

8. CLI

Add Typer CLI commands:

python app.py create-session --name 001_identity_lock
python app.py generate --session studio/sessions/001_identity_lock.yaml
python app.py review
python app.py regenerate --session 001_identity_lock --asset 001

9. README

Document:
- setup
- running Streamlit UI
- creating session manifests
- generating mock images
- review workflow
- how rejection feedback improves future prompts
- how to later plug in OpenAI, Flux, or other image APIs

10. Quality expectations

Use clean, typed Python.
Add helpful comments.
Handle missing files gracefully.
Keep code modular.
Do not hardcode Chloe except in example manifests.
The system should support any future FrikShun virtual artist.

Deliver a working local prototype.

** Additional requirements:

11. Configurable studio root

Do not hardcode the studio folder.

Support a configurable studio root via:

- CLI option: --studio-root /path/to/studio
- environment variable: FRIKSHUN_STUDIO_ROOT
- config file: frikshun_image_studio.yaml

Precedence:
CLI option > environment variable > config file > default ./studio

All sessions, outputs, approved/rejected references, canon files, logs, and metadata should resolve relative to studio_root unless an absolute path is provided.

12. Canon and directive files

Allow each session manifest to specify:

visual_canon_file: /path/to/CHLOE_VISUAL_CANON.md
image_directives_file: /path/to/IMAGE_CREATION_DIRECTIVES.md
negative_canon_file: /path/to/NEGATIVE_CANON.md

These may be absolute paths or paths relative to studio_root.

If files are missing, warn clearly but continue if possible.

13. Prompt composition

When generating an image, the final prompt sent to the image generation tool must be composed from:

A. Character visual canon  
B. Global image creation directives  
C. Session description  
D. Asset-specific purpose and prompt  
E. Prior rejection feedback for this same asset  
F. Negative canon / negative prompt

PromptBuilder should output both:

- final_prompt
- final_negative_prompt

Also save a prompt audit file beside each generated image:

prompt_audit.md

This should include:
- canon text used
- image directives used
- asset prompt
- prior rejection feedback
- final generated prompt
- final negative prompt

14. Rejection feedback loop

When an asset is rejected, store rejection feedback in metadata and in a reusable feedback log:

studio/rejection-feedback/<session_id>/<asset_id>.md

On regeneration, PromptBuilder must include the accumulated feedback for that asset as explicit avoidance guidance:

"Previous rejected attempts failed for these reasons. Avoid repeating them:
- face too young
- hair too polished
- too cyberpunk
"

15. Example Chloe manifest

Include an example manifest:

studio/sessions/examples/chloe_identity_lock.yaml

It should demonstrate:

studio_root-relative canon paths:
visual_canon_file: chloe-model/appearance.md
image_directives_file: workflows/model-v1-shot-list.md
negative_canon_file: chloe-model/negative-canon.md

images:
  - id: 001
    filename: 001_front_neutral_headshot.png
    purpose: Establish Chloe's core facial identity
    prompt: front-facing neutral headshot, 85mm portrait, natural skin texture, calm observant expression
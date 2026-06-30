# Chloe LoRA v0.2 Training Staging

Status: candidate gathering

## Goal

Train a stronger Chloe identity model that can place Chloe in varied shoots and
settings without repeatedly re-describing her face and body.

v0.1 successfully learned parts of Chloe's face, hair, skin texture, and body
canon, but it behaves more like identity gravity than a hard lock. v0.2 should
improve generalization across:

- neutral portraits
- full-body anatomy/body-shape references
- gothic cemetery / ruins / weathered architecture
- sports or movement-oriented wardrobe
- archive desk scenes with camera, photographs, and recovered documents
- performance and social-media settings

## Candidate Discipline

Reference candidates should be staged here before training. Do not automatically
train on every generated image.

Approve a candidate only if:

- Chloe is immediately recognizable.
- Skin texture, eyes, hair, and facial geometry remain close to Chloe Model v1.
- Body proportions stay realistic and canon-consistent.
- The setting is present without replacing identity.
- The image would help the model generalize rather than teach a new face.

Reject or quarantine a candidate if:

- it drifts into a generic fashion, fitness, glamour, or stock-photo face
- the body becomes overly athletic, exaggerated, fragile, or stylized
- the setting dominates and reduces Chloe to a small or blurry figure
- the image contradicts current Chloe visual canon

## Current Candidate Batches

- `reference_candidates/2026-06-30_api_refset_probe/`

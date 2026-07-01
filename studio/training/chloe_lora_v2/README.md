# Chloe LoRA v0.2 Training Staging

Status: candidate gathering

## Goal

Train a stronger Chloe identity model that can preserve her face, body, and
presence across wardrobe and accessory changes before introducing complex
settings.

v0.1 successfully learned parts of Chloe's face, hair, skin texture, and body
canon, but it behaves more like identity gravity than a hard lock. v0.2 should
stay deliberately simple: Chloe on blank or minimally textured backgrounds, with
wardrobe and jewelry variation only.

Use v0.2 to improve generalization across:

- neutral portraits
- full-body anatomy/body-shape references
- everyday wardrobe variations
- gothic wardrobe variations
- lingerie / corset / boudoir wardrobe variations
- sports or movement-oriented wardrobe, without sports environments
- controlled accessory and jewelry changes
- simple studio, plain wall, or neutral floor/background setups

Do not make v0.2 solve environmental storytelling. Once v0.2 can keep Chloe
recognizable across a good number of accepted wardrobe/accessory references,
train it and then move to v0.3 for settings.

## Version Roadmap

- v0.2: identity plus wardrobe/accessory robustness on blank or simple
  backgrounds.
- v0.3: setting robustness after v0.2 is trained, including gothic cemetery,
  archive desk, sports locations, ruins, performance scenes, and social-media
  environments.

## Candidate Discipline

Reference candidates should be staged here before training. Do not automatically
train on every generated image.

Approve a candidate only if:

- Chloe is immediately recognizable.
- Skin texture, eyes, hair, and facial geometry remain close to Chloe Model v1.
- Body proportions stay realistic and canon-consistent.
- The background is blank, plain, or minimally distracting.
- Wardrobe or jewelry variation is present without replacing identity.
- The image would help the model generalize wardrobe/accessories rather than
  teach a new face.

Reject or quarantine a candidate if:

- it drifts into a generic fashion, fitness, glamour, or stock-photo face
- the body becomes overly athletic, exaggerated, fragile, or stylized
- the setting becomes a meaningful scene rather than a simple background
- jewelry or accessories become oversized, symbolic, or visually dominant
- the image contradicts current Chloe visual canon

## Jewelry Reference Priorities

For v0.2, jewelry references should use simple backgrounds and clear framing so
the model learns correct accessory scale.

Prioritize:

- delicate silver chain with small wolf pendant
- small silver compass charm or pendant
- small bright red ruby ring, pendant, or stud earrings

Avoid training on jewelry images where the accessory becomes larger or more
important than Chloe's face, posture, or body silhouette.

## Current Candidate Batches

- `reference_candidates/2026-06-30_api_refset_probe/`
- `reference_candidates/2026-06-30_wardrobe_identity_session/`
- `reference_candidates/2026-06-30_wardrobe_identity_session_round2/`
- `reference_candidates/2026-07-01_wardrobe_identity_refinement_round3/`
- `external_reference_candidates/2026-06-30_foxyai_batch/`

## External Reference Batches

External reference batches may be useful for studying composition, style,
identity consistency, lighting, camera language, wardrobe, accessories, and
future setting diversity. They are not automatically approved as training data.

For v0.2, promote only external images that are useful as wardrobe/accessory
references and whose backgrounds are simple enough not to teach a new setting.
Scene-heavy images should be held for v0.3 planning.

Before external images are promoted into an actual training dataset, review for:

- source/provenance clarity
- unwanted logos or text artifacts
- sunglasses or props hiding identity-critical face features
- overrepresentation of glamour, lingerie, luxury, or influencer styling
- body-shape drift away from Chloe Model v1
- whether the image teaches Chloe identity or teaches a different face

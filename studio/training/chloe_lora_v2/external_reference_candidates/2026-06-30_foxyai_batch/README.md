# FoxyAI External Reference Candidates

Date added: 2026-06-30
Source: FoxyAI images provided by Allen
Status: external reference candidates, not approved training inputs

## Metadata Inspection

The PNG files do not include recoverable generation metadata. Inspection found:

- no `tEXt`, `iTXt`, or `zTXt` PNG prompt chunks
- no visible prompt/model/seed/sampler metadata in raw strings
- high-resolution PNG outputs at either `3280x4096` or `2304x4096`

Exact FoxyAI prompts and model settings cannot be recovered from these files.

## Likely Generation Pattern

These look like identity-conditioned lifestyle/editorial generations rather than
plain text-to-image prompts. FoxyAI is likely using some combination of:

- a persistent character/profile identity model
- face or image-reference conditioning
- high-resolution generation or upscale
- strong lifestyle photography priors
- phone/mirror/selfie composition prompts
- fashion/editorial setting prompts

The key lesson is not the exact Foxy prompt. It is that the identity model needs
stronger reference discipline before it can survive different camera languages.
For Chloe LoRA v0.2, use this batch mainly to study identity, wardrobe,
accessories, pose, lighting, and body continuity. Save scene-heavy lessons like
city street, car interior, beach/resort, desk, sports, and stylized costume for
v0.3 setting work.

## Review Table

| File | Use Status | Notes |
| --- | --- | --- |
| `001_rainy_city_hoodie_reference.png` | candidate_style_reference | Strong environmental realism and face continuity. Text/logo on strap and hoodie make it risky as direct training without cleanup. |
| `002_pink_feather_costume_reference.png` | quarantine_style_only | Good body/costume rendering, but pink angel wings and glamour styling are outside core Chloe canon. Do not train directly unless we intentionally need costume/cabaret variance. |
| `003_sunlit_selfie_black_tank_reference.png` | candidate_pose_reference | Strong selfie/camera realism and skin lighting. Sunglasses, extreme selfie angle, and glamour emphasis make it better for composition study than direct identity training. |
| `004_beach_sunset_casual_reference.png` | candidate_style_reference | Useful lifestyle/environment candidate. Side profile and visible brand/logo hat reduce identity-training value. |
| `005_warm_mirror_camera_lingerie_reference.png` | strong_candidate_pending_review | Strong photoreal mirror/camera reference, good face, body, and warm light. Adult lingerie styling should be balanced against non-lingerie references. |
| `006_night_car_fur_reference.png` | candidate_style_reference | Strong eye/face read and car-interior realism. Fur/luxury styling is not core Chloe and should not dominate training. |
| `007_car_sweater_sunglasses_reference.png` | quarantine_style_only | Strong scene composition but heavy sunglasses, luxury accessories, and car pose obscure identity. Better for prompt/style reconstruction than training. |
| `008_mirror_white_tank_reference.png` | strong_candidate_pending_review | Strong face, body, mirror composition, and natural wardrobe. Phone covers part of frame, but this is a useful casual selfie identity candidate. |
| `009_mirror_hoodie_underwear_reference.png` | candidate_style_reference | Good casual mirror format and expression, but phone occlusion, brand underwear text, and influencer styling make it risky as direct training. |
| `010_pool_resort_swimwear_reference.png` | candidate_style_reference | Useful resort/pool setting and body/pose variation. Side/back angle and resort glamour should be used sparingly. |
| `011_archive_desk_lingerie_fox_necklace_reference.png` | strong_candidate_pending_review | Strong archive desk, camera, recovered-photo context with useful adult wardrobe/body framing. Oversized fox pendant, dramatic pose, and lingerie emphasis require balancing before direct training. |

## Reproduction Notes

To reproduce this quality locally, prioritize:

- stronger identity conditioning than LoRA v0.1 alone
- v0.2 training data with wardrobe/accessory diversity on simple backgrounds
- phone/mirror/selfie workflows for casual realism
- full-resolution candidate generation after low-resolution probing
- v0.3 setting-specific prompts that keep Chloe large in frame
- negative prompts against generic influencer/fashion-model drift

Possible local routes:

- retrain Chloe LoRA v0.2 with carefully approved wardrobe/accessory references
- add an IPAdapter/InstantID-style reference workflow for stronger face locking
- use two-pass generation: first identity/pose, then setting/background
- use inpaint/detailer passes only when the body/scene is already good

## Direct Training Warning

Do not add this whole batch to training automatically.

Several images are visually impressive but would teach the next model unwanted
priors: glamour influencer posing, brand/logotype artifacts, luxury accessories,
pink fantasy wings, sunglasses hiding the eyes, and excessive selfie distortion.

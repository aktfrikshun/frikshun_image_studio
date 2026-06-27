# Prompt Audit

## Asset

- Session: 002_anatomical_reference
- Asset ID: 005
- Filename: 005_full_body_front.png
- Version: v003
- Status: candidate
- Prior rejection type: canon_refinement
- Revision strength: strong

## Revision Strategy

This generation treats v003 as a strong canon refinement after two rejected attempts.

The Body Specification Override supersedes weaker or older body-description language. The model should preserve approved identity and presentation characteristics while changing body proportions only.

## Structured Body Profile

```yaml
body_profile:
  femininity:
    target: medium_high
  bust:
    target: medium_full
  waist:
    target: defined
  hips:
    target: balanced_wide
  thighs:
    target: naturally_full
  shoulders:
    target: slightly_narrow
  muscle_definition:
    target: low
  body_fat_distribution:
    target: naturally_feminine
```

## Body Specification Override

Revision strength: strong.

This Body Specification Override supersedes any weaker or older body-description language in the canon or creative brief for this asset.

Preserve facial identity, expression, posture, realism, lighting, camera framing, clothing, hair, skin texture, freckles, and documentary presentation exactly.

Change body proportions only.

Femininity target: medium_high.

Bust target: medium_full.

Waist target: defined.

Hips target: balanced_wide.

Thighs target: naturally_full.

Shoulders target: slightly_narrow.

Muscle definition target: low.

Body fat distribution target: naturally_feminine.

Translate these structured targets as: Chloe has a naturally feminine hourglass silhouette; her bust is moderately fuller while remaining entirely believable; her waist is visibly more defined; her hips are gently wider to balance her shoulders; her thighs are naturally fuller; her shoulders remain natural and not broad or muscular; muscle definition is subtle; body fat distribution reflects natural femininity rather than athletic conditioning.

Because repeated canon refinements have not produced enough anatomical change, apply a clearly visible but still realistic correction to bust, waist, hips, thigh fullness, and overall feminine silhouette.

Avoid cosmetic enhancement, glamour modeling, pin-up styling, exaggerated breasts, unrealistic waist reduction, sexualized presentation, fitness-influencer physique, bodybuilder definition, and fashion-model thinness.

## Prior Rejection Feedback

- [canon_refinement] Body proportions do not match the desired feminine silhouette for Chloe. While realistic and technically excellent, the physique appears more lean and athletic than intended. Chloe should have a softer, more feminine hourglass figure while remaining believable and capable. Preserve facial identity, posture, realism, and documentary presentation.
- [canon_refinement] Although technically excellent, the anatomical revisions requested after v001 were not significant enough to satisfy the updated canon. Bust size, waist definition, hip width, and overall feminine silhouette remain too similar to the previous version. Chloe still reads as a lean athletic survivor rather than the intended naturally feminine survivor. Preserve facial identity, skin texture, freckles, eye color, hair, expression, posture, realism, documentary presentation, lighting, and camera framing. Increase the magnitude of the body refinement: naturally fuller bust, more defined waist, gently wider hips, slightly fuller thighs, and softer feminine body-fat distribution while remaining believable and non-glamorous.

## Identity References Used

1. `studio/reference-decks/rejected/002_anatomical_reference/005_v002_005_full_body_front.png`
2. `studio/reference-decks/rejected/002_anatomical_reference/005_v001_005_full_body_front.png`
3. `studio/reference-decks/approved/001_identity_lock/004_right_profile_v1.png`
4. `studio/reference-decks/approved/001_identity_lock/003_left_profile_v1.png`
5. `studio/reference-decks/approved/001_identity_lock/002_three_quarter_left_v1.png`
6. `studio/reference-decks/approved/001_identity_lock/001_front_headshot_v1.png`

## Final Generated Prompt

Generate v003 of Asset 005_full_body_front.png for Chloe Katastrophe using rejected v002 as the preserve/reference target. This is a strong canon_refinement revision after two rejected attempts. It is not a redesign.

Body Specification Override: This override supersedes any weaker or older body-description language. Preserve facial identity, expression, posture, realism, lighting, camera framing, clothing, hair, skin texture, freckles, gray-green eyes, neutral attentive expression, and documentary presentation exactly. Change body proportions only.

Structured Body Profile: femininity target medium_high; bust target medium_full; waist target defined; hips target balanced_wide; thighs target naturally_full; shoulders target slightly_narrow; muscle_definition target low; body_fat_distribution target naturally_feminine.

Translate this structured profile visually: Chloe has a naturally feminine hourglass silhouette. Her bust is moderately fuller while remaining entirely believable. Her waist is visibly more defined. Her hips are gently wider to balance her shoulders. Her thighs are naturally fuller. Her shoulders remain natural, not broad or muscular. Muscle definition is subtle. Body fat distribution reflects natural femininity rather than athletic conditioning. She should look like a naturally feminine woman with everyday strength and resilience, not an endurance athlete, fitness influencer, glamour model, or bodybuilder.

Strong revision instruction: The previous two versions were too lean and athletic, with bust size, waist definition, hip width, and overall feminine silhouette too similar across attempts. Apply a clearly visible but still realistic correction to bust, waist, hips, thigh fullness, and overall feminine silhouette. Maintain a believable, non-sexual, documentary anatomical reference. Preserve the same calm front-facing stance, relaxed shoulders, natural arms and hands, feet shoulder-width apart, charcoal athletic tank top, charcoal bike-short length shorts, bare feet, neutral studio background, 50mm lens, eye-level full-body framing from head to feet, soft window light and warm practical lighting.

## Final Negative Prompt

Avoid exaggerated hourglass proportions, glamour-model physique, exaggerated breasts, unrealistic waist reduction, cosmetic surgery aesthetic, pin-up styling, overt sexualization, fashion pose, glamour pose, heavy makeup, accessories, jewelry, distorted hands, distorted feet, AI anatomy artifacts, inconsistent facial identity, plastic skin, airbrushed skin, cinematic drama, harsh shadows, stylized anatomy, childish appearance, glossy fashion retouching, generic model poses, fitness-influencer physique, bodybuilder definition, and fashion-model thinness.

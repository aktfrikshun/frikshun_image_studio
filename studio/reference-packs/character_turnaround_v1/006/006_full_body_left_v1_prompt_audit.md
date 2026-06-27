# Prompt Audit

## Asset

- Session: 002_character_turnaround
- Asset ID: 006
- Filename: 006_full_body_left.png
- Version: v001
- Status: candidate

## Objective

Generate Chloe Katastrophe's canonical full-body left profile as a documentary reference photograph.

This image establishes her complete side silhouette and body proportions. It is not promotional artwork.

## Locked Attributes

- facial identity
- body proportions
- height
- skin tone
- freckles
- hair color
- hair texture
- body composition
- posture
- overall silhouette

## Identity And Body References Used

1. `studio/reference-decks/approved/001_identity_lock/004_right_profile_v1.png`
2. `studio/reference-decks/approved/001_identity_lock/003_left_profile_v1.png`
3. `studio/reference-decks/approved/001_identity_lock/002_three_quarter_left_v1.png`
4. `studio/reference-decks/approved/001_identity_lock/001_front_headshot_v1.png`
5. `studio/reference-decks/approved/002_anatomical_reference/005_full_body_front_v3.png`

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

## Creative Brief

Asset ID: 006

Purpose: Generate Chloe Katastrophe's canonical full-body left profile as a documentary reference photograph. This image establishes her complete side silhouette and body proportions so future generations remain consistent regardless of clothing, lighting, or scene.

Success Criteria: The image should maintain complete facial and body continuity with the approved Identity Core and approved full-body front reference. It should lock Chloe's side profile anatomy, including body depth, bust profile, spine posture, shoulder position, neck posture, abdominal contour, hip projection, glute profile, thigh profile, knee alignment, calf shape, foot profile, and overall side silhouette.

Generation Guidance: Clean documentary-style full-body left profile. Chloe stands naturally in perfect 90-degree left profile, relaxed, simply allowing herself to be photographed. Weight is distributed naturally, arms hang comfortably, hands relaxed, feet natural and approximately shoulder-width apart. Wear the approved Physical Identity attire: fitted charcoal athletic tank top, fitted charcoal athletic shorts, barefoot. No jewelry, no accessories, no makeup emphasis, no glamour styling. Hair remains loose and natural. Maintain the approved physique: naturally feminine hourglass proportions, moderately full bust, gently defined waist, naturally rounded hips, lean but healthy legs, understated muscle tone, realistic feminine body-fat distribution, healthy capable authentic presence. Use soft natural studio lighting, neutral gray background, even illumination, 50mm lens, eye level, natural perspective, full body visible from head to feet.

Review Focus: Validate body depth, bust profile, spine posture, shoulder position, neck posture, abdominal contour, hip projection, glute profile, thigh profile, knee alignment, calf shape, foot profile, and overall side silhouette. Reject body drift from approved 005, profile anatomy inconsistent with front view, exaggerated bust or hip projection, unrealistic spine curvature, unnatural posture, distorted hands or feet, facial identity drift, glamour pose, fashion pose, excessive muscle definition, or overt sexualization.

## Final Generated Prompt

Generate Asset 006_full_body_left.png for Chloe Katastrophe, Session 002_character_turnaround. Create a clean documentary-style full-body left profile reference photograph.

Use approved Identity Core references and approved Body Master front reference 005_full_body_front_v3 as canonical references. Maintain complete facial and body continuity. Do not reinterpret Chloe.

Locked attributes: facial identity, body proportions, height, skin tone, freckles, hair color, hair texture, body composition, posture, and overall silhouette are canonical and must not drift. 005_full_body_front_v3 locks Chloe's body proportions; preserve them in side view.

Chloe stands naturally in perfect 90-degree left profile, relaxed, simply allowing herself to be photographed. Weight distributed naturally, arms hang comfortably, hands relaxed, feet natural and approximately shoulder-width apart.

Approved attire: fitted charcoal athletic tank top, fitted charcoal athletic shorts, barefoot. No jewelry, accessories, makeup emphasis, or glamour styling.

Maintain naturally feminine hourglass proportions, moderately full bust, gently defined waist, naturally rounded hips, lean but healthy legs, understated muscle tone, realistic feminine body-fat distribution, healthy capable authentic presence.

Soft natural studio lighting, neutral gray background, even illumination, 50mm lens, eye level, natural perspective, full body visible from head to feet.

## Final Negative Prompt

Avoid body proportions drifting from approved 005, profile anatomy inconsistent with front view, exaggerated bust projection, exaggerated hip projection, unrealistic spine curvature, unnatural posture, distorted hands or feet, facial identity drift, glamour pose, fashion pose, excessive muscle definition, overt sexualization, pin-up styling, cosmetic enhancement aesthetic, airbrushed skin, plastic skin, cinematic drama, harsh shadows, stylized anatomy, generic model pose, jewelry, accessories, heavy makeup, and fashion-model proportions.

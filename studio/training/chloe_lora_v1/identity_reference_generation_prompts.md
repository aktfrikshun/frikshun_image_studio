# Chloe Identity LoRA v1 Synthetic Expansion Prompts

Purpose: Generate additional identity-only reference candidates for LoRA
training. These are generated artifacts until Allen approves them. They are not
recovered canon by default.

## Base Identity Block

Use this identity block in every prompt:

```text
Chloe Katastrophe, adult woman age 24-26, believable Slavic facial structure,
gray-green eyes with subtle amber flecks, fair skin with natural texture and
light freckles across nose and cheeks, dark chestnut to nearly black naturally
wavy hair, naturally feminine hourglass silhouette, realistic balanced
proportions, gently defined waist, naturally rounded hips, quiet intelligent
presence, subtle asymmetry, authentic person, not plastic, not doll-like
```

## Generation Rules

- Keep wardrobe neutral and simple.
- Prefer plain studio, window light, or simple interior backgrounds.
- Vary angle, expression, focal length, and lighting.
- Do not make wardrobe, sexuality, gothic styling, or any single setting part of
  the identity.
- Reject outputs that look too glamorous, too young, too polished, too generic,
  or unlike Chloe Model v1.

## Candidate Prompts

1. `Photoreal identity reference of [BASE IDENTITY BLOCK], front-facing headshot, neutral expression, soft natural window light, 85mm lens, visible skin texture, simple charcoal top, plain background.`

2. `Photoreal identity reference of [BASE IDENTITY BLOCK], three-quarter left portrait, observant expression, soft studio light, natural hair texture, simple black tank top, plain gray background.`

3. `Photoreal identity reference of [BASE IDENTITY BLOCK], three-quarter right portrait, restrained soft smile, natural freckles and pores, minimal makeup, simple dark knit top, plain background.`

4. `Photoreal identity reference of [BASE IDENTITY BLOCK], left profile portrait, straight nose and soft jawline visible, natural wavy hair, neutral wardrobe, documentary lighting.`

5. `Photoreal identity reference of [BASE IDENTITY BLOCK], right profile portrait, high cheekbones, soft jawline, fair textured skin, quiet expression, simple interior background.`

6. `Photoreal full-body identity reference of [BASE IDENTITY BLOCK], standing naturally, arms relaxed, simple fitted black long-sleeve top and dark jeans, plain studio background, realistic proportions.`

7. `Photoreal full-body identity reference of [BASE IDENTITY BLOCK], standing in profile, neutral fitted clothing, quiet posture, natural body proportions, plain studio background.`

8. `Photoreal three-quarter full-body identity reference of [BASE IDENTITY BLOCK], simple fitted dark dress, natural posture, full figure visible head to toe, plain studio background.`

9. `Photoreal seated identity reference of [BASE IDENTITY BLOCK], relaxed but alert posture, simple black sweater, gray-green eyes looking toward camera, natural skin texture, window light.`

10. `Photoreal identity reference of [BASE IDENTITY BLOCK], subtle dry half-smile, slight asymmetry, natural hair falling across one shoulder, simple neutral wardrobe, studio portrait.`

11. `Photoreal identity reference of [BASE IDENTITY BLOCK], melancholy expression, eyes carrying grief and intelligence, natural freckles, restrained performance, simple dark wardrobe.`

12. `Photoreal identity reference of [BASE IDENTITY BLOCK], determined expression, direct gaze, minimal makeup, natural skin texture, simple background, cinematic but not stylized.`

13. `Photoreal identity reference of [BASE IDENTITY BLOCK], listening expression, eyes turned slightly off camera, natural wavy hair, simple dark shirt, quiet interior light.`

14. `Photoreal identity reference of [BASE IDENTITY BLOCK], remembering expression, distant focus, soft mouth tension, natural hair and skin texture, plain interior background.`

15. `Photoreal identity reference of [BASE IDENTITY BLOCK], controlled anger, restrained face, intensity in eyes, natural texture, simple black top, uncluttered background.`

16. `Photoreal outdoor identity reference of [BASE IDENTITY BLOCK], overcast daylight, simple dark coat, natural wind in hair, face still clearly visible, authentic documentary portrait.`

17. `Photoreal identity reference of [BASE IDENTITY BLOCK], warm tungsten side light revealing subtle amber flecks in gray-green eyes, natural skin texture, neutral wardrobe.`

18. `Photoreal identity reference of [BASE IDENTITY BLOCK], cool daylight, front portrait, minimal makeup, visible pores and freckles, simple background, restrained expression.`

19. `Photoreal identity reference of [BASE IDENTITY BLOCK], shoulder-length natural waves, quiet hopeful expression, gray-green eyes, fair textured skin, simple dark blouse.`

20. `Photoreal identity reference of [BASE IDENTITY BLOCK], mid-back natural wavy hair, neutral expression, simple fitted clothing, plain background, no glamour posing.`

## Rejection Checklist

Reject and do not train on a candidate if it has:

- a face that would not pass as Chloe Model v1
- glossy plastic skin or airbrushed texture
- fashion-model posing as the default identity
- exaggerated bust, waist, hips, or legs
- visible youthfulness below adult Chloe canon
- locked costume language such as corset, lingerie, gothic castle, or stagewear
- heavy makeup that changes facial identity
- severe hands, limbs, neck, torso, eye, or mouth artifacts


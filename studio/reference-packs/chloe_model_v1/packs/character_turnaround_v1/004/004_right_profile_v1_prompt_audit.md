# Prompt Audit

## Canon Text Used

`studio/chloe-model/appearance.md`

Current Chloe visual canon was read immediately before generation, including Natural Imperfection, physical appearance, Emotional Presence, Presence, lighting, camera language, image tone, emotional tone, and negative canon.

## Approved References Used

Ranked by `reference_score` through `ReviewStore.approved_references("001_identity_lock", model_status="identity_core")`:

1. `studio/reference-decks/approved/001_identity_lock/003_left_profile_v1.png` — reference score 9.76, primary
2. `studio/reference-decks/approved/001_identity_lock/002_three_quarter_left_v1.png` — reference score 9.61, primary
3. `studio/reference-decks/approved/001_identity_lock/001_front_headshot_v1.png` — reference score 9.09, primary

## Creative Brief

Asset ID: 004

Purpose: Establish Chloe's canonical right facial profile as the mirror counterpart to Image 003. This image exists to lock facial geometry and silhouette, not to create a dramatic portrait.

Success Criteria: This image should immediately read as the same woman shown in Images 001, 002, and 003. The right facial profile should become part of Chloe's permanent identity reference pack. The image should feel documentary rather than promotional.

Generation Guidance: Produce a clean right-profile portrait of Chloe. Her posture is relaxed and natural. She is looking slightly above the horizon, as though quietly observing something in the distance. Her expression is calm, thoughtful, attentive, and emotionally present. She is not posing. She is simply existing in the moment. Hair should fall naturally with a few loose strands. Skin should retain natural texture and subtle freckles. Natural imperfection and small asymmetries are preferred over mathematical symmetry. No glamour styling. No dramatic makeup. No cinematic action. No exaggerated emotion.

Review Focus: Nose profile, chin and jawline continuity, ear placement, hairline consistency, eye shape in profile, neck posture, right-side facial silhouette, and overall resemblance to approved identity references.

## Prior Rejection Feedback

_None for asset 004._

## Final Generated Prompt

Use case: photorealistic-natural
Asset type: FrikShun Image Studio candidate reference image
Primary request: Generate Asset 004 — Right Profile, filename 004_right_profile.png. This is the mirror counterpart to Asset 003 Left Profile and should lock Chloe's right facial geometry.
Input images: Use the three visible approved primary identity references as anchors, weighted by reference score: 1) 003_left_profile_v1.png as the strongest profile/silhouette reference, 2) 002_three_quarter_left_v1.png as the strongest three-quarter identity reference, 3) 001_front_headshot_v1.png as the foundational frontal identity anchor. Maintain the same woman: facial proportions, eye shape, nose, lips, freckles, natural skin texture, hair color, hairline, and hair behavior.
Creative Brief - Asset ID: 004
Creative Brief - Purpose: Establish Chloe's canonical right facial profile as the mirror counterpart to 003. This image exists to lock facial geometry and silhouette, not to create a dramatic portrait.
Creative Brief - Success Criteria: The image immediately reads as the same woman shown in Images 001, 002, and 003. The right facial profile can become part of Chloe's permanent identity reference pack. The image feels documentary rather than promotional.
Creative Brief - Generation Guidance: Produce a clean right-profile portrait of Chloe. Her posture is relaxed and natural. She is looking slightly above the horizon, as though quietly observing something in the distance. Her expression is calm, thoughtful, attentive, and emotionally present. She is not posing; she is simply existing in the moment. Hair falls naturally with a few loose strands. Skin retains natural texture and subtle freckles. Natural imperfection and small asymmetries are preferred over mathematical symmetry. No glamour styling, no dramatic makeup, no cinematic action, no exaggerated emotion.
Creative Brief - Review Focus: nose profile, chin and jawline continuity, ear placement, hairline consistency, eye shape in profile, neck posture, right-side facial silhouette, overall resemblance to approved identity references.
Current visual canon: Chloe Katastrophe is an adult woman, apparent age 24-26, primarily Slavic heritage, delicate Slavic facial structure, high cheekbones, soft jawline, straight nose, naturally full lips, fair skin with natural texture and light freckles, dark chestnut to nearly black naturally wavy hair, gray-green eyes with subtle amber flecks only as reflected warm light. She has quiet resilience, attentive presence, and a lived-in expression rather than a performed one. She should never appear mathematically symmetrical; natural variation reinforces that she is believable rather than idealized.
Composition/framing: true right facial profile, eye-level camera, frame from upper chest upward, 85mm portrait lens feel, minimal perspective distortion, neutral background, shallow depth of field.
Lighting/mood: soft window light plus warm practical interior lighting. The purpose is facial definition, not atmosphere.
Style/medium: photorealistic documentary portrait photography, realistic anatomy, natural hair and skin, grounded and human.
Constraints: Preserve Chloe's approved identity from the visible references. Do not make a different woman. Do not beautify into a fashion or glamour portrait. Prioritize right-side facial geometry, silhouette, and continuity with 003.

## Final Negative Prompt

Avoid: childish, naive, anime, cartoon, superhero, fantasy, cyberpunk stereotype, robot, exposed machinery, influencer selfie, glamour model, fashion-model styling, glossy futuristic armor, excessive accessories, overly sexualized, hyper-aggressive, plastic-perfect skin, porcelain perfection, harsh studio flash, oversaturated neon, nightclub aesthetics, fisheye, extreme wide-angle distortion, dramatic makeup, cinematic action, exaggerated emotion, perfect mathematical symmetry, watermark, text.

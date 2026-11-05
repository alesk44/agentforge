# Marée Jersey Ad Studio — zero-budget edition

A cloud-renderable, no-paid-API video production workspace for Marée Jersey.

## Production brief
The Jersey-specific 45-second film storyboard is in STORYBOARD.md. It follows one catch from the sea to the restaurant: fisherman photographs the fish → species and traceability details → the same catch appears for the chef with a recipe idea → direct order → illustrative under-one-hour delivery sequence → brand reveal.

## Current renderer status
- Renderer updated to a 45-second, seven-scene storyboard animatic.
- Produces vertical (1080×1920) and landscape (1920×1080) MP4s using Python, Pillow, FFmpeg and eSpeak NG.
- This remains a motion-graphics animatic, not real video footage. It does not yet ingest live-action clips or generate photorealistic AI video.
- No paid API, token, GPU or subscription is required for this graphics-only render.
- The GitHub Actions workflow has not yet been run; no MP4 output has been verified.

## Logo asset
The renderer accepts an exact logo file at assets/logo.png, assets/logo.jpg or assets/logo.jpeg. It scales the image to fit the end-card area without redrawing or recolouring it. The logo image supplied in the conversation has not yet been committed to this repository branch; do not assume it is already included in a render.

## Jersey footage and permissions
Start with the Visit Jersey Media Asset Library: https://business.jersey.com/media/media-tools/asset-library/
Check the rights and restrictions on each selected asset before using it in a commercial advertisement. Do not assume public visibility grants advertising rights.

Useful geographic references:
- Gorey Harbour and Mont Orgueil: https://www.jersey.com/things-to-do/points-of-interest/listings/gorey-harbour/
- Rozel Bay: https://www.jersey.com/things-to-do/points-of-interest/listings/rozel-bay/
- Jersey landmarks: https://www.jersey.com/things-to-do/attractions/sights-and-landmarks/
- Ports of Jersey outlying harbours: https://www.ports.je/jerseymarinas/marinas/berthsoutlyingharbours/

Keep an asset manifest with source URL, creator, licence/permission, attribution and permitted commercial/social-ad use. Prefer genuine Jersey fishing vessels and waterfront footage; do not label generic stock boats as local vessels.

## Truth and brand safeguards
- App screens are illustrative until the corresponding live features are verified.
- Keep the same confirmed fish species in the catch, listing, chef and delivery shots.
- Do not invent a fisherman, vessel name/registration, catch metadata, QR record, verified badge, restaurant partner, price or delivery proof.
- “Delivered in under an hour” is a campaign scenario until operational performance supports it; it must not be presented as an existing guarantee.
- No paid API, paid stock subscription, paid GPU or new recurring cost without explicit approval.

## Planned deliverables
- 45-second vertical master and landscape adaptation.
- Real Jersey footage, once sourced and commercially cleared.
- British English voice-over, sound mix and captions.
- Exact official logo on the final card, unchanged.
- Asset/licence manifest and QA checklist.

## Run the current animatic
Requirements: Python 3.11+, FFmpeg, eSpeak NG.
```bash
pip install -r requirements.txt
python render.py --format both --output dist
```

## GitHub Actions
1. Keep the repository public to use standard GitHub-hosted Actions runners without charge.
2. Open Actions → Render Marée Jersey Ad → Run workflow.
3. Download the maree-jersey-ad artifact after a successful run.

No secrets are required for the current graphics-only workflow.

## Licence
The code in this folder is MIT-licensed. Third-party footage, music, fonts and logos retain their own licences.

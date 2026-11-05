# Marée Jersey Ad Studio — zero-budget edition

A cloud-renderable, no-paid-API video production workspace for Marée Jersey.

## Production brief
The Jersey-specific 45-second film storyboard is in STORYBOARD.md. It defines the complete journey: real Jersey coastline and fishing boat → fisherman photographs the catch → species and traceability screen → restaurant discovers the same fish and recipe idea → direct order → illustrative under-one-hour delivery sequence → official app/logo reveal.

The storyboard is a production specification, not a claim that the pictured app functions or delivery promise are already live.

## Current renderer status
- The existing Python + Pillow + FFmpeg + eSpeak NG renderer still produces the earlier 24-second motion-graphics prototype.
- It does not yet ingest the real video clips described in STORYBOARD.md.
- The GitHub Actions workflow has not yet been run; no MP4 output has been verified.
- It requires no AI API, paid token, GPU or subscription for the current graphics-only render.

## Jersey footage and permissions
Start with the Visit Jersey Media Asset Library: https://business.jersey.com/media/media-tools/asset-library/
It offers public imagery and video for destination promotion, but check the rights and restrictions on each selected asset before using it in a commercial advertisement. Do not assume that a publicly viewable image is automatically cleared for paid advertising.

Useful geographic references:
- Gorey Harbour and Mont Orgueil: https://www.jersey.com/things-to-do/points-of-interest/listings/gorey-harbour/
- Rozel Bay: https://www.jersey.com/things-to-do/points-of-interest/listings/rozel-bay/
- Jersey landmarks: https://www.jersey.com/things-to-do/attractions/sights-and-landmarks/
- Ports of Jersey outlying harbours: https://www.ports.je/jerseymarinas/marinas/berthsoutlyingharbours/

Keep a manifest for every asset: exact source URL, creator, licence/permission, attribution and permitted commercial/social-ad use. Prefer genuine Jersey fishing vessels and waterfront footage; do not label generic stock boats as local vessels.

## Truth and brand safeguards
- App screens are illustrative until the corresponding live features are verified.
- Keep the same confirmed fish species in the catch, listing, chef and delivery shots.
- Do not invent a fisherman, vessel name/registration, catch metadata, QR record, verified badge, restaurant partner, price or delivery proof.
- “Delivered in under an hour” is a campaign scenario until operational performance supports it; it must not be presented as an existing guarantee.
- The exact official Marée Jersey logo must be supplied as a clean standalone asset and used unchanged. A collage/logo sheet is not acceptable.
- No paid API, paid stock subscription, paid GPU or new recurring cost without explicit approval.

## Planned deliverables
- 45-second vertical master (1080×1920, H.264 MP4).
- 45-second landscape adaptation (1920×1080, H.264 MP4).
- Burned-in captions and separate subtitle file.
- British English voice-over and sound mix.
- Asset/licence manifest and QA checklist.

## Run the current prototype
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

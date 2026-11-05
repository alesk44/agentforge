# Marée Jersey Ad Studio — zero-budget cinematic animation

A reusable, no-paid-API motion-design workspace for Marée Jersey.

## Production direction
Premium cinematic 2.5D animation: layered Atlantic sea, stylised Jersey coast and harbour/castle silhouette, a fishing boat, fisherman, one recurring fish motif, demo app screens, chef, order notification, delivery handover and brand end-card. Slow camera drift, animated swell, depth layers, restrained navy/teal/coral palette and British English voice-over.

This is original motion graphics, not photorealistic AI video or live-action footage. It avoids third-party footage and location-image permissions by using original stylised illustrations. Jersey is evoked through an original coastline/castle-inspired silhouette, not represented as documentary footage of a precise location.

## Current renderer
- `render.py` creates a 45-second, seven-scene animated film.
- Exports vertical 1080×1920 and landscape 1920×1080 H.264 MP4.
- Builds at a smaller internal frame size and scales for delivery.
- Creates a British English voice-over with eSpeak NG when installed.
- Creates a separate SRT subtitle file.
- Uses the exact official logo only if supplied at `assets/logo.png`, `.jpg` or `.jpeg`; it is uniformly scaled, never redrawn or recoloured.
- If the logo asset is absent, the end-card uses text only. The logo supplied in the conversation is not yet committed to this branch.
- Optional music can be added as `assets/music.mp3`, but only with documented commercial-use rights. The render works without it.

## Free toolchain
Python 3.11+, Pillow, FFmpeg and eSpeak NG. No paid API, stock footage, GPU, token or recurring subscription is required. GitHub-hosted Actions may run on a public repository's standard hosted runner within the account's applicable usage limits. Repeated renders should respect those limits.

## Render locally
```bash
pip install -r requirements.txt
sudo apt-get install ffmpeg espeak-ng fonts-dejavu-core
python render.py --format both --output dist
```

## GitHub Actions
Open Actions → Render Marée Jersey Ad → Run workflow. Download the `maree-jersey-ad` artifact after a successful run. The workflow has not yet been run in this branch, so no MP4 output is claimed as verified.

## Reusable kit
See:
- `ANIMATION_KIT.md` — visual system, scene kit, reuse and truth safeguards.
- `STORYBOARD.md` — 45-second story and shot timing.
- `ASSET_RIGHTS_REGISTER.md` — rights/release register (not required for the original graphic scenes, but useful for any future external assets).

## Truth and brand safeguards
- App screens are demo illustrations until corresponding live features are verified.
- Use the same fish motif through catch, listing, chef and handover.
- Species, vessel, fisherman, catch metadata, method, QR record, restaurant partner, price and delivery proof are not invented.
- “UNDER 1 HOUR” is explicitly an illustrative campaign scenario, not an existing guarantee.
- Never imply cold-chain compliance or real delivery performance without evidence.
- Official logo remains unchanged.

## Licence
The code in this folder is MIT-licensed. The supplied Marée Jersey logo remains the user's brand asset. Optional music/fonts/other assets retain their own licences.

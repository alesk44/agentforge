# Marée Jersey Ad Studio — zero-budget edition

A cloud-renderable, no-paid-API advertising video pipeline for Marée Jersey.

## What it does
- Produces a 24-second cinematic vertical ad (9:16) and landscape cut (16:9).
- Uses Python + Pillow + FFmpeg + eSpeak NG; no AI API, paid token, GPU, or subscription.
- Supports an optional music bed and the official Marée Jersey logo as a separate, unchanged image asset.
- Includes a GitHub Actions workflow that renders both MP4s and publishes them as downloadable artifacts.

## Honest limits
This first version creates animated motion-graphics scenes, not AI-generated photorealistic footage. The current renderer does not yet ingest video clips automatically. The footage list below is the planned next production upgrade; adding clips alone will not change the render:
- `scene-01.mp4` — Jersey coastline / sea at dawn
- `scene-02.mp4` — fishing boat / nets
- `scene-03.mp4` — fresh catch on ice
- `scene-04.mp4` — chef preparing fish
- `scene-05.mp4` — plated seafood
- `scene-06.mp4` — restaurant / island community

Optional inputs supported now:
- `assets/logo.png` — the exact official logo file. It is placed unchanged; never redraw or recolour it.
- `assets/music.mp3` — music you own or are licensed to use.

The clean, standalone official logo has not yet been added to this branch. A logo sheet/collage is not an acceptable substitute.

Do not use stock footage unless its licence permits commercial advertising. Keep a record of each asset's source, licence and creator. Pexels offers free commercial-use content under its licence, but API access requires a free API key; this pipeline does not require one. See https://www.pexels.com/license/ and https://www.pexels.com/api/documentation/.

## Run locally
Requirements: Python 3.11+, FFmpeg, eSpeak NG.
```bash
pip install -r requirements.txt
python render.py --format both --output dist
```

## Current status

The code and workflow are committed on the `maree-jersey-ad-studio` branch. The workflow has not yet been run, so no MP4 has been verified. This is a motion-graphics proof of pipeline, not the final photorealistic campaign.

## Run in GitHub
1. Keep this repository public to use standard GitHub-hosted Actions runners without charge.
2. Open Actions → **Render Marée Jersey Ad** → Run workflow.
3. Download the `maree-jersey-ad` artifact when the job finishes.

No secrets are required. No external API is called. Do not add payment tokens or private credentials.

## Creative direction
Campaign: **THE SEA DOESN'T WAIT.**
Public copy is British English. Brand line: **MARÉE JERSEY — FROM BOAT TO PLATE.**
The official logo is an immutable asset and must be supplied as `assets/logo.png`.

## Licence
The code in this folder is MIT-licensed. Third-party footage, music, fonts and logos retain their own licences.
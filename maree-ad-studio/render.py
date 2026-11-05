#!/usr/bin/env python3
"""Render a short Marée Jersey motion-graphics ad using local open tools only."""
from __future__ import annotations
import argparse, math, os, shutil, subprocess, textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 720, 1280
FPS = 25
DURATION = 24
OUT = Path("dist")
ASSETS = Path("assets")
SCENES = [
    ("THE SEA", "DOESN'T WAIT.", "JERSEY. THE ISLAND. THE OCEAN.", (4, 242, 220)),
    ("A BETTER", "CONNECTION.", "LOCAL FISHERMEN. LOCAL RESTAURANTS.", (255, 111, 97)),
    ("FRESH FROM", "THE WATER.", "DISCOVER THE DAILY CATCH.", (4, 242, 220)),
    ("STRAIGHT TO", "THE KITCHEN.", "GIVE YOUR MENU A LOCAL STORY.", (255, 111, 97)),
    ("KNOW YOUR", "SOURCE.", "MORE TRANSPARENCY. MORE CONNECTION.", (4, 242, 220)),
    ("FROM BOAT", "TO PLATE.", "MARÉE JERSEY  •  JOIN THE MOVEMENT", (255, 111, 97)),
]

def font(size: int, bold: bool = True):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for p in candidates:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def gradient_scene(index: int, title1: str, title2: str, subtitle: str, accent: tuple[int,int,int], vertical: bool, out: Path):
    w, h = (1080, 1920) if vertical else (1920, 1080)
    im = Image.new("RGB", (w, h))
    px = im.load()
    phase = index * 0.63
    for y in range(h):
        t = y / max(1, h - 1)
        for x in range(w):
            glow = max(0.0, 1.0 - math.sqrt(((x/w)-0.18)**2 + ((y/h)-0.28)**2) * 1.8)
            wave = 0.5 + 0.5 * math.sin((x/w*2.3 + y/h*1.7 + phase) * math.pi)
            k = 0.12 + 0.13 * glow + 0.035 * wave
            px[x,y] = (int(5+accent[0]*k), int(18+accent[1]*k*0.48), int(31+accent[2]*k*0.55))
    d = ImageDraw.Draw(im, "RGBA")
    # Abstract sea lines / horizon accents
    for j in range(11):
        yy = int(h*0.57 + j*h*0.027)
        d.arc((-w*0.18, yy-h*0.08, w*1.15, yy+h*0.12), 0, 180, fill=(*accent, 38), width=max(2, w//700))
    margin = int(w*0.075)
    d.rounded_rectangle((margin, int(h*.09), margin+int(w*.12), int(h*.105)), radius=8, fill=(*accent,255))
    f1, f2 = font(int(w*.105)), font(int(w*.12))
    y1, y2 = int(h*.31), int(h*.405)
    d.text((margin, y1), title1, font=f1, fill=(245,250,252,255), stroke_width=1, stroke_fill=(0,0,0,70))
    d.text((margin, y2), title2, font=f2, fill=(*accent,255), stroke_width=1, stroke_fill=(0,0,0,80))
    sf = font(int(w*.027), False)
    d.text((margin, int(h*.56)), subtitle, font=sf, fill=(220,235,240,235))
    # brand lockup placeholder; exact supplied logo overlaid later without modification
    if not (ASSETS/"logo.png").exists():
        d.text((margin, int(h*.88)), "MARÉE JERSEY", font=font(int(w*.045)), fill=(245,250,252,255))
        d.text((margin, int(h*.925)), "FROM BOAT TO PLATE.", font=font(int(w*.022)), fill=(*accent,255))
    else:
        logo = Image.open(ASSETS/"logo.png").convert("RGBA")
        target_w = int(w*.36)
        target_h = int(logo.height * target_w / logo.width)
        logo.thumbnail((target_w, int(h*.13)), Image.Resampling.LANCZOS)
        im_rgba = im.convert("RGBA")
        im_rgba.alpha_composite(logo, (margin, int(h*.86)))
        im = im_rgba.convert("RGB")
    im.save(out, quality=95)

def run(cmd):
    print("+", " ".join(map(str, cmd)), flush=True)
    subprocess.run(list(map(str, cmd)), check=True)

def make_voice(path: Path):
    text = ("The sea doesn't wait. Jersey's fishermen bring in the catch. "
            "Marée Jersey connects local fishermen with local restaurants. "
            "Discover the daily catch. Know your source. Bring the taste of Jersey to your kitchen. "
            "Marée Jersey. From boat to plate.")
    exe = shutil.which("espeak-ng") or shutil.which("espeak")
    if not exe:
        print("eSpeak not installed; continuing without voice-over.")
        return False
    run([exe, "-v", "en-gb", "-s", "145", "-a", "175", "-w", path, text])
    return True

def render(vertical: bool, output: Path):
    output.mkdir(parents=True, exist_ok=True)
    frames = output / ("vertical-scenes" if vertical else "landscape-scenes")
    frames.mkdir(exist_ok=True)
    files = []
    for i, (a,b,c,accent) in enumerate(SCENES, 1):
        p = frames / f"scene-{i:02d}.png"
        gradient_scene(i, a,b,c,accent,vertical,p)
        files.append(p)
    # Build an FFmpeg concat list with gentle motion using zoompan.
    concat = output / ("vertical.txt" if vertical else "landscape.txt")
    lines=[]
    for p in files:
        lines.append(f"file '{p.resolve()}'\nduration 4")
    lines.append(f"file '{files[-1].resolve()}'")
    concat.write_text("\n".join(lines), encoding="utf-8")
    size = "1080x1920" if vertical else "1920x1080"
    silent = output / ("maree-jersey-vertical-silent.mp4" if vertical else "maree-jersey-landscape-silent.mp4")
    run(["ffmpeg","-y","-f","concat","-safe","0","-i",concat,
         "-vf",f"scale={size}:force_original_aspect_ratio=decrease,pad={size}:(ow-iw)/2:(oh-ih)/2,format=yuv420p",
         "-r",str(FPS),"-t",str(DURATION),"-an","-c:v","libx264","-preset","ultrafast","-crf","20",silent])
    voice = output/"voice.wav"
    has_voice = make_voice(voice)
    music = ASSETS/"music.mp3"
    final = output/("maree-jersey-vertical.mp4" if vertical else "maree-jersey-landscape.mp4")
    if has_voice and music.exists():
        run(["ffmpeg","-y","-i",silent,"-i",voice,"-stream_loop","-1","-i",music,
             "-filter_complex","[1:a]volume=1.0[v];[2:a]volume=0.16,afade=t=out:st=20:d=4[m];[v][m]amix=inputs=2:duration=first:dropout_transition=2[a]",
             "-map","0:v","-map","[a]","-c:v","copy","-c:a","aac","-shortest",final])
    elif has_voice:
        run(["ffmpeg","-y","-i",silent,"-i",voice,"-map","0:v","-map","1:a","-c:v","copy","-c:a","aac","-shortest",final])
    elif music.exists():
        run(["ffmpeg","-y","-i",silent,"-stream_loop","-1","-i",music,"-map","0:v","-map","1:a","-c:v","copy","-c:a","aac","-shortest",final])
    else:
        shutil.copy2(silent, final)
    silent.unlink(missing_ok=True)
    print(f"Created {final}")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--format", choices=["vertical","landscape","both"], default="both")
    ap.add_argument("--output", default="dist")
    args=ap.parse_args()
    if not shutil.which("ffmpeg"):
        raise SystemExit("FFmpeg is required. Install FFmpeg and retry.")
    global OUT
    OUT=Path(args.output)
    if args.format in ("vertical","both"): render(True,OUT)
    if args.format in ("landscape","both"): render(False,OUT)

if __name__=="__main__":
    main()

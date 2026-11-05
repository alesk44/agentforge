#!/usr/bin/env python3
"""Render the Marée Jersey storyboard as a no-paid-API motion-graphics animatic.

Real Jersey footage can be added as licensed assets in a later renderer upgrade.
This version is intentionally honest: it does not pretend gradient cards are footage.
"""
from __future__ import annotations
import argparse, math, shutil, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

FPS = 25
DURATION = 45
ASSETS = Path("assets")
SCENES = [
    ("JERSEY", "ONE ISLAND. ONE SEA.", "A LOCAL CATCH BEGINS AT SEA.", (4, 220, 220), 6),
    ("FRESHLY", "CAUGHT.", "A FISHERMAN PHOTOGRAPHS HIS CATCH.", (4, 220, 220), 7),
    ("KNOW YOUR", "CATCH.", "SPECIES. ORIGIN. CATCH DETAILS. METHOD.", (255, 111, 97), 7),
    ("JUST", "LANDED.", "THE SAME FISH APPEARS FOR THE CHEF.", (4, 220, 220), 8),
    ("ORDER", "DIRECTLY.", "THE RESTAURANT CONFIRMS ITS ORDER.", (255, 111, 97), 6),
    ("SEA TO", "KITCHEN.", "A FAST LOCAL DELIVERY — CAMPAIGN SCENARIO.", (4, 220, 220), 6),
    ("MARÉE", "JERSEY.", "FROM BOAT TO PLATE.  •  ONE ISLAND. ONE SEA.", (255, 111, 97), 5),
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

def load_logo():
    for p in (ASSETS / "logo.png", ASSETS / "logo.jpg", ASSETS / "logo.jpeg"):
        if p.exists():
            return Image.open(p).convert("RGBA")
    return None

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
    logo = load_logo()
    if logo is None:
        d.text((margin, int(h*.88)), "MARÉE JERSEY", font=font(int(w*.045)), fill=(245,250,252,255))
        d.text((margin, int(h*.925)), "FROM BOAT TO PLATE.", font=font(int(w*.022)), fill=(*accent,255))
    else:
        target_w = int(w*.36)
        target_h = int(h*.13)
        logo.thumbnail((target_w, target_h), Image.Resampling.LANCZOS)
        im_rgba = im.convert("RGBA")
        im_rgba.alpha_composite(logo, (margin, int(h*.84)))
        im = im_rgba.convert("RGB")
    im.save(out, quality=95)

def run(cmd):
    print("+", " ".join(map(str, cmd)), flush=True)
    subprocess.run(list(map(str, cmd)), check=True)

def make_voice(path: Path):
    text = ("Around Jersey, every catch begins with the sea. "
            "A local fisherman lands a fish and photographs it. "
            "Marée Jersey brings the species, origin, catch details and fishing method together. "
            "In the kitchen, the same catch appears with a recipe idea. "
            "The chef orders directly. The fisherman receives the order. "
            "From the coast to the kitchen, in our campaign story, in under an hour. "
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
    durations = []
    for i, (a,b,c,accent,seconds) in enumerate(SCENES, 1):
        p = frames / f"scene-{i:02d}.png"
        gradient_scene(i, a,b,c,accent,vertical,p)
        files.append(p)
        durations.append(seconds)
    concat = output / ("vertical.txt" if vertical else "landscape.txt")
    lines=[]
    for p, seconds in zip(files, durations):
        lines.append(f"file '{p.resolve()}'\nduration {seconds}")
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
             "-filter_complex","[1:a]volume=1.0,apad=pad_dur=45[v];[2:a]volume=0.16,afade=t=out:st=41:d=4[m];[v][m]amix=inputs=2:duration=first:dropout_transition=2[a]",
             "-map","0:v","-map","[a]","-c:v","copy","-c:a","aac","-t",str(DURATION),final])
    elif has_voice:
        run(["ffmpeg","-y","-i",silent,"-i",voice,"-map","0:v","-map","1:a","-af","apad=pad_dur=45","-c:v","copy","-c:a","aac","-t",str(DURATION),final])
    elif music.exists():
        run(["ffmpeg","-y","-i",silent,"-stream_loop","-1","-i",music,"-map","0:v","-map","1:a","-c:v","copy","-c:a","aac","-t",str(DURATION),final])
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
    out=Path(args.output)
    if args.format in ("vertical","both"): render(True,out)
    if args.format in ("landscape","both"): render(False,out)

if __name__=="__main__":
    main()

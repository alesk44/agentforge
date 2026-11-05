#!/usr/bin/env python3
"""Render an original, zero-paid-API cinematic motion-graphics film for Marée Jersey."""
from __future__ import annotations
import argparse, math, shutil, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

FPS = 12
DURATION = 45
W, H = 540, 960
PALETTE = {"navy":(4,17,31),"deep":(7,37,53),"sea":(9,83,101),"teal":(27,190,184),
           "foam":(190,226,224),"white":(244,248,247),"coral":(255,111,97),"gold":(238,190,116)}
SCENES = [
    {"dur":6,"eyebrow":"JERSEY","title":"ONE ISLAND. ONE SEA.","sub":"A LOCAL CATCH BEGINS AT SEA.","vo":"Around Jersey, every catch begins with the sea."},
    {"dur":7,"eyebrow":"FRESH FROM THE WATER","title":"THE CATCH.","sub":"PHOTOGRAPHED AT SOURCE.","vo":"A fisherman lands the catch and records it in seconds."},
    {"dur":7,"eyebrow":"KNOW YOUR CATCH","title":"ITS STORY.","sub":"SPECIES  •  ORIGIN  •  METHOD  •  CATCH DETAILS","vo":"Its species, origin, catch details and fishing method are brought together."},
    {"dur":8,"eyebrow":"FOR THE KITCHEN","title":"JUST LANDED.","sub":"THE SAME CATCH. A CLEARER CONNECTION.","vo":"In the kitchen, that very catch appears with its story and a recipe idea."},
    {"dur":6,"eyebrow":"DIRECT CONNECTION","title":"ORDER DIRECT.","sub":"A DEMO ORDER IS CONFIRMED.","vo":"The chef places an order directly. The fisherman gets the confirmation."},
    {"dur":6,"eyebrow":"FROM COAST TO KITCHEN","title":"HAND TO HAND.","sub":"UNDER 1 HOUR — ILLUSTRATIVE CAMPAIGN SCENARIO","vo":"From the coast to the kitchen, in our campaign story, in under an hour."},
    {"dur":5,"eyebrow":"MARÉE JERSEY","title":"FROM BOAT TO PLATE.","sub":"ONE ISLAND. ONE SEA. ONE CONNECTION.","vo":"Marée Jersey. From boat to plate."},
]
TOTAL=sum(s["dur"] for s in SCENES)
assert TOTAL == DURATION

def font(sz, bold=True):
    paths = ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
             "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf"]
    for p in paths:
        if Path(p).exists(): return ImageFont.truetype(p, sz)
    return ImageFont.load_default()

def lerp(a,b,t): return int(a+(b-a)*max(0,min(1,t)))
def draw_text_fit(d, xy, text, maxw, size, fill, bold=True):
    f=font(size,bold)
    while d.textbbox((0,0),text,font=f)[2] > maxw and size>16:
        size-=2; f=font(size,bold)
    d.text(xy,text,font=f,fill=fill,stroke_width=1,stroke_fill=(0,0,0,80))

def background(t, wide):
    w,h=(960,540) if wide else (W,H)
    im=Image.new("RGB",(w,h)); p=im.load()
    for y in range(h):
        k=y/max(1,h-1)
        c=tuple(lerp(PALETTE["navy"][i],PALETTE["deep"][i],k*.8) for i in range(3))
        for x in range(w): p[x,y]=c
    d=ImageDraw.Draw(im,"RGBA")
    # Animated, layered Atlantic swell.
    for layer in range(7):
        base=int(h*(.59+layer*.045))
        amp=5+layer*2
        pts=[]
        for x in range(-20,w+30,8):
            yy=base+math.sin(x*.012+t*(.8+layer*.13)+layer)*amp+math.sin(x*.004-t*.4)*amp*.55
            pts.append((x,int(yy)))
        d.line(pts,fill=(*PALETTE["teal"],max(18,75-layer*7)),width=max(1,w//480))
    # Soft dawn disc and distant horizon.
    d.ellipse((int(w*.72),int(h*.12),int(w*.88),int(h*.42)),fill=(*PALETTE["gold"],25))
    return im

def island(d,w,h):
    # Original stylised Jersey headland and castle-inspired silhouette.
    y=int(h*.57)
    d.polygon([(0,y+35),(w*.13,y+5),(w*.24,y+16),(w*.36,y-10),(w*.49,y+8),(w*.61,y-20),(w*.74,y+7),(w,y-5),(w,h),(0,h)],fill=(8,44,55,255))
    x=int(w*.63); base=int(h*.56); s=w*.11
    d.rectangle((x,base-int(s*.48),x+s,base),fill=(13,32,43,255))
    d.rectangle((x+s*.13,base-s*.75,x+s*.32,base-s*.48),fill=(13,32,43,255))
    d.rectangle((x+s*.58,base-s*.82,x+s*.8,base-s*.48),fill=(13,32,43,255))
    d.polygon([(x+s*.05,base-s*.75),(x+s*.22,base-s*.95),(x+s*.39,base-s*.75)],fill=(13,32,43,255))
    d.polygon([(x+s*.52,base-s*.82),(x+s*.69,base-s),(x+s*.86,base-s*.82)],fill=(13,32,43,255))

def boat(d,x,y,scale=1):
    d.polygon([(x,y),(x+120*scale,y),(x+99*scale,y+25*scale),(x+24*scale,y+25*scale)],fill=(7,22,31,255))
    d.rectangle((x+48*scale,y-27*scale,x+85*scale,y),fill=(225,235,230,255))
    d.line((x+66*scale,y-28*scale,x+66*scale,y-65*scale),fill=(220,232,229,255),width=max(2,int(3*scale)))
    d.polygon([(x+68*scale,y-62*scale),(x+68*scale,y-30*scale),(x+105*scale,y-30*scale)],fill=(255,111,97,220))

def fish(d,x,y,scale=1):
    d.ellipse((x,y,x+90*scale,y+38*scale),fill=(194,218,213,255),outline=(244,248,247,255),width=2)
    d.polygon([(x+82*scale,y+19*scale),(x+112*scale,y),(x+108*scale,y+38*scale)],fill=(255,111,97,255))
    d.ellipse((x+15*scale,y+11*scale,x+21*scale,y+17*scale),fill=(4,17,31,255))
    d.arc((x+28*scale,y+8*scale,x+66*scale,y+31*scale),180,350,fill=(80,125,130,255),width=2)

def person(d,x,y,scale=1,chef=False):
    skin=(199,164,133,255); coat=(235,241,237,255) if chef else (24,72,83,255)
    d.ellipse((x+22*scale,y,x+52*scale,y+30*scale),fill=skin)
    d.rounded_rectangle((x+8*scale,y+28*scale,x+68*scale,y+125*scale),radius=int(12*scale),fill=coat)
    if chef:
        d.rectangle((x+15*scale,y-9*scale,x+59*scale,y+3*scale),fill=(244,248,247,255))
        d.ellipse((x+18*scale,y-23*scale,x+56*scale,y+9*scale),fill=(244,248,247,255))
    d.line((x+18*scale,y+118*scale,x+5*scale,y+165*scale),fill=(20,31,39,255),width=max(4,int(9*scale)))
    d.line((x+57*scale,y+118*scale,x+72*scale,y+165*scale),fill=(20,31,39,255),width=max(4,int(9*scale)))

def phone_card(d,x,y,w,kind="catch"):
    d.rounded_rectangle((x,y,x+w,y+w*1.48),radius=int(w*.09),fill=(4,15,27,255),outline=(116,169,171,255),width=3)
    d.rounded_rectangle((x+w*.08,y+w*.13,x+w*.92,y+w*1.34),radius=8,fill=(234,243,239,255))
    d.text((x+w*.15,y+w*.2),"MARÉE  •  DEMO",font=font(max(9,int(w*.075))),fill=(8,49,59,255))
    if kind in ("catch","chef"):
        fish(d,x+w*.22,y+w*.38,w/145)
    labels={"catch":["NEW CATCH","IDENTIFY"],"trace":["SPECIES: DEMO","ORIGIN: JERSEY","METHOD: DEMO"],"chef":["JUST LANDED","RECIPE IDEA"],"order":["ORDER CONFIRMED","DEMO REFERENCE"]}
    yy=y+w*.83
    for label in labels.get(kind,labels["catch"]):
        d.text((x+w*.14,yy),label,font=font(max(8,int(w*.062))),fill=(9,62,70,255)); yy+=w*.15
    d.rounded_rectangle((x+w*.13,y+w*1.16,x+w*.87,y+w*1.27),radius=5,fill=(*PALETTE["coral"],255))
    d.text((x+w*.26,y+w*1.17),"CONTINUE",font=font(max(8,int(w*.055))),fill=(255,255,255,255))

def render_frame(scene_i, local_t, scene_t, wide):
    im=background(scene_t,wide); d=ImageDraw.Draw(im,"RGBA"); w,h=im.size
    # Cinematic camera drift and a consistent scene motif.
    drift=math.sin(scene_t*.7)*w*.012
    if scene_i==0:
        island(d,w,h); boat(d,int(w*.18+drift),int(h*.59+math.sin(scene_t)*4),w/960)
    elif scene_i==1:
        d.polygon([(0,h*.72),(w,h*.66),(w,h),(0,h)],fill=(9,40,49,255))
        boat(d,int(w*.12+drift),int(h*.72),w/960)
        person(d,int(w*.25),int(h*.43),w/960)
        fish(d,int(w*.56),int(h*.68+math.sin(scene_t*2)*5),w/960)
        phone_card(d,int(w*.69),int(h*.25),int(w*.2),"catch")
    elif scene_i==2:
        fish(d,int(w*.12+drift),int(h*.55),w/960*1.3)
        phone_card(d,int(w*.58),int(h*.23),int(w*.28),"trace")
    elif scene_i==3:
        person(d,int(w*.16),int(h*.43),w/960,chef=True)
        phone_card(d,int(w*.55),int(h*.2),int(w*.28),"chef")
        d.rounded_rectangle((w*.12,h*.78,w*.48,h*.88),radius=10,fill=(255,255,255,22),outline=(*PALETTE["teal"],150),width=2)
        d.text((w*.16,h*.81),"SAME CATCH  ✓",font=font(int(w*.035)),fill=PALETTE["white"])
    elif scene_i==4:
        phone_card(d,int(w*.14),int(h*.2),int(w*.27),"order")
        person(d,int(w*.64),int(h*.43),w/960)
        # notification pulse
        r=18+int(7*(.5+.5*math.sin(scene_t*5)))
        d.ellipse((w*.73-r,h*.28-r,w*.73+r,h*.28+r),fill=(*PALETTE["coral"],180))
        d.text((w*.71,h*.255),"!",font=font(int(w*.045)),fill=PALETTE["white"])
    elif scene_i==5:
        # simple handover: crate, van and kitchen recipient
        d.rounded_rectangle((w*.1,h*.58,w*.37,h*.82),radius=8,fill=(143,101,62,255),outline=(226,193,140,255),width=3)
        fish(d,int(w*.15),int(h*.62),w/960*.65)
        d.rounded_rectangle((w*.43,h*.52,w*.75,h*.73),radius=18,fill=(223,235,229,255),outline=(8,54,65,255),width=4)
        d.rectangle((w*.49,h*.42,w*.69,h*.54),fill=(223,235,229,255))
        d.ellipse((w*.48,h*.68,w*.57,h*.81),fill=(7,20,29,255)); d.ellipse((w*.65,h*.68,w*.74,h*.81),fill=(7,20,29,255))
        person(d,int(w*.79),int(h*.45),w/960,chef=True)
        d.line((w*.36,h*.7,w*.45,h*.7),fill=(*PALETTE["coral"],255),width=5)
        d.polygon([(w*.45,h*.7),(w*.42,h*.67),(w*.42,h*.73)],fill=(*PALETTE["coral"],255))
    else:
        island(d,w,h)
        # end card logo is composited separately, never redrawn
    # Scene heading, subtitle and animated progress marker.
    margin=int(w*.075)
    d.rounded_rectangle((margin,int(h*.085),margin+int(w*.13),int(h*.096)),radius=4,fill=(*PALETTE["coral"],255))
    small=font(max(12,int(w*.025)))
    d.text((margin,int(h*.13)),SCENES[scene_i]["eyebrow"],font=small,fill=(*PALETTE["teal"],255))
    title=SCENES[scene_i]["title"]
    draw_text_fit(d,(margin,int(h*.2)),title,int(w*.85),int(w*.075),PALETTE["white"])
    sub=SCENES[scene_i]["sub"]
    draw_text_fit(d,(margin,int(h*.9)),sub,int(w*.85),int(w*.022),PALETTE["foam"],False)
    # restrained film grain
    for i in range(28):
        x=(i*73+int(scene_t*31))%w; y=(i*137+int(scene_t*17))%h
        d.point((x,y),fill=(210,235,232,18))
    return im

def make_voice(path):
    script=" ".join(s["vo"] for s in SCENES)
    exe=shutil.which("espeak-ng") or shutil.which("espeak")
    if not exe: return False
    subprocess.run([exe,"-v","en-gb","-s","145","-a","165","-w",str(path),script],check=True)
    return True

def make_srt(path):
    cues=[]; t=0
    for s in SCENES:
        start=t; end=t+s["dur"]; t=end
        def stamp(v):
            ms=int(round(v*1000)); hh,ms=divmod(ms,3600000); mm,ms=divmod(ms,60000); ss,ms=divmod(ms,1000)
            return f"{hh:02}:{mm:02}:{ss:02},{ms:03}"
        cues.append(f"{len(cues)+1}\n{stamp(start)} --> {stamp(end)}\n{s['vo']}\n")
    path.write_text("\n".join(cues),encoding="utf-8")

def render(wide,out):
    out.mkdir(parents=True,exist_ok=True)
    size=(960,540) if wide else (540,960)
    frames=out/("frames-landscape" if wide else "frames-vertical"); frames.mkdir(exist_ok=True)
    scene_start=0; n=0
    for si,s in enumerate(SCENES):
        count=s["dur"]*FPS
        for j in range(count):
            local=j/FPS
            frame=render_frame(si,local,scene_start+local,wide)
            # Exact official logo, only uniformly scaled, on the final scene.
            if si==6:
                logo_path=next((p for p in [Path("assets/logo.png"),Path("assets/logo.jpg"),Path("assets/logo.jpeg")] if p.exists()),None)
                if logo_path:
                    logo=Image.open(logo_path).convert("RGBA")
                    logo.thumbnail((int(size[0]*.29),int(size[1]*.25)),Image.Resampling.LANCZOS)
                    frame=frame.convert("RGBA")
                    frame.alpha_composite(logo,(int(size[0]*.075),int(size[1]*.49)))
                    frame=frame.convert("RGB")
            frame.save(frames/f"{n:05d}.jpg",quality=88)
            n+=1
        scene_start+=s["dur"]
    name="maree-jersey-landscape" if wide else "maree-jersey-vertical"
    silent=out/(name+"-silent.mp4"); final=out/(name+".mp4")
    target="1920:1080" if wide else "1080:1920"
    subprocess.run(["ffmpeg","-y","-framerate",str(FPS),"-i",str(frames/"%05d.jpg"),"-vf",f"scale={target}:flags=lanczos,format=yuv420p","-c:v","libx264","-preset","ultrafast","-crf","21","-t",str(DURATION),str(silent)],check=True)
    voice=out/"voice-en-gb.wav"; has_voice=make_voice(voice)
    music=Path("assets/music.mp3")
    if has_voice and music.exists():
        subprocess.run(["ffmpeg","-y","-i",str(silent),"-i",str(voice),"-stream_loop","-1","-i",str(music),"-filter_complex","[1:a]volume=1.0,apad=pad_dur=45[v];[2:a]volume=0.14,afade=t=out:st=41:d=4[m];[v][m]amix=inputs=2:duration=first[a]","-map","0:v","-map","[a]","-c:v","copy","-c:a","aac","-t","45",str(final)],check=True)
    elif has_voice:
        subprocess.run(["ffmpeg","-y","-i",str(silent),"-i",str(voice),"-map","0:v","-map","1:a","-af","apad=pad_dur=45","-c:v","copy","-c:a","aac","-t","45",str(final)],check=True)
    else: shutil.copy2(silent,final)
    silent.unlink(missing_ok=True)
    print("Created",final)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--format",choices=["vertical","landscape","both"],default="both")
    p.add_argument("--output",default="dist")
    a=p.parse_args(); 
    if not shutil.which("ffmpeg"): raise SystemExit("FFmpeg is required.")
    out=Path(a.output)
    if a.format in ("vertical","both"): render(False,out)
    if a.format in ("landscape","both"): render(True,out)
    make_srt(out/"maree-jersey-en-gb.srt")

if __name__=="__main__": main()

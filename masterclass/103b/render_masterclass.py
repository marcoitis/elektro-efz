#!/usr/bin/env python3
"""Produce a first REAL narrated standalone masterclass MP4 (not a slideshow).
One Piper-TTS WAV per storyboard beat gives exact audio<->scene boundaries.
Sub-scene reveal timing is choreographed; not claimed as forced word alignment.
Outputs MP4 1280x720, original WAV, timing manifest and the new script.
"""
from __future__ import annotations
import bisect, hashlib, json, math, os, subprocess, sys, wave
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[2]
SRC=ROOT/"masterclass/103b/storyboard.json"
OUT=ROOT/".masterclass-output"
MODEL=ROOT/".voice-cache/de_DE-thorsten-high.onnx"
MODEL_CONFIG=ROOT/".voice-cache/de_DE-thorsten-high.onnx.json"
MODEL_SHA="9df1c43c61149ef9b39e618e2b861fbe41e1fcea9390b2dac62e8761573ea4f1"
WIDTH,HEIGHT,FPS=1280,720,16
C={"bg":(8,24,38),"panel":(15,42,60),"panel2":(23,64,78),
   "line":(117,166,184),"text":(243,251,251),"muted":(158,190,204),
   "teal":(83,229,194),"blue":(99,180,238),"amber":(255,199,107),
   "soft":(57,101,118),"grid":(24,49,62)}
FONT_DIR=Path("/usr/share/fonts/truetype/dejavu")
FB=FONT_DIR/"DejaVuSans-Bold.ttf"
FR=FONT_DIR/"DejaVuSans.ttf"
from functools import lru_cache
@lru_cache(maxsize=96)
def font(size=24,bold=False):return ImageFont.truetype(str(FB if bold else FR),size)
def txt(d,x,y,s,size=24,color="text",bold=False,anchor=None):
    fill=C.get(color,color)
    d.text((x,y),str(s),font=font(size,bold),fill=fill,anchor=anchor)
def box(d,rect,fill="panel",outline=None,r=20,width=2):
    d.rounded_rectangle(rect,radius=r,fill=C.get(fill,fill),outline=C.get(outline,outline) if outline else None,width=width)
def ln(d,points,fill="line",width=5,joint="curve"):
    d.line(points,fill=C.get(fill,fill),width=width,joint=joint)
def circ(d,x,y,r,fill="teal",outline=None,width=2):
    d.ellipse([x-r,y-r,x+r,y+r],fill=C.get(fill,fill) if fill else None,
              outline=C.get(outline,outline) if outline else None,width=width)
def arr(d,x1,y1,x2,y2,fill="teal",width=6,tip=16):
    ln(d,[(x1,y1),(x2,y2)],fill,width)
    ang=math.atan2(y2-y1,x2-x1)
    pts=[(x2,y2),(x2-tip*math.cos(ang-.48),y2-tip*math.sin(ang-.48)),
         (x2-tip*math.cos(ang+.48),y2-tip*math.sin(ang+.48))]
    d.polygon(pts,fill=C.get(fill,fill))
def lerp(a,b,t):return a+(b-a)*min(1,max(0,t))
def fade(p,start=0.1,end=0.4):return max(0,min(1,(p-start)/(end-start)))
def reveal_x(d,rectangle,p,fill="teal",r=10):
    a,b,c,e=rectangle
    box(d,(a,b,lerp(a,c,p),e),fill,r=r)
def pill(d,x,y,s,color="teal",size=24,pad=19):
    f=font(size,True);bound=d.textbbox((0,0),s,font=f);w=bound[2]-bound[0]+2*pad;h=size+26
    box(d,(x,y,x+w,y+h),"panel2",color,12,2)
    txt(d,x+pad,y+10,s,size,color,True)
    return w
def label(d,x,y,s):txt(d,x,y,s,19,"muted")
def tint(d,x,y,r=48,color="teal",alpha=.22):
    base=C[color]
    for z in range(3,0,-1):
        rad=r+z*13
        line=tuple(int(C["bg"][j]*(1-alpha/z)+base[j]*(alpha/z)) for j in range(3))
        d.ellipse((x-rad,y-rad,x+rad,y+rad),outline=line,width=7)

# Path follows the conventional DC current from + to - OUTSIDE the source.
DC_SEGMENTS=[((230,400),(230,288)),((230,288),(756,288)),
             ((756,288),(928,288)),((928,288),(1020,288)),
             ((1020,288),(1020,515)),((1020,515),(230,515)),((230,515),(230,451))]
LENGTHS=[math.dist(a,b) for a,b in DC_SEGMENTS]
TOTAL=sum(LENGTHS)
def track_point(z):
    distance=(z%1)*TOTAL
    for (p,q),length in zip(DC_SEGMENTS,LENGTHS):
        if distance<=length:return (lerp(p[0],q[0],distance/length),lerp(p[1],q[1],distance/length))
        distance-=length
    return DC_SEGMENTS[-1][-1]
def flow(d,time,intensity=1,enabled=True):
    if not enabled:return
    count=max(3,round(8*intensity))
    speed=.085*intensity
    for k in range(count):
        x,y=track_point((k/count+time*speed)%1)
        circ(d,x,y,7 if k%3 else 9,"teal")
        circ(d,x,y,14,None,"teal",1)
def circuit(d,t,p,voltage="12 V",resistance="120 Ω",current=None,closed=True,
            source_focus=False,resistor_focus=False,show_dots=True):
    wire="line"
    # Visible interruption for the optional open-circuit scene.
    x1,x2=485,557
    ln(d,[(230,401),(230,288),(x1 if not closed else 756,288)],wire,7)
    if closed:ln(d,[(928,288),(1020,288),(1020,515),(230,515),(230,451)],wire,7)
    else:
        ln(d,[(x2,288),(756,288)],wire,7)
        ln(d,[(x1,288),(x2,247)],"amber",6)
        ln(d,[(928,288),(1020,288),(1020,515),(230,515),(230,451)],wire,7)
    # Upper resistive element between source wiring and return.
    box(d,(756,258,928,319),"panel2","amber" if resistor_focus else "teal",9,4 if resistor_focus else 3)
    txt(d,842,277,"R",38,"text",True,"mt")
    # Battery plates and pole marks, no false wire short circuit.
    ln(d,[(192,401),(267,401)],"text",7)
    ln(d,[(207,451),(252,451)],"text",6)
    txt(d,166,387,"+",34,"teal",True)
    txt(d,166,445,"−",34,"blue",True)
    if source_focus:tint(d,230,426,65,"teal",.2)
    if resistor_focus:tint(d,843,288,43,"amber",.17)
    if show_dots and closed:flow(d,t)
    # A visual unit, never a competing checklist.
    box(d,(104,560,421,644),"panel2","teal" if source_focus else "soft",18)
    label(d,129,572,"SPANNUNGSQUELLE")
    txt(d,129,598,"U = "+voltage,34,"text",True)
    box(d,(754,560,1121,644),"panel2","amber" if resistor_focus else "soft",18)
    label(d,783,572,"WIDERSTAND")
    txt(d,783,598,"R = "+resistance,34,"text",True)
    if current:
        pill(d,470,585,"I = "+current,"teal",26)
    if closed:arr(d,475,245,618,245,"teal",4,14)

def large_formula(d,a,b,c,y=320,frac=False):
    if not frac:
        txt(d,640,y,a,82,"text",True,"mm")
        return
    txt(d,455,y+28,a,82,"text",True,"mm")
    txt(d,635,y+28,"=",70,"muted",True,"mm")
    txt(d,891,y-20,b,62,"text",True,"mm")
    ln(d,[(744,y+30),(1030,y+30)],"teal",6)
    txt(d,891,y+72,c,62,"text",True,"mm")

def stage(d,sc,p,t):
    kind=sc["kind"]
    if kind=="title":
        txt(d,640,220,"12 V",115,"teal",True,"mm")
        txt(d,640,328,"÷",82,"muted",False,"mm")
        txt(d,640,438,"120 Ω",115,"amber",True,"mm")
        if p>.48:
            txt(d,640,550,"= 0,1 A = 100 mA",48,"text",True,"mm")
    elif kind=="quelle":
        circuit(d,t,p,closed=True,show_dots=False,source_focus=True)
        if p>.55:pill(d,450,148,"12 VOLT · GLEICHSPANNUNG","teal",26)
    elif kind=="offen":
        circuit(d,t,p,closed=False,show_dots=False)
        pill(d,448,159,"STROMKREIS UNTERBROCHEN","amber",25)
        txt(d,640,385,"I = 0 A",55,"text",True,"mm")
    elif kind=="close":
        closed=p>.26
        circuit(d,t,p,closed=closed,show_dots=closed)
        if p>.32:pill(d,442,165,"GESCHLOSSENER STROMKREIS","teal",25)
    elif kind=="flow":
        circuit(d,t,p,show_dots=True)
        txt(d,640,176,"Technische Stromrichtung",29,"teal",True,"mm")
        if p>.55:txt(d,640,217,"Aussen: Plus  →  Widerstand  →  Minus",20,"muted",False,"mm")
    elif kind=="resistor":
        circuit(d,t,p,resistor_focus=True,show_dots=True)
        if p>.32:pill(d,473,162,"120 Ω","amber",48,24)
    elif kind=="formula":
        large_formula(d,"U = R × I","","",322)
        if p>.36:
            label(d,244,452,"U: Spannung [V]")
        if p>.53:
            label(d,530,452,"R: Widerstand [Ω]")
        if p>.72:
            label(d,884,452,"I: Strom [A]")
        txt(d,640,562,"Gültig für einen ohmschen Widerstand",22,"muted",False,"mm")
    elif kind=="isolate":
        if p<.3:large_formula(d,"U = R × I","","")
        elif p<.6:
            large_formula(d,"I = U / R","","")
        else:large_formula(d,"I","U","R",320,True)
        txt(d,640,552,"Gesuchte Grösse: Strom I",25,"teal",True,"mm")
    elif kind=="givens":
        circuit(d,t,p,show_dots=False,source_focus=p<.5,resistor_focus=p>=.5)
        if p>.6:pill(d,470,180,"U = 12 V    R = 120 Ω","teal",26)
    elif kind=="substitute":
        if p<.35:large_formula(d,"I","U","R",280,True)
        else:large_formula(d,"I","12 V","120 Ω",280,True)
        if p>.55:
            txt(d,640,516,"Volt / Ohm = Ampere",27,"teal",True,"mm")
    elif kind=="result":
        txt(d,640,245,"12 ÷ 120",55,"muted",True,"mm")
        txt(d,640,390,"0,1 A",115,"teal",True,"mm")
        if p>.55:txt(d,640,519,"Strom durch den Modellwiderstand",24,"muted",False,"mm")
    elif kind=="convert":
        txt(d,640,216,"1 A  =  1000 mA",50,"muted",True,"mm")
        txt(d,640,381,"0,1 A  =  100 mA",69,"teal",True,"mm")
        if p>.6:txt(d,640,520,"Nicht 10 mA!",36,"amber",True,"mm")
    elif kind=="compare":
        vals=[("60 Ω","200 mA"),("120 Ω","100 mA"),("240 Ω","50 mA")]
        at=min(2,int(p*3))
        for k,(r,i) in enumerate(vals):
            x=75+k*398
            box(d,(x,235,x+364,508),"panel2","teal" if k==at else "soft",22,4 if k==at else 2)
            txt(d,x+182,282,r,47,"amber" if k==at else "text",True,"mt")
            max_bar=180
            bar_h={"200 mA":max_bar,"100 mA":max_bar//2,"50 mA":max_bar//4}[i]
            box(d,(x+90,459-bar_h,x+274,459),"teal" if k==at else "soft",None,12)
            txt(d,x+182,472,i,27,"text",True,"mt")
        txt(d,640,596,"Bei U = 12 V:  R ↑  →  I ↓",28,"muted",True,"mm")
    elif kind=="graph":
        left,top,bottom,right=178,177,522,1118
        arr(d,left,bottom,left,top,"muted",4,17)
        arr(d,left,bottom,right,bottom,"muted",4,17)
        txt(d,left-68,189,"I",34,"text",True)
        txt(d,right-22,bottom+28,"U",34,"text",True)
        xend=left+804*min(1,p*1.45)
        yend=bottom-262*min(1,p*1.45)
        ln(d,[(left,bottom),(xend,yend)],"teal",7)
        pts=[(.25,"3 V · 25 mA"),(.5,"6 V · 50 mA"),(1,"12 V · 100 mA")]
        for percent,lab in pts:
            if p>.16+percent*.60:
                xx=left+804*percent; yy=bottom-262*percent
                circ(d,xx,yy,9,"amber");txt(d,xx-15,yy-38,lab,20,"text",True,"mm")
        txt(d,670,608,"Kennlinie eines idealen 120-Ω-Widerstands",23,"muted",False,"mm")
    elif kind=="dcac":
        # DC uses a travelling pulse. AC uses particles oscillating locally,
        # not two-way through an entire wire in a single instant.
        for x,col,heading in [(70,"teal","GLEICHSTROM · DC"),(664,"blue","WECHSELSTROM · AC")]:
            box(d,(x,185,x+547,558),"panel2",col,24,2)
            txt(d,x+273,223,heading,28,col,True,"mt")
            y=360
            ln(d,[(x+70,y),(x+480,y)],"line",8)
        for j in range(6):
            cx=143+((t*.18+j/6)%1)*408
            circ(d,cx,360,9,"teal")
        arr(d,257,301,472,301,"teal",5)
        osc=math.sin(2*math.pi*t*.5)
        # Particles move locally back and forth around fixed positions.
        for j in range(6):
            x=734+j*73+int(19*osc)
            circ(d,x,360,8,"blue")
        if math.cos(2*math.pi*t*.5)>=0:
            arr(d,822,301,1025,301,"blue",5)
        else:arr(d,1025,301,822,301,"blue",5)
        # DC waveform constant above zero; AC sinusoidal about the zero line.
        ln(d,[(157,493),(548,493)],"soft",2)
        ln(d,[(157,460),(548,460)],"teal",5)
        ln(d,[(752,477),(1134,477)],"soft",2)
        curve=[]
        for k in range(96):
            xx=752+k*4; yy=477-27*math.sin(k/95*4*math.pi)
            curve.append((xx,yy))
        ln(d,curve,"blue",4)
        txt(d,640,610,"Richtungsschema in Zeitlupe · keine Elektronenbahnen",18,"muted",False,"mm")
    elif kind=="summary":
        large_formula(d,"I","12 V","120 Ω",270,True)
        if p>.37:txt(d,640,472,"0,1 A  =  100 mA",62,"teal",True,"mm")
        if p>.72:txt(d,640,570,"Formel · Einheiten · Plausibilität",25,"muted",False,"mm")
    else:
        txt(d,640,340,sc["title"],40,"text",True,"mm")

def base_frame():
    im=Image.new("RGB",(WIDTH,HEIGHT),C["bg"]);d=ImageDraw.Draw(im)
    for y in range(HEIGHT):
        tint=(math.sin(y/HEIGHT*math.pi)*.025)
        if y%3==0:ln(d,[(0,y),(WIDTH,y)],tuple(min(255,int(C["bg"][i]*(1-tint))) for i in range(3)),3)
    for x in range(40,WIDTH,60):ln(d,[(x,165),(x,655)],"grid",1)
    for y in range(180,656,60):ln(d,[(50,y),(1230,y)],"grid",1)
    # Theater surface and discreet brand label
    box(d,(48,168,1232,656),"panel",None,28)
    txt(d,66,34,"ELEKTRO  /  EFZ",26,"teal",True)
    txt(d,66,68,"MASTERCLASS · OHMSCHES GESETZ",17,"muted",True)
    ln(d,[(66,91),(1214,91)],"soft",2)
    return im
BACKGROUND=base_frame()

def render(sc,index,total,p,t,elapsed,duration):
    im=BACKGROUND.copy();d=ImageDraw.Draw(im)
    txt(d,70,116,sc["title"],42,"text",True)
    txt(d,1205,126,f"{index+1:02d} / {total:02d}",20,"muted",False,"ra")
    stage(d,sc,p,t)
    # Visual cue changes only with narration scene (not arbitrary automatic cycling).
    progress=elapsed/max(duration,0.01)
    ln(d,[(70,677),(1210,677)],"soft",4)
    ln(d,[(70,677),(70+1140*progress,677)],"teal",5)
    txt(d,72,691,"THORSTEN HIGH",18,"muted",True)
    txt(d,1205,691,f"{int(elapsed//60):02d}:{int(elapsed%60):02d}",18,"muted",False,"ra")
    return im

def run(cmd,**kwargs):return subprocess.run(cmd,check=True,**kwargs)
def synthesize(data):
    assert hashlib.sha256(MODEL.read_bytes()).hexdigest()==MODEL_SHA,"Voice model hash mismatch"
    assert MODEL_CONFIG.stat().st_size>1000
    OUT.mkdir(parents=True,exist_ok=True)
    sample_rate=None;sample_width=None;channels=None
    segments=[];all_frames=[]
    for i,sc in enumerate(data["scenes"]):
        wav_path=OUT/f"segment_{i:02}.wav"
        run(["piper","--model",str(MODEL),"--config",str(MODEL_CONFIG),
             "--output_file",str(wav_path),"--length_scale","1.04","--sentence_silence","0.35"],
            input=(sc["narration"]+"\n").encode("utf-8"),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        with wave.open(str(wav_path),"rb") as wav:
            metadata=(wav.getframerate(),wav.getsampwidth(),wav.getnchannels())
            if sample_rate is None:sample_rate,sample_width,channels=metadata
            assert metadata==(sample_rate,sample_width,channels),metadata
            frames=wav.readframes(wav.getnframes())
        assert len(frames)>8000,"Empty audio "+sc["id"]
        # Small synchronized scene pause; included in this scene's timed range.
        frames+=bytes(round(sample_rate*.20)*sample_width*channels)
        segments.append(len(frames)/(sample_rate*sample_width*channels))
        all_frames.append(frames)
        print("VOICE",i,sc["id"],f"{segments[-1]:.2f}s",flush=True)
    combined=OUT/"masterclass-103b-thorsten-high.wav"
    with wave.open(str(combined),"wb") as w:
        w.setnchannels(channels);w.setsampwidth(sample_width);w.setframerate(sample_rate)
        for chunk in all_frames:w.writeframes(chunk)
    return combined,segments

def main():
    data=json.loads(SRC.read_text(encoding="utf-8"))
    assert len(data["scenes"])==16
    soundtrack,durations=synthesize(data)
    starts=[0.0]
    for sec in durations:starts.append(starts[-1]+sec)
    duration=starts[-1]
    assert 120<=duration<=320,"Unusually long/short production: "+str(duration)
    frames=int(math.ceil(duration*FPS))
    output=OUT/"Elektro_EFZ_Masterclass_1.03-B_12V_120Ohm.mp4"
    command=["ffmpeg","-nostdin","-hide_banner","-loglevel","warning","-y",
             "-f","rawvideo","-vcodec","rawvideo","-pix_fmt","rgb24","-s",f"{WIDTH}x{HEIGHT}",
             "-r",str(FPS),"-i","pipe:0","-i",str(soundtrack),
             "-c:v","libx264","-preset","veryfast","-crf","21","-pix_fmt","yuv420p",
             "-c:a","aac","-b:a","160k","-ar","22050",
             "-movflags","+faststart","-shortest",str(output)]
    with (OUT/"ffmpeg-encode.log").open("wb") as err:
        ff=subprocess.Popen(command,stdin=subprocess.PIPE,stderr=err)
        try:
            for frame in range(frames):
                sec=(frame+.5)/FPS
                idx=max(0,min(len(durations)-1,bisect.bisect_right(starts,sec)-1))
                p=min(1,max(0,(sec-starts[idx])/max(.01,durations[idx])))
                img=render(data["scenes"][idx],idx,len(durations),p,sec,sec,duration)
                ff.stdin.write(img.tobytes())
                if frame%320==0:print("VIDEO",frame,"/",frames,flush=True)
        except Exception:
            ff.kill();raise
        finally:
            try:ff.stdin.close()
            except OSError:pass
        code=ff.wait()
    if code:raise RuntimeError("ffmpeg failed "+str(code)+": "+(OUT/"ffmpeg-encode.log").read_text()[-1500:])
    probe=json.loads(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration,size:stream=codec_name,width,height",
                                              "-of","json",str(output)]).decode())
    streams=probe["streams"]
    assert any(x.get("codec_name")=="h264" and x.get("width")==WIDTH and x.get("height")==HEIGHT for x in streams)
    assert any(x.get("codec_name")=="aac" for x in streams)
    assert abs(float(probe["format"]["duration"])-duration)<1.0
    assert output.stat().st_size>1_000_000
    manifest={"source":"masterclass/103b/storyboard.json","speaker":"Piper de_DE-thorsten-high",
              "sha256_voice_model":MODEL_SHA,"runtime_seconds":round(duration,3),
              "video_fps":FPS,"resolution":[WIDTH,HEIGHT],
              "speaker_timing":"each TTS clip synthesized separately; scene boundaries precise to audio; intra-scene animations scripted, not word-for-word aligned",
              "quality_status":"technical checks passed; human/acoustic and comprehensive pedagogical signoff pending",
              "source_tts_script":"tts_scripts/1.03-B.txt", "parts":[
               {"id":sc["id"],"title":sc["title"],"start_seconds":round(starts[i],3),"end_seconds":round(starts[i+1],3),
                "narration":sc["narration"]} for i,sc in enumerate(data["scenes"])]}
    (OUT/"Unterrichtsablauf_1.03-B.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("SUCCESS",output,round(duration,1),"sec",output.stat().st_size,"bytes",flush=True)
if __name__=="__main__":main()

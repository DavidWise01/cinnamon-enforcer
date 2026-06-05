#!/usr/bin/env python3
"""
Silicon badge — the abstract essence of the Cinnamon Enforcer.

The thesis as a sigil: a beige cluster of synonyms wired in a 'like' loop
(A is like B is like C is like A — the ouroboros), with the flattened average
marked as a beige X at the centre, and ONE word picked out of the loop — sharp,
cinnamon-red, ringed: pick one. Deterministic, pure-stdlib PNG. Writes agents/<slug>.png.
"""
import json, re, zlib, struct, math
from pathlib import Path

ROOT = Path(__file__).parent
R = json.loads((ROOT/"roster.json").read_text(encoding="utf-8"))
AG = ROOT/"agents"; AG.mkdir(exist_ok=True)
CLS = {c["id"]: c for c in R["classes"]}
SIZE = 360

def slug(s): return re.sub(r"[^a-z0-9]+","-",s.lower()).strip("-") or "agent"
def clamp(v): return 0 if v<0 else 255 if v>255 else int(round(v))
def mix(a,b,t): return tuple(clamp(a[i]+(b[i]-a[i])*t) for i in range(3))

def png(path,w,h,px):
    raw=bytearray()
    for y in range(h):
        raw.append(0)
        for x in range(w): raw+=bytes(px[y*w+x])
    comp=zlib.compress(bytes(raw),9)
    def ch(t,d): return struct.pack(">I",len(d))+t+d+struct.pack(">I",zlib.crc32(t+d)&0xffffffff)
    Path(path).write_bytes(b"\x89PNG\r\n\x1a\n"+ch(b"IHDR",struct.pack(">IIBBBBB",w,h,8,2,0,0,0))+ch(b"IDAT",comp)+ch(b"IEND",b""))

def _plot(px,x,y,c,a=1.0):
    xi,yi=int(round(x)),int(round(y))
    if 0<=xi<SIZE and 0<=yi<SIZE: i=yi*SIZE+xi; px[i]=mix(px[i],c,a)
def _disk(px,x,y,r,c,a=1.0):
    for yy in range(int(y-r),int(y+r)+1):
        for xx in range(int(x-r),int(x+r)+1):
            if (xx-x)**2+(yy-y)**2<=r*r: _plot(px,xx,yy,c,a)
def _line(px,x0,y0,x1,y1,c,a,th=1):
    n=int(max(abs(x1-x0),abs(y1-y0)))+1
    for k in range(n+1):
        t=k/n; x=x0+(x1-x0)*t; y=y0+(y1-y0)*t
        _disk(px,x,y,th/2.0,c,a) if th>1 else _plot(px,x,y,c,a)
def _ringpt(px,cx,cy,r,c,a,th=1):
    steps=int(2*math.pi*r)+8
    for k in range(steps):
        t=k/steps*2*math.pi; _disk(px,cx+r*math.cos(t),cy+r*math.sin(t),th/2.0,c,a)
def _bg(base, glow_col, glow=0.10):
    cx=cy=SIZE/2.0; px=[base]*(SIZE*SIZE)
    for y in range(SIZE):
        for x in range(SIZE):
            d=math.hypot(x-cx,y-cy)/(SIZE*0.5); g=max(0.0,1.0-d*1.12)
            c=mix(base, glow_col, glow*g**2)
            c=mix(c, base, min(0.55,(d-0.72)*1.7) if d>0.72 else 0.0)
            px[y*SIZE+x]=c
    return px

def enforcer_sigil(m):
    V=(19,10,7); BEIGE=(152,136,118); BEIGE_D=(98,88,76); CIN=(224,97,63); GOLD=(232,196,90); WT=(245,235,225); BR=(150,96,52)
    px=_bg(V,CIN,0.10); cx=cy=SIZE/2.0
    pts=[]
    for k in range(7):
        a=k*(2*math.pi/7)-math.pi/2; r=SIZE*(0.19+0.05*((k*3)%5)/4)
        pts.append((cx+r*math.cos(a), cy+r*math.sin(a)))
    for k in range(7):                                              # the 'like' loop (ouroboros)
        x0,y0=pts[k]; x1,y1=pts[(k+1)%7]; _line(px,x0,y0,x1,y1, mix(BEIGE,V,0.5), 0.22, th=1)
    for (x,y) in pts: _disk(px,x,y,5,BEIGE,0.7); _disk(px,x,y,2,BEIGE_D,0.85)
    _line(px, cx-10,cy-10, cx+10,cy+10, BEIGE_D, 0.8, th=2)         # the centroid = a beige X (the flattened average)
    _line(px, cx-10,cy+10, cx+10,cy-10, BEIGE_D, 0.8, th=2)
    qx,qy = cx+SIZE*0.29, cy-SIZE*0.27                              # the picked one: a sharp cinnamon vertex
    _ringpt(px, qx,qy, 16, CIN, 0.6, th=2)
    _disk(px, qx,qy, 18, mix(CIN,V,0.6),0.20); _disk(px, qx,qy, 8, CIN, 0.95); _disk(px, qx,qy, 3.5, WT, 0.95)
    _line(px, cx+SIZE*0.10,cy-SIZE*0.09, qx-13,qy+11, GOLD, 0.75, th=2)   # 'pick one' arrow
    _line(px, qx-13,qy+11, qx-7,qy+11, GOLD,0.75,th=2); _line(px, qx-13,qy+11, qx-13,qy+5, GOLD,0.75,th=2)
    _line(px, cx-SIZE*0.17, cy+SIZE*0.30, cx-SIZE*0.02, cy+SIZE*0.345, BR, 0.7, th=3)   # cinnamon-stick accent
    _line(px, cx-SIZE*0.17, cy+SIZE*0.335, cx-SIZE*0.02, cy+SIZE*0.38, mix(BR,V,0.25), 0.6, th=3)
    return px

SIGILS = {"enforcer": enforcer_sigil}
for m in R["members"]:
    fn = SIGILS.get(m.get("domain"), enforcer_sigil)
    png(AG/f"{slug(m['name'])}.png", SIZE, SIZE, fn(m))
    print(f"silicon badge -> agents/{slug(m['name'])}.png  ({m['name']} / {m.get('domain','')})")

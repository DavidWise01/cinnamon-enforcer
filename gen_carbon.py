#!/usr/bin/env python3
"""
Carbon badge — the embodied 8-bit "photo": the Cinnamon Enforcer himself — a red
bear with glowing eyes, raised, brandishing two cinnamon-stick batons. Pure stdlib
Deflate TIFF. Writes agents/<slug>.tiff.
"""
import json, re, struct, zlib, math
from pathlib import Path

ROOT = Path(__file__).parent
R = json.loads((ROOT/"roster.json").read_text(encoding="utf-8"))
AG = ROOT/"agents"; AG.mkdir(exist_ok=True)
CLS = {c["id"]: c for c in R["classes"]}
LW, LH, S = 64, 80, 5
W, H = LW*S, LH*S
VOID=(19,10,7)
def slug(s): return re.sub(r"[^a-z0-9]+","-",s.lower()).strip("-") or "agent"
def clamp(v): return 0 if v<0 else 255 if v>255 else int(round(v))
def mix(a,b,t): return tuple(clamp(a[i]+(b[i]-a[i])*t) for i in range(3))
def shade(c,t): return mix(c,(0,0,0),t)
def tint(c,t): return mix(c,(255,255,255),t)

def tiff(path,w,h,pixels):
    raw=bytearray()
    for (r,g,b) in pixels: raw+=bytes((r,g,b))
    strip=zlib.compress(bytes(raw),9); BPS=8+len(strip); IFD=BPS+6
    hdr=b"II"+struct.pack("<H",42)+struct.pack("<I",IFD); bps=struct.pack("<HHH",8,8,8)
    def e(t,ty,c,v): return struct.pack("<HHI",t,ty,c)+v
    def sh(v): return struct.pack("<HH",v,0)
    def lo(v): return struct.pack("<I",v)
    ent=[e(256,3,1,sh(w)),e(257,3,1,sh(h)),e(258,3,3,lo(BPS)),e(259,3,1,sh(8)),
         e(262,3,1,sh(2)),e(273,4,1,lo(8)),e(277,3,1,sh(3)),e(278,3,1,sh(h)),
         e(279,4,1,lo(len(strip))),e(284,3,1,sh(1))]
    ifd=struct.pack("<H",len(ent))+b"".join(ent)+struct.pack("<I",0)
    Path(path).write_bytes(hdr+strip+bps+ifd)

def png(path,w,h,px):
    raw=bytearray()
    for y in range(h):
        raw.append(0)
        for x in range(w): raw+=bytes(px[y*w+x])
    comp=zlib.compress(bytes(raw),9)
    def ch(t,d): return struct.pack(">I",len(d))+t+d+struct.pack(">I",zlib.crc32(t+d)&0xffffffff)
    Path(path).write_bytes(b"\x89PNG\r\n\x1a\n"+ch(b"IHDR",struct.pack(">IIBBBBB",w,h,8,2,0,0,0))+ch(b"IDAT",comp)+ch(b"IEND",b""))

def finish(g, drawn):
    based=list(drawn)
    for y in range(LH):
        for x in range(LW):
            if based[y*LW+x]: continue
            for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                nx,ny=x+dx,y+dy
                if 0<=nx<LW and 0<=ny<LH and based[ny*LW+nx]: g[y*LW+x]=(28,14,10); break
    out=[VOID]*(W*H)
    for y in range(LH):
        for x in range(LW):
            c=g[y*LW+x]
            for yy in range(S):
                row=(y*S+yy)*W
                for xx in range(S): out[row+x*S+xx]=c
    return out

def cput(g,d,x,y,c):
    x=int(round(x)); y=int(round(y))
    if 0<=x<LW and 0<=y<LH: g[y*LW+x]=c; d[y*LW+x]=True
def csoft(g,x,y,c,a):
    x=int(round(x)); y=int(round(y))
    if 0<=x<LW and 0<=y<LH: i=y*LW+x; g[i]=mix(g[i],c,a)
def cell(g,d,cx,cy,rx,ry,c):
    for y in range(int(cy-ry),int(cy+ry)+1):
        for x in range(int(cx-rx),int(cx+rx)+1):
            if ((x-cx)/rx)**2+((y-cy)/ry)**2<=1.0: cput(g,d,x,y,c)
def cline(g,d,x0,y0,x1,y1,c,th=1):
    n=int(max(abs(x1-x0),abs(y1-y0)))+1
    for k in range(n+1):
        x=x0+(x1-x0)*k/n; y=y0+(y1-y0)*k/n
        if th<=1: cput(g,d,x,y,c)
        else:
            for ox in range(-(th//2),th//2+1): cput(g,d,x+ox,y,c)
def glow(g,cx,cy,col,amp,sx,sy):
    for y in range(LH):
        for x in range(LW):
            dd=((x-cx)**2/sx+(y-cy)**2/sy)
            if dd<1: csoft(g,x,y,col,amp*(1-dd))

def portrait_enforcer(m):   # the Cinnamon Enforcer — a red bear, glowing eyes, cinnamon-stick batons
    g=[VOID]*(LW*LH); d=[False]*(LW*LH)
    RED=(212,72,48); RED_D=shade(RED,0.32); RED_L=tint(RED,0.16); SNOUT=(182,60,42); NOSE=(36,18,14)
    EG=(255,150,40); EC=(255,232,140); BR=(150,98,54); BR_D=(108,68,38); WT=(255,236,226)
    cx=32; glow(g,cx,32,RED,0.10,720,680)
    cell(g,d,cx,60,16,18, RED)                     # body
    cell(g,d,cx,62,10,12, RED_L)                   # belly
    cell(g,d,cx-14,52,4,5, RED); cell(g,d,cx+14,52,4,5, RED)   # shoulders
    cline(g,d, cx-14,50, cx-23,40, RED, th=4)      # arms raised
    cline(g,d, cx+14,50, cx+23,40, RED, th=4)
    cell(g,d,cx-23,39,3,3, RED); cell(g,d,cx+23,39,3,3, RED)   # paws
    cline(g,d, cx-24,40, cx-28,27, BR, th=3); cline(g,d, cx-22,40, cx-26,27, BR_D, th=2)  # L cinnamon stick
    cline(g,d, cx+24,40, cx+28,27, BR, th=3); cline(g,d, cx+22,40, cx+26,27, BR_D, th=2)  # R cinnamon stick
    cell(g,d,cx,31,15,14, RED)                     # head
    cell(g,d,cx-12,19,5,5, RED); cell(g,d,cx+12,19,5,5, RED)   # ears
    cell(g,d,cx-12,19,2,2, RED_D); cell(g,d,cx+12,19,2,2, RED_D)
    for ex in (cx-6,cx+6):                          # glowing eyes
        cell(g,d,ex,29,3,3, EG); cell(g,d,ex,29,1,1, EC); cput(g,d,ex-1,28,WT)
    cell(g,d,cx,36,5,4, SNOUT); cell(g,d,cx,34,2,1, NOSE)      # snout + nose
    for t in range(7): cput(g,d, cx-3+t, 38+(1 if t in (0,6) else 0), shade(SNOUT,0.4))   # smile
    cell(g,d,cx-8,76,4,2, RED_D); cell(g,d,cx+8,76,4,2, RED_D) # feet
    return finish(g,d)

PORTRAITS = {"enforcer": portrait_enforcer}
import sys
if __name__=="__main__" and len(sys.argv)>1 and sys.argv[1]=="--preview":
    byname={m["name"]:m for m in R["members"]}
    for nm in (sys.argv[2:] or [R["members"][0]["name"]]):
        m=byname[nm]; px=PORTRAITS.get(m.get("domain"),portrait_enforcer)(m)
        tiff(ROOT/f"_preview_{slug(nm)}.tiff",W,H,px); png(ROOT/f"_preview_{slug(nm)}.png",W,H,px); print("preview:",nm)
else:
    for m in R["members"]:
        tiff(AG/f"{slug(m['name'])}.tiff", W, H, PORTRAITS.get(m.get("domain"),portrait_enforcer)(m))
        print(f"carbon badge -> agents/{slug(m['name'])}.tiff  ({m['name']})")

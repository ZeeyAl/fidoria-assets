#!/usr/bin/env python3
"""Sheet transisi 3 tile (edge | corner A | corner B) -> 12 tile flat + 12 tile iso + preview.
Pemakaian: trans_pipeline.py SHEET T1 T2 REF1 REF2 OUTDIR
  T1 = terrain di sisi atas (edge) dan di pojok NW (corner A); T2 = terrain lain.
"""
import sys, os, subprocess
import numpy as np
from PIL import Image, ImageFilter
sheet,T1,T2,R1,R2,OUT=sys.argv[1:7]
P=3;S=512
os.makedirs(OUT,exist_ok=True)
a=np.asarray(Image.open(sheet).convert('RGB')).astype(int)
H,W,_=a.shape
mag=lambda x:(x[...,0]>190)&(x[...,2]>170)&(x[...,1]<120)
M=mag(a)
# kolom/baris non-magenta -> segmen tile
col=M.mean(0)<0.5;row=M.mean(1)<0.5
def runs(v):
    r=[];s=None
    for i,x in enumerate(v):
        if x and s is None:s=i
        if not x and s is not None:r.append((s,i));s=None
    if s is not None:r.append((s,len(v)))
    return r
cr=[r for r in runs(col) if r[1]-r[0]>50];rr=[r for r in runs(row) if r[1]-r[0]>50]
assert len(cr)==3 and len(rr)==1,(cr,rr)
y0,y1=rr[0];TR=3
tiles={}
for n,(x0,x1) in zip(['edge','cornerA','cornerB'],cr):
    t=Image.fromarray(a[y0+TR:y1-TR,x0+TR:x1-TR].astype('uint8')).resize((S,S),Image.BOX)
    tiles[n]=np.asarray(t).astype(float)
# bersihkan sisa magenta
for n in tiles:
    t=tiles[n]
    for _ in range(8):
        m=mag(t)
        if not m.any():break
        for dy,dx in [(1,0),(-1,0),(0,1),(0,-1)]:
            sh=np.roll(t,(dy,dx),(0,1));ms=np.roll(m,(dy,dx),(0,1));ok=m&~ms
            t[ok]=sh[ok];m=mag(t)
    tiles[n]=t
ref1=np.asarray(Image.open(R1).convert('RGB')).astype(float);ref2=np.asarray(Image.open(R2).convert('RGB')).astype(float)
c1=ref1.reshape(-1,3).mean(0);c2=ref2.reshape(-1,3).mean(0)
def isT2(x):  # centroid terdekat
    d1=((x-c1)**2).sum(-1);d2=((x-c2)**2).sum(-1);return d2<d1
def split(v):
    n=len(v);cs=np.concatenate([[0],np.cumsum(v)]);best=None
    for k in range(n+1):
        sc=(k-cs[k])+(cs[n]-cs[k])
        if best is None or sc>best[0]:best=(sc,k)
    return best[1]/n
def measure(t,e):
    m=isT2(t);s=8
    if e=='L':return split(m[:,:s].mean(1)>.5)
    if e=='R':return split(m[:,-s:].mean(1)>.5)
    if e=='T':return split(m[:s].mean(0)>.5)
    if e=='B':return split(m[-s:].mean(0)>.5)
def warp(t,specs):
    h,w,_=t.shape;yy,xx=np.mgrid[0:h,0:w].astype(float);X=xx/(w-1);Y=yy/(h-1);sx=X.copy();sy=Y.copy()
    for e,b in specs:
        f=lambda q:np.interp(q,[0,.5,1],[0,b,1])
        if e in 'LR':sy+=((1-X)**P if e=='L' else X**P)*(f(Y)-Y)
        else:sx+=((1-Y)**P if e=='T' else Y**P)*(f(X)-X)
    ix=np.clip(np.rint(sx*(w-1)),0,w-1).astype(int);iy=np.clip(np.rint(sy*(h-1)),0,h-1).astype(int)
    return t[iy,ix]
cfg={'edge':['L','R'],'cornerA':['T','L'],'cornerB':['R','B']}
for n,es in cfg.items():
    b={e:measure(tiles[n],e) for e in es}
    tiles[n]=warp(tiles[n],list(b.items()))
    print(n,'batas sebelum',{k:round(v,3) for k,v in b.items()},'sesudah',{e:round(measure(tiles[n],e),3) for e in es})
# samakan warna
allp=np.concatenate([t.reshape(-1,3) for t in tiles.values()]);mk=isT2(allp)
def tf(src,dst):
    ms,ss=src.mean(0),src.std(0)+1e-6;md,sd=dst.mean(0),dst.std(0);return lambda x:(x-ms)/ss*sd+md
f2=tf(allp[mk],ref2[isT2(ref2)]);f1=tf(allp[~mk],ref1[~isT2(ref1)])
for n in tiles:
    t=tiles[n];m=(isT2(t)*255).astype('uint8')
    soft=np.asarray(Image.fromarray(m).filter(ImageFilter.GaussianBlur(2.5))).astype(float)[...,None]/255
    tiles[n]=np.clip(soft*f2(t)+(1-soft)*f1(t),0,255)
# rotasi
fl=os.path.join(OUT,'flat');os.makedirs(fl,exist_ok=True)
pre=f'{T1}_{T2}'
lab={'edge':[f'edge_{T1}{d}' for d in 'NESW'],
     'cornerA':[f'corner_{T1}{d}' for d in ['NW','NE','SE','SW']],
     'cornerB':[f'corner_{T2}{d}' for d in ['SE','SW','NW','NE']]}
L={}
for n in tiles:
    im=Image.fromarray(tiles[n].astype('uint8'))
    for k in range(4):
        r=im.rotate(-90*k);r.save(f'{fl}/{pre}_{lab[n][k]}.png');L[lab[n][k]]=r
# preview pulau
def fill(p):
    im=Image.open(p).convert('RGB');return im.resize((int(im.width*.75),)*2,Image.BOX).crop((50,50,50+S,50+S))
F1=fill(R1);F2=fill(R2)
# pulau T2 di T1: pusat T2; edge_T1N = T1 di atas -> T2 bawah
g=[[L[f'corner_{T2}SE'],L[f'edge_{T1}N'],L[f'corner_{T2}SW']],[L[f'edge_{T1}W'],F2,L[f'edge_{T1}E']],[L[f'corner_{T2}NE'],L[f'edge_{T1}S'],L[f'corner_{T2}NW']]]
h=[[L[f'corner_{T1}SE'],L[f'edge_{T1}S'],L[f'corner_{T1}SW']],[L[f'edge_{T1}E'],F1,L[f'edge_{T1}W']],[L[f'corner_{T1}NE'],L[f'edge_{T1}N'],L[f'corner_{T1}NW']]]
# NB: edge_T1X = T1 di sisi X. Pulau T1 di T2: tepi kiri grid = T2 di kiri? -> T1 di kanan (E).
def sh(grid):
    c=Image.new('RGB',(S*3,S*3))
    for j in range(3):
        for i in range(3):c.paste(grid[j][i],(i*S,j*S))
    return c.resize((720,720),Image.BOX)
o=Image.new('RGB',(1460,720),(255,255,255));o.paste(sh(g),(0,0));o.paste(sh(h),(740,0));o.save(os.path.join(OUT,'preview_islands.png'))

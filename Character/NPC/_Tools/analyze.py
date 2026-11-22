import numpy as np
from PIL import Image

SRC='/mnt/user-data/uploads/1000996367.png'
OUT=(47,37,34); SKIN=(250,243,232); SHADE=(185,179,161); MOUTH=(231,213,198); BLUSH=(209,157,167)

def load():
    return np.array(Image.open(SRC).convert('RGBA'))

def kind(px):
    if px[3]==0: return None
    t=tuple(int(v) for v in px[:3])
    return {OUT:'#',SKIN:'.',SHADE:'o',MOUTH:'s',BLUSH:'p'}.get(t,'?')

def analyze_cell(im,c,r):
    f=im[r*32:(r+1)*32,c*32:(c+1)*32]
    a=f[:,:,3]>0
    if not a.any(): return None
    ys=np.where(a.any(axis=1))[0]
    top,bot=int(ys.min()),int(ys.max())
    widths=a.sum(axis=1)
    # neck: narrowest row in window below the head widest part
    lo=top+8; hi=min(top+14,bot)
    cand=[(int(widths[y]),y) for y in range(lo,hi+1)]
    hw=int(widths[top+3:top+9].max()) if top+9<32 else int(widths.max())
    cand2=[(w,y) for w,y in cand if w<=hw-3]
    if cand2:
        m=min(w for w,y in cand2); neck=min(y for w,y in cand2 if w==m)
    else:
        neck=top+11
    # head silhouette rows top..neck-1
    # head x-range: restrict to widest row region
    hm=a[top:neck,:]
    xs=np.where(hm.any(axis=0))[0]
    # head interior: use rows top+2..neck-2 span to avoid arms
    rowsx=[np.where(a[y])[0] for y in range(top,neck)]
    # classify facing by eyes
    eyes=[];blush=0
    for y in range(top+3,neck):
        row=f[y]
        xs_y=np.where(a[y])[0]
        if len(xs_y)==0: continue
        l,rr=xs_y.min(),xs_y.max()
        for x in range(l+2,rr-1):
            k=kind(f[y,x])
            if k=='#' and a[y,x-1] and a[y,x+1]: eyes.append((x,y))
            if k=='p': blush+=1
    ex=sorted(set(x for x,y in eyes))
    # cluster eye columns
    cl=[]
    for x in ex:
        if cl and x-cl[-1][-1]<=1: cl[-1].append(x)
        else: cl.append([x])
    hx0=min(r.min() for r in rowsx if len(r)); hx1=max(r.max() for r in rowsx if len(r))
    # head centre from rows top+3..top+8
    mid=[np.where(a[y])[0] for y in range(top+3,min(top+9,neck))]
    hx0=min(m.min() for m in mid); hx1=max(m.max() for m in mid)
    cx=(hx0+hx1)/2
    if len(cl)>=2: view='F'; d=0
    elif len(cl)==1:
        ecx=np.mean(cl[0]); view='S'; d=1 if ecx>cx else -1
    else:
        view='B' if blush==0 else 'F'; d=0
    if len(cl)>=2:
        ecx=np.mean([np.mean(k) for k in cl]); 
        if abs(ecx-cx)>=1.5: d=1 if ecx>cx else -1
    return dict(c=c,r=r,top=top,bot=bot,neck=neck,hx0=int(hx0),hx1=int(hx1),cx=cx,view=view,d=d,blush=blush)

def analyze_all(im=None):
    if im is None: im=load()
    out={}
    for r in range(7):
        for c in range(35):
            g=analyze_cell(im,c,r)
            if g: out[(c,r)]=g
    return out

if __name__=='__main__':
    im=load(); A=analyze_all(im)
    print(len(A))
    # debug render: neck line in red, view letter
    from PIL import ImageDraw
    z=4
    bg=Image.new('RGBA',(1120,224),(120,160,120,255)); bg.alpha_composite(Image.fromarray(im))
    big=bg.resize((1120*z,224*z),Image.NEAREST); d=ImageDraw.Draw(big)
    for (c,r),g in A.items():
        y=(r*32+g['neck'])*z
        d.line([(c*32*z,y),(c*32*z+32*z,y)],fill=(255,0,0,255))
        d.text((c*32*z+2,r*32*z+2),g['view']+str(g['d']),fill=(0,0,255,255))
    for i,(a0,b0) in enumerate([(0,9),(9,18),(18,27),(27,35)]):
        big.crop((a0*32*z,0,b0*32*z,224*z)).save(f'/home/claude/dbg{i}.png')

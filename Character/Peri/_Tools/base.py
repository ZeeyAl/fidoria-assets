import json, numpy as np
from PIL import Image
SRC='/mnt/user-data/uploads/1001002637.png'
FD='/home/claude/out/Character/Shared/Base/frame_data.json'
sheet=np.array(Image.open(SRC).convert('RGBA'))
frames=json.load(open(FD))['frames']
CREAM=(250,243,232); DARK=(47,37,34); SHADE=(185,179,161); BLUSH=(209,157,167)

def cell(i):
    f=frames[i]; return sheet[f['y']:f['y']+32, f['x']:f['x']+32]

def cls(px):
    r,g,b,a=[int(v) for v in px]
    if a==0: return None
    if (r,g,b)==DARK: return 'D'
    if (r,g,b)==SHADE: return 'S'
    if (r,g,b)==BLUSH: return 'B'
    return 'C'

def scale_frame(i, s, Gsrc, Gdst, n=6):
    src=cell(i); H=32
    A=np.zeros((H,H)); D=np.zeros((H,H)); S=np.zeros((H,H)); B=np.zeros((H,H))
    ys,xs=np.mgrid[0:H,0:H]
    for a in range(n):
        for b in range(n):
            ox=(a+.5)/n; oy=(b+.5)/n
            sx=np.floor(16+(xs+ox-16)/s).astype(int); sy=np.floor(Gsrc+(ys+oy-Gdst)/s).astype(int)
            ok=(sx>=0)&(sx<32)&(sy>=0)&(sy<32)
            sx=np.clip(sx,0,31); sy=np.clip(sy,0,31)
            p=src[sy,sx]; al=(p[...,3]>0)&ok
            rgb=p[...,:3].astype(int)
            isD=al&(rgb==DARK).all(-1); isS=al&(rgb==SHADE).all(-1); isB=al&(rgb==BLUSH).all(-1)
            A+=al; D+=isD; S+=isS; B+=isB
    t=n*n; return A/t,D/t,S/t,B/t

def build_body(A,D,S,B):
    op=A>=0.5
    pad=np.pad(op,1)
    inter=op&pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:]
    out=np.zeros((32,32,4),np.uint8)
    for y in range(32):
        for x in range(32):
            if not op[y,x]: continue
            if not inter[y,x]: c=DARK
            else:
                a=max(A[y,x],1e-6)
                if D[y,x]/a>=0.5: c=DARK
                elif B[y,x]/a>=0.25: c=BLUSH
                elif S[y,x]/a>=0.5: c=SHADE
                else: c=CREAM
            out[y,x]=(*c,255)
    return out
if __name__=='__main__':
    import sys
    # ground baseline of idle_down frame 8
    ys=np.where(cell(8)[...,3].any(1))[0]; print('idle rows',ys.min(),ys.max())
    for s in (0.62,0.7,0.75):
        outs=[]
        for i in (0,1,3,8,12,16,20,24,70,100,125,130,135):
            A,D,S,B=scale_frame(i,s,ys.max()+1,ys.max()+1-2)
            outs.append(build_body(A,D,S,B))
        W=len(outs); im=np.zeros((32,32*W,4),np.uint8)
        for k,o in enumerate(outs): im[:,k*32:(k+1)*32]=o
        img=Image.fromarray(im); bg=Image.new('RGBA',img.size,(120,160,120,255)); bg.alpha_composite(img)
        bg.resize((img.width*4,img.height*4),Image.NEAREST).save(f'body_s{int(s*100)}.png')

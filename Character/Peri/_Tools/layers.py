import math, numpy as np
from base import *

S=0.7; GSRC=32; LIFT=2; GDST=GSRC-LIFT

# ---------- meta tiap frame ----------
ORDER=[('idle',4),('walk',4),('run',6),('interact',4),('jump',5),('attack',7)]
DIRS=['down','down_right','right','up_right','up']
META={}
for k in range(8): META[k]=('rotate',None,k,8)
_i=8
for a,n in ORDER:
    for d in DIRS:
        for k in range(n): META[_i]=(a,d,k,n); _i+=1
assert _i==158

# ---------- palet ----------
HAIR=dict(hi=(244,222,255),base=(200,158,236),shade=(150,108,198),out=(78,52,112))
DRESS=dict(hi=(214,246,200),base=(140,214,164),shade=(88,168,130),out=(40,98,86))
WING=dict(fill=(196,240,255,150),vein=(140,214,240,215),out=(92,160,214,225),hi=(255,255,255,215))

# ---------- util ----------
def new(): return np.zeros((32,32,4),np.uint8)
def put(L,x,y,c,a=255):
    if 0<=x<32 and 0<=y<32: L[y,x]=(c[0],c[1],c[2],a)
def dil(m):
    p=np.pad(m,1); return p[:-2,1:-1]|p[2:,1:-1]|p[1:-1,:-2]|p[1:-1,2:]|m
def ring(m): return dil(m)&~m
def boundary(m):
    p=np.pad(m,1); inner=p[:-2,1:-1]&p[2:,1:-1]&p[1:-1,:-2]&p[1:-1,2:]&m
    return m&~inner

def geometry(body):
    op=body[...,3]>0
    rows=np.where(op.any(1))[0]; yt,yb=rows.min(),rows.max()
    hh=8
    sub=op[yt+2:yt+5]; cols=np.where(sub.any(0))[0]
    # fokus ke kepala: ambil kolom terhadap pusat massa baris atas
    hl,hr=cols.min(),cols.max()
    cx=(hl+hr)/2
    return dict(op=op,yt=int(yt),yb=int(yb),hl=int(hl),hr=int(hr),cx=cx,hh=hh,hw=int(hr-hl+1))

def mass_mask(y0,y1,xc_fn,hw_fn):
    m=np.zeros((32,32),bool)
    for y in range(y0,y1+1):
        t=(y-y0)/max(1,(y1-y0)); xc=xc_fn(t); hw=hw_fn(t)
        a=int(round(xc-hw)); b=int(round(xc+hw))
        if y==y1: a=b=int(round(xc))
        for x in range(a,b+1):
            if 0<=x<32 and 0<=y<32: m[y,x]=True
    return m

def paint(L,fill,outline,pal,cx_light=None):
    ys,xs=np.where(fill)
    for y,x in zip(ys,xs): put(L,x,y,pal['base'])
    # bayangan: tepi kanan tiap baris + strand
    for y in range(32):
        xs_=np.where(fill[y])[0]
        if len(xs_)==0: continue
        if len(xs_)>=3: put(L,xs_.max(),y,pal['shade'])
        if len(xs_)>=5 and y%3==0: put(L,xs_[len(xs_)//2],y,pal['shade'])
        if len(xs_)>=4 and y%4==1: put(L,xs_.min()+1,y,pal['hi'])
    ys,xs=np.where(outline)
    for y,x in zip(ys,xs): put(L,x,y,pal['out'])

# ---------- gerak ----------
def motion(anim,k,n):
    t=2*math.pi*k/n
    if anim=='idle': return dict(sway=1.0*math.sin(t),stream=0,lift=0)
    if anim=='walk': return dict(sway=1.0*math.sin(t),stream=1,lift=0)
    if anim=='run': return dict(sway=1.0*math.sin(t*2),stream=3,lift=0)
    if anim=='interact': return dict(sway=1.0*math.sin(t),stream=0,lift=0)
    if anim=='jump': return dict(sway=1.5*math.sin(t),stream=1,lift=[0,1,2,2,1][k])
    if anim=='attack': return dict(sway=1.5*math.sin(t),stream=1,lift=0)
    return dict(sway=1.0*math.sin(t),stream=0,lift=0)

def sign_of(i):
    f=frames[i]
    return -1 if f['facing']=='kiri' else 1

# ---------- gaun ----------
def make_dress(body,g):
    L=new(); op=g['op']; y0=g['yt']+g['hh']; span=g['yb']-y0+1
    y1=y0+max(3,int(round(span*0.62)))-1
    m=np.zeros((32,32),bool)
    m[y0:y1+1]=op[y0:y1+1]
    # flare ke samping 1px di 2 baris terbawah + kelopak di hem
    xs=np.where(m.any(0))[0]
    if len(xs)==0: return L,m
    for y in (y1-1,y1):
        ys_=np.where(m[y])[0]
        if len(ys_): m[y,max(0,ys_.min()-1)]=True; m[y,min(31,ys_.max()+1)]=True
    ys_=np.where(m[y1])[0]
    for x in range(ys_.min(),ys_.max()+1):
        if (x-ys_.min())%2==0 and y1+1<32: m[y1+1,x]=True
    fill=m&~boundary(m); out=m&boundary(m)
    paint(L,fill,out,DRESS)
    return L,m

# ---------- rambut ----------
def make_hair(g,view,sign,mo,anim):
    Lf,Lb=new(),new()
    op=g['op']; yt,yb,hl,hr,hh=g['yt'],g['yb'],g['hl'],g['hr'],g['hh']; cx=g['cx']; hw=g['hw']
    bnd=boundary(op)
    head=np.zeros((32,32),bool); head[yt:yt+hh]=op[yt:yt+hh]
    yend=yb-1-mo['lift']
    sw=mo['sway']; st=mo['stream']
    if view=='depan':
        hairhead=np.zeros((32,32),bool)
        for y in range(yt,yt+hh):
            r=y-yt
            for x in np.where(head[y])[0]:
                if r<=1 or r==2 or (r==3 and (x-hl)%3==1) or ((x<=hl or x>=hr) and r<=hh-2): hairhead[y,x]=True
        fill=hairhead&~bnd; out=hairhead&bnd
        paint(Lf,fill,out,HAIR)
        for x in range(hl+2,hl+4): put(Lf,x,yt+1,HAIR['hi'])
        m=mass_mask(yt+2,yb+1,lambda t:cx+sw*(t**1.6)*2.0,lambda t:(hw/2+0.7)-1.2*t)
        paint(Lb,m,ring(m),HAIR)
        # helai depan jatuh di depan bahu
        locks=np.zeros((32,32),bool)
        for y in range(yt+hh-1,yt+hh+5):
            q=y-(yt+hh-1)
            for x in (hl,hl+1,hr-1,hr):
                if q<=2 or (q<=4 and x in (hl,hr)) or (q==5 and x in(hl,hr) and False): locks[y,x]=True
        locks&=op|True
        paint(Lf,locks&~ring(locks),ring(locks)&~op,HAIR)
    elif view=='belakang':
        m=head.copy()
        mm=mass_mask(yt+hh-2,yend,lambda t:cx+sw*(t**1.6)*1.6,lambda t:2.6-1.1*t)
        u=m|mm
        fill=u&~(boundary(u)); out=boundary(u)|ring(u)
        paint(Lf,fill,out,HAIR)
        for y in range(yt+hh,yend,2): put(Lf,int(round(cx))+int(round(sw*((y-yt-hh)/max(1,yend-yt-hh))**1.6*1.6)),y,HAIR['shade'])
    else: # samping
        back=-sign
        hairhead=np.zeros((32,32),bool)
        face_x=hr if sign>0 else hl
        for y in range(yt,yt+hh):
            r=y-yt
            for x in np.where(head[y])[0]:
                dfront=(face_x-x) if sign>0 else (x-face_x)
                if r<=1 or (r==2 and dfront<=4) or (r==3 and dfront in (1,2)) or dfront>=hw*0.55: hairhead[y,x]=True
        fill=hairhead&~bnd; out=hairhead&bnd
        paint(Lf,fill,out,HAIR)
        xb=(hl if sign>0 else hr)+(0 if sign>0 else 0)
        m=mass_mask(yt+3,yend,lambda t:xb+back*(0.2+(st*0.9+sw*0.8)*t**1.4),lambda t:1.6-0.8*t)
        paint(Lb,m,ring(m),HAIR)
    return Lf,Lb

# ---------- sayap ----------
def wing_mask(root,axis,L,W):
    rx,ry=root; ax,ay=axis
    m=np.zeros((32,32),bool)
    for y in range(32):
        for x in range(32):
            vx,vy=x+.5-rx,y+.5-ry
            u=vx*ax+vy*ay; w=abs(vx*(-ay)+vy*ax)
            if 0<=u<=L and w<=W*math.sin(math.pi*(u/L)**0.75)+0.2: m[y,x]=True
    return m

def paint_wing(L,m,root,axis,Ln):
    out=ring(m)
    for y,x in zip(*np.where(m)): put(L,x,y,WING['fill'][:3],WING['fill'][3])
    rx,ry=root; ax,ay=axis
    for u in np.arange(0.5,Ln*0.92,0.5):
        put(L,int(rx+ax*u),int(ry+ay*u),WING['vein'][:3],WING['vein'][3])
    for y,x in zip(*np.where(out)): 
        if L[y,x,3]==0 or L[y,x,3]<WING['out'][3]: put(L,x,y,WING['out'][:3],WING['out'][3])

def flap(anim,k,n):
    t=k/n
    cyc={'idle':1,'walk':1,'run':2,'interact':1,'jump':1,'attack':1,'rotate':2}[anim]
    f=0.5-0.5*math.cos(2*math.pi*t*cyc)   # 0=terangkat, 1=terbuka lebar
    if anim=='jump': f=[0.0,0.2,0.5,0.2,0.0][k]
    if anim=='attack': f=[0.3,0.0,0.0,0.6,1.0,0.7,0.4][k]
    return f

def make_wings(g,view,sign,anim,k,n):
    Lback,Lfront=new(),new()
    yt,hh,cx=g['yt'],g['hh'],g['cx']
    f=flap(anim,k,n); ys=yt+hh-1
    if view in('depan','belakang'):
        th=math.radians(34+48*f); ps=math.radians(55+20*f)
        tgt=Lback if view=='depan' else Lfront
        for sx in (-1,1):
            rx=cx+0.5+sx*2.4
            axu=(sx*math.sin(th),-math.cos(th)); axl=(sx*math.sin(ps),math.cos(ps))
            lu=13-1.5*f
            mu=wing_mask((rx,ys),axu,lu,4.4); ml=wing_mask((rx,ys+2),axl,8.0,2.8)
            paint_wing(tgt,mu|ml,(rx,ys),axu,lu)
    else:
        back=-sign; rx=cx+back*2.0
        for far,(da,off) in enumerate(((0,0),(16,-sign*1))):
            al=math.radians(20+46*f+da)
            ax=(back*math.sin(al),-math.cos(al)); lu=12.0-1.0*f
            root=(rx+off+0.0,ys+1)
            mu=wing_mask(root,ax,lu,3.8)
            al2=math.radians(70+10*f+da)
            ax2=(back*math.sin(al2),-math.cos(al2)*0.2+0.8); n2=math.hypot(*ax2); ax2=(ax2[0]/n2,ax2[1]/n2)
            ml=wing_mask((root[0],root[1]+2),ax2,7.0,2.4)
            tmp=new(); paint_wing(tmp,mu|ml,root,ax,lu)
            if far:   # sayap jauh: lebih redup, di belakang
                tmp[...,3]=(tmp[...,3]*0.65).astype(np.uint8)
                a=Lback; mask=tmp[...,3]>0; a[mask]=tmp[mask]
            else:
                mask=tmp[...,3]>0; Lback[mask]=tmp[mask]
    return Lback,Lfront

# ---------- bangun semua layer untuk satu frame ----------
def build_frame(i):
    A,D,Sh,B=scale_frame(i,S,GSRC,GDST)
    body=build_body(A,D,Sh,B)
    g=geometry(body)
    anim,d,k,n=META[i]; view=frames[i]['view']; sign=sign_of(i); mo=motion(anim,k,n)
    dress,_=make_dress(body,g)
    hf,hb=make_hair(g,view,sign,mo,anim)
    wb,wf=make_wings(g,view,sign,anim,k,n)
    return dict(body=body,dress=dress,hair_front=hf,hair_back=hb,wings_back=wb,wings_front=wf)

STACK=['wings_back','hair_back','body','dress','wings_front','hair_front']
def composite(layers):
    im=Image.new('RGBA',(32,32),(0,0,0,0))
    for name in STACK: im.alpha_composite(Image.fromarray(layers[name]))
    return im

if __name__=='__main__':
    sel=[0,1,2,3,4,6,8,10,12,16,20,24,28,31,36,41,50,70,95,100,118,122,128,131,135,142,150]
    ims=[composite(build_frame(i)) for i in sel]
    cols=9; rows=(len(ims)+cols-1)//cols
    sh=Image.new('RGBA',(cols*32,rows*32),(54,48,74,255))
    for k,im in enumerate(ims): sh.alpha_composite(im,((k%cols)*32,(k//cols)*32))
    sh.resize((sh.width*4,sh.height*4),Image.NEAREST).save('proto.png')
    print(sh.size)

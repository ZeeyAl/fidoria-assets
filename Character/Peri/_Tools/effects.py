import math, json, random
import numpy as np
from PIL import Image

WHITE=(255,255,255); GOLD=(255,232,140); PINK=(255,166,212); LAV=(204,160,244)
CYAN=(150,228,255); MINT=(150,236,184); DEEP=(40,32,64)

class C:
    def __init__(s,w,h): s.w,s.h=w,h; s.a=np.zeros((h,w,4),float)
    def px(s,x,y,rgb,a=255):
        x=int(math.floor(x)); y=int(math.floor(y))
        if not(0<=x<s.w and 0<=y<s.h) or a<=0: return
        sa=a/255.0; d=s.a[y,x]; da=d[3]/255.0
        oa=sa+da*(1-sa)
        if oa<=0: return
        for k in range(3): d[k]=(rgb[k]*sa+d[k]*da*(1-sa))/oa
        d[3]=oa*255
    def disc(s,cx,cy,r,rgb,a=255):
        for y in range(s.h):
            for x in range(s.w):
                if math.hypot(x+.5-cx,y+.5-cy)<=r: s.px(x,y,rgb,a)
    def ring(s,cx,cy,r,t,rgb,a=255,ry=None):
        ry=ry or r
        for y in range(s.h):
            for x in range(s.w):
                d=math.hypot((x+.5-cx)/r,(y+.5-cy)/ry)*r
                if r-t<d<=r: s.px(x,y,rgb,a)
    def star(s,cx,cy,n,rgb,a=255,core=WHITE,diag=False):
        cx=int(cx); cy=int(cy)
        for i in range(1,n+1):
            f=a*(1-0.18*(i-1))
            for dx,dy in((1,0),(-1,0),(0,1),(0,-1)): s.px(cx+dx*i,cy+dy*i,rgb,f)
        if diag:
            for i in range(1,max(1,n//2)+1):
                for dx,dy in((1,1),(-1,1),(1,-1),(-1,-1)): s.px(cx+dx*i,cy+dy*i,rgb,a*.7)
        s.px(cx,cy,core,255)
    def img(s): return Image.fromarray(np.clip(s.a,0,255).astype(np.uint8))

def strip(frames):
    w,h=frames[0].size; o=Image.new('RGBA',(w*len(frames),h),(0,0,0,0))
    for i,f in enumerate(frames): o.paste(f,(i*w,0))
    return o

FX={}   # nama -> (list of images, meta)

# 1) glow_aura 32x32 x4 loop
fr=[]
for f in range(4):
    c=C(32,32); r=12+[0,1,0.5,1][f]
    for rr,aa,col in ((r,34,LAV),(r-3,40,PINK),(r-6,46,WHITE)):
        for y in range(32):
            for x in range(32):
                d=math.hypot(x+.5-16,y+.5-16)
                if d<=rr and ((x+y)%2==0 or d<rr-2): c.px(x,y,col,aa)
    for j in range(4):
        a=math.radians(f*22.5+j*90); rx=16+math.cos(a)*13.5; ry=16+math.sin(a)*13.5
        c.px(rx,ry,WHITE,255); c.px(rx+1,ry,GOLD,150); c.px(rx,ry+1,GOLD,150)
    fr.append(c.img())
FX['glow_aura']=(fr,dict(fps=8,loop=True,anchor=[16,16],note='taruh di belakang karakter, pusat = tengah badan'))

# 2) twinkle 9x9 x6
fr=[]
for n,a in ((0,255),(1,255),(2,255),(3,255),(2,200),(1,140)):
    c=C(9,9)
    if n==0: c.px(4,4,WHITE,255)
    else: c.star(4,4,n,GOLD,a,WHITE,diag=(n==3))
    fr.append(c.img())
FX['twinkle']=(fr,dict(fps=12,loop=False,anchor=[4,4],note='kilau kecil acak di sekitar peri/sayap'))

# 3) pixie_dust 16x16 x6 loop (jatuh dari sayap)
fr=[]; rnd=random.Random(7); parts=[(rnd.uniform(-3,3),rnd.uniform(0,1),rnd.choice([GOLD,PINK,CYAN,WHITE,LAV])) for _ in range(6)]
for f in range(6):
    c=C(16,16)
    for k,(dx,ph,col) in enumerate(parts):
        life=((f/6.0)+k/6.0)%1.0
        x=8+dx+math.sin((life+ph)*6.28)*1.2; y=2+life*12
        a=255*(1-life**1.5)
        c.px(x,y,col,a)
        if life<0.4: c.px(x+1,y,col,a*.5); c.px(x,y+1,col,a*.5)
    fr.append(c.img())
FX['pixie_dust']=(fr,dict(fps=10,loop=True,anchor=[8,2],note='emitter di pangkal sayap; ikut dipakai saat walk/run/idle'))

# 4) magic_burst 48x48 x7 (attack)
fr=[]
for f in range(7):
    c=C(48,48); t=f/6.0
    if f==0:
        c.disc(24,24,2.5,WHITE,255); c.disc(24,24,4.5,GOLD,120)
    else:
        R=4+t*19; 
        c.ring(24,24,R,2.2 if f<4 else 1.2,PINK,int(255*(1-t*0.7)))
        c.ring(24,24,R-2.5,1.2,GOLD,int(230*(1-t*0.8)))
        if f<5: c.disc(24,24,max(0,4-f),WHITE,255-f*30)
        L=int(7*math.sin(math.pi*min(1,t*1.15)))+1
        for k in range(8):
            a=math.radians(k*45+(f*8)); r0=R*0.35
            for i in range(L):
                c.px(24+math.cos(a)*(r0+i),24+math.sin(a)*(r0+i),WHITE if i<2 else GOLD,230-i*30)
        for k in range(8):
            a=math.radians(k*45+22.5+f*10); rr=R*1.05
            c.px(24+math.cos(a)*rr,24+math.sin(a)*rr,[CYAN,PINK,LAV,GOLD][k%4],255*(1-t*0.8))
    fr.append(c.img())
FX['magic_burst']=(fr,dict(fps=14,loop=False,anchor=[24,24],note='ledakan sihir; pakai di titik serangan (attack frame 3-4)'))

# 5) magic_orb 16x16 x4 loop (proyektil, menghadap kanan)
fr=[]
for f in range(4):
    c=C(16,16); p=[0,1,2,1][f]
    c.disc(10,8,4+0.4*p,LAV,110); c.disc(10,8,3,PINK,230); c.disc(10,8,1.8,WHITE,255)
    for i in range(1,6): c.px(10-3-i,8+math.sin((f+i)*1.4)*1.2,GOLD,200-i*34)
    c.px(10+(-1 if p else 1),5-(p%2),WHITE,220)
    fr.append(c.img())
FX['magic_orb']=(fr,dict(fps=12,loop=True,anchor=[10,8],note='proyektil menghadap kanan; flip_x untuk kiri'))

# 6) orb_hit 32x32 x5
fr=[]
for f in range(5):
    c=C(32,32); t=f/4.0
    c.ring(16,16,3+t*11,2 if f<3 else 1,WHITE if f<2 else PINK,int(255*(1-t*.75)))
    if f<3: c.disc(16,16,4-f,WHITE,255-f*50)
    for k in range(6):
        a=math.radians(k*60+15); rr=3+t*13
        c.px(16+math.cos(a)*rr,16+math.sin(a)*rr,[GOLD,CYAN,PINK][k%3],255*(1-t*.8))
        c.px(16+math.cos(a)*(rr-1.5),16+math.sin(a)*(rr-1.5),WHITE,160*(1-t))
    fr.append(c.img())
FX['orb_hit']=(fr,dict(fps=14,loop=False,anchor=[16,16],note='saat orb mengenai target'))

# 7) blessing 32x40 x8 (interact)
fr=[]
for f in range(8):
    c=C(32,40); t=f/8.0
    c.ring(16,36,6+4*math.sin(math.pi*t),1,MINT,150,ry=3)
    for k in range(6):
        ph=(t+k/6.0)%1.0; ang=ph*6.28*1.5+k
        x=16+math.cos(ang)*(6-3*ph); y=35-ph*30
        col=[MINT,GOLD,WHITE][k%3]; a=255*(1-ph**2)
        c.px(x,y,col,a)
        if k%2==0 and ph<0.7: c.px(x-1,y,col,a*.55); c.px(x+1,y,col,a*.55); c.px(x,y-1,col,a*.55); c.px(x,y+1,col,a*.55)
    fr.append(c.img())
FX['blessing']=(fr,dict(fps=10,loop=False,anchor=[16,36],note='efek interaksi/berkat; pusat di kaki'))

# 8) landing_pollen 32x16 x5
fr=[]
for f in range(5):
    c=C(32,16); t=f/4.0
    for k in range(10):
        s_=-1 if k%2 else 1; sp=3+ (k//2)*2.2
        x=16+s_*(2+sp*t*1.6); y=12-math.sin(math.pi*min(1,t*1.2))*(2+k%3)-(k%2)*0.5
        c.px(x,y,[GOLD,WHITE,PINK,CYAN,LAV][k%5],255*(1-t**1.7))
    c.ring(16,13,3+t*12,1,WHITE,int(140*(1-t)),ry=2+t*1.5)
    fr.append(c.img())
FX['landing_pollen']=(fr,dict(fps=12,loop=False,anchor=[16,13],note='saat mendarat setelah jump'))

# 9) warp_in 32x32 x8  (warp_out = urutan dibalik)
fr=[]
for f in range(8):
    c=C(32,32)
    if f<4:
        R=15-f*3.2; c.ring(16,16,R,1.5,LAV,120+f*30)
        for k in range(8):
            a=math.radians(k*45); c.px(16+math.cos(a)*(R+2),16+math.sin(a)*(R+2),[WHITE,GOLD][k%2],220)
        c.disc(16,16,f*0.8,WHITE,200)
    elif f<6:
        w=3 if f==4 else 2
        for y in range(2,30):
            for x in range(16-w,16+w):
                c.px(x,y,WHITE,255 if abs(x+.5-16)<w-1 else 150)
        c.disc(16,16,5 if f==4 else 4,GOLD,150)
    else:
        t=(f-6)/1.0
        for k in range(10):
            a=math.radians(k*36+10); rr=4+t*8+(k%3)*2
            c.px(16+math.cos(a)*rr,16+math.sin(a)*rr*1.2,[PINK,CYAN,GOLD,WHITE,LAV][k%5],255*(1-t*.6))
        c.ring(16,16,5+t*6,1,WHITE,int(160*(1-t)))
    fr.append(c.img())
FX['warp_in']=(fr,dict(fps=12,loop=False,anchor=[16,16],note='muncul; warp_out = putar balik urutan frame'))

# 10) ground_shadow 16x8 x3 (normal, kecil, paling kecil untuk jump)
fr=[]
for rw,rh,a in ((6.5,2.6,95),(5,2,75),(3.6,1.5,55)):
    c=C(16,8)
    for y in range(8):
        for x in range(16):
            if ((x+.5-8)/rw)**2+((y+.5-4)/rh)**2<=1: c.px(x,y,DEEP,a)
    fr.append(c.img())
FX['ground_shadow']=(fr,dict(fps=0,loop=False,anchor=[8,4],note='bayangan di tanah (peri melayang 2px); frame 0 normal, 1-2 saat jump'))

if __name__=='__main__':
    import os
    os.makedirs('fx',exist_ok=True)
    for n,(f,m) in FX.items(): strip(f).save(f'fx/{n}.png')
    # lembar kontak
    rows=[strip(f) for f,_ in FX.values()]
    W=max(r.width for r in rows); H=sum(r.height+2 for r in rows)
    sh=Image.new('RGBA',(W,H),(54,48,74,255)); y=0
    for r in rows: sh.alpha_composite(r,(0,y)); y+=r.height+2
    sh.resize((sh.width*3,sh.height*3),Image.NEAREST).save('fx_contact.png'); print(sh.size)

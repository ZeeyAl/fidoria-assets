import math
from core import *

def R(m,d,h=None):
    m=hexc(m);d=hexc(d); return (m,d,hexc(h) if h else m)
RP={
 'cream':R('ece0c4','bead8c'),'white':R('f6f3ec','bebec8'),'gray':R('9a9aa4','6c6c7c'),'charcoal':R('5a5660','3a3642'),
 'black':R('3c3844','24202c'),'blue':R('4a6eb0','2e4680'),'lblue':R('8cb4e0','5e84b8'),'navy':R('2e4278','1c284c'),
 'denim':R('5878a0','3a5078'),'red':R('c03c3c','842428'),'maroon':R('8a2c3c','5a1a28'),'wine':R('a02c44','681c2e'),
 'green':R('58a058','386c3c'),'forest':R('346444','204430'),'olive':R('7c8248','545a30'),'khaki':R('b8aa78','8c7e54'),
 'brown':R('8c603c','603e28'),'leather':R('7a5032','52341e'),'leatherdk':R('5a3a24','3a2416'),'tan':R('cead78','a08450'),
 'ochre':R('c48c3c','94622a'),'orange':R('dc8232','a85a1e'),'yellow':R('ecd050','b89a28'),'gold':R('ecc448','b88c28'),
 'steel':R('aab4c4','7480a0'),'iron':R('828a9c','545c70'),'violet':R('6848a8','462c78'),'purple':R('7a4a8c','522e62'),
 'lavender':R('b096d2','8068a8'),'pink':R('e890a8','b8607c'),'rose':R('c87894','94505e'),'teal':R('3c8c90','246064'),
 'plum':R('783c5c','4c2038'),'straw':R('dcc078','b09448'),'bamboo':R('d4b45c','a8883a'),'sand':R('dccfa4','b0a47c'),
}
OUTC=(47,37,34)

def build_zones(fr):
    n=fr.neck; bot=fr.bot; total=max(4,bot-n)
    t_end=max(3,int(round(total*0.54)))
    xs=[x for y in (n+2,n+3,n+4) if y<=bot for x in range(32) if fr.A[y,x]]
    cx=(min(xs)+max(xs))/2 if xs else fr.cx
    Z={}
    for y in range(n,bot+1):
        k=y-n
        for x in range(32):
            if not fr.A[y,x]: continue
            kk=fr.K[y][x]
            if kk=='#': continue
            s=1 if kk=='o' else 0
            dx=x-cx
            if k==0: z='neck'
            elif k<=t_end:
                if k>=2 and abs(dx)>=3.5: z='hand' if k>=t_end else 'arm'
                else: z='torso'
            else:
                if abs(dx)>=3.5 and k<=t_end+1: z='hand'
                elif y>=bot-1: z='foot'
                elif k==t_end+1: z='pelvis'
                else: z='leg'
            Z[(x,y)]=(z,s)
    return Z,cx,t_end

class Ctx:
    def __init__(s,fr):
        s.fr=fr; s.Z,s.cx,s.t_end=build_zones(fr); s.out={}
        s.n=fr.neck; s.bot=fr.bot; s.view=fr.view; s.d=fr.d
    def k(s,y): return y-s.n
    def paint(s,x,y,ramp,sh=None):
        if (x,y) not in s.Z: return False
        z,s0=s.Z[(x,y)]
        s.out[(x,y)]=ramp[(s0 if sh is None else sh)]
        return True
    def put(s,x,y,col):
        if (x,y) in s.Z: s.out[(x,y)]=col
    def pix(s,zones,k0=None,k1=None):
        for (x,y),(z,sh) in s.Z.items():
            k=y-s.n
            if z in zones and (k0 is None or k>=k0) and (k1 is None or k<=k1): yield x,y,z,sh
    def dxo(s,x): return x-s.cx

# -------- decorations
def d_belt(c,ramp,buckle=None):
    k=c.t_end
    for x,y,z,sh in c.pix(('torso',),k,k): c.paint(x,y,ramp)
    if buckle and c.view=='F':
        for x,y,z,sh in c.pix(('torso',),k,k):
            if abs(c.dxo(x))<=1: c.paint(x,y,buckle,0)
def d_apron(c,ramp,k0,k1,half=3,trim=None):
    for x,y,z,sh in c.pix(('torso','pelvis','leg','arm'),k0,k1):
        dx=c.dxo(x)
        if c.view=='F':
            if abs(dx)<=half and z!='arm': c.paint(x,y,ramp)
            elif trim and abs(dx)<=half+1 and z!='arm': c.paint(x,y,trim)
        elif c.view=='S':
            if z in('torso','pelvis','leg') and 0<=(dx*c.d)<=half-0.5: c.paint(x,y,ramp)
    if c.view=='F':
        for x,y,z,sh in c.pix(('torso',),1,k0-1):
            if abs(abs(c.dxo(x))-(half-1))<=0.6: c.paint(x,y,ramp)
        if trim:
            for x,y,z,sh in c.pix(('torso','pelvis','leg'),k0,k0):
                if abs(c.dxo(x))<=half: c.paint(x,y,trim)
def d_vest(c,ramp,open_=2.0,trim=None):
    for x,y,z,sh in c.pix(('torso','arm' if False else 'torso'),1,c.t_end-1):
        dx=abs(c.dxo(x))
        if c.view=='F':
            if dx>=open_: c.paint(x,y,ramp)
            elif trim and dx<open_ and dx>=open_-1: c.paint(x,y,trim)
        else: c.paint(x,y,ramp)
def d_collar(c,ramp):
    for x,y,z,sh in c.pix(('torso',),1,1):
        if abs(c.dxo(x))<=3.5: c.paint(x,y,ramp)
    if c.view=='F':
        for x,y,z,sh in c.pix(('torso',),2,2):
            if abs(c.dxo(x))<=1.6: c.paint(x,y,ramp)
def d_vneck(c,skin=True,trim=None):
    if c.view!='F': return
    for x,y,z,sh in c.pix(('torso',),1,2):
        dx=abs(c.dxo(x))
        if (y-c.n==1 and dx<=0.6) or (y-c.n==2 and dx<=0.1): c.out.pop((x,y),None)
        elif trim and ((y-c.n==1 and dx<=1.6) or (y-c.n==2 and dx<=1.1)): c.paint(x,y,trim)
def d_buttons(c,ramp,k0=2,step=2):
    if c.view!='F': return
    x0=int(c.cx)
    for y in range(c.n+k0,c.n+c.t_end,step):
        if (x0,y) in c.Z: c.put(x0,y,ramp[0])
def d_stripes(c,ramp,period=2,k0=1,k1=None,zones=('torso','arm')):
    k1=c.t_end-1 if k1 is None else k1
    for x,y,z,sh in c.pix(zones,k0,k1):
        if (y-c.n-k0)%period==period-1: c.paint(x,y,ramp)
def d_cross_strap(c,ramp,w=1):
    t=c.t_end
    for k in range(1,t):
        xf=(k-1)/max(1,t-2)
        if c.view=='B': xc=c.cx+3.0-6.0*xf
        elif c.view=='S': xc=c.cx+0.5*c.d*(1-2*xf)*0
        else: xc=c.cx-3.0+6.0*xf
        for dx in range(w):
            x=int(round(xc-0.5))+dx; y=c.n+k
            if (x,y) in c.Z and c.Z[(x,y)][0] in('torso',): c.paint(x,y,ramp)
def d_pauldron(c,ramp,hi=None,k1=2):
    for x,y,z,sh in c.pix(('torso','arm'),1,k1):
        if c.view=='S':
            if abs(c.dxo(x))<=2.6: c.paint(x,y,ramp)
        elif abs(c.dxo(x))>=2.5:
            c.paint(x,y,ramp, 0)
            if hi and y==c.n+1 and abs(c.dxo(x))<=3.6: c.put(x,y,hi[0])
def d_plate(c,ramp,hi=None):
    for x,y,z,sh in c.pix(('torso',),1,c.t_end-1):
        dx=c.dxo(x)
        if abs(dx)<=3.0:
            c.paint(x,y,ramp)
            if hi and c.view=='F' and dx<=-1.5 and dx>=-2.6 and y<=c.n+3: c.put(x,y,hi[0])
            if c.view in('F','B') and abs(dx)<=0.6 and y>c.n+1: c.put(x,y,ramp[1])
def d_emblem(c,kind,ramp,k0=2):
    if c.view!='F': return
    cx=c.cx; pts=[]
    if kind=='cross': pts=[(-0.5,0),(0.5,0),(-0.5,1),(0.5,1),(-1.5,1),(1.5,1),(-0.5,2),(0.5,2),(-0.5,-0),(0.5,3),(-0.5,3)]
    elif kind=='cross3': pts=[(0,0),(-1,1),(0,1),(1,1),(0,2)]
    elif kind=='star': pts=[(0,0),(-1,1),(0,1),(1,1),(0,2)]
    elif kind=='crest': pts=[(-1,0),(0,0),(1,0),(-1,1),(0,1),(1,1),(0,2)]
    elif kind=='dot': pts=[(0,0),(1,0)]
    off=0.0 if kind in('cross3','star','crest') else 0
    for ox,oy in pts:
        x=int(round(cx+ox-(0.5 if kind in('cross3','star','crest') else 0.5))); y=c.n+k0+oy
        if kind in('cross3','star','crest'): x=int(cx)+ox
        c.put(x,y,ramp[0])
def d_tabard(c,ramp,trim=None,k1=None):
    k1=c.t_end+4 if k1 is None else k1
    for x,y,z,sh in c.pix(('torso','pelvis','leg'),1,k1):
        dx=abs(c.dxo(x)); lim=2.0 if c.view!='S' else 1.5
        if dx<=lim: c.paint(x,y,ramp)
        elif trim and dx<=lim+1.0 and c.view=='F' and z in('torso',): c.paint(x,y,trim)
    if trim:
        for x,y,z,sh in c.pix(('pelvis','leg'),k1,k1):
            if abs(c.dxo(x))<=2.0: c.paint(x,y,trim)
def d_waist_sash(c,ramp,rows=2,knot=None):
    t=c.t_end
    for x,y,z,sh in c.pix(('torso',),t-rows+1,t): c.paint(x,y,ramp)
    if knot and c.view in('F','B'):
        kx=int(c.cx+2.5)
        for dy in range(2,5):
            y=c.n+t+dy-1
            for dx in range(0,2):
                if dy>=3 and dx==1: continue
                c.paint(kx+dx,y,knot)
def d_scarf(c,ramp,tail=True):
    for x,y,z,sh in c.pix(('neck',),0,0): c.paint(x,y,ramp)
    for x,y,z,sh in c.pix(('torso',),1,1):
        if abs(c.dxo(x))<=3.5: c.paint(x,y,ramp)
    if tail:
        for x,y,z,sh in c.pix(('torso',),2,4):
            dx=c.dxo(x)
            if c.view=='F' and -2.6<=dx<=-1.4: c.paint(x,y,ramp)
            elif c.view=='B' and 1.4<=dx<=2.6: c.paint(x,y,ramp)
            elif c.view=='S' and -c.d*2.6<=dx*(-1)*(1)<=-c.d*1.4 and False: pass
def d_tape(c,ramp,tick):
    for x,y,z,sh in c.pix(('neck',),0,0): c.paint(x,y,ramp)
    for x,y,z,sh in c.pix(('torso',),1,1):
        if abs(c.dxo(x))<=3.5: c.paint(x,y,ramp)
    if c.view=='F':
        for x,y,z,sh in c.pix(('torso',),2,6):
            dx=c.dxo(x)
            if abs(abs(dx)-1.5)<=0.6:
                c.paint(x,y,ramp if (y-c.n)%2 else tick,0)
def d_trim_hem(c,ramp):
    ys=[y for x,y,z,sh in c.pix(('pelvis','leg')) if (x,y) in c.out]
    if not ys: return
    yb=max(ys)
    for (x,y) in list(c.out.keys()):
        if y==yb and c.Z[(x,y)][0] in('pelvis','leg'): c.paint(x,y,ramp)
def d_cuff(c,ramp):
    t=c.t_end
    for x,y,z,sh in c.pix(('arm',),t-1,t-1): c.paint(x,y,ramp)
def d_gloves(c,ramp,forearm=0):
    for x,y,z,sh in c.pix(('hand',)): c.paint(x,y,ramp)
    if forearm:
        for x,y,z,sh in c.pix(('arm',),c.t_end-forearm,c.t_end): c.paint(x,y,ramp)
def d_pattern(c,kind,ramp,zones,k0=None,k1=None):
    for x,y,z,sh in c.pix(zones,k0,k1):
        if (x,y) not in c.out: continue
        on=False
        if kind=='batik': on=((x+y)%4==0) or ((x-y)%4==0 and (x+y)%2==0)
        elif kind=='dots': on=((x*3+y*5)%7==0)
        elif kind=='stars': on=((x*7+y*13)%11==0)
        elif kind=='plaid': on=((x//2)+(y//2))%2==0
        elif kind=='hstripe': on=(y%3==0)
        elif kind=='check': on=((x//2)%2==0) ^ ((y//2)%2==0)
        elif kind=='vlines': on=(x%4==0)
        if on: c.out[(x,y)]=ramp[1 if sh else 0]
def d_skirt_flare(c,ramp,length):  # paint pelvis/leg rows as skirt
    for x,y,z,sh in c.pix(('pelvis','leg'),c.t_end+1,c.t_end+length): c.paint(x,y,ramp)
def d_pouch(c,ramp,side=1):
    if c.view=='B': return
    x0=int(c.cx+ (2.5 if side>0 else -3.5)); 
    if c.view=='S': x0=int(c.cx-c.d*0.5)
    for dx in range(2):
        for dy in range(2):
            c.put(x0+dx,c.n+c.t_end+dy,ramp[0] if dy==0 else ramp[1])
def d_chain(c,ramp):
    if c.view!='F': return
    pts=[(-2.5,2),(-1.5,3),(-0.5,4),(0.5,4),(1.5,3),(2.5,2)]
    for ox,k in pts: c.put(int(round(c.cx+ox-0.5+0.5)) if False else int(math.floor(c.cx+ox+0.0)),c.n+k,ramp[0])
def d_bib(c,ramp,k0=3,half=3.0):
    # overall bib + straps + pants colour handled by pants
    for x,y,z,sh in c.pix(('torso',),k0,c.t_end):
        if abs(c.dxo(x))<=half and c.view=='F': c.paint(x,y,ramp)
        elif c.view!='F' and abs(c.dxo(x))<=half: c.paint(x,y,ramp)
    for x,y,z,sh in c.pix(('torso',),1,k0-1):
        if abs(abs(c.dxo(x))-(half-0.5))<=0.7: c.paint(x,y,ramp)
    if c.view=='F':
        for x,y,z,sh in c.pix(('torso',),k0,k0):
            if abs(c.dxo(x))<=half: c.paint(x,y,ramp,1)
def d_cuffs_pants(c,ramp):
    for x,y,z,sh in c.pix(('leg',),c.bot-c.n-2,c.bot-c.n-2): c.paint(x,y,ramp)
def d_sarong(c,ramp,acc,length=3):
    for x,y,z,sh in c.pix(('pelvis','leg'),c.t_end,c.t_end+length):
        c.paint(x,y,ramp)
        if ((x//2)+(y//2))%2==0: c.out[(x,y)]=acc[1 if sh else 0]
    for x,y,z,sh in c.pix(('torso',),c.t_end,c.t_end): c.paint(x,y,acc)
def d_hand_bracers(c,ramp): d_gloves(c,ramp,forearm=2)

def render(fr,spec):
    c=Ctx(fr)
    top=RP[spec['top']]; sl=spec.get('sleeve','long')
    for x,y,z,sh in c.pix(('torso',)): c.paint(x,y,top)
    for x,y,z,sh in c.pix(('arm',)):
        k=y-c.n
        if sl=='long' or (sl=='short' and k<=3) : c.paint(x,y,top)
    b=spec.get('bottom',('pants','charcoal'))
    kind,col=b[0],RP[b[1]]
    if kind=='pants':
        for x,y,z,sh in c.pix(('pelvis','leg')): c.paint(x,y,col)
    elif kind=='shorts':
        for x,y,z,sh in c.pix(('pelvis','leg'),c.t_end+1,c.t_end+b[2]): c.paint(x,y,col)
        for x,y,z,sh in c.pix(('torso',),c.t_end,c.t_end): pass
    elif kind=='skirt':
        for x,y,z,sh in c.pix(('pelvis','leg'),c.t_end+1,c.t_end+b[2]): c.paint(x,y,col)
    elif kind=='robe':
        for x,y,z,sh in c.pix(('pelvis','leg')): c.paint(x,y,col)
        for x,y,z,sh in c.pix(('foot',)):
            if not spec.get('shoes'): pass
    if spec.get('shoes'):
        for x,y,z,sh in c.pix(('foot',)): c.paint(x,y,RP[spec['shoes']])
    for dec in spec.get('decor',[]):
        fn=globals()['d_'+dec[0]]
        args=[RP[a] if isinstance(a,str) and a in RP else a for a in dec[1:]]
        fn(c,*args)
    return c.out

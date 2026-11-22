import math
from core import *
from costume import RP, OUTC

class HM:
    def __init__(s): s.p={}
    def put(s,x,y,c='m'): s.p[(int(x),int(y))]=c
    def row(s,y,x0,x1,c='m'):
        for x in range(int(x0),int(x1)+1): s.put(x,y,c)

def prof(fr,i):
    j=min(max(i,0),fr.H-1); return fr.L[j],fr.R[j]

def dome(M,fr,h,vol=1,c='m',grow=0):
    for i in range(-vol,h):
        l,r=prof(fr,i+vol); M.row(fr.top+i,l-grow,r+grow,c)

def brim(M,fr,i,ext,c='m',front=True):
    top=fr.top; hl,hr=fr.hl,fr.hr
    if fr.view=='S':
        if fr.d==1: M.row(top+i,hl-1,hr+ext,c)
        else: M.row(top+i,hl-ext,hr+1,c)
    else: M.row(top+i,hl-ext,hr+ext,c)

def build_hat(fr,spec):
    kind=spec[0]; M=HM(); top=fr.top; hl,hr,cx=fr.hl,fr.hr,fr.cx; v=fr.view; d=fr.d
    ytop=top-1
    if kind=='bandana' or kind=='headband':
        dome(M,fr,0,vol=0)
        for i in (3,4): 
            l,r=prof(fr,i); M.row(top+i,l,r,'m')
        # knot tail at back
        if v=='B':
            M.put(cx-0.5,top+5,'d');M.put(cx+0.5,top+5,'d');M.put(cx-1.5,top+6,'d');M.put(cx+1.5,top+6,'d');M.put(cx-0.5,top+6,'m')
        elif v=='S':
            rx=fr.hl if d==1 else fr.hr
            for k in range(4): M.put(rx-d*(1+k//2)-d*0,top+4+k,'m')
        if kind=='bandana':
            for i in (2,):
                l,r=prof(fr,i); M.row(top+i,l+1,r-1,'m') if v!='S' else None
    elif kind=='bow':
        x=hr-1 if v!='S' else (hr-2 if d==1 else hl+2)
        if v=='S': x=cx-d*2
        y=top+1
        for dx,dy in((-2,-1),(-2,0),(-1,0),(-2,1),(2,-1),(2,0),(1,0),(2,1),(-1,-1),(1,-1),(-1,1),(1,1)): M.put(x+dx,y+dy,'m')
        M.put(x,y,'d'); M.put(x,y,'d')
        if v=='B': pass
    elif kind=='helmet':
        dome(M,fr,5,vol=1,grow=0)
        for i in range(5,9):
            l,r=prof(fr,i)
            if v=='F': M.row(top+i,l,l+1,'m'); M.row(top+i,r-1,r,'m')
            elif v=='B': M.row(top+i,l,l+1,'m'); M.row(top+i,r-1,r,'m'); 
            else:
                if d==1: M.row(top+i,l,l+3,'m')
                else: M.row(top+i,r-3,r,'m')
        if v=='F' or v=='B':
            M.row(top+4,hl,hr,'d')
        if len(spec)>2 and spec[2]:
            # plume
            if v=='S':
                for k in range(3): M.row(ytop-1-k,int(cx-2-d*k*0.5),int(cx+1),'a')
            else:
                for k in range(3): M.row(ytop-1-k,int(cx-1),int(cx),'a')
            M.p[(int(cx),top-1)]='h'
        else:
            M.put(cx,top-1,'h')
    elif kind=='conical':
        base=top+2
        for i in range(-5,3):
            hw=1+(i+5)*0.55
            M.row(top+i,cx-hw-0.5,cx+hw-0.5,'m')
        M.row(base+0,hl-3,hr+3,'m'); M.row(base+1,hl-2,hr+2,'d')
    elif kind=='straw':
        dome(M,fr,3,vol=1)
        brim(M,fr,3,4,'m'); brim(M,fr,4,3,'d')
        M.row(top+2,hl,hr,'d')
    elif kind=='mage':
        for i in range(-7,3):
            hw=0.8+(i+7)*0.5
            off=-d*0 if v=='S' else 0
            xc=cx+( (7+i)*0.12 if i<-3 else 0)*(1 if (v!='S') else d)
            M.row(top+i,xc-hw-0.5,xc+hw-0.5,'m')
        M.row(top+3,hl-3,hr+3,'m'); M.row(top+4,hl-2,hr+2,'d')
        M.row(top+1,hl,hr,'a')
        M.put(cx,top-2,'h')
    elif kind=='tophat':
        for i in range(-5,2): M.row(top+i,cx-3.5,cx+2.5,'m')
        M.row(top+1,cx-3.5,cx+2.5,'a')
        M.row(top+2,hl-1,hr+1,'m'); M.row(top+3,hl,hr,'d')
    elif kind=='peci':
        for i in range(-2,3):
            l,r=prof(fr,min(max(i+2,3),fr.H-1)); M.row(top+i,l,r,'m')
        M.row(top+3,hl+0,hr-0,'d')
    elif kind=='feather_cap':
        dome(M,fr,3,vol=1); brim(M,fr,3,2,'d') if v!='B' else None
        # feather
        if v=='S':
            fx=cx-d*1
            for k in range(5): M.put(fx-d*k//2*1, top-2-k+ (0), 'a'); M.put(fx-d*(k//2)-d*1, top-2-k,'a')
        else:
            for k in range(5): M.put(hr-2+ (k//2),top-1-k,'a'); M.put(hr-1+(k//2),top-1-k,'a')
    elif kind=='flatcap':
        dome(M,fr,3,vol=1,grow=1 if v!='S' else 0)
        M.row(top+3,hl-1,hr+1,'d') if v!='S' else brim(M,fr,3,3,'d')
        M.put(cx-0.5,top-1,'h')
    elif kind=='turban':
        dome(M,fr,4,vol=2,grow=1)
        for i in range(-2,4):
            l,r=prof(fr,min(max(i+2,0),fr.H-1))
            for x in range(l-1,r+2):
                if ((x+i)//2)%2==0: M.put(x,top+i,'a') if (x,top+i) in M.p else None
        if v=='F': M.put(cx-0.5,top+2,'h'); M.put(cx+0.5,top+2,'h'); M.put(cx-0.5,top+3,'h')
        if v=='S': M.put(cx+d*3,top+2,'h')
    elif kind=='headband_cross':
        dome(M,fr,0,vol=0)
        for i in (3,4):
            l,r=prof(fr,i); M.row(top+i,l,r,'m')
        M.row(top+2,*prof(fr,2),'m')
        if v=='F':
            for dx,dy in((0,-1),(-1,0),(0,0),(1,0),(0,1)): M.put(cx-0.5+dx,top+3+dy,'a')
            for dx in (-2,-1,0,1): M.put(cx-0.5+dx,top+4,'m')
        if v=='B': M.row(top+5,cx-1,cx,'m')
    return M

def render_hat(fr,spec):
    M=build_hat(fr,spec)
    kind=spec[0]
    main=RP[spec[1]]
    acc=RP[spec[2]] if len(spec)>2 and spec[2] and isinstance(spec[2],str) else None
    hat_acc={'tophat':RP.get('gold'),'mage':RP.get('gold'),'peci':main,'helmet':RP['red'] if (len(spec)>2 and spec[2]) else main}
    out={}
    p=M.p
    for (x,y),c in p.items():
        if not (0<=x<32 and 0<=y<32): continue
        if c=='m': col=main[0]
        elif c=='d': col=main[1]
        elif c=='h': col=main[2] if main[2]!=main[0] else tuple(min(255,v+40) for v in main[0])
        elif c=='a':
            if kind=='helmet': col=RP['red'][0]
            elif kind=='feather_cap': col=RP['red'][0]
            elif kind in('headband_cross','tophat','mage','turban'): col=(RP[spec[2]][0] if acc else main[1])
            else: col=main[1]
        # shading: lower edge dark
        if c=='m' and (x,y+1) not in p: col=main[1]
        out[(x,y)]=col
    # outline all boundary neighbours not in mask
    for (x,y) in list(p.keys()):
        for dx,dy in((1,0),(-1,0),(0,1),(0,-1)):
            q=(x+dx,y+dy)
            if 0<=q[0]<32 and 0<=q[1]<32 and q not in p:
                out.setdefault(q,OUTC)
    # outline pixels shouldn't stay over face features below hat; fine
    return out

import math
from core import *

RAMPS={
 'black':((64,54,62),(42,34,42),(112,100,116)),
 'dkbrown':((94,64,46),(62,42,32),(138,100,74)),
 'brown':((132,86,54),(96,60,38),(180,128,86)),
 'chestnut':((152,98,56),(112,68,40),(200,146,92)),
 'auburn':((148,64,42),(106,42,30),(202,108,72)),
 'ginger':((198,98,46),(152,66,32),(236,152,86)),
 'blonde':((228,188,100),(190,146,68),(250,228,152)),
 'ash':((196,176,132),(156,136,96),(228,214,176)),
 'gray':((170,170,180),(122,122,136),(220,220,230)),
 'white':((238,238,242),(180,182,198),(255,255,255)),
 'silver':((200,204,218),(150,156,180),(240,244,255)),
}
OUTC=(47,37,34)

class Mask:
    def __init__(s): s.p={}   # (x,y)->1 main
    def add(s,x,y): s.p[(int(x),int(y))]=1
    def row(s,y,x0,x1):
        for x in range(int(x0),int(x1)+1): s.add(x,y)
    def disc(s,cx,cy,r):
        for y in range(int(cy-r-1),int(cy+r+2)):
            for x in range(int(cx-r-1),int(cx+r+2)):
                if (x-cx)**2+(y-cy)**2<=r*r: s.add(x,y)
    def strand(s,x0,y0,length,w,drift=0.0,taper=2,sway=0.0):
        for k in range(length):
            ww=w if k<length-taper else max(1,w-(k-(length-taper)+1))
            xs=x0+drift*k+sway*math.sin(k*0.9)
            xa=int(round(xs))+(w-ww)//2
            for x in range(xa,xa+ww): s.add(x,y0+k)

def head_profile(fr,vol,flat):
    H=fr.H
    def Lh(i):
        j=i+vol
        if flat and i<flat: j=flat+vol-1 if False else max(j,flat)
        j=min(max(j,0),H-1)
        return fr.L[j]
    def Rh(i):
        j=i+vol
        if flat and i<flat: j=max(j,flat)
        j=min(max(j,0),H-1)
        return fr.R[j]
    return Lh,Rh

def build_hair(fr,st):
    """returns mask dict {(x,y):shade} shade 1 main 2 dark 3 hi"""
    M=Mask(); top=fr.top; H=fr.H; view=fr.view; d=fr.d
    vol=st.get('vol',1); cap=st.get('cap',3); flat=st.get('flat',0)
    puff=st.get('puff',0); puffrows=st.get('puffrows',8)
    Lh,Rh=head_profile(fr,vol,flat)
    def LL(i): return (Lh(i) if i>=-vol else Lh(-vol))-(puff if 0<=i<puffrows else 0)
    def RR(i): return (Rh(i) if i>=-vol else Rh(-vol))+(puff if 0<=i<puffrows else 0)
    fringe=st.get('fringe','straight'); fr_b=st.get('fr',4)
    side=st.get('side',6); sw=st.get('sw',2); back=st.get('back',7)
    drop=st.get('drop',0); dropw=st.get('dropw',3)
    ss=st.get('ss',cap); dropf=st.get('dropf',drop); dropb=st.get('dropb',drop); drops=st.get('drops',drop); bstart=st.get('bstart',-vol)
    exts=st.get('ext',[])
    hl,hr,cx=fr.hl,fr.hr,fr.cx
    ycx=cx
    # view mapping: 3/4 front treated as front
    if view=='F':
        # cap
        for i in range(-vol,cap):
            M.row(top+i,LL(i),RR(i))
        # fringe
        for i in range(cap,fr_b):
            l,r=LL(i),RR(i); n=r-l+1; t=(i-cap+1)/max(1,(fr_b-cap))
            if fringe=='straight':
                if i==fr_b-1 and st.get('comb',1):
                    for x in range(l,r+1):
                        if (x-l)%3!=1: M.add(x,top+i)
                else: M.row(top+i,l,r)
            elif fringe=='swept_r':
                M.row(top+i,l,l+int(n*(1.0-0.75*(i-cap)/max(1,fr_b-cap-0)))-1)
                if i==cap: M.row(top+i,l,r)
            elif fringe=='swept_l':
                M.row(top+i,r-int(n*(1.0-0.75*(i-cap)/max(1,fr_b-cap-0)))+1,r)
                if i==cap: M.row(top+i,l,r)
            elif fringe=='part':
                k=int((i-cap+1)*1.2+0.5)
                M.row(top+i,l,int(cx-0.5)-k+ (1 if i==cap else 0)); M.row(top+i,int(cx+1.0)+k-(1 if i==cap else 0),r)
            elif fringe=='curtain':
                k=1+(i-cap)
                M.row(top+i,l,int(cx-0.5)-k+1); M.row(top+i,int(cx+1.0)+k-1,r)
            elif fringe=='spiky':
                for x in range(l,r+1):
                    if (x-l)%2==0 or i==cap: M.add(x,top+i)
            elif fringe=='wispy':
                for x in range(l,r+1):
                    if (x+i)%2==0 or i==cap: M.add(x,top+i)
            elif fringe=='side_l':  # long side bang on left
                M.row(top+i,l,l+max(2,n//2-(i-cap)))
            elif fringe=='side_r':
                M.row(top+i,r-max(2,n//2-(i-cap)),r)
            elif fringe=='none': pass
        # sides
        for i in range(ss,min(side,H)):
            M.row(top+i,LL(i),LL(i)+sw-1); M.row(top+i,RR(i)-sw+1,RR(i))
        # drop (long hair beyond chin) over shoulders
        for k in range(dropf):
            y=fr.neck+k
            if y>31: break
            l,r=fr.edge(y) if fr.A[y].any() else (None,None)
            if l is None: continue
            if k==0: l,r=min(l,fr.L[-1]),max(r,fr.R[-1])
            ww=max(1,dropw-(1 if k>=drop-1 else 0))
            M.row(y,l,l+ww-1); M.row(y,r-ww+1,r)
        # sides between head-bottom rows to neck (if side>=H)
    elif view=='B':
        for i in range(bstart,min(back,H)):
            M.row(top+i,LL(i),RR(i))
        for k in range(dropb):
            y=fr.neck+k
            if y>31: break
            l,r=fr.edge(y) if fr.A[y].any() else (None,None)
            if l is None: continue
            if k==0: l,r=min(l,fr.L[-1]),max(r,fr.R[-1])
            sh=st.get('dropshape','full')
            if sh=='full':
                ww=max(4,(r-l+1)-(0 if k<drop-2 else 2))
                M.row(y,int(cx-ww/2+0.5),int(cx+ww/2-0.5))
            elif sh=='sides':
                M.row(y,l,l+dropw-1); M.row(y,r-dropw+1,r)
    else: # side view, d = facing dir
        rear=-d
        ra=hl if d==1 else hr   # rear edge x
        fa=hr if d==1 else hl   # front edge x
        for i in range(-vol,cap):
            M.row(top+i,LL(i),RR(i))
        # fringe: front-of-forehead block
        for i in range(cap,fr_b):
            l,r=LL(i),RR(i)
            if fringe=='none': break
            span=max(3,(r-l)-1-(i-cap))
            if d==1: M.row(top+i,r-span-1,r-1)
            else: M.row(top+i,l+1,l+span+1)
        # rear mass
        rl=int((hr-hl)*0.58)
        for i in range(cap,min(back,H)):
            l,r=LL(i),RR(i)
            if d==1: M.row(top+i,l,l+rl+(1 if i<back-1 else -1))
            else: M.row(top+i,r-rl-(1 if i<back-1 else -1),r)
        for k in range(drops):
            y=fr.neck+k
            if y>31: break
            l,r=fr.edge(y) if fr.A[y].any() else (None,None)
            if l is None: continue
            ww=max(3,dropw+1-(1 if k>=drop-1 else 0))
            if d==1: M.row(y,l,l+ww-1)
            else: M.row(y,r-ww+1,r)
    # --- extensions
    for e in exts: ext(M,fr,e,view,d,vol)
    return M

def ext(M,fr,e,view,d,vol):
    top=fr.top; H=fr.H; hl,hr,cx=fr.hl,fr.hr,fr.cx
    name=e[0]; a=e[1:]
    rear=-d; ra=hl if d==1 else hr
    ytop=top-vol
    if name=='bun_top':
        r=a[0] if a else 2.3; off=a[1] if len(a)>1 else 0
        if view=='S': cxb=cx+rear*2
        else: cxb=cx
        M.disc(cxb-0.5+0.0,ytop-r+0.5,r)
    elif name=='bun_low':
        if view=='F': return
        r=a[0] if a else 2.2
        if view=='S': M.disc(ra+rear*1.5, top+H-3, r)
        else: M.disc(cx-0.5, top+H-2, r)
    elif name=='bun_side':  # high bun offset
        if view=='S': M.disc(cx+rear*2, ytop-1.5, 2.2)
        else: M.disc(cx+2.5,ytop-1.5,2.2)
    elif name=='double_bun':
        r=a[0] if a else 1.9
        if view=='S': M.disc(cx+rear*1-0.5, ytop+1, r)
        else:
            M.disc(hl+0.5,top+1,r); M.disc(hr-0.5,top+1,r)
    elif name=='knot':  # topknot small
        if view=='S': M.disc(cx+rear*1.5,ytop-1.5,1.6)
        else: M.disc(cx-0.5,ytop-1.5,1.6)
        M.row(ytop,int(cx-1),int(cx))
    elif name=='tail':   # a=(attach_row, length, width, drift)
        ar,length,w=a[0],a[1],a[2]; drift=a[3] if len(a)>3 else 0
        if view=='F':
            if ar<=3: # high tail peeks above head
                M.row(ytop-1,int(cx-1),int(cx)); 
            return
        if view=='B':
            M.strand(int(cx-w/2+0.5),top+ar,length,w,0,2,sway=0.5*drift)
        else:
            x0=(ra+rear*1) if rear==-1 else ra
            xs=ra+rear*(w) if True else ra
            # start at rear edge, go outward then downward
            for k in range(length):
                ww=w if k<length-2 else max(1,w-1)
                xx=ra+rear*(1+min(k,2)*0) + rear*(min(k,3)//2) + int(drift*k)*rear
                if rear==-1: M.row(top+ar+k,xx-ww+1,xx)
                else: M.row(top+ar+k,xx,xx+ww-1)
    elif name=='side_tail':
        ar,length,w=a[0],a[1],a[2]
        if view=='F': M.strand(hl-w+1-0,top+ar,length,w,0,2)
        elif view=='B': M.strand(hr-1,top+ar,length,w,0,2)
        else:
            M.strand(ra+rear*(w)-(w-1 if rear==-1 else 0) if False else (ra-w if rear==-1 else ra+1),top+ar,length,w,0,2)
    elif name=='twin':  # a=(attach_row,length,width,out)
        ar,length,w=a[0],a[1],a[2]; out=a[3] if len(a)>3 else 1
        if view=='S':
            M.strand(ra+(0 if rear==1 else -w+1)+rear*out,top+ar,length,w,0,2); return
        M.strand(hl-w+1-out+1,top+ar,length,w,-0.0,2); M.strand(hr+out,top+ar,length,w,0.0,2)
    elif name=='braid':  # single hanging braid back/side
        ar,length=a[0],a[1]
        if view=='F': return
        if view=='B': M.strand(int(cx-1),top+ar,length,2,0,1)
        else: M.strand(ra+rear*2-(1 if rear==-1 else 0),top+ar,length,2,0,1)
    elif name=='front_braid':  # braid over shoulder (front view)
        side_=a[0]; length=a[1]
        if view=='F':
            x=hr-0 if side_>0 else hl-1
            M.strand(x,top+H-2,length,2,0,1)
    elif name=='twin_braid':
        ar,length=a[0],a[1]
        if view=='F':
            M.strand(hl-1,top+ar,length,2,0,1); M.strand(hr,top+ar,length,2,0,1)
        elif view=='B':
            M.strand(hl-0,top+ar+1,length-1,2,0,1); M.strand(hr-1,top+ar+1,length-1,2,0,1)
        else:
            M.strand(ra+rear*2-(1 if rear==-1 else 0),top+ar,length,2,0,1)
    elif name=='mohawk':
        h=a[0] if a else 4
        if view in('F','B'):
            for k in range(h):
                M.row(ytop-k,int(cx-1),int(cx))
            for i in range(0,H-3 if view=='B' else 2): M.row(top+i,int(cx-1),int(cx))
        else:
            for k in range(h): M.row(ytop-k, int(cx-3+ (1 if d==1 else 0)), int(cx+3-(0 if d==1 else 1)))
    elif name=='spikes':
        n=a[0] if a else 3; h=a[1] if len(a)>1 else 3
        if view=='S':
            xs=[int(cx-3),int(cx),int(cx+3)] if n>=3 else [int(cx-1),int(cx+2)]
        else:
            xs=[int(hl+2+i*(hr-hl-4)/(max(1,n-1))) for i in range(n)]
        for j,x in enumerate(xs):
            hh=h-(1 if j%2 else 0)
            for k in range(hh):
                M.row(ytop-1-k,x-(1 if k<hh-2 else 0)+(0), x+(1 if k<hh-2 else 0)+0)
    elif name=='tuft':  # ahoge/quiff up front
        h=a[0] if a else 2
        for k in range(h): M.row(ytop-1-k,int(cx-2+k*(1 if view!='S' else d)),int(cx+1+k*(1 if view!='S' else d)))
    elif name=='quiff':
        h=a[0] if a else 3
        for k in range(h):
            if view=='S':
                M.row(ytop-1-k, int(cx-2+d*(k)), int(cx+2+d*(k+1)))
            else:
                M.row(ytop-1-k, int(hl+2+(k//2)), int(hr-2-(k//2)))
    elif name=='afro_top':
        r=a[0] if a else 8
        M.disc(cx-0.5,top+4.5,r)
    elif name=='dread':  # hanging locks
        L_=a[0] if a else 8
        if view=='F':
            for off in (hl-1,hl+1,hr-2,hr):
                M.strand(off,top+5,L_,1,0,1)
        elif view=='B':
            for off in range(int(hl),int(hr)-1,2):
                M.strand(off,top+7,L_-2+(off%3),1,0,1)
        else:
            for k in range(3): M.strand(ra+rear*(k)-(0 if rear==1 else 0),top+5+k,L_-k,1,0,1)
    elif name=='ribbon':
        pass
    elif name=='bangs_long':
        pass

def shade_and_outline(fr,M,ramp,style_hi=True):
    main,dark,hi=ramp
    occ=set((x,y) for y in range(32) for x in range(32) if fr.A[y,x])
    pix=dict(M.p)
    # include head outline pixels adjacent to ext pixels (outside head silhouette)
    for (x,y) in list(pix.keys()):
        for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
            q=(x+dx,y+dy)
            if q in occ and fr.K[q[1]][q[0]]=='#' and q[1]<fr.neck and q not in pix:
                # add outline px only when it would be enclosed by hair on both sides
                ox,oy=q[0]+dx,q[1]+dy
                if (ox,oy) in pix or ((ox,oy) not in occ and False): pix[q]=1
    # drop mask pixels on face features: keep eyes/mouth/blush: any pixel inside head that is face (not outline) and not hair row .. handled by geometry
    out={}
    union=set(pix.keys())|occ
    for (x,y),v in pix.items():
        if not(0<=x<32 and 0<=y<32): continue
        k=fr.K[y][x] if fr.A[y,x] else None
        # boundary check vs transparent
        bnd=False
        for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
            q=(x+dx,y+dy)
            if q not in union: bnd=True
            elif q not in pix and y>=fr.neck and q in occ and not (fr.A[q[1],q[0]] and q[1]<fr.neck): bnd=True
        if bnd and not (k=='#' and False):
            out[(x,y)]=OUTC; continue
        if k=='#' and y<fr.neck and (x,y) not in pix: continue
        # shade
        col=main
        below=(x,y+1) not in pix
        if k=='o': col=dark
        elif below and (x,y-1) in pix: col=dark
        elif style_hi and fr.top<=y<=fr.top+2 and abs(x-(fr.cx-2))<=1.6 and (x,y-1) in pix: col=hi
        out[(x,y)]=col
    # outline around mask where neighbour is transparent
    for (x,y) in list(pix.keys()):
        for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
            q=(x+dx,y+dy)
            if 0<=q[0]<32 and 0<=q[1]<32 and q not in pix and q not in occ and q not in out:
                out[q]=OUTC
    return out

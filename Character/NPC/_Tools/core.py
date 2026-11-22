import numpy as np
from PIL import Image
from analyze import load, analyze_all, kind, OUT

W,Hh=1120,224
class Frame:
    def __init__(self,im,g):
        self.g=g; c,r=g['c'],g['r']
        self.c,self.r=c,r
        self.px=im[r*32:(r+1)*32,c*32:(c+1)*32]
        self.A=self.px[:,:,3]>0
        self.K=[[kind(self.px[y,x]) for x in range(32)] for y in range(32)]
        self.top,self.neck,self.bot=g['top'],g['neck'],g['bot']
        self.view,self.d=g['view'],g['d']
        self.H=self.neck-self.top
        # head row extents
        L=[];R=[]
        for i in range(self.H):
            y=self.top+i
            xs=[x for x in range(max(0,g['hx0']-1),min(32,g['hx1']+2)) if self.A[y,x]]
            if xs: L.append(min(xs));R.append(max(xs))
            else: L.append(None);R.append(None)
        # fill gaps
        for i in range(self.H):
            if L[i] is None:
                j=i-1
                while j>=0 and L[j] is None: j-=1
                if j>=0: L[i],R[i]=L[j],R[j]
                else: L[i],R[i]=g['hx0'],g['hx1']
        self.L,self.R=L,R
        self.hl=min(L);self.hr=max(R);self.cx=(self.hl+self.hr)/2
    def edge(self,y):
        xs=[x for x in range(32) if self.A[y,x] and abs(x-self.cx)<=9]
        return (min(xs),max(xs)) if xs else (None,None)

def new_canvas():
    return np.zeros((Hh,W,4),dtype=np.uint8)

def place(canvas,fr,layer):
    """layer: dict (x,y)->(r,g,b) or rgba"""
    for (x,y),col in layer.items():
        if 0<=x<32 and 0<=y<32:
            canvas[fr.r*32+y,fr.c*32+x,:3]=col[:3]
            canvas[fr.r*32+y,fr.c*32+x,3]=255

def hexc(h):
    h=h.lstrip('#'); return tuple(int(h[i:i+2],16) for i in (0,2,4))

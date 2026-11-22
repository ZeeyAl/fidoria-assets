from core import *
from hair import *
im=load(); A=analyze_all(im)
FR={k:Frame(im,g) for k,g in A.items()}

def compose_frame(fr,layers):
    img=np.zeros((32,32,4),dtype=np.uint8)
    img[:]=fr.px
    for lay in layers:
        for (x,y),col in lay.items():
            if 0<=x<32 and 0<=y<32:
                img[y,x,:3]=col[:3]; img[y,x,3]=255
    return img

def strip(frames,layers_fn,z=4,bg=(120,160,120)):
    n=len(frames)
    out=np.zeros((32,32*n,4),dtype=np.uint8)
    for i,k in enumerate(frames):
        fr=FR[k]; out[:,i*32:(i+1)*32]=compose_frame(fr,layers_fn(fr))
    I=Image.fromarray(out); b=Image.new('RGBA',I.size,bg+(255,)); b.alpha_composite(I)
    return b.resize((b.width*z,b.height*z),Image.NEAREST)

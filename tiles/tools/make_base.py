import numpy as np, sys
from PIL import Image
from scipy.ndimage import gaussian_filter
T=512
def seamless_crop(S,seed=0,sigma=12):
    h,w,_=S.shape;rng=np.random.default_rng(seed)
    y0=(h-T)//2;x0=(w-T)//2
    C=S[y0:y0+T,x0:x0+T].astype(float)
    Sh=np.roll(C,(T//2,T//2),(0,1))
    n=gaussian_filter(rng.standard_normal((T,T)),sigma,mode='wrap')
    n=(np.argsort(np.argsort(n.ravel())).reshape(T,T)+.5)/(T*T)   # uniform 0..1
    x=np.arange(T);wx=0.5-0.5*np.cos(2*np.pi*x/T)
    wgt=np.outer(wx,wx)  # 1 di tengah, 0 di tepi/pojok
    # perlu 1 di sepanjang tengah-tengah silang? tepi x=0 -> pakai Sh; tepi y=0 -> pakai Sh; Sh valid di semua tepi
    m=(n<wgt**0.8)[...,None]
    return np.where(m,C,Sh).astype('uint8')
if __name__=='__main__':
    specs={'grass':('grass_01.png',0.87),'dirt':('dirt_01.png',0.76),'sand':('sand_02.png',0.78),'water':('water_01.png',0.85)}
    tiles={}
    for t,(p,s) in specs.items():
        im=Image.open(p).convert('RGB');S=np.asarray(im.resize((round(im.width*s),)*2,Image.BOX))
        tiles[t]=seamless_crop(S)
        Image.fromarray(tiles[t]).save(f'mb_{t}.png')
    # montase 2x2 tiling tiap terrain
    m=Image.new('RGB',(1024*2,1024*2))
    for k,(t,a) in enumerate(tiles.items()):
        im=Image.fromarray(a);g=Image.new('RGB',(1024,1024))
        for i in range(2):
            for j in range(2):g.paste(im,(i*T,j*T))
        m.paste(g,((k%2)*1024,(k//2)*1024))
    m.resize((1400,1400),Image.BOX).save('mb_montage.png')

from pathlib import Path
from PIL import Image
import effects as E
P=Path('/home/claude/out/Character/Peri')
def fr(anim,d,k): return Image.open(P/'frames'/anim/d/f'{anim}_{d}_{k:02d}.png').convert('RGBA')
def fx(name,k):
    s=Image.open(P/'Effects'/f'{name}.png').convert('RGBA'); n=len(E.FX[name][0]); w=s.width//n
    return s.crop((k*w,0,(k+1)*w,s.height))
CW=48; BG=(40,34,62,255)
def put(cell,im,ax,ay,x,y): cell.alpha_composite(im,(x-ax,y-ay))
def cell(anim,d,k,steps,s):
    c=Image.new('RGBA',(CW,CW),BG); fx_dy=0
    if anim in('idle',): put(c,fx('glow_aura',s%4),16,16,24,28)
    sh=0 if anim!='jump' else [0,1,2,1,0][k]
    put(c,fx('ground_shadow',sh),8,4,24,38)
    c.alpha_composite(fr(anim,d,k),(8,6))
    if anim in('idle','walk','run'):
        put(c,fx('pixie_dust',s%6),8,2,24,19)
        if anim=='run': put(c,fx('pixie_dust',(s+3)%6),8,2,24,19)
    if anim=='jump' and k>=4: put(c,fx('landing_pollen',min(4,s%5)),16,13,24,37)
    if anim=='interact': put(c,fx('blessing',s%8),16,36,24,37)
    return c
N=16; frames=[]
for s in range(N):
    sheet=Image.new('RGBA',(CW*3,CW*2),BG)
    cells=[cell('idle','down',s%4,N,s),cell('walk','right',s%4,N,s),cell('run','right',s%6,N,s),
           cell('jump','down',s%5,N,s),None,cell('interact','down',s%4,N,s)]
    # attack + orb
    k=min(s,6) if s<8 else 6
    c=Image.new('RGBA',(CW,CW),BG); put(c,fx('ground_shadow',0),8,4,24,38); c.alpha_composite(fr('attack','right',min(s,6)),(2,6))
    if 3<=s<=9: put(c,fx('magic_orb',s%4),10,8,18+(s-3)*4,22)
    if 10<=s<=14: put(c,fx('orb_hit',s-10),16,16,44,22)
    cells[4]=c
    for i,cc in enumerate(cells): sheet.alpha_composite(cc,((i%3)*CW,(i//3)*CW))
    frames.append(sheet.resize((sheet.width*4,sheet.height*4),Image.NEAREST).convert('RGB'))
frames[0].save(P/'Preview/peri_preview.gif',save_all=True,append_images=frames[1:],duration=100,loop=0,optimize=True,disposal=2)
frames[5].save('/home/claude/peri/preview_still.png')
bg=Image.new('RGBA',(1120,224),BG); bg.alpha_composite(Image.open(P/'peri_full_sheet.png')); bg.resize((2240,448),Image.NEAREST).convert('RGB').save(P/'Preview/peri_full_sheet_preview.png')
print('ok')

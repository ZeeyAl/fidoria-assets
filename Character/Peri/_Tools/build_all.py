import json, shutil, copy
from pathlib import Path
from PIL import Image, ImageOps
import numpy as np
from layers import *
import effects as E

ROOT=Path('/home/claude/out/Character'); P=ROOT/'Peri'
if P.exists(): shutil.rmtree(P)
(P/'Layers').mkdir(parents=True); (P/'Effects').mkdir(); (P/'Preview').mkdir()

# ---- semua frame ----
LAY=['body','dress','hair_back','hair_front','wings_back','wings_front']
sheets={n:Image.new('RGBA',(1120,224),(0,0,0,0)) for n in LAY}
full=Image.new('RGBA',(1120,224),(0,0,0,0)); comp={}
for i in range(158):
    L=build_frame(i); f=frames[i]
    for n in LAY: sheets[n].paste(Image.fromarray(L[n]),(f['x'],f['y']))
    c=composite(L); comp[i]=c; full.paste(c,(f['x'],f['y']))
for n,im in sheets.items(): im.save(P/'Layers'/f'peri_{n}.png')
full.save(P/'peri_full_sheet.png')

# ---- frame per file (sama dengan Shared/Animations/frames) ----
atlas=json.load(open(ROOT/'Shared/Animations/json/animations_atlas.json'))
src_idx={}   # (anim,dir,k) -> sheet index
for i,(a,d,k,n) in META.items(): src_idx[(a,d,k)]=i
mirror={'down_left':'down_right','left':'right','up_left':'up_right'}
cnt=0
for anim,n in ORDER:
    for d in DIRS+list(mirror):
        for k in range(n):
            if d in mirror: im=ImageOps.mirror(comp[src_idx[(anim,mirror[d],k)]])
            else: im=comp[src_idx[(anim,d,k)]]
            out=P/'frames'/anim/d/f'{anim}_{d}_{k:02d}.png'; out.parent.mkdir(parents=True,exist_ok=True); im.save(out); cnt+=1
for k in range(8):
    out=P/'frames/rotate'/f'rotate_{k:02d}.png'; out.parent.mkdir(parents=True,exist_ok=True); comp[k].save(out); cnt+=1
print('frame files',cnt)
# validasi atlas
bad=[fp for a in atlas['animations'].values() for fp in a['frames'] if not (P/fp).exists()]
print('atlas path rusak',len(bad))
shutil.copy(ROOT/'Shared/Animations/json/animations_atlas.json',P/'atlas.json')

# ---- efek ----
efx={}
for n,(fr,m) in E.FX.items():
    E.strip(fr).save(P/'Effects'/f'{n}.png')
    efx[n]=dict(file=f'Effects/{n}.png',frameSize=dict(w=fr[0].width,h=fr[0].height),frames=len(fr),**m)
efx['warp_out']=dict(**{**efx['warp_in'],'note':'sama dengan warp_in, mainkan urutan frame terbalik'},reverse_of='warp_in')
meta=dict(
  name='Peri', frameSize=dict(w=32,h=32), scale_vs_human=S, hover_px=LIFT,
  layer_stack_bottom_to_top=[f'Layers/peri_{n}.png' for n in STACK],
  atlas='atlas.json',
  effects=efx,
  effect_cues=dict(
    idle=['glow_aura (loop, di belakang)','pixie_dust (loop, dari pangkal sayap)','ground_shadow[0]'],
    walk=['pixie_dust','ground_shadow[0]'],
    run=['pixie_dust (dobel)','ground_shadow[0]'],
    interact=['blessing'],
    jump=['ground_shadow[0..2] sesuai tinggi','landing_pollen saat frame terakhir'],
    attack=['magic_orb di frame 3 (lempar)','orb_hit / magic_burst saat kena'],
    spawn=['warp_in'], despawn=['warp_out']))
(P/'peri.json').write_text(json.dumps(meta,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print('ok')

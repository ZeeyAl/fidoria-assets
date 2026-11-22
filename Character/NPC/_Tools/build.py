import os, json, shutil, traceback
from prev import *
from costume import render, RP
from headgear import render_hat
from hair import build_hair, shade_and_outline, RAMPS
from styles import MALE, FEMALE
from npcs import NPCS

OUT='/mnt/user-data/outputs/NPC_Sprite_Pack'
if os.path.exists(OUT): shutil.rmtree(OUT)
for d in ('hair/male','hair/female','costumes','headgear','previews','base'): os.makedirs(f'{OUT}/{d}')
shutil.copy('/mnt/user-data/uploads/1000996367.png',f'{OUT}/base/base_body_reference.png')

HAIR_MAP={1:('M',1),2:('M',11),3:('F',14),4:('M',6),5:('M',2),6:('M',2),7:('M',3),8:('F',6),9:('F',18),10:('F',17),
 11:('M',16),12:('M',21),13:('M',9),14:('F',7),15:('M',13),16:('F',2),17:('M',25),18:('M',12),19:('F',20),20:('M',26),21:('M',24),22:('M',22)}
errs=[]
def hair_layer(fr,st):
    M=build_hair(fr,st); return shade_and_outline(fr,M,RAMPS[st['color']])

def sheet_from(fn):
    cv=new_canvas()
    for k,fr in FR.items():
        try: place(cv,fr,fn(fr))
        except Exception as e: errs.append((k,repr(e)))
    return Image.fromarray(cv)

for gender,styles,folder in (('male',MALE,'male'),('female',FEMALE,'female')):
    for i,st in enumerate(styles,1):
        img=sheet_from(lambda fr,st=st: hair_layer(fr,st))
        img.save(f"{OUT}/hair/{folder}/hair_{gender}_{i:02d}_{st['name']}.png")

def slug(s): return s.replace(' ','_')
manifest=[]
for n in NPCS:
    base=f"{n['id']:02d}_{slug(n['name'])}_{slug(n['role'])}"
    img=sheet_from(lambda fr,n=n: render(fr,n)); img.save(f"{OUT}/costumes/{base}.png")
    hp=None
    if n['hat']:
        img=sheet_from(lambda fr,n=n: render_hat(fr,n['hat'])); hp=f"headgear/{n['id']:02d}_{slug(n['name'])}_headgear.png"; img.save(f"{OUT}/{hp}")
    g,idx=HAIR_MAP[n['id']]; st=(MALE if g=='M' else FEMALE)[idx-1]; fol='male' if g=='M' else 'female'
    manifest.append(dict(id=n['id'],name=n['name'],role=n['role'],gender='Laki-laki' if n['g']=='M' else 'Perempuan',
      costume=f"costumes/{base}.png",headgear=hp,hair=f"hair/{fol}/hair_{fol}_{idx:02d}_{st['name']}.png"))
json.dump(manifest,open(f'{OUT}/npc_manifest.json','w'),indent=2,ensure_ascii=False)
print('errors',len(errs),errs[:5])

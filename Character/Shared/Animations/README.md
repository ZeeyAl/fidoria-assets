# Animations (Eris Esra 4.1, 32x32 per frame)

```
frames/<anim>/<arah>/<anim>_<arah>_NN.png   1 file = 1 frame (32x32)
sheets/    sheet PNG per animasi
source/    file .aseprite asli
json/      <anim>.json (metadata), all_animations.json (sheet 1120x224),
           animations_atlas.json (nama animasi -> daftar frame + durasi, siap dipakai di game)
```

Animasi: idle(4) walk(4) run(6) interact(4) jump(5) attack(7) rotate(8, tanpa arah)

Arah asli (5): down, down_right, right, up_right, up
Arah mirror (3): down_left, left, up_left -> flip horizontal dari kanan (di atlas ada `flip_x: true`)

Catatan:
- Di .aseprite, tag Jump_Side kedua (frame 118-122) sebenarnya Jump_Up.
- Tag asli ("Walk_Side_Up", "Punch_Down", dst.) disimpan di field `source_tag` / `frameTags`.
- Durasi frame diambil dari .aseprite (attack punya 50/100/200 ms, lainnya 100 ms).
- Path di json relatif terhadap folder `Shared/Animations/`.

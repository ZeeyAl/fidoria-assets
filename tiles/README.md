# Fidoria Terrain Tiles (top-down)

Tile terrain untuk game top-down: grass, dirt, sand, water, cobblestone, rocky.
Transisi (blend) tersedia untuk: grass-dirt, dirt-sand, grass-sand, sand-water, grass-water, dirt-cobblestone, grass-cobblestone, sand-cobblestone, water-cobblestone, grass-rocky, dirt-rocky.

## Isi
```
tiles/{512,128,64,32}/base/            tile polos per terrain (persegi, seamless)
tiles/{size}/transitions/<pair>/       12 tile transisi per pasangan terrain
autotile_rules.json                    aturan: mask 4 kuadran -> nama file
tools/autotile.py                      implementasi referensi + renderer peta contoh
tools/trans_pipeline.py, make_base.py  pembuat tile dari sheet GPT (kalau mau bikin pasangan baru)
previews/                              hasil render peta contoh
(master asli dari GPT ada di zip terpisah: fidoria_source.zip)
```
512 = master (kecuali water, cobblestone & rocky: master 256, base dibuat ulang). 128/64/32 = hasil downscale (BOX) dari master. Pilih yang sesuai ukuran tile game lu.

## Cara kerja (dual-grid)
Terrain disimpan per **cell**. Tile digambar per **vertex** (titik pertemuan 4 cell), digeser setengah tile ke kiri-atas:

    px = vx * size - size/2 ;  py = vy * size - size/2      (grid vertex = (kolom+1) x (baris+1))

Untuk tiap vertex ambil 4 cell sekitarnya, urutan **NW, NE, SE, SW**:
`NW=(vx-1,vy-1)  NE=(vx,vy-1)  SE=(vx,vy)  SW=(vx-1,vy)` (cell di luar peta = cell terdekat).
- Keempatnya sama -> tile base terrain itu.
- Dua terrain (A dan B) -> bikin mask 4 huruf (a/b), cari di `autotile_rules.json` -> `pairs[].tiles[mask]`.

Contoh mask (a = terrain pertama di nama pasangan, mis. `grass` di `grass_dirt`):

| mask | tile | artinya |
|---|---|---|
| aabb / baab / bbaa / abba | edge_aN / E / S / W | a di sisi itu, b di sisi seberang |
| abbb / babb / bbab / bbba | corner_aNW / NE / SE / SW | a hanya di satu pojok |
| aaba / aaab / baaa / abaa | corner_bSE / SW / NW / NE | b hanya di satu pojok |

N = atas layar, E = kanan, S = bawah, W = kiri.

## Pakai
```
python3 tools/autotile.py --demo hasil.png --size 64
python3 tools/autotile.py peta.txt hasil.png --size 64      # g d s w c r per cell
python3 tools/autotile.py peta.txt --validate               # cek kombinasi yang tidak didukung
```
Di engine: baca `autotile_rules.json`, ganti `{size}` dengan ukuran tile, lalu ulangi logika `Autotiler.resolve()` di `tools/autotile.py` (sekitar 30 baris).

## Batasan
- **Diagonal** (dua cell sama saling menyilang, pola catur) tidak punya tile -> otomatis dipatahkan.
- **3 terrain dalam satu vertex** atau pasangan tanpa tile (dirt-water, rocky dengan terrain selain grass/dirt) -> jadi tepi keras. Hindari lewat aturan editor, cek dengan `--validate`.
- Skala detail base tile sudah disamakan dengan tile transisi (grass, dirt, sand). Water base memakai tekstur penuh di-resize, jadi sel caustic-nya lebih kecil dari di tile transisi. Kalau mengganggu, generate ulang water dengan sel lebih besar.
- Tile base berukuran satu cell, jadi pola kelihatan berulang di area yang sangat luas. `dirt_alt` tersedia sebagai variasi tanah.

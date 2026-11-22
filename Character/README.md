# Character Assets

Aset sprite 32x32 untuk karakter player, NPC, kostum, rambut, animasi, dan ekspresi.

```
Character/
├── Player/Jobs/<Job>/     preview sheet gabungan per job (male/female)
├── Costume/<Job>/         layer kostum per job: <job>_male.png, <job>_female.png
├── Hair/<Gaya>/           layer rambut dikelompokkan per gaya (player + NPC)
├── NPC/<Nama>/            costume.png, headgear.png, preview.png, npc.json
├── Peri/                  karakter peri kecil: layer, frame, efek (lihat Peri/README.md)
└── Shared/
    ├── Animations/        frames/, sheets/, json/, source/ (.aseprite)
    ├── Expressions/       set ekspresi profil + sheet + expressions.json
    └── Base/              body_template.png, frame_data.json
```

Job: Novice, Swordsman, Archer, Mage, Assassin.
Gaya rambut: Short, Medium, Long, Ponytail, Pigtails, Braid, Bun, Curly, Spiky.

## Penamaan rambut
- `player_<KODE>_<nama>_front.png` / `_back.png` (M01-M30, F01-F30)
- `npc_<male|female>_<NN>_<nama>.png`

## Urutan layer player (bawah ke atas)
1. `Hair/.../player_*_back.png` (jika ada)
2. `Shared/Base/body_template.png`
3. `Costume/<Job>/<job>_<gender>.png`
4. `Hair/.../player_*_front.png`

Semua layer player 1120x224 (grid 32x32, 35 kolom x 7 baris, 158 frame), jadi cukup ditumpuk.

## Urutan layer NPC
Base body -> `costume.png` -> rambut (path di `npc.json`) -> `headgear.png` (jika ada).

`NPC/npc_manifest.json` berisi seluruh NPC; path di dalamnya relatif terhadap folder `Character/`.
`NPC/_Tools/` adalah skrip pembuat sprite NPC (path di dalamnya masih path lama, hanya sebagai referensi).

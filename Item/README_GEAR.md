# Fidoria – Weapons & Equipment (pixel art, transparent PNG)

Struktur mengikuti repo ZeeyAl/fidoria-assets — salin folder `Item/` ke root repo.

## Senjata (animasi) — Item/Weapon/<Job>/<rarity>/
- `<id>_sheet.png`  : spritesheet horizontal, 8 frame @ 64x64 (512x64), loop. Basic=statis, Uncommon+ = bob, kilau, partikel.
- `<id>_icon.png`   : 1 frame statis 64x64 untuk inventory.
- Job: Warrior (=Swordman), Archer, Mage, Assassin. Rarity: basic, uncommon, rare, epic, mythic, legend. 3 desain per rarity -> 72 senjata.
- fps: 8 (basic-mythic), 10 (legend).

## Gear — Item/Equipment/<Job>/<slot>/<job>_<slot>_<rarity>.png
- 48x48, slot: helm, armor, gloves, boots. 4 job x 4 slot x 6 rarity = 96 item.

## Atlas
- `Item/items_atlas.json` : id, nama, rarity, path icon/sheet, frame_w/h, frames, fps.
- `_preview/` : GIF & PNG preview (bukan untuk dipakai di game).

Efek rarity: Uncommon kilau hijau, Rare glow biru, Epic glow ungu + partikel, Mythic glow api + bara, Legend glow emas + bintang orbit + kilau pelangi.
Pixel art, tanpa anti-alias: gunakan nearest-neighbor saat di-scale.

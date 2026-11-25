WINGS PIXEL ART - Basic s/d Mythic
===================================
Kanvas 80x80 px, PNG transparan. 8 frame loop (8 fps).
Tiap spritesheet = 640x640: kolom = frame 0-7, baris = arah:
  baris 0 S, 1 SW, 2 W, 3 NW, 4 N, 5 NE, 6 E, 7 SE

Per rarity ada 4 layer (urutan gambar dari bawah ke atas):
  1. <rarity>_ground_fx.png  lingkaran sihir di kaki (Epic+)
  2. <rarity>_wing_back.png  sayap + glow + sinar + partikel yang ada di BELAKANG badan
  3. (badan karakter 32x32 ditempel di x=24, y=26)
  4. <rarity>_wing_front.png sayap + glow + partikel yang ada di DEPAN badan (arah N/NE/NW dan sisi dekat kamera)
  5. <rarity>_halo_fx.png    halo di atas kepala (Uncommon+)

Catatan:
- Layer halo & ground sama untuk ke-8 arah (simetris), baris tetap disediakan supaya indeks sheet seragam.
- Sayap otomatis ikut 8 arah; sayap dekat kamera masuk layer front, yang jauh masuk layer back.
- Badan di Preview/ hanyalah dummy placeholder, bukan karakter aslimu.
- Tinggi karakter ref: kepala y=33, bahu y=46, kaki y=57 (di kanvas 80x80).

Rarity: Basic, Uncommon, Rare, Epic, Legendary, Mythic.

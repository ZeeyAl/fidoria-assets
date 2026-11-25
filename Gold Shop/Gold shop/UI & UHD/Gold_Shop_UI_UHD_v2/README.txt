FIDORIA - GOLD SHOP UI v2 (UHD 3840x2160)
==========================================
Revisi: lebih berdimensi (shadow, bevel, glow per rarity, state kartu), ada panel PREVIEW (stage + pedestal, putar,
chip animasi, bandingkan/includes, TRY + BUY), toolbar (search/filter/sort), slot kosong. Pixel-art 8x dari grid 480x270.

TIDAK ADA HARGA. Slot harga/saldo dikosongkan: kartu (price pill), panel detail (price_well), header (balance pill).
Teks lain (nama, deskripsi) memakai font stand-in; ganti dengan font game bila perlu (versi blank/ tanpa teks tersedia).

REVISI BARU : 00_Full_Layout (4 tab + empty_template), 01_Window_Panels, 03_Buttons (blank), 05_Item_Cards, 09_UI_Misc, stars/ikon baru
TIDAK DIREVISI (salinan asli) : 02_Tabs, 04_Gold_Currency (tanpa price_tag angka & balance_pill_sample), 08_Popups, scrollbar/divider/slot di 09
Catatan: 08_Popups masih desain lama (belum diberi depth) dan mungkin memuat angka contoh.

Kartu: 05_Item_Cards/blank/card_{premium|epic|legendary|neutral|bundle}_{normal|hover|selected|owned|locked}.png (tanpa teks, tanpa sprite)
       05_Item_Cards/{skins|mounts|badges|bundles}/card_{id}_{state}.png (sprite + nama, harga KOSONG)
Semua kartu satu ukuran canvas (672x736): tumpuk di titik yang sama, state selected/hover otomatis terangkat.
Ribbon NEW/HOT/OWNED = 06_Tags_Ribbons (overlay terpisah).

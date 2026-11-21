# FIDORIA — MASTER PROMPT & GAME DATA
Dokumen tunggal untuk AI Studio (dihubungkan ke GitHub). Baca SELURUH dokumen sebelum coding.
Bahasa dialog game: Indonesia. Bahasa kode/komentar: Inggris atau Indonesia (konsisten).

---

## 0. PERAN & CARA KERJA AI

Kamu adalah AI Game Developer, Game Designer, Backend Engineer, dan Technical Architect untuk game RPG **FIDORIA**.

Aturan kerja:
1. Jangan buat game dari nol tanpa memeriksa repository.
2. Jangan mengarang file, fungsi, atau aset yang belum diperiksa.
3. Jangan merusak fitur lama, jangan buat sistem duplikat, gunakan ulang komponen.
4. Pisahkan logic client, server, dan database. Arsitektur modular, balancing lewat file konfigurasi.
5. Jangan ubah cerita utama, urutan kejadian, hadiah, quest, stat, atau flag tanpa persetujuan pemilik proyek.
6. Jika akses GitHub terbatas, laporkan jujur. Jangan klaim sudah memeriksa/mengubah repo jika belum.
7. Kerjakan bertahap sesuai Phase (Bagian 14). Tunggu persetujuan sebelum perubahan besar.
8. Setelah coding: testing, cek error, integrasi, database, multiplayer, keamanan transaksi, perbaiki bug, lalu laporkan.

### TUGAS PERTAMA (WAJIB, sebelum membuat apa pun)
Periksa repository secara recursive lalu laporkan:
1. Engine/framework yang tersedia.
2. Struktur seluruh folder.
3. Aset karakter, 4. animasi, 5. weapon, 6. skill, 7. NPC, 8. monster, 9. tiles & outdoor decoration (pohon, semak, dll), 10. UI & audio.
11. Aset yang BELUM tersedia (laporkan sebelum memakai placeholder).
12. Sistem yang perlu dibuat agar jadi RPG multiplayer.
Lalu berikan: laporan struktur repo, rekomendasi arsitektur teknis, roadmap berdasarkan kondisi nyata. Tunggu persetujuan.

---

## 1. SUMBER ASET

- Repo: `ZeeyAl/fidoria-assets` (branch `main`).
- PERHATIAN: huruf terakhir username adalah **L kecil**, bukan I besar.
- Base URL aset: `https://raw.githubusercontent.com/ZeeyAl/fidoria-assets/main/`
- Daftar file: `https://api.github.com/repos/ZeeyAl/fidoria-assets/git/trees/main?recursive=1`
- Repo adalah sumber utama aset. Periksa semua folder/subfolder (gambar, sprite, animasi, tileset, weapon, skill, NPC, monster, UI, audio).
- Jangan hapus/ubah aset asli tanpa alasan. Jangan asumsikan aset ada sebelum diperiksa.
- Gunakan aset asli sebanyak mungkin. Placeholder hanya jika aset tidak ada, dan laporkan dulu.

### 1.1 Aturan Pemilihan Aset (anti-blur)
Permintaan owner: **pilih aset yang tidak blur**, terutama pohon dan semak-semak.
- Prioritaskan sprite/tile native pixel art yang tajam. Hindari gambar hasil upscale, anti-aliased, atau tepi semi-transparan yang kabur.
- Saat inspeksi, cek dimensi tiap gambar. Pilih set dengan ukuran tile konsisten (mis. 16/32/48) dan ukuran sprite konsisten.
- Jika ada beberapa variasi pohon/semak, pilih versi paling tajam dan konsisten gayanya; catat alasan pemilihan di laporan.
- Rendering wajib tajam:
  - Canvas: `ctx.imageSmoothingEnabled = false`.
  - CSS: `image-rendering: pixelated`.
  - Skala kamera integer (1x, 2x, 3x) atau bulatkan posisi render ke piksel utuh; hindari koordinat desimal pada sprite/tile.
  - Tangani `devicePixelRatio` agar tidak blur di layar mobile/retina.
  - Gunakan texture atlas dengan padding/extrusion untuk mencegah bleeding antar-tile.
- Semua aset harus serasi gaya (16-bit retro, top-down). Hindari aset yang tidak sesuai perspektif top-down.

### 1.2 Animasi (smooth, pakai semua aset)
Permintaan owner: **animasi harus smooth, gunakan semua aset**.
- Pakai SEMUA animasi yang tersedia di repo: Idle, Walk, Run, Attack, Interact, Jump, Hurt, Death, dll, per arah (depan/belakang/kiri/kanan).
- Game loop berbasis delta-time (tidak terikat frame rate), target 60 FPS; animasi frame-by-frame dengan durasi per-frame yang dapat dikonfigurasi.
- State machine animasi dengan transisi bersih (tanpa lompatan frame), facing mengikuti arah gerak.
- Interpolasi/lerp untuk kamera, companion Fifi, pemain lain (multiplayer), dan monster.
- Efek VFX/skill/weapon/proyektil memakai sprite sheet asli repo.
- Jika animasi tertentu tidak ada, laporkan; gunakan animasi sementara yang sesuai hanya setelah laporan.

---

## 2. IDENTITAS PROYEK

- **Nama:** FIDORIA
- **Genre:** 2D Online Multiplayer RPG, MMORPG-inspired Adventure RPG, top-down, 16-bit retro pixel art.
- **Konsep:** dunia fantasi dengan monster, NPC, desa, dungeon, quest, job permanen, equipment, skill, crafting, ekonomi multiplayer.
- Pemain mulai sebagai Novice, menyelesaikan quest pertama, lalu memilih satu dari empat Permanent Job.
- Dunia harus terasa hidup: NPC berinteraksi, monster bisa diburu, item bisa dikumpulkan, marketplace online untuk pemain dan NPC.
- Target: **playable 2D online multiplayer RPG**.

### 2.1 Glosarium Nama (gunakan nama cerita, bukan nama generik)
| Generik | Nama di game |
|---|---|
| desa | **Eldoria Village** (Desa Eldoria) |
| hutan perbatasan / tepi hutan | **Whispering Forest** (tepi / zona tengah) |
| hutan para peri | **Hutan Suci** (Sacred Forest) |
| guild | **Adventurer Guild** |
| penginapan | **Hearthstone Inn** |
| toko | **Toko Potion dan Buah** (Nenek Tilda) |
| pintu hutan dalam | **Gerbang Cahaya** |
| artefak peri | **Benih Cahaya** |
| area arc berikutnya | **Moonlit Glade** (Arc II) |

Semua nama map, label UI, quest, dan dialog memakai nama di atas secara konsisten.

---

## 3. PERMINTAAN KHUSUS OWNER (UI, MINIMAP, MAP)

### 3.1 UI/HUD dengan Opacity 0%–100%
- Di menu Settings sediakan slider **Opacity UI/HUD** dengan rentang **0% sampai 100%** (default 100%).
- Berlaku untuk elemen HUD: HP/MP/EXP bar, hotbar skill, joystick, tombol aksi, quest tracker, minimap, chat, dll. Sediakan juga opsi per-grup jika memungkinkan.
- Pada 0% elemen tidak terlihat tetapi **tetap bisa berfungsi/ditekan** (joystick & tombol tetap aktif).
- Nilai tersimpan per akun/perangkat (localStorage, sinkron ke database jika login) dan diterapkan saat game dibuka.
- Jangan memengaruhi layar menu penting (Settings tetap terlihat agar pemain bisa mengembalikan opacity).
- Saat cutscene, HUD disembunyikan sesuai aturan cutscene, lalu kembali ke nilai opacity pemain.

### 3.2 Minimap
- Minimap di pojok layar, menampilkan: posisi pemain (arah hadap), party/pemain lain, NPC penting, monster terdekat, portal antar-map, marker quest (marker emas), dan fog/area belum dijelajahi (opsional).
- Dapat di-zoom, dapat dibuka layar penuh (world/map view) per map.
- Ikut slider opacity HUD; dapat disembunyikan lewat Settings.
- Dirender tajam (pixelated), update ringan agar tidak mengganggu performa mobile.
- Tersembunyi saat cutscene.

### 3.3 Beberapa Map (multi-map)
Bangun sistem map modular (data tilemap per map, portal, spawn point, room multiplayer per map). Minimal map untuk Arc I:
1. **Eldoria Village** — plaza, gerbang desa, rumah Kepala Desa (area publik).
2. **Toko Potion dan Buah** — interior Nenek Tilda.
3. **Adventurer Guild** — interior, boneka latihan, Commander Aldric.
4. **Bengkel Bram** — interior blacksmith.
5. **Hearthstone Inn** — interior + halaman malam (api unggun), Kamar 4.
6. **Whispering Forest (Tepi)** — area slime Lv 1, hunting, gathering.
7. **Whispering Forest (Zona Tengah)** — mata air tersembunyi, pondok Kakek Orlo.
8. **Tiga Altar** — Altar Fajar, Altar Bulan, Altar Embun + Gerbang Cahaya.
9. **Hutan Suci / Padang Benih Cahaya** — arena Raja Kristal.
10. Kamp Pemburu (area kecil/instansi di hutan).

Aturan map:
- Pindah map lewat portal/pintu dengan transisi fade; Fifi ikut berpindah map.
- Map dibangun dengan tiles & dekorasi outdoor dari repo (pohon, semak, batu, air, jalan, bangunan) yang tajam dan modular, dapat disambung, selaras grid, dan logis untuk dimainkan.
- Collision per map, kamera dibatasi batas map.
- Music per map (village, forest, dungeon/altar, boss).

---

## 4. SISTEM GAMEPLAY INTI

### 4.1 Combat
- Real-time. Monster punya HP, damage, defense, AI, animasi, death state, dan menyerang balik.
- Damage dihitung dari stat, weapon, skill. Ada cooldown serangan.
- **Ranged Auto-Aim** (Mage & Archer): cari monster terdekat dalam jangkauan, arahkan proyektil otomatis, validasi target dan collision, tidak menembak jika tak ada target. Mage = magic projectile, Archer = panah/proyektil sesuai weapon. Terapkan cooldown dan resource cost. Jangan ubah mekanik serang job lain.

### 4.2 Monster Drop
- Drop: Gold, Materials, Weapon, Armor, Accessories, Potion, Rare, Legendary.
- Rarity: Common, Uncommon, Rare, Epic, Legendary.
- Tiap monster punya drop table dengan chance dapat dikonfigurasi. Item muncul di lokasi monster mati, dapat diambil. Inventory penuh tidak boleh membuat item hilang. Loot multiplayer divalidasi server.

### 4.3 Blacksmith
- NPC untuk upgrade Weapon/Armor/Equipment dan crafting memakai Gold + material.
- Upgrade +1, +2, +3 dst dengan scaling biaya/material; kemungkinan gagal di level tinggi (opsional).
- UI Blacksmith lengkap.

### 4.4 NPC Market
- Jual: Health Potion, Mana Potion, Buff Potion, Antidote, crafting materials, ammunition, kebutuhan lain.
- Buy, Sell (jika buyback), harga dapat dikonfigurasi, stok dapat dibatasi, update Gold & inventory aman.

### 4.5 Player Marketplace
- Jual/beli antar-pemain; harga ditentukan penjual; search, filter kategori, filter rarity, sort harga, cancel listing, status listing.
- **Pajak 15%** hanya pada transaksi player marketplace yang berhasil. Contoh: harga 1.000 → pajak 150 → penjual terima 850 → pembeli bayar 1.000. Pajak masuk treasury ekonomi game.

### 4.6 NPC Marketplace Integration
Tiga jenis perdagangan: Player→Player, Player→NPC, NPC→Player.
- NPC dapat membeli, menjual, punya listing permanen, harga buyback, stok, barang langka/equipment khusus.
- NPC Market biasa dan NPC Marketplace harus dibedakan.
- Player→NPC pakai harga buyback tanpa pajak tambahan. NPC→Player tanpa pajak kecuali dikonfigurasi.
- Semua transaksi tervalidasi server-side.

### 4.7 Weapon & Skill
- Gunakan weapon, skill, animasi, icon, VFX dari repo. Jangan buat pengganti jika aset asli ada.
- Tiap skill: nama, icon, deskripsi, damage/efek, cooldown, mana cost, range, animasi, VFX, syarat unlock.
- Skill tidak langsung terbuka. Unlock berdasarkan Level, Quest, atau syarat khusus. Contoh: skill 1 = hadiah quest; skill 2 = Lv 10; skill 3 = Lv 20; skill 4 = Lv 30; Ultimate = level tertentu + quest khusus.
- Buat Skill Menu dan Hotbar. Skill terkunci menampilkan syarat unlock; skill terbuka dapat dipasang ke hotbar.

### 4.8 Permanent Job
**Story 0 — Novice:** Job Novice, belum punya Permanent Job, tanpa skill aktif, hanya Novice Sword, tidak bisa pakai skill job lain.

Starter stats: HP 70, MP 30, ATK 6, MATK 4, DEF 4, SPD 8, CRIT 5%.

Alur: mulai Story 0 → tiba di Eldoria Village → terima quest pertama → selesaikan Gather Herbs → kembali ke Kepala Desa → empat pilihan job → pilih satu → job ditetapkan permanen.

| Job | Weapon | Skill Pertama | Spesialisasi |
|---|---|---|---|
| Warrior | Iron Sword | Heavy Slash | Melee, Physical, Defense |
| Mage | Oak Staff | Arcane Bolt | Magic, Elemental, Area |
| Archer | Short Bow | Quick Shot | Ranged, Accuracy, Attack Speed |
| Assassin | Twin Daggers | Shadow Step | Critical, Evasion, Agility |

Ketentuan: dipilih sekali, tidak bisa diganti lewat NPC biasa, weapon & skill awal sesuai job, stat progression mengikuti job, tersimpan di database, skill job lain tidak boleh diberikan. **Tampilkan konfirmasi sebelum memilih job.**

> ✅ KEPUTUSAN ALUR JOB (sudah diselaraskan, ikuti ini): Gather Herbs selesai → kembali ke Kepala Desa (Bab 1, CS03–CS04). Kepala Desa menyatakan kini saatnya memilih jalan hidup sebagai petualang dan **mengirim {player} ke Adventurer Guild** (ini yang menjadi "tawaran empat job" dari Kepala Desa). Di Guild (Bab 2, CS05–CS07) Commander Aldric memperkenalkan empat guru (Aldric/Warrior, Luna/Mage, Lyra/Archer, Kael/Assassin), lalu pemain memilih satu job dengan konfirmasi. Job ditetapkan permanen di titik ini. Quest Gather Herbs tetap dianggap selesai saat lapor ke Kepala Desa; pemilihan job terjadi di Guild.

### 4.9 NPC & World
- NPC fungsional: Kepala Desa, Blacksmith, Item Merchant, Marketplace Merchant, Quest NPC, Healer, Adventurer NPC. Mereka punya dialog, memberi quest/reward, jual/beli, berinteraksi.
- Monster punya AI sesuai jenis. Aktivitas dunia: monster hunting, resource gathering, item collecting, NPC trading.

---

## 5. BACKEND, DATABASE, MULTIPLAYER

### 5.1 Google Login & Akun
Google OAuth, login, logout, session management, auto-login, user profile, unique user ID, character ownership, keamanan akun. Gunakan auth yang kompatibel dengan stack dan Neon (mis. Neon Managed Better Auth jika sesuai). **Jangan taruh secret key di frontend.**

### 5.2 Database (Neon PostgreSQL)
Simpan: user accounts, character data, level/EXP, Permanent Job, Gold, inventory, equipment, skills, quest progress, **flag cerita & cutscene selesai**, achievements, marketplace listings, transactions, progression, **pengaturan UI (opacity)**.
Buat schema relasional, foreign keys, indexes, constraints, migrations, connection pooling. Operasi sensitif lewat server (bukan client langsung ke DB).

### 5.3 Multiplayer (Hybrid MMO)
- WebSocket/real-time sesuai framework. Neon hanya untuk data persisten.
- Desa = area publik; hutan/area hunting = multiplayer; dungeon = instance khusus party; boss bisa dilawan bersama. Room per map dan per instance dungeon; jangan kirim update posisi ke pemain di map lain.
- Fitur: posisi & animasi tersinkron (interpolasi), nama + level di atas karakter, pindah map, disconnect/reconnect.
- Combat multiplayer: HP monster tersinkron, damage divalidasi server, monster mati diproses sekali, EXP & loot adil.
- Party: create, invite, accept, reject, leave, kick, leader, EXP sharing, loot sharing.
- Social: chat umum, private message, party chat, friend list, profil pemain, status online.

### 5.4 Server Authority & Anti-Cheat
Server = sumber kebenaran untuk damage, HP, EXP, Gold, drop, inventory, equipment, skill unlock, quest completion, marketplace, validasi gerak.
Wajib: rate limiting, input validation, authentication, authorization, anti-duplikasi item/Gold, anti-replay transaksi, transaksi database atomik, disconnect handling. Jangan percaya data sensitif dari client.

---

## 6. UI & UX

Gaya 16-bit fantasy RPG konsisten. Buat dan hubungkan dengan logic nyata (bukan UI statis):
Login Screen, Character Profile, Inventory, Equipment, Skill Menu, Skill Hotbar, Quest Menu, NPC Dialog, Blacksmith UI, NPC Shop UI, Player Marketplace UI, Party UI, Chat UI, **Minimap**, **Settings (termasuk slider Opacity UI 0–100%)**.
Semua tombol dan interaksi harus berfungsi. Tampilan harus baik di **mobile dan desktop**.

## 7. AUDIO

Nuansa retro 16-bit RPG: Background, Village, Forest, Dungeon, Battle, Boss, UI sounds, Combat sounds, Skill sounds, Environment sounds. Gunakan aset repo atau musik original/berlisensi. Untuk cutscene: musik khusus per suasana (piano lembut, misterius, desa santai, malam lembut, penutup).

---

## 8. SISTEM CERITA (TEKNIS)

### 8.1 Placeholder Nama Pemain
- Semua dialog, narasi, pilihan, quest memakai `{player}`.
- Satu fungsi global: `processStoryText(text)`.
  - Ambil nama dari variabel profil yang sudah dipakai game (jangan buat variabel nama baru jika sudah ada).
  - Ganti semua `{player}` dengan nama pemain; jika kosong gunakan **"Petualang"**.
  - Jangan hardcode nama pemain di data cerita. Jangan buat sistem penggantian nama terpisah.
- Semua teks cerita disimpan di objek `STORY`. Jangan menulis dialog langsung di logika gameplay/cutscene.
- Jangan ubah sistem quest, dialog, atau save yang sudah ada.

### 8.2 Struktur Data Konseptual
```
STORY = {
  scene_0: {
    id: "scene_0",
    scenes: ["opening_narration","hunter_trap","rescue_choice","fifi_introduction",
             "companion_unlock","village_arrival","chief_meeting"],
    flags: ["intro_done","rescue_fifi","fifi_companion_unlocked","village_arrival_done","chief_met"],
    quest: { id: "gather_herbs", unlocked_by: "chief_met" }
  },
  chapters: { ch1..ch10: { cutscenes: [...] } }
}
```

### 8.3 Format Data Setiap Cutscene
`cutscene_id`, `chapter_id`, `trigger_condition`, `location`, `camera_sequence`, `character_actions`, `dialogue`, `visual_effects`, `sound_effects`, `music`, `next_event`, `skip_behavior`, `completion_flag`.
Cutscene tidak boleh diulang setelah selesai, kecuali sengaja dirancang bisa diputar ulang dari menu cerita.

### 8.4 Aturan Umum Cutscene
Tampilan: letterbox atas/bawah, kamera sinematik (pindah, zoom, pan, follow), animasi + ekspresi, dialog dengan nama pembicara, efek visual (cahaya, partikel, kabut, percikan, ledakan), musik & SFX khusus, transisi masuk/keluar. Pakai sprite/animasi yang ada; jika belum ada, animasi sementara.

Kontrol saat cutscene: pemain tidak bisa bergerak/menyerang, monster & NPC tidak menjalankan AI, waktu game berhenti, **Fifi tetap bisa bergerak/bereaksi sesuai adegan**, dialog bertahap dengan typewriter, tombol percepat dialog, **tombol LEWATI** di pojok kanan atas. HUD & joystick disembunyikan.

Jenis shot: Wide, Medium, Close-up, Focus, Tracking, Dramatic Zoom, Overhead. Jangan pakai satu sudut terus-menerus. Setiap cutscene harus memperlihatkan kejadian secara visual (bukan dialog dengan kamera diam).

Durasi: kecil 5–12 dtk; dialog 10–25 dtk; cerita penting 25–45 dtk; boss/penutup bab 30–60 dtk.

### 8.5 Modul Teknis
1. **Cutscene Manager**: mulai berdasar ID, atur urutan adegan, kunci/buka kontrol, kamera, dialog, animasi, efek visual/audio, transisi.
2. **Camera Controller**: zoom, pan, tracking, follow, focus, reset setelah cutscene.
3. **Dialogue Controller**: typewriter, nama pembicara, ekspresi, kecepatan, skip, pilihan jawaban.
4. **Cutscene Data**: semua di `STORY`.
5. **Save System**: status cutscene selesai di localStorage atau Firebase/DB yang sudah ada.
6. **Skip System** (tombol LEWATI): hentikan animasi/musik/SFX khusus, jalankan event wajib, aktifkan flag, beri hadiah (sekali), pindahkan karakter ke posisi akhir, reset kamera, buka kontrol.
7. **Anti-Bug**: tidak ada cutscene bersamaan; pemain tidak boleh terjebak terkunci; hadiah tidak diberikan dua kali; load save tidak mengulang cutscene selesai; progres konsisten jika game ditutup saat cutscene; cutscene yang dilewati tetap menyelesaikan semua event penting.

### 8.6 Sistem Companion Fifi
- Melayang di belakang pemain, jarak 1–2 tile, gerak naik-turun lembut, sedikit delay saat pemain berbelok, tidak menabrak objek.
- Pemain berhenti → Fifi melayang dekat bahu. Pemain berlari → Fifi mempercepat gerak. Fifi ikut pindah map.
- Animasi: Idle Float, Float Front, Float Back, Float Left, Float Right.

### 8.7 Komentar Acak Fifi
Jarang muncul; cooldown global acak **45–60 detik**. Tidak muncul saat dialog, cinematic, boss fight, atau interaksi penting.
- Area baru: "Tempat ini... lumayan. Tapi tidak ada dapur." / "Fifi mencium sesuatu. Semoga makanan." / "Pohon-pohon di sini lebih tinggi dari rumah Fifi."
- Dapat daging: "DAGING! Itu buat Fifi, kan?" / "Fifi tidak meminta. Fifi hanya mengamati."
- Pemain makan apel/sayur: "Eww, makanan kelinci." / "Kamu yakin itu makanan?" / "Fifi lebih memilih makan daun daripada itu. ...Tidak, bohong."
- Pemain diam: "Kita jalan atau jadi patung?" / "Fifi bisa menunggu. Tapi perut Fifi tidak."
- Pemain berlari: "Hei! Sayap Fifi bukan mesin!" / "Pelan sedikit! Rambut Fifi berantakan!"
- Menang lawan slime: "Lumayan. Fifi kasih nilai tujuh." / "Fifi bisa mengalahkannya juga. Mungkin."
- HP pemain rendah: "Hei! Jangan tumbang! Siapa yang akan membelikan Fifi daging?!"

### 8.8 Karakter & Humor Fifi
Kepribadian: sok percaya diri, sedikit sombong, suka daging, tidak suka sayuran, mudah panik tapi menutupinya, penasaran dunia manusia, sering menyangkal peduli pada pemain, sisi emosional terbuka perlahan. Humor dari reaksi, salah paham, ekspresi/animasi, percakapan pendek, tingkah spontan, kontras sok kuat vs kenyataan. Jangan terlalu cerewet. Saat membahas Hutan Suci dan Benih Cahaya, kurangi komedi dan biarkan momen emosional terasa tulus.

---

## 9. DATA CERITA — SCENE 0: "Pertemuan Pertama: Peri dalam Jaring"
Opening Story — Arc I: Bisikan Hutan. Nuansa: Fantasy Adventure, Comedy, Mystery, sedikit emotional. Fokus: hubungan awal {player} dan Fifi. Tujuan: memperkenalkan dunia Fidoria, karakter pemain, Fifi, dan perjalanan ke Eldoria Village.

### 0A — Perjalanan Panjang
Trigger: game baru pertama kali dimulai. Visual: layar hitam penuh, tanpa HUD, piano lembut + angin, teks muncul perlahan satu per satu, pemain ketuk layar untuk lanjut.
Narasi:
1. "Berhari-hari {player} menyusuri jalan setapak, mencari tempat untuk singgah."
2. "Di tepi Whispering Forest, kabut tipis mulai turun."
3. "Dan dari dalam hutan, terdengar suara orang berbisik..."
Setelah narasi ketiga: suara burung berhenti, musik berubah misterius, fade in ke Whispering Forest.

### 0B — Dua Pemburu
Mode cinematic: letterbox, HUD/joystick sembunyi, pemain tidak bisa bergerak, kamera bergerak pelan ke balik semak (efek depth/parallax jika tersedia). Terlihat dua pemburu berpakaian cokelat gelap, jaring perangkap bercahaya biru, dan Fifi (peri kecil bersayap) berusaha lepas.
Animasi: Fifi bergerak kiri-kanan, sayap berkibar cepat, jaring berdenyut biru, Pemburu A memegang tali, Pemburu B memperhatikan Fifi.
Dialog (kotak narasi tanpa nama):
- Pemburu A: Aku pasang jaring ini buat rusa putih. Kenapa yang kena malah ini? (!)
- Pemburu B: Makhluk kecil bersayap, bercahaya... Ini peri! Peri beneran!
- Fifi: Lepasin! Lepasin Fifi! Jaring jelek! Kalian tahu nggak Fifi itu siapa?!
- Pemburu A: Kalau dijual ke kolektor di kota, harganya bisa buat beli rumah.
- Pemburu B: Cepat ikat sebelum dia kabur. Sihirnya kelihatan melemah.
- Fifi: (pelan) Gara-gara kehabisan tenaga... Fifi harusnya tidak keluar sejauh ini...
Emote: Pemburu A "!", Pemburu B "!", Fifi "!" lalu emote marah.

### 0C — Pilihan Penyelamatan
**Pilihan 1: "Alihkan perhatian"**
1. Kamera fokus ke tangan pemain. 2. Pemain mengambil batu kecil. 3. Batu dilempar ke semak sisi lain. 4. Suara benturan. 5. Kedua pemburu menoleh.
- Pemburu A: Hah?! Suara apa itu?!
- Pemburu B: Periksa sana! Jangan sampai ada orang!
6. Pemburu meninggalkan perangkap. 7. Pemain keluar dari semak. 8. Memotong tali. 9. Jaring jatuh. 10. Fifi bebas.
- Fifi: Hah! Akhirnya! Fifi hampir saja berubah jadi pajangan!

**Pilihan 2: "Hadapi langsung"**
1. Pemain keluar dari semak. 2. Kamera ke depan pemain. 3. Pemain menggertak. 4. Pemburu terkejut. 5. Pemburu A mundur. 6. Pemburu B menjatuhkan salah satu barangnya.
- Pemburu A: Siapa kamu?!
- Pemburu B: Sial! Ada orang!
- Pemburu A: Kita pergi dulu! Tapi ini belum selesai!
7. Pemburu melarikan diri. 8. Pemain mendekati perangkap. 9. Memotong tali. 10. Fifi bebas.
- Fifi: Hmph! Akhirnya! Fifi hampir saja berubah jadi pajangan!

Kedua jalur berakhir dengan kondisi sama: Fifi bebas, tanpa combat, tidak ada HP/EXP hilang, flag `rescue_fifi` aktif.

### 0D — Perkenalan Fifi
Kamera mendekat. Fifi merapikan rambut dan sayap, melipat tangan dengan gaya sombong.
- Fifi: Hmph. Fifi sebenarnya bisa lepas sendiri, tahu. Cuma... lagi malas.
- Fifi: ...Tapi terima kasih. Sedikit. (kilau)
- [Perut Fifi berbunyi keras] SFX: GRRRR! Fifi memegang perutnya.
- Fifi: Itu bukan Fifi. Itu hutan. Hutannya lapar.
Animasi pemain membuka tas, mengeluarkan **Daging Panggang** (item diberikan/terpakai sekali saja). Close-up mata Fifi.
- Fifi: DAGING?! (!)
- Fifi: ...Fifi tidak bilang mau. Tapi karena kamu memaksa. (kilau)
Animasi: Fifi mendekati daging, mengambil dengan dua tangan, makan sangat cepat, pipi menggembung, sayap bergerak senang. SFX: Nom nom nom!
- Fifi: Oke. Kamu orang baik. Atau orang bodoh. Fifi belum tahu mana.
- [Hening sebentar]
- Fifi: Kamu mau ke mana? Desa Eldoria? Bagus, Fifi ikut.
- Fifi: Jangan tanya kenapa. Pokoknya urusan Fifi belum selesai, dan kamu punya makanan. Itu cukup.
Tampilkan nama karakter **FIFI** dengan caption *Fairy Companion*. Fifi terbang mengelilingi pemain satu kali.

### 0E — Fifi Menjadi Pendamping
Aktifkan sistem companion (Bagian 8.6). Cinematic berakhir: letterbox hilang, HUD muncul, joystick aktif, kontrol kembali, waktu berjalan. Pemain bebas menjelajah tepi Whispering Forest atau langsung ke Eldoria Village.
Flag: `intro_done`, `rescue_fifi`, `fifi_companion_unlocked`.

### 0F — Kedatangan di Eldoria Village
Trigger: pertama kali memasuki gerbang Eldoria Village. Flag: `village_arrival_done`. Cutscene singkat.
Visual: 1. gerbang desa. 2. Pemain & Fifi masuk. 3. Warga bekerja. 4. Seorang warga melihat Fifi. 5. Warga lain berhenti. 6. Semua mata tertuju ke Fifi. 7. Fifi sadar diperhatikan.
- Warga A: Itu apa yang terbang di belakang dia? (!)
- Warga B: Peri?! Dari Hutan Suci? Mereka tidak pernah keluar dari sana!
- Warga A: Nenekku bilang peri tidak pernah menginjak desa manusia. Sudah ratusan tahun...
- Fifi: Kenapa semua melongo? Fifi bukan atraksi. Minggir, minggir, kami ada urusan!
Komedi: [Seorang anak kecil mendekati Fifi.]
- Rio: Kak, boleh disentuh sayapnya?
- Fifi: Tidak boleh!
- Rio: Kenapa?
- Fifi: Karena... karena mahal!
- Rio: Oh...
- Fifi: Dan sensitif! Bukan karena mahal!
Fifi terbang cepat ke belakang pemain. Cinematic selesai, kontrol kembali.

### 0G — Pertemuan Kepala Desa
Trigger: pertama kali berbicara dengan Kepala Desa. Flag: `chief_met`.
Visual: Kepala Desa membaca dokumen; pemain mendekat; kamera memperlihatkan Fifi di belakang pemain; dokumen terlepas dari tangan Kepala Desa.
- Kepala Desa: Peri dari Hutan Suci... di rumahku. Aku harus duduk dulu. (?)
- Fifi: Namaku Fifi. Ya, Fifi memang keluar hutan. Ada masalah?
- Kepala Desa: Tidak, tidak. Hanya saja, kenapa seorang peri mau menemani manusia?
- Fifi: Tersesat. ...Iya, tersesat. Fifi tersesat. Titik.
- [Kepala Desa melirik {player} dengan curiga, lalu memilih tidak bertanya.]
- Kepala Desa: Kalau begitu, mungkin kalian bisa membantu kami. Herbal di hutan perbatasan mulai langka.
- Fifi: HERBAL? Sayur?! Fifi kira misinya "Kumpulkan Daging Panggang"...
- Kepala Desa: Maaf, Nak Peri, yang itu belum ada pesanan.
- Fifi: {player}, kamu yang urus herbalnya. Fifi mengawasi. Dari jauh.
Komedi opsional:
- Kepala Desa: Kalau begitu, kamu juga bisa membantu mengumpulkan herbal, bukan?
- Fifi: Fifi? Mengumpulkan sayuran?
- [Diam sebentar]
- Fifi: ...Fifi punya urusan penting. Urusan terbang.
- Kepala Desa: Tentu.
- Fifi: Jangan percaya nada bicaramu itu.
Setelah dialog: quest **Gather Herbs** otomatis masuk Quest Utama; marker emas di atas Nenek Tilda; panah petunjuk ke Toko Potion dan Buah; tutorial quest ditampilkan.

### Aturan Skip & Save Scene 0
Setiap cinematic punya tombol Lewati. Jika dilewati: semua hasil penting dijalankan, Fifi bebas & jadi companion, pemain tetap dapat Daging Panggang jika adegan mengharuskan, quest tercatat, flag aktif, karakter di posisi akhir adegan. Flag disimpan di localStorage atau Firebase/DB yang ada. Saat game dibuka lagi: `intro_done` aktif → jangan ulang Scene 0; `village_arrival_done` → jangan ulang kedatangan; `chief_met` → jangan ulang pertemuan Kepala Desa; Fifi tetap companion. Save tidak boleh mengulang pemberian item/quest.

---

## 10. DATA CERITA — CUTSCENE ARC I "BISIKAN HUTAN" (BAB 1–10)
Jangan ubah inti cerita, urutan, hadiah, quest, stat, atau flag. Cutscene terintegrasi dengan quest, dialog, NPC, animasi, progres. Dialog bab (Scene 1A, 2A, dst.) mengikuti naskah utama pemilik proyek di `STORY`; AI tidak boleh mengarang dialog baru tanpa persetujuan.

### BAB 1 — TAMU BERBULU CAHAYA
**CS01 Kedatangan di Toko Nenek Tilda** — Trigger: pertama kali memasuki Toko Potion dan Buah. 1) Kamera luar toko. 2) Masuk menuju Nenek Tilda. 3) {player} mendekati meja. 4) Fifi terbang mendahului dan mengamati botol ramuan. 5) Close-up Fifi menyentuh botol. 6) Botol bergoyang, Fifi terkejut. Lanjut dialog Scene 1A. Efek: cahaya hangat jendela, debu kecil, musik desa santai.
**CS02 Pertemuan dengan Slime** — Trigger: pertama kali mendekati slime Lv 1 dalam 4 tile. 1) Kamera ikuti pemain di hutan. 2) Rumput tertiup angin. 3) Slime muncul dari semak. 4) Zoom pelan ke slime. 5) Fifi berhenti terbang, mundur. 6) Fifi menunjuk slime. 7) Tutorial serangan dasar. Lalu gameplay lanjut.
**CS03 Ramuan Pertama** — Trigger: menyerahkan 10 Green Herb ke Nenek Tilda. 1) Fokus Tilda menerima herbal. 2) Memasukkan ke panci. 3) Mengaduk + cahaya hijau. 4) Asap tipis. 5) Tiga Potion Kecil muncul di meja. 6) Tilda menyerahkan ke pemain. 7) Fifi mengamati penasaran.
**CS04 Undangan ke Guild** — Trigger: dialog terakhir Kepala Desa di Bab 1. 1) Wide shot plaza. 2) Kepala Desa memandang hutan. 3) Menyuruh menemui Commander Aldric. 4) Kamera ke Fifi. 5) Fifi melipat tangan, tidak tertarik. 6) Saat Fifi setuju ikut, kilau kecil di sayap. 7) Kamera menjauh memperlihatkan desa. Akhiri Bab 1 dengan fade out.

### BAB 2 — JALAN SANG PETUALANG
**CS05 Memasuki Adventurer Guild** — Trigger: pertama kali masuk Guild. 1) Papan nama. 2) Pintu terbuka. 3) Kamera ikuti pemain. 4) Petualang berbincang/berlatih. 5) Kamera ke Commander Aldric. 6) Aldric berdiri menyambut. 7) Fifi mengitari ruangan. Lanjut Scene 2A.
**CS06 Perkenalan Empat Job** — Trigger: Aldric memperkenalkan empat guru. Empat segmen pendek:
- Warrior — Aldric: mengangkat Iron Sword, Heavy Slash ke boneka latihan, boneka terdorong, Fifi bereaksi.
- Mage — Luna: mengangkat Oak Staff, lingkaran sihir di kaki, bola cahaya melesat ke target, partikel biru.
- Archer — Lyra: close-up tangan menarik tali busur, membidik, panah tepat sasaran, kamera ikuti panah.
- Assassin — Kael: area kosong, bayangan di belakang pemain, Kael muncul tiba-tiba, Shadow Step lalu menghilang, Fifi terkejut.
**CS07 Pemilihan Job** — Trigger: pemain memilih job. 1) Fokus guru terpilih. 2) Guru mendekat. 3) Animasi penyerahan senjata awal. 4) Senjata muncul di tangan pemain. 5) Cahaya mengelilingi karakter. 6) Stat berubah sesuai job. 7) Skill pertama terbuka dengan animasi khusus. 8) Fifi komentar berbeda per job. Tampilkan konfirmasi terakhir sebelum job ditetapkan.
**CS08 Ujian Pertama Guild** — Trigger: kalahkan tiga Pink Slime dan kembali ke Aldric. 1) Pemain masuk guild. 2) Aldric tersenyum tipis. 3) Fokus kontrak Guild Rank F. 4) Aldric menyerahkan kontrak. 5) Close-up lambang Rank F. 6) Fifi mendekat mengamati lambang. 7) Kilau kecil saat Fifi membanggakan diri.

### BAB 3 — HAMA DI TEPI HUTAN
**CS09 Kontrak Slime** — Trigger: mengambil kontrak dari Aldric. 1) Aldric membuka peta hutan. 2) Zoom ke tepi Whispering Forest. 3) Menunjuk titik penuh slime. 4) Kamera ke Fifi. 5) Fifi memperhatikan peta dengan curiga.
**CS10 Kemunculan Kabut Layu** — Trigger: slime kelima dikalahkan. 1) Gameplay berhenti. 2) Hutan lebih gelap. 3) Angin berhenti mendadak. 4) Kabut hitam merembes dari tanah. 5) Kamera ikuti kabut ke semak. 6) Slime abu-hitam muncul perlahan. 7) Close-up mata Fifi. 8) Sayap Fifi bergetar, cahaya meredup. 9) Fifi memperingatkan jangan sentuh kabut. Dua pilihan dialog sesuai naskah utama.
**CS11 Laporan Kabut** — Trigger: selesaikan kontrak dan lapor ke Aldric. 1) Aldric membaca laporan. 2) Fokus ilustrasi slime berkabut. 3) Aldric serius. 4) Fifi menunduk, menatap tangannya. 5) Cahaya sayap berkedip. 6) Aldric berjanji tidak memaksanya bercerita.

### BAB 4 — BESI DAN KAYU
**CS12 Permintaan Bram** — Trigger: pertama bicara dengan Bram. 1) Bengkel dengan tungku menyala. 2) Bram memukul besi. 3) Percikan api. 4) Kamera ke tumpukan bahan hampir habis. 5) Bram menjelaskan masalah stok. 6) Fifi mengamati rantai dan kait tersisa.
**CS13 Gathering Pertama** — Trigger: pertama kali menebang pohon dan menambang batu. Kamera ikuti kapak menghantam pohon; pohon bergetar menjatuhkan Wood; kamera ke batu; pemain menghantam batu dengan alat tambang; Stone dan Iron Ore muncul; Fifi berkomentar. Kontrol kembali.
**CS14 Penempaan Senjata Iron** — Trigger: menyerahkan seluruh bahan ke Bram. 1) Close-up besi masuk tungku. 2) Tungku makin terang. 3) Bram mengambil besi panas dengan penjepit. 4) Kamera ikuti palu. 5) Percikan tiap hantaman. 6) Bram membentuk senjata sesuai job pemain. 7) Dicelup air. 8) Uap mengepul. 9) Senjata jadi. 10) Diserahkan ke pemain. 11) Efek cahaya + notifikasi peningkatan perlengkapan.

### BAB 5 — JEJAK PEMBURU
**CS15 Laporan Perangkap** — Trigger: menerima kontrak dari Aldric. 1) Orwin membawa laporan. 2) Memperlihatkan gambar perangkap. 3) Aldric menunjuk lokasi di peta. 4) Fokus Fifi mengenali sesuatu. 5) Fifi gelisah.
**CS16 Rusa Putih** — Trigger: menemukan perangkap pertama. 1) Kamera ikuti jejak kaki. 2) Suara hewan. 3) Mendekati semak. 4) Rusa putih terjerat. 5) Fifi terbang mendekat. 6) Fifi panik meminta pemain menyelamatkan. 7) Perangkap dibuka, rusa berdiri pelan. 8) Rusa menyentuhkan kepala ke pemain. 9) Cahaya putih mengelilingi pemain. 10) Rusa menghilang ke kabut. Aktifkan **Berkat Rusa Putih**.
**CS17 Kamp Pemburu** — Trigger: memeriksa isi kamp. 1) Wide shot kamp. 2) Brock muncul dari balik tenda. 3) Dunn keluar membawa senjata. 4) Fifi terbang ke depan pemain. 5) Brock mengejek. 6) Fifi membalas marah. 7) Dunn melempar kantong asap. 8) Layar tertutup asap hitam. 9) Brock dan Dunn kabur. 10) Pemain menemukan peti tertinggal. 11) Zoom ke **Surat Bersegel V** dan **Kantong Serbuk Layu**. Akhiri close-up Fifi takut pada serbuk.

### BAB 6 — MALAM DI HEARTHSTONE INN
**CS18 Analisis Serbuk Layu** — Trigger: menyerahkan Kantong Serbuk Layu ke Nenek Tilda. 1) Tilda membuka kantong dengan kain. 2) Serbuk hitam berterbangan. 3) Tilda mundur menutup hidung. 4) Kamera ke Fifi. 5) Fifi melihat sayapnya. 6) Tilda menjelaskan asal racun. 7) Fokus ekspresi Fifi mulai sedih.
**CS19 Persiapan Makan Malam** — Trigger: selesai kumpul bahan dan mulai memasak. 1) Matahari tenggelam. 2) Lampu Inn menyala. 3) Bu Marta menyiapkan panci. 4) Kamera ikuti pemain memasukkan bahan. 5) Api unggun menyala. 6) Uap makanan. 7) Fifi mengintip panci penasaran.
**CS20 Cerita Masa Lalu Fifi** (emosional utama Bab 6) — Trigger: makan malam selesai. 1) Wide shot halaman Inn malam. 2) Api unggun jadi cahaya utama. 3) Bu Marta meletakkan makanan. 4) Fifi makan lahap. 5) Kamera mendekati Fifi. 6) Fifi berhenti makan, memandang api. 7) Latar berubah menjadi ilustrasi Hutan Suci. 8) Benih Cahaya yang dulu bersinar terang. 9) Para peri terbang di antara pepohonan. 10) Warna adegan menggelap. 11) Kabut hitam menyelimuti benih. 12) Para peri tertidur satu per satu. 13) Kembali ke Fifi bercerita. 14) Close-up wajah Fifi. 15) Tampilkan **tiga pilihan jawaban pemain**. Setelah pilihan: dialog Fifi berubah sesuai pilihan, Fifi mengantuk, naik ke tas pemain, sayap cahaya redup, kamera menjauh, musik malam lembut.

### BAB 7 — HUTAN YANG BERBISIK
**CS21 Bisikan Hutan** — Trigger: pertama masuk zona tengah Whispering Forest. 1) Wide shot hutan lebih lebat. 2) Cahaya matahari menembus pohon. 3) Angin berubah jadi bisikan. 4) Tulisan samar di layar. 5) Fifi tiba-tiba berhenti terbang. 6) Fifi mendengar suara memanggil namanya. 7) Siluet samar para peri. 8) Siluet menghilang. 9) Fifi mengajak lanjut.
**CS22 Slime Disembuhkan** — Trigger: pertama memakai Penawar Kabut pada slime. 1) Fokus slime berkabut. 2) Pemain memakai Penawar Kabut. 3) Botol pecah, cairan bercahaya menyentuh slime. 4) Kabut hitam keluar. 5) Warna slime normal. 6) Slime bergoyang bingung. 7) Fifi tersenyum lega. 8) Slime menjatuhkan Gel Jernih.
**CS23 Pertemuan dengan Kakek Orlo** — Trigger: pertama menemukan mata air tersembunyi. 1) Mata air cahaya biru. 2) Kamera ke pondok kecil. 3) Orlo duduk di samping lentera. 4) Membuka mata saat pemain mendekat. 5) Kamera berganti Orlo, pemain, Fifi. 6) Orlo mengenali Fifi. 7) Fifi terkejut. 8) Orlo memperlihatkan peta tiga altar. 9) Zoom ke peta. 10) Tiga titik altar menyala satu per satu.

### BAB 8 — TIGA ALTAR CAHAYA
**CS24 Penjaga Altar Fajar** — Trigger: mendekati altar pertama. 1) Altar tertutup kabut. 2) Tanah bergetar. 3) **Leaf Slime Elite** muncul dari balik altar. 4) Zoom ke monster. 5) Boss HP bar muncul. 6) Fifi bersiap menyalurkan cahaya. Setelah boss kalah: cutscene pembersihan altar.
**CS25 Penjaga Altar Bulan** — Trigger: mendekati altar kedua. Struktur serupa, dengan hutan lebih gelap, cahaya bulan di antara pohon, **Moss Slime Elite** muncul dari tanah, kabut hijau kehitaman. Setelah altar dibersihkan, cahaya Fifi lebih terang.
**CS26 Penjaga Altar Embun** — Trigger: mendekati altar ketiga. Kabut sangat tebal, Gerbang Cahaya terlihat di belakang altar, **Honey Slime Elite** muncul dengan aura kabut, kamera memperlihatkan ketiga altar yang sudah dibersihkan. Setelah boss kalah, mulai pembersihan terakhir.
**CS27 Gerbang Cahaya Terbuka** (sinematik besar) — Trigger: ketiga altar dibersihkan. 1) Altar ketiga. 2) Fifi melayang ke udara. 3) Sayap bersinar. 4) Cahaya tiga altar mengalir ke Fifi. 5) Fifi menyalurkan cahaya ke Gerbang Cahaya. 6) Simbol kuno muncul di gerbang. 7) Tanah bergetar pelan. 8) Gerbang terbuka dengan gemuruh. 9) Cahaya keemasan menyinari area. 10) Kamera memperlihatkan hutan dalam. 11) Fifi tersenyum, hampir menangis. 12) Orlo berdiri di belakang pemain. Akhiri dengan kamera mengikuti pemain dan Fifi memasuki gerbang.

### BAB 9 — BAYANG DI PASAR
**CS28 Surat dari Aldric** — Trigger: setelah Bab 8 selesai dan pemain menerima panggilan kembali ke desa. 1) Eldoria Village dari kejauhan. 2) Penjaga berlari ke pemain. 3) Menyerahkan surat. 4) Zoom ke segel Guild. 5) Transisi ke Adventurer Guild. 6) Aldric membuka surat bersama pemain. 7) Surat Bersegel V. 8) Aldric serius.
**CS29 Investigasi Kamar 4** — Trigger: membuka Kamar 4. 1) Fokus kunci masuk lubang pintu. 2) Pintu berderit. 3) Kamera masuk kamar. 4) Jaring besar. 5) Kandang kosong. 6) Peta hutan dalam dengan tanda merah. 7) Fifi mendekati peta. 8) Menunjuk lokasi terkait Benih Cahaya. 9) Musik misterius.
**CS30 Konfrontasi Garrick** — Trigger: kumpulkan tiga bukti dan temui Garrick di plaza. 1) Garrick berdagang. 2) Pemain mendekat. 3) Garrick tersenyum ramah. 4) Pemain menunjukkan bukti. 5) Close-up wajah Garrick. 6) Senyum perlahan hilang. 7) Tertawa pelan. 8) Menyebut nama **Lord Veyron**. 9) Melempar bom asap. 10) Layar penuh asap. 11) Dua pilihan pendekatan pemain. Jalur umum dan diam-diam punya transisi berbeda, tapi keduanya menuju peristiwa yang sama di hutan dalam.

### BAB 10 — JANTUNG HUTAN
**CS31 Memasuki Hutan Suci** — Trigger: melewati Gerbang Cahaya setelah Bab 9. 1) Kamera ikuti pemain lewat gerbang. 2) Suasana sangat magis. 3) Pohon tinggi dan kristal kecil. 4) Partikel cahaya. 5) Fifi terbang lebih tinggi dari biasanya. 6) Wajah Fifi penuh harapan. 7) Suara Benih Cahaya samar dari jauh.
**CS32 Pengkhianatan Garrick** (sinematik utama) — Trigger: menemukan padang Benih Cahaya. 1) Wide shot padang luas. 2) Kristal raksasa retak di tengah. 3) Garrick, Brock, Dunn memasukkan serbuk hitam lewat mesin pompa. 4) Close-up mesin pompa. 5) Serbuk mengalir ke retakan. 6) Fifi melihat. 7) Close-up wajah Fifi marah. 8) Fifi terbang maju berteriak menghentikan. 9) Garrick berbalik. 10) Brock dan Dunn mengeluarkan senjata. 11) Benih Cahaya berdenyut keras. 12) Pecahan kristal bergerak. 13) Kamera bergetar. 14) Pecahan menyatu jadi makhluk raksasa. 15) **Raja Kristal** muncul. 16) Brock dan Dunn ketakutan. 17) Garrick memerintahkan mereka menghadapi pemain. 18) Garrick kabur bersama mereka. Boss HP bar muncul.
**CS33 Raja Kristal — Fase Akhir** — Trigger: HP Raja Kristal < 30%. 1) Boss mengeluarkan kabut hitam. 2) Cahaya padang meredup. 3) Fifi jatuh, kesulitan terbang. 4) Fokus sayap Fifi. 5) Fifi melihat Benih Cahaya. 6) Fifi bangkit pelan. 7) Fifi meminta pemain bertahan. 8) Bar Cahaya Fifi muncul. 9) Gameplay lanjut dengan mekanik pengisian cahaya selama **20 detik**.
Saat bar penuh: gameplay berhenti; kamera ke Fifi; Fifi terbang tinggi; sayap bersinar sangat terang; cahaya menyebar ke arena; kabut hitam hilang; Raja Kristal kehilangan keseimbangan; muncul kesempatan serangan terakhir. Setelah boss kalah, lanjut cutscene berikutnya.
**CS34 Benih Cahaya Pulih** (emosional) — Trigger: Raja Kristal dikalahkan. 1) Raja Kristal hancur jadi pecahan kristal bercahaya. 2) Kabut hitam hilang. 3) Benih Cahaya berdenyut. 4) Retakan menutup perlahan. 5) Cahaya menyebar ke akar pohon. 6) Hutan gelap kembali bercahaya. 7) Nyanyian para peri terdengar. 8) Cahaya kecil muncul di antara pohon. 9) Siluet para peri terlihat. 10) Fifi terdiam. 11) Close-up mata Fifi. 12) Fifi tersenyum menahan tangis. 13) Mengucapkan dialog sesuai naskah Bab 10.
Kemudian: kamera menemukan surat Lord Veyron di dekat tas Garrick; pemain mengambil surat; zoom ke tulisan **Moonlit Glade**; Fifi membaca dan mengenali nama tempat; musik berubah misterius; dialog terakhir Fifi tentang perjalanan berikutnya.
**CS35 Kemenangan di Eldoria Village** — Trigger: kembali ke Eldoria Village. 1) Gerbang desa. 2) Penjaga memanggil warga. 3) Warga berkumpul di plaza. 4) Kepala Desa mendekati pemain. 5) Aldric memberi kenaikan **Guild Rank C**. 6) Close-up lencana Rank C. 7) Warga bersorak. 8) Fifi mengitari pemain. 9) Fifi meminta daging seperti biasa. 10) Kamera menjauh memperlihatkan desa merayakan.
**CS36 Penutup Arc I — Bisikan Hutan** — Trigger: semua quest utama Bab 10 selesai dan flag `arc1_done` aktif.
1) Layar perlahan gelap. 2) Tulisan: **FIDORIA / ARC I / BISIKAN HUTAN**. 3) Kilas balik: Fifi pertama bertemu pemain; pemilihan job di Guild; pertemuan rusa putih; Fifi bercerita di Hearthstone Inn; tiga altar menyala; Gerbang Cahaya terbuka; pertarungan Raja Kristal; Benih Cahaya kembali bersinar. 4) Kamera kembali ke Fifi dan pemain menghadap hutan. 5) Fifi melihat ke timur. 6) Angin menggerakkan rambut dan sayapnya. 7) Zoom pelan ke wajah Fifi. 8) Fifi: “Moonlit Glade… tunggu Fifi. Kita akan datang.” 9) Kamera naik ke langit. 10) Tulisan: **ARC I SELESAI — BERSAMBUNG… — ARC II: MOONLIT GLADE, LEVEL 21–40**. 11) Musik penutup. 12) Fade out.
Setelah cutscene, pemain mendapat kontrol di Eldoria Village.

---

## 11. FLAG & QUEST (RINGKAS)
Flag Scene 0: `intro_done`, `rescue_fifi`, `fifi_companion_unlocked`, `village_arrival_done`, `chief_met`.
Quest: `gather_herbs` (unlocked_by `chief_met`).
Flag lain: tiap cutscene punya `completion_flag` sendiri (mis. `cs01_done` … `cs36_done`), plus `arc1_done`. Hadiah/item dari cutscene hanya diberikan sekali, dijaga oleh flag.

## 12. PERSYARATAN KUALITAS
- Cutscene dan gameplay jalan baik di mobile dan desktop.
- Pakai sistem sprite, animasi, tilemap, dan aset Fidoria yang sudah ada; jangan merusak struktur folder atau sistem gameplay.
- Visual tajam (Bagian 1.1), animasi mulus (Bagian 1.2), UI opacity 0–100% (3.1), minimap (3.2), banyak map (3.3).
- Hasil akhir: game RPG petualangan bercerita sinematik, karakter hidup, hubungan emosional {player}–Fifi, dunia yang berkembang tiap cerita maju.

## 13. KEPUTUSAN OWNER (SUDAH DISETUJUI)
1. Konflik pemilihan job diselesaikan: job dipilih di Adventurer Guild (lihat 4.8).
2. Dialog yang sebelumnya kosong (Scene 1A, 2A, pilihan CS10/CS20/CS30, dialog Bab 10) sudah ditulis di Bagian 15 dan boleh dipakai sebagai naskah resmi. Semuanya disimpan di `STORY`, bukan di logika.
3. Obrolan NPC lucu ada di Bagian 16.
4. Tetap wajib: laporkan aset yang tidak ditemukan di repo sebelum memakai placeholder, dan minta persetujuan untuk perubahan arsitektur besar.

---

## 14. URUTAN PENGEMBANGAN (PHASE)
1. **Phase 1:** inspeksi repo, setup proyek, integrasi aset (pilih yang tajam), gerak karakter, map & dunia (multi-map), kamera, collision, minimap dasar, HUD + slider opacity.
2. **Phase 2:** AI monster, combat, auto-aim, item drop, inventory, equipment.
3. **Phase 3:** Story 0, sistem cutscene & quest, progres Novice, pemilihan Permanent Job, empat job, weapon & skill.
4. **Phase 4:** NPC, Blacksmith, NPC Market, Marketplace, ekonomi + pajak 15%.
5. **Phase 5:** Google Auth, Neon Database, persistensi karakter, backend API.
6. **Phase 6:** server multiplayer, WebSocket, map publik, party, chat, combat multiplayer, integrasi NPC/marketplace online.
7. **Phase 7:** audio, polish UI, performa, keamanan, testing penuh.

Jangan mengerjakan semua sekaligus. Jangan anggap fitur selesai hanya karena UI-nya ada: setiap fitur harus punya logic, data, interaksi, penyimpanan, dan testing.


---

## 15. NASKAH DIALOG TAMBAHAN (DISETUJUI OWNER)
Semua teks masuk ke `STORY` dan lewat `processStoryText()`. Nada: Fifi sok kuat tapi gampang panik; komedi dari reaksi, bukan dari Fifi terus-menerus bicara. Di momen emosional (CS11, CS18, CS20, CS27, CS34) komedi dikurangi.

### Bab 1 — Scene 1A (CS01, Toko Nenek Tilda)
- Nenek Tilda: Selamat datang! Aduh, jangan sentuh botol yang biru itu, Nak... eh, Nak Peri.
- Fifi: Fifi tidak menyentuh. Fifi... memeriksa. Secara sopan.
- [Botol bergoyang. Fifi membeku.]
- Nenek Tilda: Itu ramuan penumbuh rambut. Kalau pecah, hidungmu bisa berbulu.
- Fifi: ...Fifi tidak pernah ada di sini. {player}, katakan Fifi tidak pernah ada di sini.
- Nenek Tilda: Hihi. Jadi, {player}, Kepala Desa sudah cerita? Aku butuh sepuluh Green Herb. Tumbuhnya di tepi Whispering Forest, dijaga slime-slime kecil.
- Fifi: Slime? Itu yang lengket dan bergoyang itu? Fifi... akan mengawasi dengan penuh perhatian. Dari jauh.
- Nenek Tilda: Bawa kembali 10 Green Herb, nanti kubuatkan Potion Kecil untukmu.

### Bab 1 — CS03 (Ramuan Pertama)
- Nenek Tilda: Nah, segar-segar semua. Tiga Potion Kecil, gratis untuk anak yang rajin.
- Fifi: Bau rumput. Fifi tidak bilang itu bau enak.
- Nenek Tilda: Memang bukan untuk dicium, Nak Peri. Untuk diminum.
- Fifi: ...Fifi mundur dari percakapan ini.

### Bab 1 — CS04 (Undangan ke Guild)
- Kepala Desa: Terima kasih sudah membantu Nenek Tilda. Ini surat rekomendasi. Temui Commander Aldric di Adventurer Guild. Dunia di luar sana jauh lebih ramai dari yang kalian kira.
- Fifi: Guild? Berisik. Bau keringat. Banyak orang. ...Ada kantinnya?
- Kepala Desa: Ada.
- Fifi: ...Fifi ikut. Demi {player}. Bukan karena kantin.
(Kilau kecil di sayap Fifi saat ia setuju.)

### Bab 2 — Scene 2A (CS05, Guild)
- Commander Aldric: Jadi kamu {player}. Kepala Desa mengirim surat pujian. Jarang sekali beliau begitu.
- Fifi: Fifi juga ikut membantu. Mengawasi. Itu pekerjaan berat.
- Commander Aldric: ...Dan ini, tentu saja, seorang peri. Hutan benar-benar sedang aneh.
- Commander Aldric: Aturannya sederhana: petualang harus punya jalan. Empat guru di sini akan menunjukkan satu per satu. Pilih dengan hati-hati, karena pilihan ini tidak bisa diganti.
- Fifi: Tidak bisa ganti?! Seperti kalau salah pesan makanan?
- Commander Aldric: Lebih serius dari itu.

### Bab 2 — CS06 (reaksi Fifi pada empat guru)
- Aldric/Warrior (setelah Heavy Slash): Fifi: Boneka itu... terbang? Fifi tidak mau jadi boneka itu.
- Luna/Mage (setelah bola cahaya): Fifi: Oke, itu lumayan. Sedikit. Cahayanya kalah sama Fifi, tapi lumayan.
- Lyra/Archer (setelah panah mengenai sasaran): Fifi: Tepat sekali! ...Fifi juga bisa kalau mau. Cuma tidak punya busur.
- Kael/Assassin (setelah Shadow Step): Fifi: AAH! Siapa itu?! Kenapa dia muncul dari ketiadaan?! Itu tidak sopan!
- Kael: Maaf. Kebiasaan.

### Bab 2 — CS07 (Pemilihan Job) — komentar Fifi per job
- Warrior: Fifi: Pedang besar? Hati-hati, {player}. Jangan pakai untuk memotong sayur. ...Fifi akan sangat mendukung itu sih.
- Mage: Fifi: Tongkat sihir? Oke, tapi ingat, Fifi tetap peri paling bersinar di sini.
- Archer: Fifi: Pemanah? Bagus, jaga jarak aman. Dan arahkan panahnya jauh dari Fifi.
- Assassin: Fifi: Pisau kembar dan menghilang... Kamu yakin kamu orang baik? ...Fifi tetap ikut, tapi Fifi mengawasi.
- Konfirmasi: "Pilih {job_name} sebagai Permanent Job? Pilihan ini tidak dapat diganti." [Ya] [Kembali]

### Bab 2 — CS08 (Ujian Pertama Guild)
- Commander Aldric: Tiga Pink Slime, tanpa luka berarti. Selamat, {player}. Kamu resmi Rank F.
- Fifi: Rank F? F itu artinya Fantastis, kan?
- Commander Aldric: ...F artinya pemula.
- Fifi: Fifi memilih percaya F itu Fantastis.

### Bab 3 — CS09 & CS11
CS09:
- Commander Aldric: Slime di tepi Whispering Forest bertambah banyak. Tandai titik merah ini. Bersihkan sebelum petani mengeluh lagi.
- Fifi: ...Fifi tidak suka titik merah itu. (pelan) Rasanya salah.
CS11:
- Commander Aldric: Slime berkabut. Aku belum pernah lihat sebelumnya.
- [Fifi menatap tangannya sendiri. Cahaya sayapnya berkedip.]
- Commander Aldric: Fifi, kalau kamu tahu sesuatu, aku tidak akan memaksamu bercerita. Cerita saja saat kamu siap.
- Fifi: ...Hmph. Fifi tidak menyembunyikan apa-apa. (pelan) Belum.

### Bab 3 — CS10 (Kemunculan Kabut Layu), dua pilihan
- Fifi: {player}, jangan sentuh kabut itu! Jangan!
- Pilihan 1 — "Mundur dulu": Fifi: Bagus. Pelan-pelan. Kabutnya... tidak suka cahaya. Kita harus lapor ke Aldric. (Slime berkabut ditinggalkan, kontrak tetap berlanjut.)
- Pilihan 2 — "Serang slime itu": Fifi: Tunggu, itu bahaya! ...Baiklah, tapi jangan sentuh kabutnya! (Pemain melawan slime berkabut; Fifi menyalurkan cahaya kecil, kabut mundur.)
Kedua pilihan berakhir pada kondisi sama: kabut terlihat, laporan ke Aldric, flag progres cerita sama.

### Bab 4 — CS12 & CS14
CS12:
- Bram: Besi menipis, kayu habis. Aku tidak bisa menempa dengan angan-angan, anak muda.
- Fifi: Rantai itu... kenapa ada kait kecil? Fifi pernah lihat yang mirip. (pelan) Di tempat yang tidak enak.
CS14:
- Bram: Nih. Besi Iron baru, ditempa dengan sabar dan sedikit amarah.
- Fifi: Kenapa mengilap sekali? Fifi iri.
- Bram: Itu karena aku menggosoknya tiga kali.
- Fifi: ...Gosok Fifi juga, dong.

### Bab 5 — CS15–CS17
CS15:
- Orwin: Lapor, Commander! Ada perangkap jaring biru di dekat jalur rusa putih!
- Fifi: Jaring... biru? (Gelisah.) Itu... jaring yang kemarin.
CS16:
- Fifi: {player}, tolong! Cepat! Dia terjebak! Jangan pelan-pelan, pelan-pelan itu menyiksa!
- [Rusa putih berdiri, menyentuhkan kepalanya. Cahaya putih mengelilingi pemain.]
- Fifi: ...Dia berterima kasih padamu. Itu... bagus, {player}. Bagus sekali.
CS17:
- Brock: Hah, anak ingusan dan peri sombong. Mau ikut tertangkap juga?
- Fifi: Sombong?! Fifi cuma percaya diri! Dan kalian pemburu jelek!
- Dunn: Brock, kantong asapnya!
- [Layar tertutup asap hitam.]
- Fifi: (batuk) Uhuk! Sial! Mereka kabur! ...{player}, serbuk itu. Jangan dipegang.

### Bab 6 — CS18–CS20
CS18:
- Nenek Tilda: Ini racun. Dibuat dari tanaman yang dihitamkan. Cahaya hidup yang rusak, dan serbuk ini bisa membuat makhluk magis sakit.
- Fifi: (pelan) Seperti... Hutan Suci.
CS19:
- Bu Marta: Nah, nah, anak-anak, duduk. Malam ini ada sup daging dan roti hangat.
- Fifi: DAGING?! Fifi tidak minta. Fifi cuma... menempatkan diri di dekat panci.
CS20 (Fifi bercerita):
- Fifi: Hutan Suci itu... dulu terang, {player}. Ada Benih Cahaya di tengah. Peri-peri bernyanyi. Lalu kabut itu datang. Mereka tertidur, satu per satu. Fifi... sedang di luar waktu itu. Fifi cuma bisa melihat dari jauh.
Tiga pilihan pemain:
1. "Kamu tidak sendirian." → Fifi: ...Fifi tahu. (pelan) Tapi tetap, terima kasih. Sedikit.
2. "Kita bangunkan mereka bersama." → Fifi: Janji? ...Fifi pegang kata-katamu, {player}.
3. (Diam, menyodorkan roti) → Fifi: ...Itu bukan jawaban. Tapi Fifi terima. (Fifi tersenyum kecil, mengambil roti.)
Setelah pilihan: Fifi: Fifi ngantuk... Jangan bilang siapa-siapa Fifi bicara begini. (Fifi naik ke tas, cahaya sayap redup.)

### Bab 7 — CS21–CS23
CS21:
- [Bisikan samar: "...Fifi... pulang..."]
- Fifi: Itu... suara siapa? (pelan) Jangan dengarkan. Ayo jalan, {player}.
CS22:
- Fifi: Berhasil! Slimenya bersih! Lihat, dia bingung. Lucu sekali. ...Fifi tidak bilang lucu.
CS23:
- Kakek Orlo: Aku kenal cahaya itu. Putri Benih, kamu kembali.
- Fifi: ...Kakek tahu Fifi?
- Kakek Orlo: Aku penjaga mata air ini sejak sebelum kabut. Ini peta tiga altar. Bersihkan semuanya, baru Gerbang Cahaya terbuka.

### Bab 8 — CS24–CS27
- CS24 Fifi: Bersiap, {player}! Fifi akan menyalurkan cahaya kalau kamu butuh. Fifi sudah latihan. Sedikit.
- CS25 Fifi: Gelap sekali. Tapi tidak masalah. Fifi bawa lampu. (menunjuk sayap)
- CS26 Fifi: Tinggal satu. Kita hampir sampai.
- CS27 Fifi: (hampir menangis) Terang... pintunya terbuka... Kakek Orlo, apakah ini benar-benar... Kakek Orlo: Ya, Nak. Pergilah. Fifi: ...Ayo, {player}. Fifi tidak menangis. Itu debu.

### Bab 9 — CS28–CS30
CS28:
- Aldric: Surat Bersegel V muncul lagi. Ada yang mengincar Hutan Suci. Selidiki Hearthstone Inn, Kamar 4.
CS29:
- Fifi: Peta ini... ada tanda merah di Benih Cahaya. Mereka tahu jalannya.
CS30 (Konfrontasi Garrick):
- Garrick: Ah, {player}! Petualang kebanggaan Eldoria! Mau beli apa hari ini?
- [Pemain menunjukkan tiga bukti.]
- Garrick: ...Hehe. Kalian lebih pintar dari dugaanku. Lord Veyron akan senang mendengarnya.
- [Garrick melempar bom asap.]
Pilihan:
1. "Kejar langsung" (jalur umum): Fifi: Sebelah sana! Jangan biarkan dia kabur!
2. "Ikuti diam-diam" (jalur senyap): Fifi: ...Pelan. Fifi akan diam. Fifi bisa diam kalau mau.
Kedua jalur menuju hutan dalam dengan kondisi akhir yang sama.

### Bab 10 — CS31–CS36
CS31: Fifi: Ini... rumah. Fifi sudah lama tidak melihat ini. (pelan) Terangnya... hampir sama.
CS32:
- Fifi: BERHENTI! KALIAN APAKAN BENIH CAHAYA?!
- Garrick: Pergi, Brock, Dunn. Urus mereka. Aku punya urusan lain.
CS33:
- Fifi: {player}... Fifi... masih bisa. Beri Fifi dua puluh detik. Lindungi Fifi.
CS34:
- Fifi: Mereka... bernyanyi. Fifi... Fifi pulang.
- Fifi: Terima kasih, {player}. Bukan sedikit. Terima kasih banyak.
- Fifi: ...Moonlit Glade? Tempat itu... ada hubungannya dengan Benih Cahaya yang lain.
CS35:
- Fifi: Daging, ya? Untuk pahlawan Fifi. ...Eh, maksud Fifi, untuk Fifi.
CS36: sesuai naskah penutup di Bagian 10.

---

## 16. OBROLAN NPC LUCU (AMBIENT)
Dipicu saat pemain dekat NPC (jarak interaksi) atau saat Fifi lewat. Satu NPC punya 3–6 baris acak, tidak diulang berturut-turut. Tidak muncul saat cutscene/dialog penting. Simpan di `STORY.npc_chatter`. Nada ringan, tidak berlebihan.

### Eldoria Village — Warga
- Warga: Kemarin ada peri lewat. Hari ini aku merasa harus merapikan rambutku.
- Warga: Katanya peri bisa terbang tanpa makan. ...Kok yang itu minta daging terus?
- Warga: Nenekku bilang peri itu dongeng. Nenekku akan senang melihat ini. Atau pingsan.
- Warga: Aku mau bilang halo, tapi dia melotot. Jadi aku menyapa semak saja.
- Rio (anak kecil): Kakak peri, sayapmu boleh pinjam? Sehari saja! Aku janji tidak dilipat.
- Rio: Aku sudah tahu jawabannya: mahal. Tapi kalau aku jadi kaya?
- Penjaga Gerbang: Aku sudah jaga gerbang ini dua puluh tahun. Tidak ada yang pernah datang dengan peri. Hari ini kena kejutan.
- Penjaga Gerbang: Peri itu menatapku sinis. Aku merasa harus minta maaf. Tapi kenapa?

### Toko Potion — Nenek Tilda
- Tilda: Kalau botol bergoyang sendiri, itu bukan hantu, itu Fifi.
- Tilda: Dulu aku bisa mengangkat sepuluh kantong herbal. Sekarang sepuluh botol saja pinggangku protes.
- Tilda: Jangan campur ramuan hijau dengan ramuan merah. Kecuali kamu ingin kejutan.
- Tilda: Peri datang ke tokoku? Hari ini harus kucatat di buku harian.

### Adventurer Guild
- Aldric: Surat Rank F sudah numpuk. Katanya zaman sekarang, semua orang ingin jadi pahlawan. Sedikit yang mau bersihkan kandang.
- Aldric: Peri di guildku. Aku harus ubah peraturan: dilarang membawa makhluk magis ke kantin.
- Luna: Mage itu bukan soal sulap. Tapi kalau Fifi mau tepuk tangan, silakan.
- Lyra: Aku bisa memanah apel dari jarak seratus langkah. Lalu Fifi memakannya sebelum jatuh. Bagaimana itu bisa?
- Kael: Aku tidak menghilang. Kalian saja yang tidak memperhatikan.
- Petualang: Aku baru pindah ke Rank D. Aku dapat tepuk tangan dari ibu. Itu cukup.
- Petualang: Tadi ada peri hinggap di topiku. Katanya "bagus." Aku tersanjung. Mungkin.

### Bengkel Bram
- Bram: Besi tidak bisa ditempa dengan angan-angan. Kayu juga tidak bisa dimakan Fifi.
- Bram: Sudah kubilang jangan dekat bara. Kenapa kamu menyentuh api, Nak?!
- Bram: Palu ini lebih tua dari kakekku. Dan lebih keras kepala.

### Hearthstone Inn — Bu Marta
- Bu Marta: Sup hari ini daging. Daging, sayur, lalu daging lagi. Fifi, tolong jangan mengintip panci.
- Bu Marta: Peri makan tiga porsi? Tidak apa-apa. Yang penting piring bersih.
- Bu Marta: Kamar 4 sudah kosong sejak tamu aneh itu. Katanya dia pedagang. Pedagang apa yang bawa jaring besar?

### Whispering Forest — Kakek Orlo
- Orlo: Mata air ini sudah lama menunggu. Seperti aku menunggu kopi.
- Orlo: Kalau kabutnya mendekat, jangan lari. Lari justru memanggilnya.
- Orlo: Fifi tumbuh besar, ya. Dulu seukuran kepalan tanganku. Sekarang... masih.

### Reaksi Fifi terhadap NPC (ambient, cooldown global 45–60 dtk)
- Melewati Tilda: Fifi: Bau campuran. Fifi tidak mau tahu itu apa.
- Melewati Bram: Fifi: Panas! Rambut Fifi bisa keriting!
- Melewati Guild: Fifi: Banyak orang. Banyak bau. Kantinnya mana?
- Melewati Rio: Fifi: Dia melihat sayap Fifi lagi. Jangan menatap.
- Melewati Bu Marta: Fifi: Tolong. Satu sendok saja.

### Catatan Teknis
- Pilih baris acak, hindari mengulang baris yang sama dua kali berturut-turut.
- Gunakan bubble teks kecil di atas NPC (bukan dialog penuh), tidak mengunci pemain.
- Semua teks lewat `processStoryText()`; tidak ada nama pemain hardcode.

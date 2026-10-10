# 🎮 Yuk, Jalankan KuyoMuyo!

Di game ini, kamu menggerakkan karakter untuk menghindari peluru dan mengalahkan dua boss. Ikuti langkah di bawah sampai jendela game terbuka!

Panduan ini untuk laptop **Windows dan Mac**. Pilih langkah yang sesuai dengan laptopmu. Kamu membutuhkan internet saat mengunduh aplikasi dan perlengkapan game. Setelah semuanya terpasang, game bisa dimainkan tanpa internet.

## 1. Kenali alat yang akan kita pakai

| Alat | Kegunaannya |
| --- | --- |
| **Python** | Menjalankan kode game. |
| **Visual Studio Code (VS Code)** | Membuka folder game dan membaca atau mengubah kodenya. |
| **Extension Python** | Menambahkan tombol dan bantuan untuk Python di VS Code. |
| **Pygame Zero dan Pygame** | Membantu game menampilkan gambar dan membaca gerakan mouse. |

Python, VS Code, dan extension-nya dipasang secara terpisah. Kita akan memasangnya satu per satu.

## 2. Pasang Python 🐍

Gunakan **Python 3.13** untuk mengikuti panduan ini. Game sudah diuji dengan Python 3.13.14, Pygame Zero 1.2.1, dan Pygame 2.6.1.

Buka [halaman unduhan Python 3.13.16](https://www.python.org/downloads/release/python-31316/), lalu cari bagian **Files**. Ini versi pembaruan dalam keluarga Python 3.13.

### Kalau kamu memakai Windows

1. Pilih **Windows installer (64-bit)** untuk kebanyakan laptop Windows. Jika laptopmu memakai ARM, minta guru membantu memilih installer yang sesuai.
2. Buka file `.exe` yang selesai diunduh.
3. Centang **Add python.exe to PATH**. Ini membantu laptop menemukan Python.
4. Klik **Install Now**, lalu tunggu sampai selesai.
5. Klik **Close**.

### Kalau kamu memakai Mac

1. Pilih **macOS installer**.
2. Buka file `.pkg` yang selesai diunduh.
3. Ikuti tombol **Continue**, lalu **Install**.
4. Tunggu sampai selesai, lalu klik **Close**.

Jika laptop meminta kata sandi atau izin pemasangan yang tidak kamu miliki, minta bantuan orang tua atau guru.

## 3. Pasang VS Code 💻

Buka [halaman unduhan VS Code](https://code.visualstudio.com/Download).

### Windows

1. Unduh installer untuk Windows. Pilih **User Installer** untuk kebanyakan laptop.
2. Buka file `.exe` yang sudah diunduh.
3. Ikuti petunjuk pemasangan sampai selesai, lalu buka **Visual Studio Code**.

### Mac

1. Unduh versi Mac. Pilihan **Universal** bisa dipakai untuk Mac Intel maupun Apple Silicon.
2. Buka file unduhan. Jika berbentuk `.zip`, klik dua kali untuk mengekstraknya. Jika berbentuk `.dmg`, buka file tersebut.
3. Seret aplikasi **Visual Studio Code** ke folder **Applications**.
4. Buka VS Code dari folder **Applications**.

## 4. Pasang extension Python 🧩

Extension adalah tambahan untuk VS Code.

1. Di sisi kiri VS Code, klik **Extensions**, yaitu ikon beberapa kotak.
2. Pada kolom pencarian, ketik `Python`.
3. Pilih extension **Python** dari penerbit **Microsoft**. Nama identitasnya adalah `ms-python.python`.
4. Klik **Install** dan tunggu sampai selesai.

Untuk langkah dalam panduan ini, cukup pasang extension Python tersebut.

## 5. Siapkan dan buka folder game 📁

1. Dapatkan folder game dari guru. Jika dikirim sebagai ZIP, ekstrak dulu: di Windows gunakan **Extract All**, di Mac klik dua kali file ZIP.
2. Simpan folder hasil ekstrak di tempat yang mudah ditemukan, misalnya **Documents**.
3. Di VS Code, pilih **File → Open Folder…**.
4. Pilih folder yang berisi **`main.py` dan `images`**, lalu buka.
5. Jika muncul pertanyaan kepercayaan folder, pilih **Yes, I trust the authors** untuk folder game yang kamu terima dari guru.

Di sisi kiri VS Code, kamu harus melihat susunan seperti ini. Nama folder terluarnya boleh berbeda.

```text
final-gwen/
├── README.md
├── main.py
└── images/
    ├── geishukuu.png
    ├── background_a.png
    └── ... gambar lainnya
```

**`main.py` adalah kode game. `images` adalah tempat gambar game.** Salin seluruh folder game, termasuk semua gambarnya.

Jika ada folder `venv` dari laptop lain, biarkan saja. Pada langkah berikutnya kita membuat folder baru bernama `.venv` khusus untuk laptopmu.

## 6. Buka terminal ⌨️

Terminal adalah tempat kita mengetik perintah untuk laptop.

1. Pilih menu **Terminal → New Terminal** di VS Code.
2. Panel terminal akan muncul di bagian bawah.
3. Pastikan terminal berada di folder game dengan mengetik:

**Windows:**

```powershell
dir
```

**Mac:**

```bash
ls
```

Tekan **Enter**. Daftar yang muncul harus memuat `main.py` dan `images`. Jika belum, ulangi langkah **Open Folder**, lalu tutup terminal lama dengan ikon tempat sampah dan buka terminal baru.

**Cara mengikuti perintah:** salin satu baris, tempel di terminal, tekan **Enter**, lalu tunggu sampai selesai sebelum melanjutkan. Salin hanya isi kotaknya, bukan tulisan `Windows` atau `Mac`.

## 7. Siapkan perlengkapan game 🛠️

Folder `.venv` seperti kotak perlengkapan khusus game ini. Kita memasukkan Pygame Zero dan Pygame ke dalam kotak tersebut.

### Windows

Cek Python terlebih dahulu:

```powershell
py -3.13 --version
```

Jika muncul `Python 3.13.x` (misalnya `Python 3.13.16`), lanjutkan. Jalankan **satu baris setiap kali**:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install pgzero==1.2.1 pygame==2.6.1
```

### Mac

Cek Python terlebih dahulu:

```bash
python3.13 --version
```

Jika muncul `Python 3.13.x`, lanjutkan. Jalankan **satu baris setiap kali**:

```bash
python3.13 -m venv .venv
./.venv/bin/python -m pip install --upgrade pip
./.venv/bin/python -m pip install pgzero==1.2.1 pygame==2.6.1
```

Saat memasang perlengkapan, pastikan internet tersambung. Tunggu sampai terminal selesai dan kamu bisa mengetik lagi. Biasanya ada tulisan **Successfully installed**. Jika ada tulisan **Requirement already satisfied**, berarti perlengkapan itu sudah terpasang.

Perintah di atas langsung memakai Python di dalam `.venv`, jadi kamu tidak perlu mengetik perintah aktivasi tambahan. Penjelasannya ada di [panduan resmi lingkungan Python](https://docs.python.org/3.13/library/venv.html).

## 8. Pilih Python untuk VS Code

Supaya tombol menjalankan game memakai kotak perlengkapan yang benar:

1. Tekan **Ctrl + Shift + P** di Windows, atau **Command + Shift + P** di Mac.
2. Ketik `Python: Select Interpreter`, lalu pilih perintah tersebut.
3. Pilih Python yang memiliki tulisan **`.venv`** dari folder game ini.
4. Jika belum terlihat, pilih **Enter interpreter path… → Find…**, lalu pilih file berikut di folder game:

| Laptop | File yang dipilih |
| --- | --- |
| Windows | `.venv\Scripts\python.exe` |
| Mac | `.venv/bin/python` |

Di Mac, jika folder `.venv` tidak terlihat pada jendela pemilihan file, tekan **Command + Shift + .** (titik) untuk menampilkan folder tersembunyi.

## 9. Jalankan game! 🚀

Di terminal yang masih berada di folder game, jalankan perintah sesuai laptopmu.

**Windows:**

```powershell
.\.venv\Scripts\python.exe main.py
```

**Mac:**

```bash
./.venv/bin/python main.py
```

Jendela berjudul **KuyoMuyo: Bullet Hell Project** akan terbuka. Kamu berhasil jika karakter, background, dan boss muncul!

Kamu juga bisa membuka `main.py`, klik kanan pada kodenya, lalu pilih **Run Python → Run Python File in Terminal** setelah menyelesaikan langkah 8. Langkah memilih Python dan menjalankan file mengikuti [panduan Python dari VS Code](https://code.visualstudio.com/docs/python/python-tutorial).

## 10. Cara bermain 🕹️

| Aksi | Caranya |
| --- | --- |
| Menggerakkan karakter | Gerakkan mouse atau jari di trackpad di dalam jendela game. |
| Menembak | Otomatis saat melawan boss. |
| Menggunakan bom | Tekan **E**. Kamu punya 3 bom untuk setiap permainan. |
| Mengalahkan boss | Hindari peluru dan tembak boss sampai HP-nya habis. |
| Bermain lagi | Klik di jendela saat muncul **GAME OVER** atau **STAGE CLEAR!**. |
| Menutup game | Klik tombol tutup jendela. |

Klik jendela game terlebih dahulu agar tombol **E** bisa diterima oleh game.

## Kalau ingin bermain lagi besok

Kamu cukup membuka folder game di VS Code, membuka terminal, lalu menjalankan perintah pada **langkah 9**. Pemasangan aplikasi dan perlengkapan cukup dilakukan sekali untuk folder game tersebut di laptopmu.

## Kalau muncul error, coba ini 🔍

### `py` atau `python3.13` tidak ditemukan

Tutup VS Code lalu buka kembali. Jika masih gagal, cek pemasangan Python pada langkah 2. Di Windows, pastikan pilihan **Add python.exe to PATH** dicentang saat memasang Python. Jika tertulis Python 3.13 belum terpasang, pasang versi 3.13 yang ada di tautan panduan ini.

### `No module named pgzrun`, `pgzero`, atau `pygame`

Ulangi perintah pemasangan pada langkah 7. Lalu jalankan game dengan perintah pada langkah 9. Jika memakai tombol VS Code, pastikan Python yang dipilih berasal dari `.venv` pada langkah 8.

### `can't open file ... main.py` atau `.venv` tidak ditemukan

Periksa folder terminal dengan `dir` di Windows atau `ls` di Mac. Buka folder yang berisi `main.py` melalui **File → Open Folder…**. Jika `.venv` belum dibuat, kerjakan langkah 7.

### `No 'images' directory found` atau gambar tidak ditemukan

Pastikan folder `images` berada di sebelah `main.py` dan berisi seluruh gambar dari guru. Nama gambar harus sama dengan yang diminta kode, termasuk huruf kecil dan tanda garis bawah. Jika ada gambar yang hilang, salin kembali dari folder game asli.

### `Actor is not defined` atau `schedule_interval is not defined`

Pastikan kamu memakai `main.py` terbaru dari proyek ini. File ini sudah mengaktifkan Pygame Zero melalui `import pgzrun` dan `pgzrun.go()`, serta memakai `clock.schedule_interval(...)` untuk timer. Minta guru membantu mengecek jika file milikmu berbeda.

### Windows menampilkan `running scripts is disabled`

Ini bisa muncul saat VS Code mencoba mengaktifkan `.venv` secara otomatis. Jalankan game dengan perintah lengkap **Windows pada langkah 9**, yang langsung memanggil `python.exe`.

### Bom tidak keluar

Klik jendela game, lalu tekan **E** saat melawan boss. Cek jumlah bom di sebelah ikon bintang: jika sudah `0`, mulai permainan baru untuk mendapatkan bom lagi.

### Masih belum berhasil?

Salin pesan error lengkap dari terminal atau ambil screenshot, lalu tunjukkan kepada guru. Sertakan apakah kamu memakai Windows atau Mac dan langkah terakhir yang kamu lakukan.

Selamat bermain dan belajar membuat game! 🌟

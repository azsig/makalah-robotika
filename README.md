# Template UAS Intelligent Systems and Robotics (ISR) - Modular LaTeX

Repository ini berisi template pengerjaan Tugas Akhir / UAS mata kuliah **Intelligent Systems and Robotics (ISR)**. Struktur direktori didesain secara modular agar memudahkan kolaborasi kelompok.

---

## 📂 Struktur Folder Proyek

```text
makalah2/
├── main.tex                 # File utama untuk makalah (paper)
├── references.bib           # Database sitasi / daftar pustaka (BibLaTeX)
├── README.md                # Petunjuk penggunaan ini
├── config/                  # Pengaturan LaTeX
│   ├── metadata.tex         # Informasi kelompok (Nama, NIM, Dosen, Judul)
│   └── preamble.tex         # Import package, margin halaman, style koding
├── sections/                # Isi Bab Makalah (Modular)
│   ├── 01-pendahuluan.tex
│   ├── 02-tinjauan-pustaka.tex
│   ├── 03-perancangan-sistem.tex
│   ├── 04-pengujian-hasil.tex
│   └── 05-kesimpulan-saran.tex
├── slides/                  # Folder presentasi
│   └── slides.tex           # File utama Beamer (slide presentasi .pdf)
├── figures/                 # Folder penyimpanan foto robot, logo kampus, diagram
├── data/                    # Folder penyimpanan data hasil pengujian (.csv, dll)
└── koding/                  # Folder penyimpanan source code robot (.ino, .py, .cpp)
```

---

## 🚀 Cara Penggunaan & Kompilasi

### Option 1: Menggunakan Overleaf (Sangat Direkomendasikan)
1. Buat proyek baru (*Blank Project*) di [Overleaf](https://www.overleaf.com/).
2. Unggah (*Upload*) seluruh folder/file dari repository ini.
3. Pastikan **Compiler** di menu Overleaf diatur ke **pdfLaTeX** (default).
4. Klik **Recompile** pada `main.tex` untuk membuat file Makalah PDF, atau pada `slides/slides.tex` untuk membuat file Presentasi PDF.

### Option 2: Menggunakan Compiler Lokal (TeX Live / MiKTeX)
Gunakan perintah berikut di terminal Anda untuk mengompilasi file LaTeX secara lokal:
```bash
# Kompilasi Makalah Utama
pdflatex main.tex
biber main
pdflatex main.tex
pdflatex main.tex

# Kompilasi Slide Presentasi
cd slides
pdflatex slides.tex
```

---

## 🎓 Cara Mengubah Data Kelompok Anda
Buka file [config/metadata.tex](file:///home/azsig/Documents/Robotika/makalah2/config/metadata.tex) dan ubah data berikut sesuai dengan identitas kelompok Anda:
*   `\JudulMakalah`: Judul penelitian/proyek robotika Anda.
*   `\DosenPengampu`: Nama dosen pembimbing kuliah ISR.
*   `\AnggotaSatu` s.d. `\AnggotaEmpat` beserta `\NIMSatu` s.d. `\NIMEmpat`: Nama & NIM semua anggota kelompok.

---

## 📥 Persyaratan Pengumpulan UAS
Sesuai dengan instruksi, pastikan dokumen lengkap berikut dikumpulkan dalam satu zip/folder terorganisir:
1.  **Makalah**:
    *   Format `.pdf` (Hasil compile dari `main.tex`).
    *   Format `.docx` (Bisa dikonversi dari PDF atau ditulis manual menggunakan Microsoft Word dengan mengikuti struktur bab yang sama).
2.  **Slide**:
    *   Format `.pdf` (Hasil compile dari `slides/slides.tex`).
    *   Format `.ppt` / `.pptx` (Presentasi PowerPoint).
3.  **Folder Tambahan**:
    *   Folder berisi dokumentasi foto-foto robot nyata (`figures/`).
    *   Folder berisi tabel/file data pengujian (`data/`).
    *   Folder berisi kodingan/program robot (`koding/`).

*Selamat Mengerjakan dan Semoga Sukses UAS ISR!* 🤖🚀

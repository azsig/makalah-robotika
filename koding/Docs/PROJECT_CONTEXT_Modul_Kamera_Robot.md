# Project Context
# Modul Visi, Estimasi Jarak, dan Monitoring pada Robot Navigasi Otonom

**Nama Proyek:** Robot Navigasi Otonom Berbasis Deteksi Warna dan Penghindaran Rintangan  
**Dokumen:** Project Context  
**Versi:** 1.0  
**Tanggal:** 28 Mei 2026

---

## 1. Gambaran Umum Proyek

Proyek ini bertujuan membangun sebuah robot navigasi otonom yang dapat bergerak di arena, mendeteksi objek berdasarkan warna, mengenali area Finish sebagai target utama, serta membedakan obstacle dan objek pengecoh di sekitarnya. Robot tidak hanya dituntut untuk bergerak, tetapi juga harus mampu menunjukkan proses pengambilan keputusannya secara visual agar dapat diverifikasi selama pengujian maupun presentasi.

Dalam keseluruhan sistem robot, modul yang dibahas dalam dokumen ini adalah **Modul Visi, Estimasi Jarak, dan Monitoring**. Modul ini menjadi “mata” robot sekaligus “jendela observasi” bagi operator. Artinya, modul ini bukan hanya bertugas melihat objek, tetapi juga menerjemahkan apa yang dilihat robot menjadi informasi yang bisa dipahami manusia melalui browser.

---

## 2. Masalah yang Ingin Diselesaikan

Robot yang hanya bergerak tanpa penjelasan visual sulit diverifikasi. Dalam proyek seperti ini, dosen, tim, atau operator perlu melihat bahwa robot benar-benar:

- sedang mencari objek target,
- dapat membedakan target dan obstacle,
- memahami posisi objek terhadap kamera,
- dan mengestimasi jarak objek secara logis.

Masalah lainnya adalah kondisi pengujian yang tidak selalu tetap. Warna target bisa berubah, pencahayaan arena dapat berbeda, dan posisi objek tidak selalu ideal. Karena itu, sistem tidak boleh bersifat kaku. Modul harus mendukung kalibrasi ulang secara fleksibel tanpa perlu mengubah kode program setiap kali kondisi arena berubah.

---

## 3. Peran Modul dalam Sistem Robot

Modul ini memiliki fungsi sentral dalam keseluruhan sistem robot. Perannya dapat dijelaskan sebagai berikut:

1. Menjadi sumber informasi visual utama dari kamera robot.
2. Mendeteksi objek-objek yang terlihat di arena.
3. Memberi bounding box pada objek agar proses deteksi terlihat jelas.
4. Mengklasifikasikan objek menjadi target, obstacle, atau unknown.
5. Mengestimasi jarak objek terhadap kamera.
6. Menyediakan stream visual real-time melalui browser.
7. Menjadi titik kalibrasi runtime untuk warna target dan parameter jarak.
8. Menyediakan output data yang nantinya dibaca oleh modul navigasi.

Dengan kata lain, modul ini berada di antara “dunia nyata” yang ditangkap kamera dan “keputusan robot” yang dilakukan modul navigasi.

---

## 4. Sumber Visual Sistem

Satu keputusan penting dalam desain sistem ini adalah bahwa **seluruh citra yang diproses hanya berasal dari kamera robot**. Browser yang dibuka melalui HP atau laptop operator tidak berfungsi sebagai sumber kamera, melainkan hanya sebagai antarmuka untuk melihat hasil pemrosesan dan mengirim input kalibrasi.

Ini berarti:

- gambar yang diproses selalu diambil dari webcam USB pada robot,
- bounding box selalu dihitung dari frame kamera robot,
- kalibrasi warna target selalu mengambil sampel dari frame kamera robot,
- kalibrasi jarak juga dilakukan terhadap objek yang terlihat pada frame kamera robot saat itu.

Keputusan ini penting agar arsitektur sistem tetap konsisten dan tidak membingungkan saat implementasi.

---

## 5. Lingkungan Operasional

Modul ini dirancang untuk bekerja pada konteks arena robot skala kecil hingga menengah, seperti arena praktikum, tugas besar, atau kompetisi sederhana. Karakteristik lingkungannya antara lain:

- Arena berada pada lingkungan indoor atau semi-kontrol.
- Terdapat target visual berupa area atau objek dengan warna tertentu.
- Terdapat obstacle atau pengecoh yang juga mungkin terlihat oleh kamera.
- Pencahayaan dapat berubah, meskipun tidak ekstrem.
- Kamera robot dipasang pada posisi tetap di bodi robot.

Dalam lingkungan seperti ini, sistem harus cukup adaptif terhadap perubahan warna dan posisi objek, namun tetap ringan agar bisa berjalan di Raspberry Pi.

---

## 6. Profil Pengguna Sistem

### 6.1 Operator pengujian

Operator adalah orang yang membuka browser untuk melihat output sistem secara real-time. Operator juga bertanggung jawab melakukan kalibrasi awal sebelum robot dijalankan atau melakukan kalibrasi ulang jika kondisi arena berubah.

### 6.2 Tim pengembang

Tim pengembang menggunakan modul ini sebagai subsistem yang menyediakan data visual untuk kebutuhan navigasi. Tim perlu memahami format output, logika kerja, dan keterbatasan modul agar integrasi berjalan lancar.

### 6.3 Dosen / pembimbing

Dosen atau pembimbing melihat dokumen ini sebagai penjelasan naratif atas sistem yang dibangun. Karena itu, penjelasan dalam file konteks harus cukup deskriptif dan dapat dipahami tanpa harus melihat kode program terlebih dahulu.

---

## 7. Masalah Teknis Utama yang Dipecahkan Modul

Ada empat masalah teknis utama yang secara khusus ditangani modul ini.

### 7.1 Deteksi target visual

Sistem harus mengetahui objek mana yang menjadi target utama berdasarkan warna yang sudah dikalibrasi. Karena target bisa berubah, warna target tidak boleh dikunci permanen dalam kode.

### 7.2 Deteksi multi-objek

Sistem tidak hanya mendeteksi target, tetapi juga object lain di arena. Ini penting karena target dapat tertutup oleh obstacle dan karena navigasi membutuhkan konteks lingkungan, bukan hanya keberadaan target.

### 7.3 Visual verification

Sistem harus menunjukkan bounding box dan label pada setiap objek terdeteksi. Bounding box berfungsi sebagai bukti visual bahwa sistem benar-benar mencari objek tertentu, bukan sekadar melakukan pengambilan keputusan tersembunyi.

### 7.4 Estimasi jarak

Sistem harus mengestimasi jarak antara objek dan kamera. Pendekatan yang disepakati adalah menggunakan metode berbasis kamera tunggal (monocular) melalui parameter bounding box dan kalibrasi jarak awal.

---

## 8. Keputusan Desain yang Sudah Disepakati

Beberapa keputusan penting yang sudah disepakati dan menjadi landasan pengembangan modul ini adalah sebagai berikut.

### 8.1 Kamera robot sebagai satu-satunya sumber citra

Semua proses computer vision bekerja hanya pada frame yang berasal dari webcam robot.

### 8.2 HSV sebagai dasar deteksi warna

Ruang warna HSV dipilih karena lebih cocok untuk pemisahan warna target dibandingkan BGR/RGB biasa, terutama ketika pencahayaan sedikit berubah.

### 8.3 Bounding box wajib ditampilkan

Setiap objek valid yang terdeteksi harus memiliki bounding box. Ini merupakan tuntutan teknis sekaligus kebutuhan presentasi.

### 8.4 Kalibrasi target dilakukan dari browser

Warna target tidak dipilih dari daftar preset, tetapi diambil dari objek yang terlihat oleh kamera robot saat operator melakukan sampling melalui browser.

### 8.5 Kalibrasi jarak dilakukan saat runtime

Operator harus dapat memasukkan parameter ukuran nyata objek dan jarak referensi melalui browser, lalu sistem menghitung parameter jarak tanpa harus mengubah kode atau merestart program.

### 8.6 Browser sebagai panel kontrol dan monitoring

Browser digunakan untuk menampilkan live stream, status sistem, dan panel kalibrasi. Browser bukan sumber kamera tambahan.

---

## 9. Alasan Pemilihan Pendekatan Jarak

Estimasi jarak pada sistem ini tidak menggunakan stereo camera atau depth sensor khusus. Sebagai gantinya, dipilih pendekatan yang lebih realistis untuk platform Raspberry Pi, yaitu estimasi jarak berbasis ukuran bounding box dari objek yang dideteksi kamera.

Pendekatan ini dipilih karena:

- tidak memerlukan hardware kamera stereo,
- lebih ringan untuk Raspberry Pi,
- dapat diterapkan dengan objek target yang ukurannya diketahui,
- dan tetap cukup relevan untuk kebutuhan tugas besar atau pengujian robot skala mahasiswa.

Pendekatan ini memang memiliki keterbatasan, tetapi dengan kalibrasi awal yang benar, sistem masih dapat memberikan estimasi jarak yang berguna untuk kebutuhan navigasi dan observasi.

---

## 10. Hubungan Modul dengan Browser

Browser dalam sistem ini bukan sekadar tampilan pasif. Browser berfungsi sebagai antarmuka dua arah:

- Dari robot ke browser: sistem mengirim live stream hasil anotasi, status runtime, dan informasi objek.
- Dari browser ke robot: operator mengirim perintah kalibrasi warna, input ukuran objek, dan input jarak referensi.

Interaksi ini membuat browser menjadi dashboard operasional untuk sistem visi robot.

---

## 11. Hubungan Modul dengan Navigasi

Modul visi tidak mengendalikan motor secara langsung. Namun, modul ini menghasilkan data yang sangat penting untuk navigasi, yaitu:

- label objek,
- posisi centroid,
- ukuran bounding box,
- estimasi jarak objek,
- dan status target aktif.

Modul navigasi dapat menggunakan data tersebut untuk menentukan arah gerak, prioritas objek, atau kebutuhan menghindari rintangan. Karena itu, format output modul visi harus jelas, stabil, dan mudah diintegrasikan.

---

## 12. Asumsi dan Batasan Penting

Agar implementasi tidak melenceng, berikut asumsi dan batasan utama yang harus selalu diingat:

### Asumsi

- Objek target dapat dilihat oleh kamera setidaknya pada fase kalibrasi.
- Ukuran nyata objek target dapat diketahui saat proses kalibrasi jarak.
- Kamera robot dipasang pada posisi yang tetap selama pengujian.
- Operator bisa mengakses IP Raspberry Pi melalui jaringan lokal.

### Batasan

- Akurasi estimasi jarak bergantung pada kualitas kalibrasi awal.
- Perubahan sudut objek yang terlalu ekstrem dapat memengaruhi ukuran bounding box.
- Pencahayaan yang berubah drastis dapat memengaruhi hasil deteksi warna.
- Jika objek terlalu kecil atau terlalu jauh, deteksi bisa menjadi tidak stabil.

---

## 13. Gambaran Hasil Akhir yang Diharapkan

Pada akhir pengembangan, modul ini diharapkan mampu memberikan pengalaman sebagai berikut:

1. Robot dinyalakan dan kamera aktif.
2. Operator membuka browser melalui alamat IP Raspberry Pi.
3. Browser menampilkan live stream dari kamera robot.
4. Sistem mendeteksi objek target dan obstacle, lalu memberi bounding box.
5. Operator dapat melakukan kalibrasi warna target langsung dari browser.
6. Operator dapat melakukan kalibrasi jarak langsung dari browser.
7. Sistem menampilkan label objek dan jarak estimasi pada stream.
8. Modul navigasi menerima data objek dari modul visi.

Jika seluruh alur ini berjalan lancar, maka modul dianggap telah menjalankan perannya secara utuh.

---

## 14. Fungsi Dokumen Ini terhadap PRD

Dokumen konteks ini bukan pengganti PRD. Dokumen ini berfungsi sebagai pendamping PRD agar setiap orang yang membaca spesifikasi teknis juga memahami konteks besar sistem, alasan keputusan desain, asumsi utama, dan arah implementasi.

Singkatnya:

- **PRD** menjelaskan apa yang harus dibangun secara terstruktur.
- **Project Context** menjelaskan makna, tujuan, dan konteks sistem secara deskriptif.

Keduanya harus dibaca bersama agar pengerjaan berjalan lebih lancar dan tidak kehilangan arah.

---

## 15. Penutup

Modul Visi, Estimasi Jarak, dan Monitoring merupakan subsistem penting yang menjembatani penglihatan robot dengan kebutuhan operasional manusia dan modul navigasi. Dengan adanya dokumen konteks ini, pengembangan modul tidak hanya berlandaskan daftar requirement, tetapi juga pemahaman menyeluruh tentang mengapa sistem dirancang seperti ini, bagaimana ia akan digunakan, dan apa batasan yang harus dihormati selama implementasi.

Dokumen ini diharapkan menjadi pegangan awal sebelum masuk ke tahap implementasi teknis, integrasi sistem, dan pengujian lapangan.

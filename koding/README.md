# Robot Navigasi Otonom (Vision + PID + Ultrasonic) 🤖🚀

Sistem navigasi otonom terpadu yang menggabungkan persepsi visual (OpenCV), kendali logika (PID), sensor jarak (Ultrasonik), dan kendali motor DC. Robot dirancang untuk mengejar target warna dan menghindari rintangan secara cerdas.

## 🌟 Fitur Utama

*   **Integrated Multiprocessing:** Server Visi (Flask) dan Logika Navigasi berjalan secara paralel dan berbagi data secara real-time.
*   **PID Steering Control:** Navigasi halus dengan kontrol Proportional-Integral-Derivative.
*   **Dual-Calibration Web GUI:** Kalibrasi warna target, jarak kamera, dan sensor ultrasonik langsung melalui browser.
*   **Hardware PWM Support:** Menggunakan pin PWM hardware Raspberry Pi untuk kendali motor yang sangat halus.
*   **Adaptive Avoidance:** Menghindar rintangan secara halus dengan pergeseran setpoint PID.

## 📂 Struktur Proyek

```text
.
├── main_app.py                 # ENTRY POINT Utama
├── robot_vision_module/        # Modul Persepsi Visual
│   ├── app.py                  # API & Web Server
│   ├── camera_manager.py       # Driver Kamera (Threading)
│   ├── image_processor.py      # HSV Masking & Noise Reduction
│   └── ...
├── robot_navigation_module/    # Modul Kendali & Hardware
│   ├── navigator.py            # State Machine & Logika PID
│   ├── motor_manager.py        # Driver Motor (L298N)
│   ├── ultrasonic_manager.py   # Driver HC-SR04
│   └── ...
├── faktor_koreksi.txt          # Data kalibrasi Ultrasonik (Auto-save)
└── Docs/                       # Dokumen PRD & Konteks
```

## 🛠️ Konfigurasi Hardware (Pinout BCM)

### 1. Motor Driver (L298N/L293D)
| Komponen | Pin GPIO | Fungsi |
|----------|----------|--------|
| **ENA**  | 19 (PWM) | Kecepatan Motor Kiri |
| **IN1**  | 13       | Arah 1 Motor Kiri |
| **IN2**  | 26       | Arah 2 Motor Kiri |
| **ENB**  | 12 (PWM) | Kecepatan Motor Kanan |
| **IN3**  | 16       | Arah 1 Motor Kanan |
| **IN4**  | 20       | Arah 2 Motor Kanan |

### 2. Sensor Ultrasonik (HC-SR04)
| Komponen | Pin GPIO | Fungsi |
|----------|----------|--------|
| **Trigger** | 17     | Signal Trigger |
| **Echo**    | 27     | Signal Echo |

## 🚀 Cara Menjalankan

1.  Pastikan semua hardware terhubung sesuai pinout di atas.
2.  Jalankan aplikasi utama:
    ```bash
    python main_app.py
    ```
3.  Buka browser di `http://[IP_RASPBERRY_PI]:5000`.

## 🎯 Panduan Kalibrasi di Web GUI

### A. Kalibrasi Target (Visi)
1.  Klik tepat pada warna benda di layar video untuk menjadikannya **TARGET** (Mode Tracking Aktif).
2.  Input jarak aktual benda ke kamera (cm) lalu klik **Set Jarak Kamera**.

### B. Kalibrasi Sensor Ultrasonik
1.  Letakkan robot di depan tembok pada jarak tetap (misal 20 cm).
2.  Lihat "Pembacaan Mentah" pada panel biru di Web GUI.
3.  Masukkan angka "20" pada kotak input, lalu klik **Kalibrasi HC-SR04**.
4.  Sistem akan menyimpan faktor koreksi dan memperbarui navigasi secara instan.

## ⚙️ Tuning PID

Edit file `robot_navigation_module/navigator.py` untuk menyesuaikan performa gerak:
*   `Kp` (0.5): Mengatur agresivitas belokan.
*   `Ki` (0.01): Mengatur koreksi error akumulatif.
*   `Kd` (0.2): Meredam sentakan agar robot tidak berayun berlebihan.

---
*Dikembangkan untuk Tugas Besar Instrumentasi Sistem Robotika.*

import RPi.GPIO as GPIO
import time
import os

# Konfigurasi Pin GPIO
PIN_TRIGGER = 17
PIN_ECHO = 27

# Nama file untuk menyimpan nilai kalibrasi
FILE_KALIBRASI = "faktor_koreksi.txt"

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_TRIGGER, GPIO.OUT)
GPIO.setup(PIN_ECHO, GPIO.IN)
GPIO.output(PIN_TRIGGER, GPIO.LOW)

def ukur_jarak_mentah():
    """Mengambil rata-rata dari 5 pembacaan mentah agar data lebih stabil"""
    total_jarak = 0
    pembacaan_valid = 0
    
    for _ in range(5):
        GPIO.output(PIN_TRIGGER, GPIO.HIGH)
        time.sleep(0.00001) # 10 mikrodetik
        GPIO.output(PIN_TRIGGER, GPIO.LOW)

        waktu_mulai = time.time()
        waktu_selesai = time.time()
        timeout = time.time() + 0.5

        while GPIO.input(PIN_ECHO) == 0:
            waktu_mulai = time.time()
            if waktu_mulai > timeout:
                break

        while GPIO.input(PIN_ECHO) == 1:
            waktu_selesai = time.time()
            if waktu_selesai > timeout:
                break

        durasi = waktu_selesai - waktu_mulai
        jarak = (durasi * 34300) / 2
        
        if 2 <= jarak <= 400:
            total_jarak += jarak
            pembacaan_valid += 1
        
        time.sleep(0.05)
        
    if pembacaan_valid > 0:
        return total_jarak / pembacaan_valid
    return None

def simpan_faktor_koreksi(nilai):
    """Menyimpan faktor koreksi ke dalam file txt"""
    with open(FILE_KALIBRASI, "w") as f:
        f.write(str(nilai))
    print(f"[INFO] Faktor koreksi {nilai:.4f} berhasil disimpan ke {FILE_KALIBRASI}")

def baca_faktor_koreksi():
    """Membaca faktor koreksi dari file txt, jika tidak ada return 1.0 (default)"""
    if os.path.exists(FILE_KALIBRASI):
        try:
            with open(FILE_KALIBRASI, "r") as f:
                nilai = float(f.read().strip())
                return nilai
        except ValueError:
            print("[MODUL] File kalibrasi rusak, menggunakan nilai default (1.0).")
            return 1.0
    else:
        return None

def jalankan_kalibrasi():
    """Prosedur interaktif untuk kalibrasi"""
    print("\n=== MEMULAI PROSES KALIBRASI ===")
    print("1. Tempatkan benda/halangan datar di depan sensor.")
    print("2. Ukur jarak fisik dari sensor ke benda menggunakan penggaris.")
    print("------------------------------------------------------------")
    input("Tekan ENTER jika Anda sudah siap untuk mengukur...")
    
    print("Mengukur jarak mentah... Mohon jangan gerakkan benda.")
    jarak_sensor = ukur_jarak_mentah()
    
    if jarak_sensor is None:
        print("Error: Sensor tidak merespons. Kalibrasi gagal.")
        return 1.0
    
    print(f"-> Jarak terbaca sensor (mentah): {jarak_sensor:.2f} cm")
    
    while True:
        try:
            jarak_nyata = float(input("-> Masukkan jarak sesungguhnya dari penggaris (cm): "))
            if jarak_nyata <= 0:
                print("Jarak harus lebih besar dari 0.")
                continue
            break
        except ValueError:
            print("Input tidak valid. Masukkan angka saja.")

    faktor_koreksi = jarak_nyata / jarak_sensor
    simpan_faktor_koreksi(faktor_koreksi)
    return faktor_koreksi

# --- PROGRAM UTAMA ---
try:
    print("Mengecek file kalibrasi...")
    faktor_koreksi = baca_faktor_koreksi()

    if faktor_koreksi is None:
        print("[!] File kalibrasi tidak ditemukan.")
        faktor_koreksi = jalankan_kalibrasi()
    else:
        print(f"[OK] Ditemukan file kalibrasi lama dengan Faktor Koreksi: {faktor_koreksi:.4f}")
        pilihan = input("Apakah Anda ingin melakukan kalibrasi ulang? (y/n): ").lower()
        if pilihan == 'y':
            faktor_koreksi = jalankan_kalibrasi()

    print(f"\n[INFO] Menggunakan Faktor Koreksi: {faktor_koreksi:.4f}")
    print("Mulai membaca data sensor akurat... (Tekan Ctrl+C untuk berhenti)\n")
    time.sleep(1)

    while True:
        jarak_mentah = ukur_jarak_mentah()
        
        if jarak_mentah is not None:
            # Implementasi faktor koreksi langsung dalam kode
            jarak_akurat = jarak_mentah * faktor_koreksi
            print(f"Jarak Terkoreksi: {jarak_akurat:.2f} cm  (Mentah: {jarak_mentah:.2f} cm)")
        else:
            print("Error: Gagal membaca sensor.")
            
        time.sleep(1)

except KeyboardInterrupt:
    print("\nProgram dihentikan oleh pengguna.")
finally:
    GPIO.cleanup()
    print("GPIO Cleanup selesai.")
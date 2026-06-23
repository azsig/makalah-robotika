import RPi.GPIO as GPIO
import time
import sys

# Konfigurasi Pin BCM (Samakan dengan program utama)
TRIGGER_PIN = 17
ECHO_PIN = 27

def test_sensor():
    print("=== TEST HARDWARE HC-SR04 ===")
    print(f"Trigger Pin: BCM {TRIGGER_PIN}")
    print(f"Echo Pin: BCM {ECHO_PIN}")
    
    # 1. Inisialisasi GPIO
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(TRIGGER_PIN, GPIO.OUT)
        GPIO.setup(ECHO_PIN, GPIO.IN)
        GPIO.output(TRIGGER_PIN, GPIO.LOW)
        print("[1] GPIO Setup: BERHASIL")
    except Exception as e:
        print(f"[1] GPIO Setup: GAGAL ({e})")
        return

    # Jeda sejenak agar sensor stabil
    time.sleep(1)

    print("\n--- Memulai Tes Pembacaan (10 Kali) ---")
    for i in range(1, 11):
        print(f"\nPembacaan ke-{i}:")
        
        # Cek kondisi awal Echo Pin (Harus LOW sebelum Trigger dikirim)
        echo_awal = GPIO.input(ECHO_PIN)
        print(f"  - Status awal Echo Pin: {'HIGH (Bermasalah)' if echo_awal == 1 else 'LOW (Normal)'}")
        
        # Kirim sinyal Trigger (10 microsecond HIGH)
        GPIO.output(TRIGGER_PIN, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(TRIGGER_PIN, GPIO.LOW)
        
        t_start = time.time()
        t_timeout = t_start + 1.0 # Timeout 1 detik
        
        # Tunggu Echo Pin menjadi HIGH
        waktu_mulai = time.time()
        stuck_low = False
        while GPIO.input(ECHO_PIN) == 0:
            waktu_mulai = time.time()
            if waktu_mulai > t_timeout:
                stuck_low = True
                break
                
        if stuck_low:
            print("  - [ERROR] Echo Pin tidak pernah berubah menjadi HIGH (Mungkin kabel Echo longgar atau salah pin)")
            continue
            
        # Tunggu Echo Pin kembali menjadi LOW
        waktu_selesai = time.time()
        stuck_high = False
        while GPIO.input(ECHO_PIN) == 1:
            waktu_selesai = time.time()
            if waktu_selesai > t_timeout:
                stuck_high = True
                break
                
        if stuck_high:
            print("  - [ERROR] Echo Pin tertahan di HIGH (Mungkin sensor rusak, pin Trigger tidak terhubung, atau Ground lepas)")
            continue
            
        # Hitung jarak
        durasi = waktu_selesai - waktu_mulai
        jarak = (durasi * 34300) / 2
        
        print(f"  - Durasi Echo: {durasi * 1000:.3f} ms")
        print(f"  - Jarak Terukur: {jarak:.2f} cm")
        
        time.sleep(0.5)

    # Cleanup
    GPIO.cleanup()
    print("\nTes selesai, GPIO telah di-cleanup.")

if __name__ == "__main__":
    try:
        test_sensor()
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("\nTes dibatalkan oleh pengguna.")

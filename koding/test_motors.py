import sys
import os
import time

# Tambahkan path agar bisa import dari folder
sys.path.append(os.getcwd())

from robot_navigation_module.motor_manager import MotorManager
import RPi.GPIO as GPIO

def test_motor_sequence():
    motors = MotorManager()
    
    try:
        print("\n=== PROGRAM PENGUJIAN MOTOR ===")
        print("Pastikan robot dalam kondisi aman (roda menggantung atau di lantai luas)")
        print("Setiap tahap berlangsung selama 2 detik.\n")

        # 1. MAJU
        print("[1/6] MAJU...")
        motors.set_motors(150, 150)
        time.sleep(2)
        
        # 2. MUNDUR
        print("[2/6] MUNDUR...")
        motors.set_motors(-150, -150)
        time.sleep(2)

        # 3. BELOK KANAN (Hanya roda kiri maju)
        print("[3/6] BELOK KANAN (Roda Kiri Saja)...")
        motors.set_motors(150, 0)
        time.sleep(2)

        # 4. BELOK KIRI (Hanya roda kanan maju)
        print("[4/6] BELOK KIRI (Roda Kanan Saja)...")
        motors.set_motors(0, 150)
        time.sleep(2)

        # 5. PUTAR KANAN (Di tempat)
        print("[5/6] PUTAR KANAN (Pivot)...")
        motors.set_motors(150, -150)
        time.sleep(2)

        # 6. PUTAR KIRI (Di tempat)
        print("[6/6] PUTAR KIRI (Pivot)...")
        motors.set_motors(-150, 150)
        time.sleep(2)

        print("\n[OK] Pengujian Selesai. Menghentikan motor.")
        motors.stop()

    except KeyboardInterrupt:
        print("\n[!] Dihentikan oleh pengguna.")
    finally:
        motors.stop()
        GPIO.cleanup()
        print("GPIO Cleanup selesai.")

if __name__ == "__main__":
    test_motor_sequence()

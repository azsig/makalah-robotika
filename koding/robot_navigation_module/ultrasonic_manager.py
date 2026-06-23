import RPi.GPIO as GPIO
import time
import os

class UltrasonicManager:
    def __init__(self, trigger_pin=17, echo_pin=27, file_kalibrasi="faktor_koreksi.txt"):
        self.PIN_TRIGGER = trigger_pin
        self.PIN_ECHO = echo_pin
        self.FILE_KALIBRASI = file_kalibrasi
        self.faktor_koreksi = 1.0
        
        # Setup GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.PIN_TRIGGER, GPIO.OUT)
        GPIO.setup(self.PIN_ECHO, GPIO.IN)
        GPIO.output(self.PIN_TRIGGER, GPIO.LOW)
        
        self.load_kalibrasi()

    def load_kalibrasi(self):
        if os.path.exists(self.FILE_KALIBRASI):
            try:
                with open(self.FILE_KALIBRASI, "r") as f:
                    self.faktor_koreksi = float(f.read().strip())
                    print(f"[ULTRASONIC] Faktor koreksi dimuat: {self.faktor_koreksi:.4f}")
            except:
                print("[ULTRASONIC] Gagal membaca file kalibrasi, menggunakan 1.0")

    def ukur_jarak_mentah(self):
        total_jarak = 0
        pembacaan_valid = 0
        
        for _ in range(3): # Dikurangi ke 3 pembacaan agar navigasi lebih responsif
            GPIO.output(self.PIN_TRIGGER, GPIO.HIGH)
            time.sleep(0.00001)
            GPIO.output(self.PIN_TRIGGER, GPIO.LOW)

            waktu_mulai = time.time()
            waktu_selesai = time.time()
            timeout = time.time() + 0.1 # Timeout dipercepat

            while GPIO.input(self.PIN_ECHO) == 0:
                waktu_mulai = time.time()
                if waktu_mulai > timeout: break

            while GPIO.input(self.PIN_ECHO) == 1:
                waktu_selesai = time.time()
                if waktu_selesai > timeout: break

            durasi = waktu_selesai - waktu_mulai
            jarak = (durasi * 34300) / 2
            
            if 2 <= jarak <= 400:
                total_jarak += jarak
                pembacaan_valid += 1
            time.sleep(0.01)
            
        if pembacaan_valid > 0:
            return total_jarak / pembacaan_valid
        return None

    def get_jarak(self):
        mentah = self.ukur_jarak_mentah()
        if mentah is not None:
            return mentah * self.faktor_koreksi
        return 999 # Kembalikan nilai jauh jika gagal baca agar robot tidak stop tiba-tiba

    def cleanup(self):
        # GPIO.cleanup() sebaiknya dipanggil di level main app
        pass

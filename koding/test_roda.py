import RPi.GPIO as GPIO
import time

# Gunakan penomoran BCM (GPIO)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Definisikan Pin sesuai tabel
IN1 = 16  # Motor Kiri
IN2 = 20  # Motor Kiri
IN3 = 13  # Motor Kanan
IN4 = 26  # Motor Kanan

# Atur pin sebagai OUTPUT
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

def stop_motor():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)

def maju():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)

def mundur():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)

def belok_kanan():
    # Motor kiri maju, motor kanan mundur
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)

def belok_kiri():
    # Motor kiri mundur, motor kanan maju
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)

try:
    while True:
        print("Maju...")
        maju()
        time.sleep(2)
        
        print("Stop...")
        stop_motor()
        time.sleep(1)
        
        print("Belok Kanan...")
        belok_kanan()
        time.sleep(1.5)
        
        print("Stop...")
        stop_motor()
        time.sleep(1)
        
        print("Belok Kiri...")
        belok_kiri()
        time.sleep(1.5)
        
        print("Stop...")
        stop_motor()
        time.sleep(1)
        
        print("Mundur...")
        mundur()
        time.sleep(2)
        
        print("Stop... Selesai 1 Siklus")
        stop_motor()
        time.sleep(3)

except KeyboardInterrupt:
    # Jaga-jaga kalau program dihentikan (Ctrl+C), motor langsung mati
    print("\nProgram dihentikan oleh pengguna.")
    stop_motor()
    GPIO.cleanup()
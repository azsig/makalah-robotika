import requests
import time

# =========================================================================
# PARAMETER & KONFIGURASI
# =========================================================================

# --- Parameter PID (Digunakan untuk kalkulasi steer) ---
Kp = 0.8  # Lebih agresif
Ki = 0.0   
Kd = 0.05   

# --- Pengaturan Kecepatan Motor (PWM 0-255) ---
V_BASE = 125   # Diturunkan sedikit agar selisih kecepatan lebih terasa
V_SLOW = 100
MAX_SPEED_LIMIT = 180 

# --- Konstanta Kamera ---
SETPOINT_TENGAH = 160

# --- Koneksi Visi ---
API_URL = "http://127.0.0.1:5000/api/objects"

# =========================================================================
# VARIABEL GLOBAL PID
# =========================================================================
last_error = 0
integral = 0

def hitung_PID(current_error):
    global last_error, integral
    P = current_error
    integral += current_error
    if integral > 50: integral = 50
    if integral < -50: integral = -50
    derivative = current_error - last_error
    total_output = (Kp * P) + (Ki * integral) + (Kd * derivative)
    last_error = current_error
    return total_output

from .motor_manager import MotorManager
from .ultrasonic_manager import UltrasonicManager

# --- Init Hardware ---
# Bias 1.14 untuk mengimbangi roda kiri secara permanen
motors = MotorManager(max_speed_limit=MAX_SPEED_LIMIT, left_bias=1.14)
ultrasonic = UltrasonicManager()

def jalankan_motor(v_kiri, v_kanan):
    # Pastikan motor yang harusnya jalan punya torsi cukup (min 90)
    if v_kiri > 0 and v_kiri < 90: v_kiri = 90
    if v_kanan > 0 and v_kanan < 90: v_kanan = 90
    if v_kiri < 0 and v_kiri > -90: v_kiri = -90
    if v_kanan < 0 and v_kanan > -90: v_kanan = -90
    
    motors.set_motors(v_kiri, v_kanan)

def stop_robot():
    motors.stop()

def ambil_data_visi():
    try:
        r = requests.get(API_URL, timeout=0.1)
        if r.status_code == 200:
            return r.json()
    except:
        pass
    return None

# =========================================================================
# LOOP UTAMA (LOGIKA SEKUENSIAL: AMBIL GAMBAR -> JALAN -> STOP)
# =========================================================================

def main_loop(shared_data=None):
    SAFE_MARGIN_PIXELS = 100 
    MIN_AREA_TARGET = 600       # Abaikan target terlalu kecil/jauh
    MIN_AREA_OBSTACLE = 2000     # Abaikan rintangan jauh
    TARGET_REACHED_AREA = 10000  # Target dianggap "Penuh" di kamera (Finish)
    
    print(f"Memulai Navigasi Sekuensial (Smooth | Bias: 1.18 | Body: 15cm)...")
    
    last_known_target_direction = "CENTER"
    
    while True:
        nav_aktif = shared_data.get('nav_active', False) if shared_data is not None else True

        # 1. Baca Sensor Ultrasonik
        jarak_mentah = ultrasonic.ukur_jarak_mentah()
        if shared_data is not None:
            if jarak_mentah is not None: shared_data['raw_distance'] = round(jarak_mentah, 2)
            current_factor = shared_data.get('faktor_koreksi', ultrasonic.faktor_koreksi)
            jarak_depan = (jarak_mentah * current_factor) if jarak_mentah else 999
        else:
            jarak_depan = ultrasonic.get_jarak()

        if not nav_aktif:
            stop_robot()
            time.sleep(0.1)
            continue

        # --- STATE 1: JARAK DEKAT (MUNDUR & HINDAR) ---
        if jarak_depan <= 15:
            stop_robot()
            time.sleep(0.1)
            
            # Cek apakah ini target finish (Harus berwarna target DAN area besar)
            vision_data = ambil_data_visi()
            target_area = 0
            if vision_data:
                for obj in vision_data.get('objects', []):
                    if obj['label'] == 'TARGET':
                        area = obj['bbox']['w'] * obj['bbox']['h']
                        if area > target_area: target_area = area
            
            if target_area > TARGET_REACHED_AREA and jarak_depan <= 12:
                print(f"[FINISH] Target Terpenuhi (Area: {target_area}) | Stop.")
                stop_robot()
                if shared_data is not None: shared_data['nav_active'] = False
                continue
            else:
                # Jika jarak dekat tapi bukan target penuh -> Itu Obstacle
                print(f">> OBSTACLE TERDETEKSI ({jarak_depan:.1f} cm) | Manuver Mundur...")
                jalankan_motor(-V_SLOW, -V_SLOW)
                time.sleep(0.5)
                stop_robot()
                time.sleep(0.2)
                
                # Belok sedikit untuk mencari jalan lain
                if last_known_target_direction == "LEFT":
                    print(">> MANUVER: Belok KANAN menghindari rintangan")
                    jalankan_motor(120, -100)
                else:
                    print(">> MANUVER: Belok KIRI menghindari rintangan")
                    jalankan_motor(-100, 110)
                time.sleep(0.3)
                stop_robot()
                time.sleep(0.2)
                continue

        # --- STATE 2: AMBIL GAMBAR & TENTUKAN ARAH ---
        stop_robot() # Diam saat ambil gambar agar akurat
        time.sleep(0.1)
        vision_data = ambil_data_visi()
        
        x_target = -1
        x_obstacle = -1
        if vision_data:
            max_area_target = 0
            max_area_obs = 0
            for obj in vision_data.get('objects', []):
                area = obj['bbox']['w'] * obj['bbox']['h']
                if obj['label'] == 'TARGET' and area > MIN_AREA_TARGET:
                    if area > max_area_target:
                        max_area_target = area
                        x_target = obj['bbox']['x'] + (obj['bbox']['w'] / 2)
                elif obj['label'] == 'OBSTACLE' and area > MIN_AREA_OBSTACLE:
                    if area > max_area_obs:
                        max_area_obs = area
                        x_obstacle = obj['bbox']['x'] + (obj['bbox']['w'] / 2)

        # --- STATE 3: EKSEKUSI GERAKAN ---
        # PRIORITAS 1: Jika ada target, kejar target!
        if x_target != -1:
            error = x_target - 160
            steer = hitung_PID(error)
            
            v_kiri = V_BASE + steer
            v_kanan = V_BASE - steer

            # Logging lebih sensitif (ambang batas diturunkan dari 40 ke 20)
            if error < -20: 
                last_known_target_direction = "LEFT"
                print(f">> BELOK KIRI: Target X:{x_target:.1f} | L:{v_kiri:.1f} R:{v_kanan:.1f}")
            elif error > 20: 
                last_known_target_direction = "RIGHT"
                print(f">> BELOK KANAN: Target X:{x_target:.1f} | L:{v_kiri:.1f} R:{v_kanan:.1f}")
            else: 
                last_known_target_direction = "CENTER"
                print(f">> MAJU: Target X:{x_target:.1f} | L:{v_kiri:.1f} R:{v_kanan:.1f}")

            jalankan_motor(v_kiri, v_kanan)
            time.sleep(0.25)

        # PRIORITAS 2: Jika tidak ada target tapi ada rintangan, hindari!
        elif x_obstacle != -1:
            # Safe margin dipersempit agar tidak terlalu penakut (75px)
            if x_obstacle < (160 + 75) and x_obstacle > (160 - 75):
                if x_obstacle < 160:
                    print(f">> HINDAR KANAN: Ada rintangan di kiri")
                    jalankan_motor(V_BASE + 35, V_BASE - 35)
                else:
                    print(f">> HINDAR KIRI: Ada rintangan di kanan")
                    jalankan_motor(V_BASE - 25, V_BASE + 25)
            else:
                print(f">> MAJU: Rintangan di luar jalur (Aman)")
                jalankan_motor(V_BASE, V_BASE)
            time.sleep(0.25)

        else:
            # PRIORITAS 3: Cari target berdasarkan memori
            if last_known_target_direction == "LEFT":
                print(f">> SEARCH: Putar KIRI mencari target...")
                jalankan_motor(-100, 110)
            elif last_known_target_direction == "RIGHT":
                print(f">> SEARCH: Putar KANAN mencari target...")
                jalankan_motor(120, -100)
            else:
                print(f">> SEARCH: Target hilang, robot diam.")
                stop_robot()
            time.sleep(0.2)
            
        stop_robot() 
        time.sleep(0.1) # Jeda stabilisasi

if __name__ == "__main__":
    try:
        main_loop()
    except KeyboardInterrupt:
        stop_robot()
    finally:
        motors.cleanup()

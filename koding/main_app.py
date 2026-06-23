import multiprocessing
import time
import sys
import os

# Tambahkan path root agar bisa import paket dengan nama lengkap
sys.path.append(os.getcwd())

def run_vision_server(shared_data):
    """Menjalankan Flask Server untuk Visi"""
    # Import di dalam fungsi agar isolasi proses sempurna
    from robot_vision_module.app import app
    app.config['SHARED_DATA'] = shared_data
    print("[MAIN] Menjalankan Server Visi di port 5000...")
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True, use_reloader=False)

def run_navigation_logic(shared_data):
    """Menjalankan Logika Navigasi Robot"""
    from robot_navigation_module.navigator import main_loop
    print("[MAIN] Menjalankan Logika Navigasi (PID)...")
    time.sleep(3) 
    main_loop(shared_data)

if __name__ == "__main__":
    import RPi.GPIO as GPIO
    
    # Load faktor koreksi terkalibrasi jika ada
    faktor_koreksi_awal = 1.0
    if os.path.exists("faktor_koreksi.txt"):
        try:
            with open("faktor_koreksi.txt", "r") as f:
                faktor_koreksi_awal = float(f.read().strip())
                print(f"[MAIN] Memuat faktor koreksi terkalibrasi: {faktor_koreksi_awal:.4f}")
        except:
            pass

    # Manager untuk berbagi data antar proses
    manager = multiprocessing.Manager()
    shared_data = manager.dict()
    shared_data['raw_distance'] = 0.0
    shared_data['faktor_koreksi'] = faktor_koreksi_awal
    shared_data['nav_active'] = False  # Default: Navigasi mati saat startup

    vision_process = multiprocessing.Process(target=run_vision_server, args=(shared_data,))
    navigation_process = multiprocessing.Process(target=run_navigation_logic, args=(shared_data,))

    try:
        vision_process.start()
        
        # Jeda 5 detik agar Kamera & Server Visi siap sepenuhnya 
        # sebelum hardware motor/sensor diakses
        print("[MAIN] Menunggu inisialisasi kamera (5 detik)...")
        time.sleep(5)
        
        navigation_process.start()

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n[MAIN] Menghentikan sistem...")
        # Force stop motors before cleanup
        try:
            from robot_navigation_module.motor_manager import MotorManager
            m = MotorManager()
            m.cleanup()
        except:
            pass
            
        vision_process.terminate()
        navigation_process.terminate()
        vision_process.join()
        navigation_process.join()
        
    finally:
        try:
            import RPi.GPIO as GPIO
            GPIO.setmode(GPIO.BCM)
            GPIO.cleanup()
            print("[MAIN] GPIO Cleanup berhasil dilakukan.")
        except Exception as e:
            print(f"[MAIN] GPIO Cleanup Error: {e}")
        print("[MAIN] Keluar.")

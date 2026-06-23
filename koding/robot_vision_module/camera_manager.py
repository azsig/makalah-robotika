import cv2
import threading
import time
import numpy as np

class CameraManager:
    def __init__(self, src=0):
        self.src = src
        # Gunakan backend V4L2 yang jauh lebih stabil di Raspberry Pi/Linux
        self.stream = cv2.VideoCapture(self.src, cv2.CAP_V4L2)
        
        # Set format ke MJPG untuk menghemat bandwidth USB di Raspberry Pi
        self.stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        
        self.grabbed = False
        # Inisialisasi dengan frame hitam agar tidak None
        self.frame = np.zeros((240, 320, 3), dtype=np.uint8)
        self.stopped = False
        
        if self.stream.isOpened():
            print(f"[CAM] Kamera {self.src} terdeteksi.")
            # Ambil satu frame awal secara sinkron
            self.grabbed, self.frame = self.stream.read()
        else:
            print(f"[CAM] [ERROR] Kamera {self.src} tidak ditemukan!")

    def start(self):
        # Jalankan pembacaan frame di background thread
        threading.Thread(target=self.update, args=(), daemon=True).start()
        return self

    def update(self):
        while not self.stopped:
            if not self.stream.isOpened():
                break
            self.grabbed, self.frame = self.stream.read()
            # Jeda kecil agar tidak membebani CPU
            time.sleep(0.03)

    def read(self):
        return self.frame

    def stop(self):
        self.stopped = True
        self.stream.release()

    def switch_source(self, new_src):
        """Mengganti input kamera secara dinamis"""
        self.stopped = True
        time.sleep(0.1)  # Beri jeda kecil agar thread update selesai
        self.stream.release()
        
        self.src = new_src
        self.stream = cv2.VideoCapture(self.src, cv2.CAP_V4L2)
        self.stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        
        self.grabbed = False
        self.frame = np.zeros((240, 320, 3), dtype=np.uint8)
        self.stopped = False
        
        if self.stream.isOpened():
            print(f"[CAM] Berhasil beralih ke Kamera {self.src}")
            self.grabbed, self.frame = self.stream.read()
            self.start()
            return True
        else:
            print(f"[CAM] [ERROR] Gagal membuka Kamera {self.src}")
            # Nyalakan thread update kembali agar program tidak macet
            self.start()
            return False

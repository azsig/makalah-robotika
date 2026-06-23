import os

class DistanceEstimator:
    def __init__(self, file_path="kalibrasi_jarak.txt"):
        self.file_path = file_path
        self.reference_pixel_width = 0.0
        self.known_distance = 0.0
        self.is_calibrated = False
        self.load_calibration()

    def load_calibration(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r") as f:
                    lines = f.readlines()
                    if len(lines) >= 2:
                        self.reference_pixel_width = float(lines[0].strip())
                        self.known_distance = float(lines[1].strip())
                        self.is_calibrated = True
                        print(f"[JARAK] Kalibrasi dimuat: {self.reference_pixel_width}px pada {self.known_distance}cm")
            except Exception as e:
                print(f"[JARAK] Gagal memuat file kalibrasi: {e}")

    def calibrate(self, known_distance, pixel_width):
        if known_distance > 0 and pixel_width > 0:
            self.reference_pixel_width = pixel_width
            self.known_distance = known_distance
            self.is_calibrated = True
            try:
                with open(self.file_path, "w") as f:
                    f.write(f"{pixel_width}\n{known_distance}\n")
                print(f"[JARAK] Kalibrasi disimpan: {pixel_width}px pada {known_distance}cm")
            except Exception as e:
                print(f"[JARAK] Gagal menyimpan file kalibrasi: {e}")
            return True
        return False

    def estimate_distance(self, pixel_width):
        if not self.is_calibrated or pixel_width <= 0:
            return 0.0
            
        # Rumus Jarak yang disederhanakan: D_baru = (Piksel_Awal * Jarak_Awal) / Piksel_Baru
        distance = (self.reference_pixel_width * self.known_distance) / pixel_width
        return round(distance, 1)

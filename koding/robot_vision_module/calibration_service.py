import numpy as np
import cv2
from robot_vision_module.distance_estimator import DistanceEstimator

class CalibrationService:
    def __init__(self):
        self.mode = "DISCOVERY" # Mode awal adalah mencari benda apapun
        self.target_lower = np.array([0, 0, 0])
        self.target_upper = np.array([180, 255, 255])
        self.is_calibrated = False
        self.last_discovery_objects = []
        
        self.distance_estimator = DistanceEstimator()
        self.last_target_bbox = None
        self.latest_objects_data = []

    def calibrate_color(self, frame, x, y):
        h, w = frame.shape[:2]
        if x < 0 or x >= w or y < 0 or y >= h:
            return False

        # Ambil sampel dari area kecil di sekitar titik klik (agar lebih representatif)
        y_min, y_max = max(0, y-5), min(h, y+5)
        x_min, x_max = max(0, x-5), min(w, x+5)
        roi = frame[y_min:y_max, x_min:x_max]
        
        hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        
        # Rata-rata warna
        if hsv_roi.size > 0:
            avg_hsv = np.average(np.average(hsv_roi, axis=0), axis=0)
        else:
            return False
            
        hue, sat, val = avg_hsv[0], avg_hsv[1], avg_hsv[2]
        
        # Toleransi
        lower_hue = max(0, hue - 15)
        upper_hue = min(180, hue + 15)
        
        lower_sat = max(50, sat - 60) 
        upper_sat = min(255, sat + 60)
        
        lower_val = max(50, val - 60) 
        upper_val = min(255, val + 60)

        self.target_lower = np.array([lower_hue, lower_sat, lower_val])
        self.target_upper = np.array([upper_hue, upper_sat, upper_val])
        self.mode = "TRACKING"
        self.is_calibrated = True

        print(f"[KALIBRASI] Klik ({x}, {y}) | AVG HSV: {avg_hsv}")
        return True

    def calibrate_distance(self, known_distance):
        if self.last_target_bbox is not None:
            _, _, w, _ = self.last_target_bbox
            success = self.distance_estimator.calibrate(known_distance, w)
            if success:
                print(f"[KALIBRASI JARAK] Berhasil! Piksel {w}px = {known_distance}cm")
            return success
        return False
        
    def reset_mode(self):
        self.mode = "DISCOVERY"

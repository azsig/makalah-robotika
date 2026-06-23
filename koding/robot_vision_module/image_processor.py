import cv2
import numpy as np

class ImageProcessor:
    def process_masks(self, frame, lower_color, upper_color):
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        
        # 1. Masker untuk Target (Sesuai dengan warna klik pengguna)
        mask_target = cv2.inRange(hsv, lower_color, upper_color)
        mask_target = cv2.erode(mask_target, None, iterations=2)
        mask_target = cv2.dilate(mask_target, None, iterations=2)
        
        # 2. Masker untuk Benda Berwarna Tajam (Kertas origami/binder)
        # Kertas warna-warni biasanya memiliki nilai Saturation dan Value tinggi (> 100)
        lower_colorful = np.array([0, 100, 80])
        upper_colorful = np.array([180, 255, 255])
        mask_colorful = cv2.inRange(hsv, lower_colorful, upper_colorful)
        
        mask_colorful = cv2.erode(mask_colorful, None, iterations=2)
        mask_colorful = cv2.dilate(mask_colorful, None, iterations=2)
        
        # 3. Masker Obstacle
        # Benda dianggap Pengecoh JIKA warnanya tajam, TAPI BUKAN merupakan warna target
        mask_obstacle = cv2.bitwise_and(mask_colorful, cv2.bitwise_not(mask_target))
        
        return mask_target, mask_obstacle

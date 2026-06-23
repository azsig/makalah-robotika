import cv2

class ObjectDetector:
    def __init__(self, min_area=500):
        # min_area adalah ukuran minimal piksel agar benda tidak dianggap sebagai debu/noise
        self.min_area = min_area

    def find_objects(self, mask):
        # Cari kontur (garis luar benda putih) pada masker
        contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        valid_objects = []
        for contour in contours:
            area = cv2.contourArea(contour)
            # Abaikan objek yang terlalu kecil
            if area > self.min_area:
                # Dapatkan koordinat x, y, lebar (w), dan tinggi (h)
                x, y, w, h = cv2.boundingRect(contour)
                valid_objects.append((x, y, w, h))
                
        # Urutkan objek berdasarkan luas bounding box (terbesar ke terkecil)
        valid_objects = sorted(valid_objects, key=lambda obj: obj[2] * obj[3], reverse=True)
        return valid_objects

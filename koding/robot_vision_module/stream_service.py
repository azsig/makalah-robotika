import cv2
import time
from robot_vision_module.image_processor import ImageProcessor
from robot_vision_module.object_detector import ObjectDetector

class StreamService:
    @staticmethod
    def generate_stream(camera_manager, calibration_svc):
        img_processor = ImageProcessor()
        detector = ObjectDetector(min_area=800) # Area dikecilkan karena resolusi proses turun

        while True:
            frame = camera_manager.read()
            # Cek jika frame tidak ada atau kosong
            if frame is None or frame.size == 0:
                time.sleep(0.1) # Jeda lebih lama saat inisialisasi
                continue
            
            # Frame sudah berukuran 320x240 secara native dari camera_manager
            annotated_frame = frame.copy()
            
            # --- MODE DISCOVERY ---
            if calibration_svc.mode == "DISCOVERY":
                cv2.putText(annotated_frame, "MODE: DISCOVERY", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                cv2.putText(annotated_frame, "Klik TEPAT di warna kertas target pada layar!", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                    
            # --- MODE TRACKING ---
            elif calibration_svc.mode == "TRACKING":
                # Dapatkan dua jenis masker dari gambar
                mask_target, mask_obstacle = img_processor.process_masks(frame, calibration_svc.target_lower, calibration_svc.target_upper)
                
                # Cari objek dari masker
                target_objects = detector.find_objects(mask_target)
                
                # Simpan objek terbesar sebagai patokan kalibrasi jarak
                if len(target_objects) > 0:
                    calibration_svc.last_target_bbox = target_objects[0]
                else:
                    calibration_svc.last_target_bbox = None
                    
                current_objects_data = []
                
                # 1. Gambar kotak Hijau untuk TARGET
                for (x, y, w, h) in target_objects:
                    dist = calibration_svc.distance_estimator.estimate_distance(w)
                    label_text = "TARGET" if dist == 0 else f"TARGET ({dist}cm)"
                    cv2.rectangle(annotated_frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(annotated_frame, label_text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                    current_objects_data.append({"label": "TARGET", "bbox": {"x": x, "y": y, "w": w, "h": h}, "distance_cm": dist})
                    
                # 2. Gambar kotak Merah untuk PENGANCOH/OBSTACLE
                obstacle_objects = detector.find_objects(mask_obstacle)
                for (x, y, w, h) in obstacle_objects:
                    dist = calibration_svc.distance_estimator.estimate_distance(w)
                    label_text = "OBSTACLE" if dist == 0 else f"OBSTACLE ({dist}cm)"
                    cv2.rectangle(annotated_frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
                    cv2.putText(annotated_frame, label_text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                    current_objects_data.append({"label": "OBSTACLE", "bbox": {"x": x, "y": y, "w": w, "h": h}, "distance_cm": dist})
                    
                calibration_svc.latest_objects_data = current_objects_data
                cv2.putText(annotated_frame, "MODE: TRACKING (Klik layar untuk mereset)", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            ret, buffer = cv2.imencode('.jpg', annotated_frame)
            if not ret:
                continue
            
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

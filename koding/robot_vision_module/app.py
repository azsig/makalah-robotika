from flask import Flask, render_template, Response, request, jsonify
import os

# Gunakan absolute import dari root package
from robot_vision_module.camera_manager import CameraManager
from robot_vision_module.stream_service import StreamService
from robot_vision_module.calibration_service import CalibrationService

import logging

app = Flask(__name__)

# Suppress Flask/Werkzeug logs
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

cam = CameraManager(src=1).start()
calibration_svc = CalibrationService()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(StreamService.generate_stream(cam, calibration_svc),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/available-cameras', methods=['GET'])
def get_available_cameras():
    import os
    cameras = []
    if os.path.exists('/dev'):
        for dev in sorted(os.listdir('/dev')):
            if dev.startswith('video'):
                try:
                    idx = int(dev[5:])
                    # Ambil video device normal di bawah 10 (mengabaikan metadata ISP)
                    if idx < 10:
                        cameras.append(idx)
                except ValueError:
                    pass
    if not cameras:
        # Fallback jika diuji coba di laptop Windows
        cameras = [0, 1, 2]
    
    # Selalu pastikan kamera yang aktif masuk ke daftar
    if cam.src not in cameras:
        cameras.append(cam.src)
        
    return jsonify({"cameras": sorted(list(set(cameras))), "current": cam.src})

@app.route('/api/switch-camera', methods=['POST'])
def switch_camera():
    data = request.json
    idx = data.get('camera_index')
    if idx is not None:
        try:
            idx = int(idx)
            success = cam.switch_source(idx)
            if success:
                return jsonify({"status": "success", "message": f"Berhasil beralih ke Kamera {idx}!"})
            else:
                return jsonify({"status": "error", "message": f"Gagal membuka Kamera {idx}."}), 400
        except ValueError:
            return jsonify({"status": "error", "message": "Indeks kamera tidak valid."}), 400
    return jsonify({"status": "error", "message": "Data tidak lengkap."}), 400

@app.route('/api/calibrate-color', methods=['POST'])
def calibrate_color():
    data = request.json
    x = data.get('x')
    y = data.get('y')
    
    frame = cam.read()
    if frame is not None and x is not None and y is not None:
        if calibration_svc.mode == "DISCOVERY":
            success = calibration_svc.calibrate_color(frame, int(x), int(y))
            if success:
                return jsonify({"status": "success", "message": "Target dikunci! Beralih ke mode Tracking."})
            else:
                return jsonify({"status": "error", "message": "Gagal mengambil warna."}), 400
        elif calibration_svc.mode == "TRACKING":
            calibration_svc.reset_mode()
            return jsonify({"status": "success", "message": "Kembali ke Mode Discovery."})
            
    return jsonify({"status": "error", "message": "Gagal membaca sistem."}), 400

@app.route('/api/calibrate-distance', methods=['POST'])
def api_calibrate_distance():
    data = request.json
    known_distance = float(data.get('known_distance', 0))
    
    if calibration_svc.calibrate_distance(known_distance):
        return jsonify({"status": "success", "message": "Kalibrasi jarak berhasil!"})
    else:
        return jsonify({"status": "error", "message": "Gagal! Pastikan Target ada di layar saat Anda mengklik Kalibrasi."}), 400

@app.route('/api/objects', methods=['GET'])
def api_objects():
    return jsonify({
        "calibration_status": calibration_svc.distance_estimator.is_calibrated,
        "objects": getattr(calibration_svc, 'latest_objects_data', [])
    })

@app.route('/api/ultrasonic-status', methods=['GET'])
def ultrasonic_status():
    shared_data = app.config.get('SHARED_DATA', {})
    return jsonify({
        "raw_distance": shared_data.get('raw_distance', 0),
        "faktor_koreksi": shared_data.get('faktor_koreksi', 1.0)
    })

@app.route('/api/calibrate-ultrasonic', methods=['POST'])
def calibrate_ultrasonic():
    data = request.json
    actual_dist = float(data.get('actual_distance', 0))
    shared_data = app.config.get('SHARED_DATA')
    
    if shared_data and actual_dist > 0:
        raw_dist = shared_data.get('raw_distance', 0)
        if raw_dist > 0:
            new_factor = actual_dist / raw_dist
            shared_data['faktor_koreksi'] = new_factor
            
            # Simpan secara permanen ke file
            try:
                with open("faktor_koreksi.txt", "w") as f:
                    f.write(str(new_factor))
            except:
                pass
                
            return jsonify({"status": "success", "message": f"Kalibrasi Berhasil! Faktor baru: {new_factor:.4f}"})
    
    return jsonify({"status": "error", "message": "Gagal kalibrasi. Pastikan sensor membaca benda."}), 400

@app.route('/api/toggle-navigation', methods=['POST'])
def toggle_navigation():
    shared_data = app.config.get('SHARED_DATA')
    if shared_data is not None:
        current_state = shared_data.get('nav_active', False)
        new_state = not current_state
        shared_data['nav_active'] = new_state
        status_msg = "AKTIF" if new_state else "MATI"
        return jsonify({"status": "success", "nav_active": new_state, "message": f"Navigasi {status_msg}"})
    return jsonify({"status": "error", "message": "Shared data tidak terakses."}), 500

@app.route('/api/navigation-status', methods=['GET'])
def navigation_status():
    shared_data = app.config.get('SHARED_DATA', {})
    return jsonify({
        "nav_active": shared_data.get('nav_active', False)
    })

if __name__ == '__main__':
    os.makedirs('templates', exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)

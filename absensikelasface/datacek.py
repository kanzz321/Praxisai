import cv2
import face_recognition
import os
import numpy as np
import json
import tkinter as tk
from tkinter import simpledialog
from collections import deque
from datetime import datetime

# Folder untuk menyimpan wajah terdaftar
REGISTERED_FACES_DIR = "C:\\Users\\MyBook Hype AMD\\Documents\\Praxisai\\siswahadir"
os.makedirs(REGISTERED_FACES_DIR, exist_ok=True)

# Threshold untuk memastikan bahwa wajah baru dikenali secara akurat
FACE_RECOGNITION_THRESHOLD = 0.4

# Buffer untuk menyimpan hasil deteksi wajah
DETECTION_BUFFER_SIZE = 5
detection_buffer = deque(maxlen=DETECTION_BUFFER_SIZE)

# Waktu mulai video
start_time = datetime.now()

# Variabel untuk menyimpan wajah yang sudah terdaftar
registered_names = set()

# Fungsi untuk menyimpan wajah baru dan data dalam format JSON
def register_face(face_encoding, name, role):
    # Simpan encoding wajah ke file numpy
    encoding_file_path = os.path.join(REGISTERED_FACES_DIR, f"{name}_{role}.npy")
    np.save(encoding_file_path, face_encoding)

    # Simpan data registrasi dalam format JSON
    data = {
        "name": name,
        "role": role,
        "file_path": encoding_file_path
    }
    json_file_path = os.path.join(REGISTERED_FACES_DIR, f"{name}_{role}.json")
    with open(json_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    
    print(f"Wajah {name} sebagai {role} telah terdaftar dan disimpan ke {json_file_path}")
    registered_names.add(name)  # Tambahkan nama ke set

# Fungsi untuk memeriksa apakah wajah dikenal dengan threshold yang lebih ketat
def check_known_face(face_encoding):
    results = []
    for file_name in os.listdir(REGISTERED_FACES_DIR):
        if file_name.endswith(".npy"):
            known_face_encoding = np.load(os.path.join(REGISTERED_FACES_DIR, file_name))
            distance = face_recognition.face_distance([known_face_encoding], face_encoding)[0]
            if distance < FACE_RECOGNITION_THRESHOLD:
                # Mengambil nama dan role dari nama file
                name_role = os.path.splitext(file_name)[0]
                name, role = name_role.split('_')
                results.append((name, role))
    return results

# Fungsi untuk meningkatkan akurasi dalam kondisi gelap
def improve_lighting(image):
    # Lakukan equalize histogram untuk meningkatkan kontras
    yuv_img = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
    yuv_img[:, :, 0] = cv2.equalizeHist(yuv_img[:, :, 0])
    img_output = cv2.cvtColor(yuv_img, cv2.COLOR_YUV2BGR)
    return img_output

# Fungsi untuk menangani buffering dan deteksi wajah
def process_face_detection(face_encoding):
    detection_buffer.append(face_encoding)
    # Rata-rata encoding dalam buffer untuk mengurangi noise
    avg_encoding = np.mean(np.array(detection_buffer), axis=0)
    return check_known_face(avg_encoding)

# Fungsi untuk menjalankan stream video
def start_video_stream():
    video_capture = cv2.VideoCapture(0)
    arrival_times = {}  # Menyimpan waktu kedatangan wajah yang dikenal

    while True:
        ret, frame = video_capture.read()

        # Peningkatan kualitas gambar dalam kondisi pencahayaan rendah
        frame = improve_lighting(frame)

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        # Set untuk menyimpan nama wajah yang terdeteksi pada frame ini
        detected_names = set()

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            names_roles = check_known_face(face_encoding)

            if names_roles:
                for name, role in names_roles:
                    detected_names.add(name)  # Tambahkan nama ke set nama yang terdeteksi

                    if name not in arrival_times:
                        arrival_times[name] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        print(f"{name} ({role}) datang pada {arrival_times[name]}")

                    # Tampilkan nama jika wajah sudah terdaftar
                    label = f"{name} ({role})"

            else:
                # Jika wajah tidak dikenali, beri label pendaftaran
                label = "Press 'S' to register"

            # Gambar kotak di sekitar wajah
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            cv2.putText(frame, label, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)

        # Menampilkan nama pendaftaran untuk wajah yang belum terdaftar
        if not detected_names:
            for (top, right, bottom, left) in face_locations:
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                cv2.putText(frame, "Press 'S' to register", (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)

        # Tampilkan hasil
        cv2.imshow('Video', frame)

        # Tunggulah hingga tombol ditekan
        key = cv2.waitKey(1) & 0xFF

        if key == ord('s'):
            # Jika 's' ditekan dan wajah belum dikenal, buka jendela registrasi
            root = tk.Tk()
            root.withdraw()  # Sembunyikan jendela utama
            name = simpledialog.askstring("Registrasi", "Masukkan nama:")
            role = simpledialog.askstring("Registrasi", "Sebagai apa:")
            if name and role:
                # Hanya mendaftarkan wajah terakhir yang dideteksi
                for face_encoding in face_encodings:
                    register_face(face_encoding, name, role)
            root.destroy()
        elif key == ord('q'):
            break

    # Lepaskan webcam dan tutup jendela
    video_capture.release()
    cv2.destroyAllWindows()

# Mulai streaming video
start_video_stream()
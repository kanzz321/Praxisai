import face_recognition
import cv2
import numpy as np
import os
import datetime
import tkinter as tk

# Direktori untuk gambar wajah
image_directory = "C:/Users/MyBook Hype AMD/Documents/Praxisai/absensikelas/images/"

# Fungsi untuk memuat dan mengenali wajah dari gambar
def load_face(name, image_path):
    try:
        image = face_recognition.load_image_file(image_path)
        face_encoding = face_recognition.face_encodings(image)[0]
        return (name, face_encoding)
    except IndexError:
        print(f"[ERROR] Wajah tidak ditemukan di gambar: {image_path}")
    except Exception as e:
        print(f"[ERROR] Kesalahan saat memuat gambar: {image_path}. Error: {e}")
    return None

def jendela_pendaftaran():
    # Membuat jendela utama
    window = tk.Tk()
    window.title("Input Data")

    # Label dan Entry untuk nama
    tk.Label(window, text='Masukkan nama Anda:').pack()
    name_entry = tk.Entry(window)
    # name_entry.insert(tk.INSERT, data['name'])
    name_entry.pack()

    # Label dan Entry untuk level
    tk.Label(window, text='Masukkan level berapa:').pack()
    level_entry = tk.Entry(window)
    # level_entry.insert(tk.INSERT, data['level'])
    level_entry.pack()

    # Fungsi untuk menyimpan data
    def save_command():
        name = name_entry.get()
        level = level_entry.get()
        data = {
            'name': name,
            'level': level
        }
        # with open(filename, 'w') as f:
        #     json.dump(data, f)
        # messagebox.showinfo('info', f'Hello {name}! Level Anda: {level}')

    # Tombol untuk menyimpan
    tk.Button(window, text='Simpan', command=save_command).pack()

    # Menjalankan jendela
    window.mainloop()

# Daftar wajah yang dikenal
known_faces = []

# Daftar file gambar dengan nama
faces = [
    ("ardan", "ardan.jpg"),
    ("arsya", "arsya.jpg"),
    ("fachri", "fachri.jpg"),
    ("faiz", "faiz.jpg"),
    ("fattan", "fattan.jpg"),
    ("ilmikecil", "ilmikecil.jpg"),
    ("nabil", "nabil.jpg")
]

# Memuat wajah yang dikenal
for name, img_file in faces:
    face_data = load_face(name, os.path.join(image_directory, img_file))
    if face_data:
        known_faces.append(face_data)

# Nama-nama yang sudah dicatat hari ini
attendance = {}

# Inisialisasi video capture
video_capture = cv2.VideoCapture(0)

while True:
    # Mulai video stream
    ret, frame = video_capture.read()
    
    # Ubah frame ke RGB (face_recognition membutuhkan RGB)
    rgb_frame = frame[:, :, ::-1]
    
    # Temukan semua wajah di frame video
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
    
    for face_encoding, face_location in zip(face_encodings, face_locations):
        matches = face_recognition.compare_faces([face[1] for face in known_faces], face_encoding)
        face_distances = face_recognition.face_distance([face[1] for face in known_faces], face_encoding)
        best_match_index = np.argmin(face_distances)
        
        if matches[best_match_index]:
            name = known_faces[best_match_index][0]
            
            if name not in attendance:
                now = datetime.datetime.now()
                attendance[name] = {"role": "student", "expression": "happy", "first_seen": now, "last_seen": now}
                print(f"{name} hadir pada {now}")
            else:
                # Update waktu terakhir dilihat
                attendance[name]["last_seen"] = datetime.datetime.now()

        else:
            # Jika wajah tidak dikenal, tampilkan jendela pendaftaran
            # cv2.putText(frame, "Unknown face detected!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)
            print("Wajah tidak dikenal. Silakan daftar!")

    # Tampilkan hasil videonya
    cv2.imshow('Video', frame)

    # Tekan 'q' untuk keluar dari video
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Rilis video capture
video_capture.release()
cv2.destroyAllWindows()

# Simpan data kehadiran ke file
attendance_file = os.path.join(image_directory, "attendance.txt")
with open(attendance_file, "w") as f:
    for name, info in attendance.items():
        f.write(f"{name}: Role={info['role']}, Expression={info['expression']}, "
                f"First seen={info['first_seen']}, Last seen={info['last_seen']}\n")

print(f"Data kehadiran telah disimpan ke {attendance_file}")

import cv2
import face_recognition
import os
import numpy as np
from datetime import datetime
import pyttsx3
import csv
import database

engine = pyttsx3.init()

DATABASE_PATH = "C:\\Users\\MyBook Hype AMD\\Documents\\Praxisai\\siswahadir.db"
FACE_RECOGNITION_THRESHOLD = 0.4
CSV_FILE_PATH = "C:\\Users\\MyBook Hype AMD\\Documents\\Praxisai\\attendance.csv"

def play_greeting(message):
    engine.say(message)
    engine.runAndWait()

def check_known_face(face_encoding):
    students = database.get_students()
    results = []
    for name, role, known_face_encoding in students:
        known_face_encoding = np.frombuffer(known_face_encoding)
        distance = face_recognition.face_distance([known_face_encoding], face_encoding)[0]
        if distance < FACE_RECOGNITION_THRESHOLD:
            results.append((name, role))
    return results

def sharpen_image(image):
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    sharpened = cv2.filter2D(image, -1, kernel)
    return sharpened

def improve_lighting(image):
    yuv_img = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
    yuv_img[:, :, 0] = cv2.equalizeHist(yuv_img[:, :, 0])
    img_output = cv2.cvtColor(yuv_img, cv2.COLOR_YUV2BGR)
    return img_output

def write_to_csv(name, role, status, timestamp):
    with open(CSV_FILE_PATH, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, role, status, timestamp])

def start_video_stream():
    video_capture = cv2.VideoCapture(0)
    arrival_times = {}

    while True:
        ret, frame = video_capture.read()
        frame = improve_lighting(frame)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            names_roles = check_known_face(face_encoding)
            current_time = datetime.now().time()
            current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if names_roles:
                for name, role in names_roles:
                    if name not in arrival_times:
                        if datetime.strptime("07:00:00", "%H:%M:%S").time() <= current_time <= datetime.strptime("12:00:00", "%H:%M:%S").time():
                            arrival_times[name] = current_timestamp
                            play_greeting(f"Selamat datang di Praxis High School, {name}.")
                            write_to_csv(name, role, 'Arrival', current_timestamp)
                            print(f"{name} ({role}) datang pada {arrival_times[name]}")
                        elif datetime.strptime("14:00:00", "%H:%M:%S").time() <= current_time <= datetime.strptime("17:00:00", "%H:%M:%S").time():
                            if name in arrival_times:
                                play_greeting(f"Selamat jalan, {name}.")
                                write_to_csv(name, role, 'Departure', current_timestamp)
                                print(f"{name} ({role}) sedang meninggalkan sekolah.")
                                del arrival_times[name]

                    label = f"{name} ({role})"
            else:
                label = "Press 'S' to register"

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            cv2.putText(frame, label, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)

        cv2.imshow('Video', frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

start_video_stream()
database.close()

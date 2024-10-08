# import cv2
# import numpy as np
# import imutils
# import time
# import os
# from collections import deque
# from imutils.video import VideoStream

# # Konfigurasi video dan buffer
# buffer_size = 32
# output_folder = "C:\\Users\\MyBook Hype AMD\\Documents\\Praxisai\\rekaman_goal var"

# # Batasan warna "green" dalam ruang warna HSV
# greenLower1 = (40, 50, 50)
# greenUpper1 = (80, 255, 255)

# # Inisialisasi variabel
# pts = deque(maxlen=buffer_size)
# counter = 0
# score = 0
# goal_counted = False
# recording = False
# out = None
# record_count = 1
# goal_time = None

# # Mulai video stream dari webcam
# vs = VideoStream(src=0).start()
# time.sleep(2.0)

# # Buat folder output jika belum ada
# if not os.path.exists(output_folder):
#     os.makedirs(output_folder)

# def play_video(video_path):
#     cap = cv2.VideoCapture(video_path)
#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break
#         cv2.imshow("Replay", frame)
#         if cv2.waitKey(25) & 0xFF == ord('q'):
#             break
#     cap.release()
#     cv2.destroyWindow("Replay")

# # Loop utama
# while True:
#     frame = vs.read()
#     frame = imutils.resize(frame, width=600)
#     blurred = cv2.GaussianBlur(frame, (11, 11), 0)
#     hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

#     mask = cv2.inRange(hsv, greenLower1, greenUpper1)
#     mask = cv2.erode(mask, None, iterations=2)
#     mask = cv2.dilate(mask, None, iterations=2)

#     cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     cnts = imutils.grab_contours(cnts)
#     center = None

#     height, width = frame.shape[:2]
#     blue_line_y = height - 150  # Garis biru sebagai garis pre-goal
#     green_line_y = height - 50  # Garis hijau sebagai garis goal

#     # Gambar garis hijau (goal)
#     cv2.line(frame, (0, blue_line_y), (width, blue_line_y), (255, 0, 0), 2)
#     cv2.line(frame, (0, green_line_y), (width, green_line_y), (0, 255, 0), 2)
    

#     if len(cnts) > 0:
#         c = max(cnts, key=cv2.contourArea)
#         ((x, y), radius) = cv2.minEnclosingCircle(c)
#         M = cv2.moments(c)
#         center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

#         if radius > 10:
#             cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
#             cv2.circle(frame, center, 5, (0, 0, 255), -1)
#             pts.appendleft(center)
            
# # Memulai rekaman jika bola melewati garis biru (pre-goal)
#             if int(y - radius) > blue_line_y and not recording:
#                 video_name = os.path.join(output_folder, f"rekaman_{record_count}.avi")
#                 out = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'XVID'), 20, (width, height))
#                 print(f"Started recording: {video_name}")
#                 recording = True
#                 record_count += 1

#             # Mulai rekaman ketika bola mendekati garis goal
#             if int(y + radius) >= green_line_y - 20 and not recording:
#                 recording = True
#                 video_name = os.path.join(output_folder, f"rekaman_{record_count}.avi")
#                 out = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'XVID'), 20.0, (width, height))
#                 print(f"Started recording: {video_name}")
#                 record_count += 1
            
#             # Setelah bola melewati garis hijau (goal)
#             if int(y - radius) > green_line_y and recording:
#                 score += 1
#                 goal_counted = True
#                 print(f"Goal scored!")

#             # Jika rekaman aktif, simpan frame ke video
#             if recording:
#                 out.write(frame)

#     else:
#         if recording:
#             recording = False
#             out.release()
#             print("Stopped recording")

#     # Menampilkan skor
#     cv2.putText(frame, f"Score: {score}", (width - 150, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)

#     cv2.imshow("Frame", frame)
#     key = cv2.waitKey(1) & 0xFF
#     counter += 1

#     # Jika 'q' ditekan, berhenti
#     if key == ord("q"):
#         break

#     # Replay video jika tombol 'r' ditekan
#     if key == ord("r") and not recording and goal_counted:
#         last_video_path = os.path.join(output_folder, f"rekaman_{record_count - 1}.avi")
#         if os.path.exists(last_video_path):
#             play_video(last_video_path)

#     # Jeda 5 detik setelah 'goal' dan setelah video disimpan
#     if goal_counted:
#         out.release()  # Stop and save video
#         print("Video saved")
#         time.sleep(5)
#         goal_counted = False  # Reset flag setelah jeda

# # Memberhentikan stream dan menutup semua jendela
# vs.stop()
# if out is not None:
#     out.release()
# cv2.destroyAllWindows()
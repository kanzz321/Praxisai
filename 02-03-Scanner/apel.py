import cv2
import numpy as np
import os

def get_color_name(hue):
    if 20 < hue < 30:
        return "Kuning - Terlalu Matang"
    elif 0 <= hue < 10 or 160 < hue <= 180:
        return "Merah - Matang"
    elif 35 < hue < 85:
        return "Hijau - Belum Matang"
    else:
        return "Warna Tidak Dikenal"

def process_images(images_path):
    if not os.path.isfile(images_path): #os.path.isfile(images_path): Memeriksa apakah file gambar ada.
        print(f"Error: File {images_path} not found.")
        return
    
    images = cv2.imread(images_path) #cv2.imread(images_path): Membaca gambar dari path yang diberikan.
    if images is None:
        print(f"Error: Could not read image {images_path}.")
        return
    
    hsv = cv2.cvtColor(images, cv2.COLOR_BGR2HSV) #cv2.cvtColor(images, cv2.COLOR_BGR2HSV): Mengonversi gambar dari ruang warna BGR (default OpenCV) ke ruang warna HSV.
    
    mask = cv2.inRange(hsv, (0, 50, 50), (180, 255, 255))
    result = cv2.bitwise_and(images, images, mask=mask)
    
    blurred = cv2.GaussianBlur(result, (5, 5), 0)
    gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)
    
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        if cv2.contourArea(contour) > 500:  # Filter by size if necessary
            x, y, w, h = cv2.boundingRect(contour)
            roi = hsv[y:y+h, x:x+w]
            average_hue = np.mean(roi[:, :, 0])
            
            color_name = get_color_name(average_hue)
            cv2.rectangle(images, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(images, color_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    
    cv2.imshow("Detected Apples", images)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    image_path = "images/apel3.png"  # Pastikan path ini benar
    process_images(image_path)
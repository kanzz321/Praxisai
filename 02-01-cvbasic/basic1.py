import cv2
import imutils

image = cv2.imread("C:\\Users\\MyBook Hype AMD\\Documents\\Praxisai\\02-01-cvbasic\\bocilokky.png") 

h,w,d = image.shape
print("image size:", h,w,d)

cv2.imshow("bocilokky", image)
cv2.waitKey(0)

resized = cv2.resize(image, (200, 200))
cv2.imshow("Fixed Resizing", resized)
cv2.waitKey(0)

roi = image[40:180, 320:420]
cv2.imshow("ROI", roi)
cv2.waitKey(0)

rotated = imutils.rotate(image, 180)
cv2.imshow("Imutils Rotation", rotated)
cv2.waitKey(0)

purplered = cv2.GaussianBlur(image, (40, 40), 0)
cv2.imshow("purplered", purplered)
cv2.waitKey(0)

output = image.copy()
cv2.rectangle(output, (260, 50), (410, 230), (500, 0, 500), 7)
cv2.imshow("Rectangle", output)
cv2.waitKey(0)

output = image.copy()
cv2.circle(output, (300, 150), 20, (255, 0, 0), 4)
cv2.imshow("Circle", output)
cv2.waitKey(0)

output = image.copy()
cv2.line(output, (60, 20), (400, 200), (0, 0, 255), 3)
cv2.line(output, (60, 200), (400, 20), (0, 0, 255), 3)
cv2.imshow("Line", output)
cv2.waitKey(0)
cv2.destroyAllWindows()
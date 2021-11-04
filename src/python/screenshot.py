import cv2
from time import sleep
import os, os.path

name = 'capture'

cam = cv2.VideoCapture(1)

cv2.namedWindow("Press space to capture live stream image", cv2.WINDOW_NORMAL)
#cv2.resizeWindow("Press space to capture live stream image", 500, 300)

path, dirs, file = next(os.walk("/home/pi/Documents/AquaVision/Screenshots"))
img_counter = len(file)
print(img_counter)

while True:
    ret, frame = cam.read()
    cv2.imshow("Press space to capture live stream image", frame)
    if not ret:
        print("Failed to grab frame")
        break
    

    k = cv2.waitKey(1)
    if k % 256 == 32:
        # SPACE pressed
        img_name = "/home/pi/Documents/AquaVision/Screenshots/image_{}.jpg".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1

cam.release()

cv2.destroyAllWindows()

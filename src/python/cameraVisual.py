#!/usr/bin/env python

import cv2
from time import sleep
import os, os.path

name = 'capture'

cam = cv2.VideoCapture(1)

# 
cv2.namedWindow("Press space to capture live stream image", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Press space to capture live stream image", 500, 300)

path, dirs, file = next(os.walk("/home/pi/Documents/AquaVision"))
img_counter = len(file)
print(img_counter)

while True:
    ret, frame = cam.read()
    if not ret:
        print("Failed to grab frame")
        break
    
    cv2.imshow("Press space to capture live stream image", frame)

    k = cv2.waitKey(1)
    k = input ('input: ')
    if k == 's':
        # SPACE pressed
        img_name = "Screenshots/" + "/Screenshot{}.jpg".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1
    if k == 'q':
        # Q pressed
        break
    
cam.release()
cv2.destroyAllWindows()

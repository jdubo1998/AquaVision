import cv2

cam = cv2.VideoCapture(0)

while True:
    ret, frame = cam.read()

    # cv2.imwrite('image.jpg', frame)

    cv2.imshow('Show test image.', frame)

    if cv2.waitKey(10) & 0xFF == ord('q') :
        # break out of the while loop
        break

cam.release()
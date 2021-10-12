import cv2

name = 'capture'

cam = cv2.VideoCapture(0)

cv2.namedWindow("Press space to capture live stream image", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Press space to capture live stream image", 500, 300)

img_counter = 0

while True:
    ret, frame = cam.read()
    if not ret:
        print("Failed to grab frame")
        break
    cv2.imshow("Press space to capture live stream image", frame)

    k = cv2.waitKey(1)
    if k % 256 == 32:
        # SPACE pressed
        img_name = "dataset/" + name + "/image_{}.jpg".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1

cam.release()

cv2.destroyAllWindows()

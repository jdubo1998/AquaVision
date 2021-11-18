import cv2
from datetime import datetime
import os

dir = '../../screenshots'
cam = cv2.VideoCapture(0)

def take_screenshot():
    adir = os.path.abspath(dir)
    ret, frame = cam.read()
    cv2.imwrite('{}/{}.jpg'.format(adir, datetime.today().strftime('%m-%d-%Y_%H-%M-%S')), frame)

def release():
    cam.release()

def record_vid(duration):
    cam = cv2.VideoCapture(-1)

    if not cam.isOpened():
        print('Failed to capture video.')
        cam.release()
        return

    frame_width = int(cam.get(3))
    frame_height = int(cam.get(4))

    size = frame_width, frame_height

    adir = os.path.abspath(dir)

    recording = cv2.VideoWriter('{}/{}.avi'.format(adir, datetime.today().strftime('%m-%d-%Y_%H-%M-%S')), cv2.VideoWriter_fourcc(*'MJPG'), 30, size)

    for i in range(duration):
        ret, frame = cam.read()

        if not ret:
            print('Error trying to read frame.')
            break

if __name__ == '__main__':
    while True:
        i = input('> ')

        if i == 's':
            take_screenshot()

        if i == 'q':
            break

        if i == 'r':
            cv2.namedWindow('capture', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('capture', 500, 300)

            while True:
                success, frame = cam.read()
                if success:
                    cv2.imshow('capture', frame)

                else:
                    print("Can't read image.")

                k = cv2.waitKey(1)

                print(k)

                if k == 'q':
                    cv2.destroyAllWindows()
                    break
            break

    release()

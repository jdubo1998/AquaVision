import cv2
from datetime import datetime
import os

dir = '../../screenshots'
cam = cv2.VideoCapture(1)

def take_screenshot():
    adir = os.path.abspath(dir)
    ret, frame = cam.read()
    cv2.imwrite('{}/{}.jpg'.format(adir, datetime.today().strftime('%m-%d-%Y_%H-%M-%S')), frame)

def release():
    cam.release()


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
                ret, frame = cam.read()
                cv2.imshow('capture', frame)

                k = cv2.waitKey(1)

                if k == 'q':
                    cv2.destroyAllWindows()
                    break
            break

    release()

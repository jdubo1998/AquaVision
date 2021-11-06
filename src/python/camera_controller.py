import RPi.GPIO as GPIO
import cv2
import time

class CameraController():
    def __init__(self):
        self.down_pin = 16
        self.up_pin = 18
        self.ledlight_pin = 22

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.down_pin, GPIO.OUT)
        GPIO.setup(self.up_pin, GPIO.OUT)
        GPIO.setup(self.ledlight_pin, GPIO.OUT)

        GPIO.output(self.down_pin, True)
        GPIO.output(self.up_pin, True)
        GPIO.output(self.ledlight_pin, True)
        # print("Waiting for command")
        # time.sleep(1)

    def motor_up(self):
        print('Move motor up.')
        GPIO.output(self.down_pin, False)
        GPIO.output(self.up_pin, True)
        time.sleep(2.5)
        self.motor_off()

    def motor_down(self):
        print('Move motor down.')
        GPIO.output(self.down_pin, True)
        GPIO.output(self.up_pin, False)
        time.sleep(2.5)
        self.motor_off()

    def motor_off(self):
        GPIO.output(self.down_pin, True)
        GPIO.output(self.up_pin, True)
        # print("motor turned off")
        # time.sleep(2.5)

    def toggle_lights(self):
        self.toggleLight = not self.toggleLight
        GPIO.output(self.ledlight_pin, self.toggleLight)
        time.sleep(1)
        self.toggleLight = not self.toggleLight
        GPIO.output(self.ledlight_pin, self.toggleLight)
        time.sleep(1)
        print('Toggled lights. (pin {})'.format(self.ledlight_pin))

    def takeScreenshot(self):
        cam = cv2.VideoCapture(1)
        cv2.namedWindow('Press space to capture live stream image', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Press space to capture live stream image', 500, 300)
        
        #change path with USB
        path, dirs, file = next(os.walk('/home/pi/Documents/AquaVision/Screenshots'))
        img_counter = len(file)
        ret, frame = cam.read()
        print(frame)
        cv2.imshow('Press space to capture live stream image', frame)
        k = cv2.waitKey(1)
        img_name = '/home/pi/Documents/AquaVision/Screenshots/image_{}.jpg'.format(img_counter)
        cv2.imwrite(img_name, frame)
        cam.release()
        cv2.destroyAllWindows()
        print('{} Screenshot written!'.format(img_name))
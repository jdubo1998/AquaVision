import RPi.GPIO as GPIO
# import cv2
import os
from datetime import datetime
import time

class CameraController():
    def __init__(self):
        self.down_pin = 16
        self.up_pin = 18
        self.ledlight_pin = 22
        self.down_count = 0
        self.down_count_max = 50
        self.dir = '../../screenshots'
        
        GPIO.setwarnings(False)
        
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
        if self.down_count > 0:
            self.down_count = self.down_count - 1
            print('Move motor up.')
            GPIO.output(self.down_pin, False)
            GPIO.output(self.up_pin, True)
            time.sleep(2.5)
            self.motor_off()
        else:
            print("Can't go up anymore.")

    def motor_down(self):
        if self.down_count < self.down_count_max:
            self.down_count = self.down_count + 1
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
        print('Toggled lights. (pin {})'.format(self.ledlight_pin))
        GPIO.output(self.ledlight_pin, True)
        time.sleep(1)
        GPIO.output(self.ledlight_pin, False)
        time.sleep(1)
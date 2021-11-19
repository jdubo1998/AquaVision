import RPi.GPIO as GPIO
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

    def motor_up(self):
        if self.down_count > 0:
            print('Raising camera.')
            self.down_count = self.down_count - 1
            GPIO.output(self.down_pin, False)
            GPIO.output(self.up_pin, True)
            time.sleep(2.5)
            self.motor_off()
        else:
            print('Motor is reeled up.')

    def motor_down(self):
        if self.down_count < self.down_count_max:
            print('Lowering camera.')
            self.down_count = self.down_count + 1
            GPIO.output(self.down_pin, True)
            GPIO.output(self.up_pin, False)
            time.sleep(2.5)
            self.motor_off()
        else:
            print('Maximum depth reached.')

    def motor_off(self):
        GPIO.output(self.down_pin, True)
        GPIO.output(self.up_pin, True)

    def toggle_lights(self):
        print('Toggling lights.')
        GPIO.output(self.ledlight_pin, True)
        time.sleep(1)
        GPIO.output(self.ledlight_pin, False)
        time.sleep(1)

    def toggle_night_vision(self):
        print('Toggling night vision.')

    def reset(self):
        for i in range(self.down_count):
            self.motor_up()
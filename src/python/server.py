from flask import Flask
from flask_socketio import SocketIO, emit
import RPi.GPIO as GPIO
import time
import cv2
from time import sleep
import os, os.path
import signal



# Wrapper class that will incorporate all needed functions and members in order to work as a translate module.
class TranslateModule:
    in1 = 16
    in2 = 18
    in3 = 22
    def __init__(self):
        self.app = Flask(__name__)
        # self.app.config['SECRET_KEY'] = 'secret'
        self.sio = SocketIO(self.app, cors_allowed_origins='*')
        self.toggleLight = False

    def takeScreenshot(self):
        cam = cv2.VideoCapture(1)
        cv2.namedWindow("Press space to capture live stream image", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Press space to capture live stream image", 500, 300)
        
        #change path with USB
        path, dirs, file = next(os.walk("/home/pi/Documents/AquaVision/Screenshots"))
        img_counter = len(file)
        ret, frame = cam.read()
        print(frame)
        cv2.imshow("Press space to capture live stream image", frame)
        k = cv2.waitKey(1)
        img_name = "/home/pi/Documents/AquaVision/Screenshots/image_{}.jpg".format(img_counter)
        cv2.imwrite(img_name, frame)
        cam.release()
        cv2.destroyAllWindows()
        print("{} Screenshot written!".format(img_name))

    def toggleLights(self):
        self.toggleLight = not self.toggleLight
        GPIO.output(self.in3, self.toggleLight)
        time.sleep(1)
        self.toggleLight = not self.toggleLight
        GPIO.output(self.in3, self.toggleLight)
        time.sleep(1)
        print('toggleLights' + str(self.toggleLight))
        
    def motorOff(self):
        GPIO.output(self.in1, True)
        GPIO.output(self.in2, True)
        print("motor turned off")
        time.sleep(2.5)

    def moveUp(self):
        print('moveUp')
        GPIO.output(self.in1, False)
        GPIO.output(self.in2, True)
        time.sleep(2.5)
        self.motorOff()

    def moveDown(self):
        print('moveDown')
        GPIO.output(self.in1, True)
        GPIO.output(self.in2, False)
        time.sleep(2.5)
        self.motorOff()
    
    def start(self):
        self.sio.run(self.app, host='0.0.0.0', debug=True)
        
    def quitFunction(self):
        print("quitting program")
        os.kill(p.pid, signal.SIGINT)
#         exit(1)

translator = TranslateModule()

# Event that triggers when a successful connection is made.
@translator.sio.on('connect')
def connect(sid):
    pass
    # print("connect ", sid)
    
def gpioStart():
    in1 = 16
    in2 = 18
    in3 = 22

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(in1, GPIO.OUT)
    GPIO.setup(in2, GPIO.OUT)
    GPIO.setup(in3, GPIO.OUT)

    GPIO.output(in1, True)
    GPIO.output(in2, True)
    GPIO.output(in3, True)
    print("Waiting for command")
    time.sleep(1)

# Event that triggers when a command is received from the user.
@translator.sio.on('relaycommand')
def relayCommand(command):
    if command == 'screenshot':
        translator.takeScreenshot()
    elif command == 'lights':
        translator.toggleLights()
    elif command == 'moveup':
        translator.moveUp()
    elif command == 'movedown':
        translator.moveDown()
    elif command == "quit":
        translator.quitFunction()
        


def main():
    print('\n-----------------------------------------------------------\n')
    gpioStart()
    translator.start()
    

if __name__ == "__main__":
    main()

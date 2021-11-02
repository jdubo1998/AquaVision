from flask import Flask
from flask_socketio import SocketIO, emit
import RPi.GPIO as GPIO
import time




# Wrapper class that will incorporate all needed functions and members in order to work as a translate module.
class TranslateModule:
    in1 = 16
    in2 = 18
    in3 = 22
    toggleLight = True
    def __init__(self):
        self.app = Flask(__name__)
        # self.app.config['SECRET_KEY'] = 'secret'
        self.sio = SocketIO(self.app, cors_allowed_origins='*')

    def takeScreenshot(self):
        print('takeScreenshot')

    def toggleLights(self):
        toggleLight = not toggleLight
        GPIO.output(self.in3, toggleLight)
        print('toggle Lights')

    # def turnOffLights(self):
    #     GPIO.output(self.in3, True)
    #     print("turn off lights")

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

def main():
    print('\n-----------------------------------------------------------\n')
    gpioStart()
    translator.start()
    

if __name__ == "__main__":
    main()

from flask import Flask
from flask.logging import default_handler
from flask_socketio import SocketIO, Namespace, emit

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.WARNING)

class Server(Namespace):
    namespace = '/'

    app = Flask(__name__)
    sio = SocketIO(app, cors_allowed_origins='*')

    def __init__(self, target=None):
        self.app.logger.removeHandler(default_handler)
        self.sio.on_namespace(self)

        if target != None:
            self.bgtask = target

	# Function used to send a socket.io event for the GPS coordinates.
    def relay_gps_data(self, lat, lon):
        self.sio.emit('relaydata', 'Latitude: {}   Longitude: {}'.format(lat, lon))
        # print('relay_gps_data: Latitude: {}   Longitude: {}'.format(lat, lon))

    def on_relaydata(self, data):
        print('on_relaydata')

    def take_screenshot(self):
        print('takeScreenshot')

    def toggle_lights(self):
        print('toggleLights')
        
    def motorOff(self):
        GPIO.output(self.in1, True)
        GPIO.output(self.in2, True)
        print("motor turned off")
        time.sleep(2.5)

    def move_up(self):
        print('moveUp')
        GPIO.output(self.in1, False)
        GPIO.output(self.in2, True)
        time.sleep(2.5)
        self.motorOff()

    def move_down(self):
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

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(in1, GPIO.OUT)
    GPIO.setup(in2, GPIO.OUT)

    GPIO.output(in1, True)
    GPIO.output(in2, True)
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

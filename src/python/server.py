from flask import Flask
from flask.logging import default_handler
from flask_socketio import SocketIO, Namespace, emit
from camera_controller import CameraController
import sys

# import logging
# log = logging.getLogger('werkzeug')
# log.setLevel(logging.WARNING)

class Server(Namespace):
    namespace = '/'

    app = Flask(__name__)
    sio = SocketIO(app, cors_allowed_origins='*')

    def __init__(self, target=None):
        self.app.logger.removeHandler(default_handler)
        self.sio.on_namespace(self)
        self.cam_controller = CameraController()

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
        self.cam_controller.toggle_lights()
        
    # def motorOff(self):
    #     GPIO.output(self.in1, True)
    #     GPIO.output(self.in2, True)
    #     print("motor turned off")
    #     time.sleep(2.5)

    def move_up(self):
        self.cam_controller.motor_up()
        # print('moveUp')
        # GPIO.output(self.in1, False)
        # GPIO.output(self.in2, True)
        # time.sleep(2.5)
        # self.motorOff()

    def move_down(self):
        self.cam_controller.motor_down()
        # print('moveDown')
        # GPIO.output(self.in1, True)
        # GPIO.output(self.in2, False)
        # time.sleep(2.5)
        # self.motorOff()
    
    def start(self):
        self.sio.run(self.app, host='0.0.0.0', debug=True)
        
    def quitFunction(self):
        print("quitting program")
        sys.exit()

server = Server()

# Event that triggers when a successful connection is made.
@server.sio.on('connect')
def connect(sid):
    pass
    # print("connect ", sid)

# Event that triggers when a command is received from the user.
@server.sio.on('relaycommand')
def relayCommand(command):
    if command == 'screenshot':
        server.take_screenshot()
    elif command == 'lights':
        server.toggle_lights()
    elif command == 'moveup':
        server.move_up()
    elif command == 'movedown':
        server.move_down()
    elif command == "quit":
        server.quitFunction()
        
def main():
    print('\n-----------------------------------------------------------\n')
    server.start()

if __name__ == "__main__":
    main()

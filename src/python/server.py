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

    def move_up(self):
        print('moveUp')

    def move_down(self):
        print('moveDown')

    def start_background_task(self, target):
        self.sio.start_background_task(target)
    
    def start(self):
        self.sio.run(self.app, host='0.0.0.0')
    
    def stop(self):
        self.sio.stop()

    # Event that triggers when a successful connection is made.
    def on_connect(self, sid):
        pass

    # Event that triggers when a command is received from the user.
    def on_relaycommand(self, command):
		self.start_background_task(self.bgtask) # TODO: Remove this
        if command == 'screenshot':
            self.take_screenshot()
        elif command == 'lights':
            self.toggle_lights()
        elif command == 'moveup':
            self.move_up()
        elif command == 'movedown':
            self.move_down()

def main():
    print('\n-----------------------------------------------------------\n')
    server = Server()
    server.start()

if __name__ == "__main__":
    main()

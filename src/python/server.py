from flask import Flask
from flask.logging import default_handler
from flask_socketio import SocketIO, Namespace
import sys

# import logging
# log = logging.getLogger('werkzeug')
# log.setLevel(logging.WARNING)

class Server(Namespace):
    namespace = '/'

    # app = Flask(__name__)
    # sio = SocketIO(app, cors_allowed_origins='*')

    def __init__(self, target):
        # self.app.logger.removeHandler(default_handler)
        self.app = Flask(__name__)
        self.sio = SocketIO(self.app, cors_allowed_origins='*')
        self.sio.on_namespace(self)
        self.callback = target

    # Function used to send a socket.io event for the GPS coordinates.
    def relay_gps_data(self, lat, lon):
        self.sio.emit('relaydata', 'Latitude: {}   Longitude: {}'.format(lat, lon))

    def on_connect(sid):
        print('Connected. ({})'.format(sid))

    def on_relaycommand(self, command):
        self.callback(command)

    def on_relaydata(self, data):
        print('on_relaydata')
    
    def start(self):
        self.sio.run(self.app, host='0.0.0.0', debug=True)
        
    def stop(self):
        self.sio.stop()
        
def main():
    print('\n-----------------------------------------------------------\n')
    server.start()

if __name__ == "__main__":
    main()

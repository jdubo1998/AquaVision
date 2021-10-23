from flask import Flask
from flask_socketio import SocketIO

# Wrapper class that will incorporate all needed functions and members in order to work as a translate module.
class Server:
    def __init__(self):
        self.app = Flask(__name__)
        # self.app.config['SECRET_KEY'] = 'secret'
        self.sio = SocketIO(self.app, cors_allowed_origins='*')

    def relay_gps_data(self):
        self.sio.emit('relaydata', )

    def take_screenshot(self):
        print('takeScreenshot')

    def toggle_lights(self):
        print('toggleLights')

    def move_up(self):
        print('moveUp')

    def move_down(self):
        print('moveDown')
    
    def start(self):
        self.sio.run(self.app, host='0.0.0.0', debug=True)

server = Server()

# Event that triggers when a successful connection is made.
@server.sio.on('connect')
def connect(sid):
    pass

# Event that triggers when a command is received from the user.
@server.sio.on('relaycommand')
def relay_command(command):
    if command == 'screenshot':
        server.take_screenshot()
    elif command == 'lights':
        server.toggle_lights()
    elif command == 'moveup':
        server.move_up()
    elif command == 'movedown':
        server.move_down()

def main():
    print('\n-----------------------------------------------------------\n')
    server.start()

if __name__ == "__main__":
    main()

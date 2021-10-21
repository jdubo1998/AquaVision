from flask import Flask
from flask_socketio import SocketIO, emit

# Wrapper class that will incorporate all needed functions and members in order to work as a translate module.
class TranslateModule:
    def __init__(self):
        self.app = Flask(__name__)
        # self.app.config['SECRET_KEY'] = 'secret'
        self.sio = SocketIO(self.app, cors_allowed_origins='*')

    def takeScreenshot(self):
        print('takeScreenshot')

    def toggleLights(self):
        print('toggleLights')

    def moveUp(self):
        print('moveUp')

    def moveDown(self):
        print('moveDown')
    
    def start(self):
        self.sio.run(self.app, host='0.0.0.0', debug=True)

translator = TranslateModule()

# Event that triggers when a successful connection is made.
@translator.sio.on('connect')
def connect(sid):
    pass
    # print("connect ", sid)

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
    translator.start()

if __name__ == "__main__":
    main()

from flask import Flask
import socketio

class AquaVisionServer:
    def __init__(self):
        self.sio = socketio.Server(async_mode='threading')
        self.app = Flask(__name__)
        self.app.wsgi_app = socketio.WSGIApp(self.sio, self.app.wsgi_app)
    
    def start(self):
        self.app.run()

server = AquaVisionServer()

def main():
    server.start()

@server.sio.event
def connect(sid, environ):
    print("connect ", sid)

if __name__ == "__main__":
    main()
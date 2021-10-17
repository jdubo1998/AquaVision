from flask import Flask
from flask_cors import CORS
import socketio
import sys 

class AquaVisionServer:
    def __init__(self):
        self.sio = socketio.Server(async_mode='threading')
        self.app = Flask(__name__)
        CORS(self.app, origins=['*'])
        self.app.wsgi_app = socketio.WSGIApp(self.sio, wsgi_app=self.app.wsgi_app, static_files={'/':'test.html'})
    
    def start(self, h):
        self.app.run(host=h, debug=True)

server = AquaVisionServer()

def main():
    host = '0.0.0.0'

    if (len(sys.argv) > 1):
        if (sys.argv[1] == '1'):
            host = ''
        else:
            host = sys.argv[1]
    
    server.start(host)

@server.sio.event
def connect(sid, environ):
    print("connect ", sid)

if __name__ == "__main__":
    main()
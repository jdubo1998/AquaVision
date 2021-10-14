import socketio

sio = socketio.Server()
app = socketio.WSGIApp(sio)

@sio.event
def connect(sid, environ, auth):
    print('connect ', sid)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

@sio.on('relayData')
def relayData():
    print('Data relayed.')

while True:
    command = input('Command: ')
    sio.emit('relayCommand', {'data': command})
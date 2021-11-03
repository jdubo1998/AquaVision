import re
from server import Server
from gpsreader import GPSReader
from threading import Thread

server = None
reader = None

def start_bg_task():
    global reader
    if reader == None:
		# Creates a new GPS reader, the target is a callback function which takes 2 arguments: latitude and longitude.
        reader = GPSReader(target=server.relay_gps_data)
    reader.start()

def main():
    global server
    global reader
    try:
        if server == None:
            server = Server(target=start_bg_task)

        server.start()

    except KeyboardInterrupt:
        server.stop()
        reader.stop()

if __name__ == '__main__':
    main()
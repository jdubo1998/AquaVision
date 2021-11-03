from serial import Serial
from serial.serialutil import SerialException
from pynmeagps import NMEAReader
from pynmeagps.exceptions import NMEAStreamError
from io import BufferedReader

class GPSReader:
    def __init__(self, port='/dev/ttyAMA0', baudrate=9600, timeout=3, target=None):
        self._serial = Serial(port, baudrate, timeout=timeout)
        self._nmea_reader = NMEAReader(BufferedReader(self._serial), nmeaonly=True)
        self.running = False
        self.callback = target

	# Starts a while loop. Currently the loop is only used to get the coordinates once.
    def start(self):
        self.running = True

        while self.running:
            try:
                if self._serial.in_waiting:
                    (data, nmea_msg) = self._nmea_reader.read()
                    if nmea_msg.msgID == 'RMC':
                        if self.callback != None:
							# Sends the coordinates to the callback function.
                            self.callback(nmea_msg.lat, nmea_msg.lon)
                            self.running = False # Exits loop once coordinates are sent. Remove this if we create a polling loop.
            except:
                continue
    
	def set_callback(self, target):
        self.callback = target

    def stop(self):
        if self.running:
            self.running = False

def _callback(lat, lon):
    print('Latitude: {}   Longitude: {}'.format(lat, lon))

if __name__ == '__main__':
    reader = GPSReader(target=_callback)
    reader.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        reader.stop()
from serial import Serial
from pynmeagps import NMEAReader, exceptions
from io import BufferedReader
from threading import Thread

class GPSReader:
    def __init__(self, port='/dev/ttyAMA0', baudrate=9600, timeout=3):
        self._serial = Serial(port, baudrate, timeout=timeout)
        self._nmea_reader = NMEAReader(BufferedReader(self._serial), nmeaonly=True)
        self._thread = Thread(target=self._start_thread)
        self.running = False

    def start(self):
        if not self.running:
            self._thread.start()

    def _start_thread(self):
        while self.running:
            try:
                if self._serial.in_waiting:
                    (data, nmea_msg) = self._nmea_reader.read()
                    if nmea_msg.msgID == 'RMC' or nmea_msg.msgID == 'GLL' or nmea_msg.msgID == 'GGA':
                        self.send_gps_data(nmea_msg.lon, nmea_msg.lat)
            except exceptions.NMEAStreamError:
                continue
    
    def send_gps_data(self, lon, lat):
        print('Longitude: {}     Lattitude: {}'.format(lon, lat))

    def stop(self):
        if self.running:
            self.running = False
            self._thread.join()

if __name__ == '__main__':
    reader = GPSReader()
    reader.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        reader.stop()
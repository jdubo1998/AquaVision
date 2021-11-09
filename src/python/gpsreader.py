from serial import Serial
from pynmeagps import NMEAReader
from threading import Thread
from io import BufferedReader

class GPSReader:
    def __init__(self, port='/dev/ttyACM0', baudrate=9600, timeout=3):
        self._serial = Serial(port, baudrate, timeout=timeout)
        self._nmea_reader = NMEAReader(BufferedReader(self._serial), nmeaonly=True)
        self.reader_thread = Thread(target=self._start_reader_thread)
        self.reading = False
        self.lat = 0.0
        self.log = 0.0

	# Starts a while loop. Currently the loop is only used to get the coordinates once.
    def _start_reader_thread(self):
        while self.reading:
            try:
                if self._serial.in_waiting:
                    data, nmea_msg = self._nmea_reader.read()
                    if nmea_msg.msgID == 'RMC':
                        self.lat = nmea_msg.lat
                        self.log = nmea_msg.lon
            except:
                continue

    def get_coor(self):
        return self.lat, self.log

    def start(self):
        if not self.reading:
            self.reading = True
            self.reader_thread.start() 

    def stop(self):
        if self.reading:
            self.reading = False
        if self.reader_thread.is_alive():
        	self.reader_thread.join()

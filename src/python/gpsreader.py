from serial import Serial
from pynmeagps import NMEAReader
from threading import Thread
from io import BufferedReader

class GPSReader:
    def __init__(self, port='/dev/ttyACM0', baudrate=9600, timeout=3):
        self._serial = Serial(port, baudrate, timeout=timeout)
        self._nmea_reader = NMEAReader(BufferedReader(self._serial), nmeaonly=True)
        self.reader_thread = None
        self.reading = False
        self.lat = '30.615789'
        self.lon = '-96.336980'

	# Starts a while loop. Currently the loop is only used to get the coordinates once.
    def _start_reader_thread(self):
        self.reading = True

        while self.reading:
            try:
                if self._serial.in_waiting:
                    data, nmea_msg = self._nmea_reader.read()
                    if nmea_msg.msgID == 'RMC' and nmea_msg.lat and nmea_msg.lon:
                        self.lat = nmea_msg.lat
                        self.lon = nmea_msg.lon
                        break
            except:
                continue
        
        self.reading = False

    def get_coor(self):
        return self.lat, self.lon

    def read(self):
        self._start_reader_thread()

    def read_async(self):
        if not self.reading:
            self.reader_thread = Thread(target=self._start_reader_thread)
            self.reader_thread.start()

    def stop(self):
        if self.reading:
            self.reading = False

        if not self.reader_thread == None:
            if self.reader_thread.is_alive():
                self.reader_thread.join()

if __name__ == '__main__':
    reader = GPSReader()
    reader.read()

    try:
        while True:
            reader.read_async()

            lat, lon = reader.get_coor()

            if not lat == '' or not lon == '':
                print('{}   {}'.format(lat, lon))

    except KeyboardInterrupt:
        pass

    reader.stop()
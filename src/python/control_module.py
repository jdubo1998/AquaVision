import sys
from struct import pack, unpack
from lora_radio import LoRaRadio
from gpsreader import GPSReader
from camera_controller import CameraController
from time import sleep

class ControlModule():
    def __init__(self):
        self.radio = LoRaRadio(3, 5, self.interpret_lora_message)
        self.gps = GPSReader()
        self.camera = CameraController()
        self.tm_addr = 4

    # Interprets a received message and runs the appropriate function based on the contents.
    def interpret_lora_message(self, message):
        if 'mu' in message:
            self.camera.motor_up()
        elif 'md' in message:
            self.camera.motor_down()
        elif 'tl' in message:
            self.camera.toggle_lights()
        elif 'ss' in message:
            self.camera.take_screenshot()
        elif message.__contains__('exit'):
            self.running = False

    def _loop(self):
        while self.running:
            self.radio.send_message('hs', self.tm_addr)
            sleep(3)

            lat, lon = self.gps.get_coor()
            self.radio.send_message('gps {} {}'.format(lat, lon), self.tm_addr)
            self.gps.read_async()
            sleep(3)

        self.stop()

    def start(self):
        self.running = True
        self._loop()

    def stop(self):
        self.radio.close()
        self.gps.stop()
        sys.exit(0)

if __name__ == '__main__':
    controller = ControlModule()
    controller.start()

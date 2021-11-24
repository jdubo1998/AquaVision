import sys
from struct import pack, unpack
from lora_radio import LoRaRadio
# from gpsreader import GPSReader
from camera_controller import CameraController
from time import sleep

class ControlModule():
    def __init__(self):
        self.radio = LoRaRadio(3, 5, self.interpret_lora_message)
        # self.gps = GPSReader()
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
        elif 'gps' in message:
            print('Send GPS data.')
            # self.radio.set_mode(0)
            # lat, log = self.gps.get_coor()

            # self.radio.send_message('gps {:.6f} {:.6f}'.format(lat, log), self.tm_addr)

            # self.radio.set_mode(1)
        elif 'exit' in message:
            self.running = False

    def _loop(self):
        while self.running:
            # self.gps.read_async()
            self.radio.send_message('hs', self.tm_addr)
            sleep(5)

        self.stop()

    def start(self):
        self.running = True
        self._loop()

    def stop(self):
        self.radio.close()
        # self.gps.stop()
        sys.exit(0)

if __name__ == '__main__':
    controller = ControlModule()
    controller.start()

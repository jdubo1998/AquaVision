import sys
from struct import pack, unpack
from lora_radio import LoRaRadio
from gpsreader import GPSReader
from camera_controller import CameraController
from time import sleep

class ControlModule():
    def __init__(self):
        self.radio = LoRaRadio(3, 5, self.interpret_lora_message)
        self.radio.set_mode(1)
        self.gps = GPSReader()
        self.camera = CameraController()

    # Interprets a received message and runs the appropriate function based on the contents.
    def interpret_lora_message(self, message):
        send_addr = 4

        if message.__contains__('mu'):
            self.camera.motor_up()
        elif message.__contains__('md'):
            self.camera.motor_down()
        elif message.__contains__('tl'):
            self.camera.toggle_lights()
        elif message.__contains__('ss'):
            self.camera.take_screenshot()
        elif message.__contains__('gps'):
            self.radio.set_mode(0)
            lat, log = self.gps.get_coor()

            self.radio.send_message('{}{}'.format(hex(unpack('<I', pack('<f', lat))[0])[2:],hex(unpack('<I', pack('<f', log))[0])[2:]), send_addr)

            self.radio.set_mode(1)
    
        elif message.__contains__('exit'):
            self.running = False

    def _loop(self):
        while self.running:
            self.gps.read_async()
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

    try:
        controller.start()
    except KeyboardInterrupt:
        controller.stop()

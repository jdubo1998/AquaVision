import sys
from struct import pack, unpack
from lora_radio import LoRaRadio
from gpsreader import GPSReader
from camera_controller import CameraController

class ControlModule():
    def __init__(self):
        self.radio = LoRaRadio('0100', self.interpret_lora_message)
        self.gps = GPSReader()
        self.camera = CameraController()

        self.running = True
        self.loop()

    def loop(self):
        while self.running:
            pass

    # Interprets a received message and runs the appropriate function based on the contents.
    def interpret_lora_message(self, message):
        if message.__contains__('md'):
            self.camera.motor_down()
        elif message.__contains__('mu'):
            self.camera.motor_up()
        elif message.__contains__('ss'):
            self.camera.take_screenshot()
        elif message.__contains__('tl'):
            self.camera.toggle_lights()
        elif message.__contains__('gps'):
            self.radio.set_mode(0)
            lat, log = self.gps.get_coor()

            self.radio.send_bytes(
                '{}{}'.format(hex(unpack('<I', pack('<f', lat))[0])[2:],hex(unpack('<I', pack('<f', log))[0])[2:])
            )

            self.radio.set_mode(1)
    
        elif message.__contains__('quit'):
            self.quit()

    def quit(self):
        self.radio.close()
        self.gps.close()
        self.camera()

        sys.exit(0)
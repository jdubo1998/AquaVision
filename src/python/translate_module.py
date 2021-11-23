import sys
import screenshot
from lora_radio import LoRaRadio
from server import Server
from struct import pack, unpack
from time import sleep

class TranslateModule():
    def __init__(self):
        self.radio = LoRaRadio(3, 4, self._interpret_lora_message)
        self.server = Server(self._interpret_command)
        self.cm_addr = 5
        self.get_gps = False
        self.lat = 0.0
        self.log = 0.0

    def _interpret_command(self, command):
        if command == 'moveup':
            print("moveup")
            self.radio.send_message('mu', self.cm_addr)
        elif command == 'movedown':
            print("movedown")
            self.radio.send_message('md', self.cm_addr)
        elif command == 'lights':
            print("lights")
            self.radio.send_message('tl', self.cm_addr)
        elif command == 'screenshot':
            print("screenshot")
            screenshot.take_screenshot()
            # screenshot.release()
        elif command == 'getgps':
            print("getgps")
            self.get_gps = False
            self.radio.send_message('gps', self.cm_addr)
            while not self.get_gps:
                sleep(3)

            self.server.relay_gps_data(self.lat, self.log)
        elif command == 'exit':
            print("exit")
            self.radio.send_message('exit', self.cm_addr)
            self.exit()

    def _interpret_lora_message(self, message):
        if 'gps' in message:
            params = message.split(' ')

            self.lat = params[1]
            self.lat = params[2]
            
            self.radio.set_mode(0)
            self.get_gps = True

    def start(self):
        self.server.start()

    def exit(self):
        self.radio.close()
        self.server.stop()
        sys.exit(0)

if __name__ == '__main__':
    translator = TranslateModule()
    translator.start()

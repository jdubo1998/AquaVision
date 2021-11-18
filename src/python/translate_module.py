import sys
import screenshot
from lora_radio import LoRaRadio
from server import Server
from struct import pack, unpack

class TranslateModule():
    def __init__(self):
        self.radio = LoRaRadio(3, 4, self._interpret_lora_message)
        self.server = Server(self._interpret_command)
        self.cm_addr = 5
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
        elif command == 'getgps':
            print("getgps")
            self.server.relay_gps_data(self.lat, self.log)
            self.radio.send_message('gps', self.cm_addr)
            self.radio.set_mode(1)
        elif command == 'exit':
            print("exit")
            self.radio.send_message('exit', self.cm_addr)
            self.exit()

    def _interpret_lora_message(self, message):
        try:
            self.lat = unpack('!f', bytes.fromhex(message[:8]))[0]
            self.log = unpack('!f', bytes.fromhex(message[8:]))[0]
        except:
            pass

        self.radio.set_mode(0)

    def start(self):
        self.server.start()

    def exit(self):
        self.radio.close()
        self.server.stop()
        screenshot.exit()
        sys.exit(0)

if __name__ == '__main__':
    translator = TranslateModule()
    translator.start()

    # try:
    #     while True:
    #         i = input('> ')

    #         if i == 'mu':
    #             translator._interpret_command('moveup')
    #         elif i == 'md':
    #             translator._interpret_command('movedown')
    #         elif i == 'tl':
    #             translator._interpret_command('lights')
    #         elif i == 'ss':
    #             translator._interpret_command('screenshot')
    #         elif i == 'gps':
    #             translator._interpret_command('getgps')
    #         elif i == 'q':
    #             translator._interpret_command('exit')

    # except KeyboardInterrupt:
    #     pass

    translator.exit()

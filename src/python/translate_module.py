import sys
from lora_radio import LoRaRadio
from server import Server

class TranslateModule():
    def __init__(self):
        self.radio = LoRaRadio('0200', self._interpret_lora_message)
        self.server = Server(self._interpret_command)

    def _interpret_command(self, command):
        if command == 'moveup':
            self.radio.send_message('mu')
        elif command == 'movedown':
            self.radio.send_message('md')
        elif command == 'lights':
            self.radio.send_message('tl')
        elif command == 'screenshot':
            self.radio.send_message('ss')
        elif command == 'getgps':
            self.radio.send_message('gps')

    def _interpret_lora_message(self, message):
        print(message)
        self.radio.set_mode(0)
        # if message.__contains__():
        #     pass

    def start(self):
        self.server.start()

    def exit(self):
        self.radio.close()
        self.server.stop()
        sys.exit(0)

if __name__ == '__main__':
    translator = TranslateModule()
    translator.start()

    translator.exit()

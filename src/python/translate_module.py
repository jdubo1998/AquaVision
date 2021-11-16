import sys
import screenshot
from lora_radio import LoRaRadio
from server import Server

class TranslateModule():
    def __init__(self):
        self.radio = LoRaRadio('0200', self._interpret_lora_message)
        self.server = Server(self._interpret_command)

    def _interpret_command(self, command):
        if command == 'moveup':
            print("moveup")
            self.radio.send_message('md') # Swiched due to wiring.
        elif command == 'movedown':
            print("movedown")
            self.radio.send_message('mu') # Swiched due to wiring.
        elif command == 'lights':
            print("lights")
            self.radio.send_message('tl')
        elif command == 'screenshot':
            print("screenshot")
            screenshot.take_screenshot()
        elif command == 'getgps':
            print("getgps")
            self.radio.send_message('gps')
        elif command == 'exit':
            print("exit")
            self.radio.send_message('exit')
            self.exit()

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

from serial import Serial, PARITY_NONE
from serial.serialutil import SerialException
from threading import Thread

class LoRaRadio():
    def __init__(self, addr, port='/dev/serial0', baudrate=9600, timeout=0.5):
        self.ser = Serial(port, baudrate, timeout=timeout, parity=PARITY_NONE, stopbits=1)
        self.addr = addr
        self.recv_thread = Thread(target=self._recv_thread)
        self.open()

    # Writes to the serial port.
    def write_serial(self, command):
        self.ser.write(str.encode('{}\r\n'.format(command), encoding='utf-8'))

    # Quick method to send a message to another LoRa module.
    # FFFF is the broadcast address.
    def send_message(self, message, addr='FFFF'):
        # Converts message to an 8 byte hex array.
        message_hex = ''.join('{:02x}'.format(ord(c)) for c in i.ljust(10))

        self.write_serial('AT+SEND {},"{}"'.format(addr, message_hex))

    # Reads from the serial port.
    def read_serial(self):
        try:
            response = self.ser.readline()
            if response:
                self.interpret_response(response)
        except SerialException as e:
            print(e)

    # Interprets a received message and runs the appropriate function based on the contents.
    def interpret_response(self, response):
        s = str(response, 'utf-8', errors='ignore')

        if s.__contains__('md'):
            print('Move Down')
        elif s.__contains__('mu'):
            print('Move Up')
        elif s.__contains__('ss'):
            print('Screenshot')
        elif s.__contains__('tl'):
            print('Toggle Lights')
        elif s.__contains__('gps'):
            print('Get GPS')

    # Toggles between two modes: Receiving and Transmitting mode.
    def toggle_mode(self):
        if self.receiving:
            self.receiving = False
            
            self.write_serial('+++')
            self.write_serial('AT+SADDR {}'.format(self.addr))
            self.write_serial('AT+ROLE 1')
            self.write_serial('AT+USERMODE 0')

            self.ser.readline()
        else:
            self.receiving = True
            self.recv_thread.start()

    # Opens the serial port and sets the LoRa parameters to the default configuration.
    def open(self):
        self.receiving = True
        self.toggle_mode()
        
        if not self.ser.is_open:
            self.ser.open()

    # Closes the serial port and any thread that is polling for received data.
    def close(self):
        self.receiving = False
        self.ser.close()

    # Polls the serial port to read any messages received by the LoRa radio.
    def _recv_thread(self):
        while self.receiving:
            self.ser.write('AT+RECV\r\n'.encode('utf-8'))
            self.read_serial()

if __name__ == '__main__':
    # Creates a radio module with the address 0001.
    # The address is a 2-byte hexidecmial which uses this conversion: ABCD => CDAB
    radio = LoRaRadio('0100')

    try:
        while True:
            i = input('> ')

            if radio.receiving:
                if i == 'q':
                    radio.toggle_mode()
        
            else:
                if i == 'q':
                    break
                
                elif i == 'r':
                    radio.toggle_mode()

                elif i.__contains__('+'):
                    radio.write_serial('AT+{}'.format(i[1:]))
                    radio.read_serial()
                
                radio.send_message(i[:8])
    except KeyboardInterrupt:
        pass

    radio.close()

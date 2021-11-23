from serial import Serial, PARITY_NONE
from serial.serialutil import SerialException
import time
from threading import Thread
import os

class LoRaRadio():
    def __init__(self, network, addr, target, port='/dev/serial0', baudrate=115200, timeout=0.5):
        self.ser = Serial(port, baudrate, timeout=timeout, parity=PARITY_NONE, stopbits=1)
        self.receiving = False
        self.network = network
        self.addr = addr
        self.callback = target
        self.recv_thread = Thread(target=self._recv_thread)
        self.init()
        self.open()

    # Writes to the serial port.
    def write_serial(self, command, wait_for_ok=False):
        while True:
            self.ser.write(str.encode('{}\r\n'.format(command), encoding='utf-8'))
            r = self.read_serial()

            if not wait_for_ok:
                break

            if r is not None and '+OK' in r:
                break

    # Quick method to send a message to another LoRa module.
    # FFFF is the broadcast address.
    def send_message(self, message, addr=11):
        # Converts message to an 8 byte hex array.
        # message_hex = ''.join('{:02x}'.format(ord(c)) for c in message.ljust(8))
        self.write_serial('AT+SEND={},{},{}'.format(str(addr), str(len(message)), str(message)), wait_for_ok=True)

    # def send_message(self, bytes, addr=11):
    #     self.write_serial('AT+SEND={},"{}"'.format(addr, bytes))

    # Reads from the serial port.
    def read_serial(self):
        try:
            r = self.ser.readline()
            # print(r)
            if r:
                response = str(r, 'utf-8', errors='ignore')
                self.callback(response)
                return response
        except SerialException as e:
            print(e)

    def wait_for_ok(self):
        while True:
            self.ser.write(str.encode('AT\r\n', encoding='utf-8'))
            r = self.ser.readline()
            response = str(r, 'utf-8', errors='ignore')

            if response == '+OK\r\n':
                break

            print(r)
            if response == '+ERR=4\r\n':
                time.sleep(1)

    def init(self):
        self.write_serial('AT+NETWORKID={}'.format(self.network), wait_for_ok=True)
        self.write_serial('AT+ADDRESS={}'.format(self.addr), wait_for_ok=True)
        self.write_serial('AT+MODE=0', wait_for_ok=True)

        self.ser.readline()

    # Toggles between two modes: Receiving and Transmitting mode.
    def set_mode(self, mode):
        if mode == 0:
            self.receiving = False
            if self.recv_thread.is_alive():
                self.recv_thread.join()
            
        elif mode == 1:
            print('In receiving mode.')
            if not self.receiving:
                self.receiving = True
                self.recv_thread = Thread(target=self._recv_thread)
                self.recv_thread.start()

    # Opens the serial port and sets the LoRa parameters to the default configuration.
    def open(self):
        self.set_mode(0)
        
        if not self.ser.is_open:
            self.ser.open()

    # Closes the serial port and any thread that is polling for received data.
    def close(self):
        self.receiving = False
        if self.recv_thread.is_alive():
            self.recv_thread.join()
        self.ser.close()

    # Polls the serial port to read any messages received by the LoRa radio.
    def _recv_thread(self):
        while self.receiving:
            # self.ser.write('AT+RECV\r\n'.encode('utf-8'))
            self.read_serial()

def print_response(response):
    if not response == str(b'A\x00\x01\x01', 'utf-8'):
        # pass
        print(response)

if __name__ == '__main__':
    # network = input('Network: ')
    # addr = input('Address: ')
    # send_addr = input('Other Device: ')
    if os.uname()[1] == 'JD-RaspberryPi':
        print('addr: 4')
        addr = 4
        send_addr = 5
    else:
        print('addr: 5')
        addr = 5
        send_addr = 4

    addr = 4
    send_addr = 5

    radio = LoRaRadio(3, addr, print_response)

    try:
        while True:
            i = input('> ')

            if radio.receiving:
                if i == 'q':
                    radio.set_mode(0)
        
            else:
                if i == 'q':
                    break
                
                elif i == 'r':
                    radio.set_mode(1)

                elif i.__contains__('+'):
                    radio.write_serial('AT+{}'.format(i[1:]))
                
                radio.send_message(i[:8], send_addr)
    except KeyboardInterrupt:
        pass

    radio.close()

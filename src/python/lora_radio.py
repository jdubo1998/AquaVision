
from serial import Serial, PARITY_NONE
from serial.serialutil import SerialException
import time
from threading import Thread
import os
import sys

class LoRaRadio():
    def __init__(self, network, addr, target, port='/dev/serial0', baudrate=115200, timeout=0.5):
        self.ok = False
        self.receiving = False
        self.network = network
        self.addr = addr
        
        self.ser = Serial(port, baudrate, timeout=timeout, parity=PARITY_NONE, stopbits=1)
        self.open()

        self.callback = target
        self.start_recv_thread()
        
        self.reset()

    # Writes directly to the serial port, used for AT commands.
    def write_serial(self, command, wait_for_ok=False):
        while True:
            self.ser.write(str.encode('{}\r\n'.format(command), encoding='utf-8'))
            # r = self.read_serial()

            if not wait_for_ok:
                break

            # if r is not None and '+OK' in r:
            if self.ok:
                self.ok = False
                break
            
            time.sleep(1)

    # Sends a message to the given address using the LoRa radio.
    def send_message(self, message, addr=11):
        self.write_serial('AT+SEND={},{},{}'.format(str(addr), str(len(message)), str(message)), wait_for_ok=True)

    # Reads from the serial port.
    def read_serial(self):
        try:
            r = self.ser.readline()
            if r:
                response = str(r, 'utf-8', errors='ignore')
                if 'OK' in response:
                    self.ok = True
                self.callback(response)
                # return response
        except SerialException as e:
            print(e)

    def reset(self):
        self.write_serial('AT+NETWORKID={}'.format(self.network), wait_for_ok=True)
        self.write_serial('AT+ADDRESS={}'.format(self.addr), wait_for_ok=True)
        self.write_serial('AT+MODE=0', wait_for_ok=True)

    def start_recv_thread(self):
        self.recv_thread = Thread(target=self._recv_thread)
        self.recv_thread.start()

    # Opens the serial port and sets the LoRa parameters to the default configuration.
    def open(self):
        # self.set_mode(0)
        
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
        self.receiving = True

        while self.receiving:
            # self.ser.write('AT+RECV\r\n'.encode('utf-8'))
            self.read_serial()

def print_response(response):
    if not 'OK' in response:
        print('\n{}>'.format(response), end='')

if __name__ == '__main__':
    if len(sys.argv) == 2:
        addr = int(sys.argv[1])
        send_addr = 4
    elif len(sys.argv) == 3:
        addr = int(sys.argv[1])
        send_addr = int(sys.argv[2])
    else:
        addr = 5
        send_addr = 4

    print('Starting radio at addr: {}, sending to addr: {}'.format(addr, send_addr))
    radio = LoRaRadio(3, addr, print_response)

    try:
        while True:
            i = input('> ')

            if i == 'q':
                break

            if '+' in i:
                radio.write_serial('AT+{}'.format(i[1:]))
                continue
                
            radio.send_message(i, send_addr)
    except KeyboardInterrupt:
        pass

    radio.close()

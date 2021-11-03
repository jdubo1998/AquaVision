from serial import Serial
from serial.serialutil import Timeout

serial = Serial('/dev/ttyAMA0', 9600, timeout=10)

while True:
    i = input('Input: ')

    if i == 'q':
        break
    
    print('Sending {}'.format(i))

    serial.write(str.encode(i))

    print('Reading {}'.format(serial.read(10)))
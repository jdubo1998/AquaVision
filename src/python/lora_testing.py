from serial import Serial, PARITY_NONE
from serial.serialutil import SerialException
# from serial.threaded import ReaderThread, LineReader
import time
from threading import Thread

ser = Serial('/dev/serial0', 9600, timeout=3, parity=PARITY_NONE, stopbits=1)
if not ser.is_open:
    ser.open()
    print('Serial port is opened.')

def read_serial():
    try:
        # ser.write('AT+RECV\r\n'.encode('utf-8'))
        response = ser.readline()
        if response:
            print('Response: ' + str(response, 'utf-8', errors='ignore'))
    except SerialException as e:
        pass
        # print(e)

def startReaderThread():
    while ser.is_open:
        read_serial()
        # time.sleep(1)

    print('Serial has been closed.')
            
# readerThread = Thread(target=startReaderThread)
# readerThread.start()

while True:
    try:
        # time.sleep(1)
        i = input('Message: ')

        if i == '+':
            ser.write(str.encode('+++\r\n', encoding='utf-8'))
            read_serial()

        elif i[0] == 'b':
            ser.write('AT+BAUD{}\r\n'.format(i[1:]).encode('utf-8'))
            read_serial()

        elif i[0] == 'm':
            ser.write('AT+USERMODE{}\r\n'.format(i[1:]).encode('utf-8'))
            read_serial()

        elif i == 'r':
            # ser.write('AT+RECV\r\n'.encode('utf-8'))
            read_serial()
        
        elif i[0] == 't':
            ser.write('AT+ROLE{}\r\n'.format(i[1:]).encode('utf-8'))
            read_serial()

        else:
            # message = ''.join('{:02x}'.format(ord(c)) for c in i.ljust(10))
            
            # ser.write('{}\r\n'.format(i).encode('utf-8'))
            ser.write('AT+SEND 0001,"{}"\r\n'.format(message).encode('utf-8'))
            read_serial()
    
    except KeyboardInterrupt:
        break

if ser.is_open:
    ser.close()
    print('\nSerial closed.')
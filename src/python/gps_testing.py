from serial import Serial
from pynmeagps import NMEAReader, exceptions
# from pyubx2 import UBXReader, exceptions
from io import BufferedReader

serial_object = Serial('/dev/ttyAMA0', 9600, timeout=3)
# ubr = UBXReader(BufferedReader(serial_object), ubxonly=True)
nmr = NMEAReader(BufferedReader(serial_object), nmeaonly=True)

while serial_object:
    try:
        if serial_object.in_waiting:
            (raw_data, parsed_data) = nmr.read()
            if parsed_data.msgID == 'RMC' or parsed_data.msgID == 'GLL' or parsed_data.msgID == 'GGA':
                print(str(parsed_data.lon) + '   ' + str(parsed_data.lat))
    except exceptions.NMEAStreamError:
        print('Error')
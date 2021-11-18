from struct import pack, unpack
import struct

lat = 15.262648256
log = 45.277884525

message = '{}{}'.format(hex(unpack('<I', pack('<f', lat))[0])[2:],hex(unpack('<I', pack('<f', log))[0])[2:])

print(message)

print(struct.unpack('!f', bytes.fromhex(message[:8]))[0])
print(struct.unpack('!f', bytes.fromhex(message[8:]))[0])
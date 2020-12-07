import machine
from network import Sigfox
import socket
import struct
import time

# init Sigfox for RCZ2 (USA, Mexico, Brazil)
# other zones:
# RCZ1: Europe, Oman, South Africa
# RCZ2: USA, Mexico, Brazil
# RCZ3: Japan
# RCZ4: Australia, New Zealand, Singapore, Taiwan, Hong Kong, Columbia, Argentina
sigfox = Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ2)

# create a Sigfox socket
s = socket.socket(socket.AF_SIGFOX, socket.SOCK_RAW)

# make the socket blocking
s.setblocking(True)

# configure it as uplink only
s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, False)

adc = machine.ADC()
apin = adc.channel(pin='P16')

while True:
    millivolts = apin.voltage()
    degC = (millivolts - 500.0) / 10.0
    degF = ((degC * 9.0) / 5.0) + 32.0
    
    print(millivolts)
    print(degC)
    print(degF)
    
    # Convert to byte array for transmission
    raw = bytearray(struct.pack("f", degC))
    
    s.send(raw)
    print("Bytes sent, sleeping for 15 minutes.")
    
    time.sleep(900)

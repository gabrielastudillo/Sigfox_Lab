import machine
from network import Sigfox
import socket
import struct
import time
import pycom
from pysense import Pysense

#from LIS2HH12 import LIS2HH12
from SI7006A20 import SI7006A20
#from LTR329ALS01 import LTR329ALS01
#from MPL3115A2 import MPL3115A2,ALTITUDE,PRESSURE

pycom.heartbeat(False)
pycom.rgbled(0x0A0A08) # white

py = Pysense()

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

while True:
    si = SI7006A20(py)
    tempC = si.temperature()
    print(tempC)
    
    # Convert to byte array for transmission
    raw = bytearray(struct.pack("f", tempC))
    
    s.send(raw)
    print("Bytes sent, sleeping for 15 minutes")
    
    time.sleep(900)

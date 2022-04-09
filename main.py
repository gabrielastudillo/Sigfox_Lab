import machine
from network import Sigfox
import socket
import struct
import time
import pycom
import ubinascii
from pycoproc_1 import Pycoproc
from LIS2HH12 import LIS2HH12
from SI7006A20 import SI7006A20
from LTR329ALS01 import LTR329ALS01
from MPL3115A2 import MPL3115A2,ALTITUDE,PRESSURE

pycom.heartbeat(False)
pycom.rgbled(0x0A0A08) # white
pysense = Pycoproc(Pycoproc.PYSENSE)
mpl3115a2 = MPL3115A2() # Barometric Pressure Sensor with Altimeter
ltr329als01 = LTR329ALS01() # Digital Ambient Light Sensor
si7006a20 = SI7006A20() # Humidity and Temperature sensor
lis2hh12 = LIS2HH12() # 3-Axis Accelerometer

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
    voltage = pysense.read_battery_voltage()
    temperature = mpl3115a2.temperature()
    pressure = mpl3115a2.pressure()
    light = ltr329als01.light()[0]
    humidity = si7006a20.humidity()
    roll = lis2hh12.roll()
    pitch = lis2hh12.pitch()
    # Debug sensor values
    print('voltage:{}, temperature:{}, pressure:{}, light:{}, humidity:{}, roll:{}, pitch:{}'.format(voltage, temperature, pressure, light, humidity, roll, pitch))
    # Convert to byte array for transmission
    clean_bytes = struct.pack(">ii",
        int(temperature * 100), # Temperature in celcius
        int(pressure * 100)) # Atmospheric pressure in bar
        #int(light * 100), # Light in lux
        #int(humidity * 100), # Humidity in percentages
        #int(roll * 100), # Roll in degrees in the range -180 to 180
        #int(pitch * 100), # Pitch in degrees in the range -90 to 90
        #int(voltage * 100)) # Battery voltage
    s.send(clean_bytes)
    print("Bytes sent, sleeping for 30 secs")
    time.sleep(30)
    

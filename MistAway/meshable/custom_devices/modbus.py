'''
Created on Aug 27, 2013

@author: lewiswight
'''
#!/usr/bin/env python
import minimalmodbus

instrument = minimalmodbus.Instrument('/dev/tty.usbserial-A800B7PQ', 1) # port name, slave address (in decimal)
instrument.debug = True
instrument.serial.port          # this is the serial port name
instrument.serial.baudrate = 9600   # Baud
instrument.serial.bytesize = 8
instrument.serial.stopbits = 1
instrument.serial.timeout  = 0.1 # seconds
instrument.address = 1
## Read temperature (PV = ProcessValue) ##
temperature = instrument.read_register(299, 0, functioncode=4) # Registernumber, number of decimals
print temperature

## Change temperature setpoint (SP) ##
NEW_TEMPERATURE = 0
instrument.write_register(401, NEW_TEMPERATURE, 0) # Registernumber, value, number of decimals for storage
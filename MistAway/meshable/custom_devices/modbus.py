'''
Created on Aug 27, 2013

@author: lewiswight
'''
#!/usr/bin/env python
import minimalmodbus

instrument = minimalmodbus.Instrument('/dev/cu.usbserial-A800B7PQ', 10) # port name, slave address (in decimal)
instrument.debug = True
instrument.serial.port          # this is the serial port name
instrument.serial.baudrate = 9600   # Baud
instrument.serial.bytesize = 8
instrument.serial.stopbits = 1
instrument.serial.timeout  = 5 # seconds
instrument.address = 1
print instrument.address
## Read temperature (PV = ProcessValue) ##
temperature = instrument.read_registers(299, 5, functioncode=4) # Registernumber, number of decimals
print temperature
"""
## Change temperature setpoint (SP) ##
#NEW_TEMPERATURE = 0
instrument.write_registers((256+32), [0000, 1]) # Registernumber, value, number of decimals for storage

temperature = instrument.read_registers(4, 3, functioncode=3) # Registernumber, number of decimals
print temperature"""
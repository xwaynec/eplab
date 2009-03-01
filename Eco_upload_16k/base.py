#! /usr/bin/python
# base.py - v0.0.1
# python program that handle the communication between base and eco
# sensor
# v0.0.1 targets on the UART interface

# import modules
import serial
# open a serial port
uart = serial.Serial('/dev/ttyUSB0', 19200)
str = ''
while 1:
	uart.write('A')
while 1: 
	c = uart.read()
	if c == '\n':
		print str
		str = ''
		continue
	str = str + c

uart.close()
a = 2
b = 4
print a + b

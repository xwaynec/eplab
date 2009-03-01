# eeprep.py
#
# This program 
#	1) parses the input hex file, 
# 	2) appends eeprom header bytes for nRF24E1,
# 	3) and write address-ordered hex into the output file
#	 (no instruction holes allowed in this version..)
#
# Author: Jiwon Hahn
#
# [code modified]
#	1) assume the code is compiled by Un*x or Windows system
#	When building code under windows, use Cygwin
#	2) modify the code to accept interrupt service routine
#	i.e., previous version assume that the code in HEX file
#	is continuous, however, interrupt vector is in fixed address
#	hence there exits some "holes" between the interrupt vector n
# 	and unused interrupt vector k, where k < n.
#
#	a easy way to fix this: fill the "holes" with 0xff
#
# Min-Hua Chen <orca.chen@gmail.com> 

# Specify the machine where sdcc is compiled
#SDCC = 'Linux'	#[Windows, MacOS, Linux]
# EEPROM header bytes for nRF24E1
#BYTE_0 = '03'	# EEPROM max: 1MHz, clk: 16MHz
BYTE_0 = '0B'	# EEPROM max: 0.5MHz, clk: 16MHz
BYTE_1 = '03'	# offset to start of user program

# Length of data per line in packed hex format
DLEN = 16


# data input/output in string format
def getchecksum(data):
	import binascii
	data = binascii.unhexlify(data)

	sum = 0
	for x in data:
		sum += ord(x)
	sum %= 256
	if sum:	
		sum = 0x100-sum
	return '%.2X' % sum


def load_hex(infile):
	'''read, extract data, sort by address, append header'''
	import binascii, os
	file = open(infile, 'r')
	all = file.read()
	file.close()
	# make sure that the windows trailing '\r\n' is eliminated.
	all = all.replace('\r\n', '\n')

	total = 0
	addr_data = []
	if os.name == 'posix' or os.name == 'nt':
		lines = all.split('\n')[:-1]
	else:
		print os.name, 'not supported!'
	
	for line in lines:
		# skip CRC check, trusting sdcc 
		lastbyte = -2

		count, addr, data = line[1:3], line[3:7], line[9:lastbyte]
		
		datalen = ord(binascii.unhexlify(count)) 
		total += datalen
		addr_data.append([addr, data])	
	addr_data.sort()

	datastr = ''
	dlen = 0
	for addr, data in addr_data:
		# if there exists a hole
		if (int(addr, 16) - dlen > 0):		
			datastr += ('%.2X' % 0xff) * (int(addr, 16) - dlen)
			datastr += data		
			dlen = int(addr, 16) + len(data) / 2
		else:
			datastr += data		
			dlen += len(data) / 2

	# since we fill the "holes" in our image, the length is changed
	# after we did this
	num256blocks = dlen/256
	header = BYTE_0 + BYTE_1 + '%.2X'%num256blocks
	
	datastr = header+datastr
	return datastr	


def write_hex(datastr, outfile):
	'''write a nicely packed, ordered hex file'''
	file = open(outfile, 'w')

	eof = 0
	address = 0	
	while not eof:
		addr = '%.4X' %address
		type = '00'
		if len(datastr) > DLEN*2:
			count = '%.2X' %DLEN
			data, datastr = datastr[0:32], datastr[32:]
			address += DLEN
		else:
			count = '%.2X' %(len(datastr)/2)
			data = datastr
			eof = 1

		line = '%s%s%s%s'%(count, addr, type, data)
		checksum = getchecksum(line)		
		file.write(':%s%s\n' %(line,checksum))
	
	file.write(':00000001FF\n')	
	file.close()


if __name__=='__main__':
	import sys
	if len(sys.argv) < 3:
		print 'python %s input.hex output.hex' %sys.argv[0]
		sys.exit(1)

	inf = sys.argv[1]
	outf = sys.argv[2]

	internal = load_hex(inf)
	write_hex(internal, outf)	

# eco_uart connection module
# Min-Hua Chen <orca.chen@gmail.com> 

import serial
import os
import sys
import struct
import prog_bar
import time
# max port number
MAXPORT = 10

class eco_uart:
	def __init__ (self, baud):		
		self.availablePort = []
		self.portCnt = 0
		# try to find correct serial port
		print "initializing serial port..."
		self.conn = 0
		if os.name == "posix":
			#self.port = "/dev/ttyUSB"
			self.port = "/dev/tty.SLAB_USBtoUART"
		elif os.name == "nt":
			self.port = "COM"
		else:
			print "OS %s is not supported" % os.name
			self.port = ""
		#for i in range(MAXPORT):
		#	try:
		#		self.uart = serial.Serial()
		#		self.uart.port = self.port 
		#		self.uart.baudrate = baud
		#		self.uart.timeout = None
		#		self.uart.open()
		#		self.uart.close()
		#		self.availablePort.append(i)
		#		#self.portCnt += 1
		#		#print "port %s%d opened" % (self.port, i)
		#		#break
		#	except:
		#		pass
				
		self.uart = serial.Serial()
		self.uart.port = self.port 
		self.uart.baudrate = baud
		self.uart.timeout = None
		self.uart.open()
		#if self.portCnt > 0:			
		#	input = 0
		#	while(input != 1):
		#		print "Available Ports:  ('q' to exit)"
		#		for j in range(self.portCnt):
		#			print "(%d) Port%d" %(j, self.availablePort[j])
		#		ch = raw_input("Eco:$ ")
		#		if(ch == "q"):
		#			sys.exit()
		#		else:					
		#			try:
		#				num = ord(ch) - 48
		#				
		#				if  num < self.portCnt and num > -1:
		#					input = 1
		#				else:
		#					print "Invalid input"
		#			except:
		#				print "Invalid input"
		#	try:
		#		self.uart = serial.Serial()			
		#		self.uart.port = self.port + `self.availablePort[num]`
		#		self.uart.baudrate = baud			
		#		self.uart.timeout = None			
		#		self.uart.open()
		#		
		#		print "port %s%d opened" % (self.port, self.availablePort[num])			
		#	except:
		#		print "Port not open, Goodbye!"
		#else:
		#	print "No available ports"
		#	sys.exit()

			
			
		# verifying data buffer
		self.dump_data = ""
		self.ori_data = ""
		if not self.uart:
			print "serial port %s%d-%d are not available" % \
				(self.port, 0, MAXPORT)
			sys.exit(1)
	def close (self):
		print "serial port closed" 
		self.uart.close()
	# send a communication testing string to eco and receive an ack
	def eco_test (self):
		print "establishing connection"
		self.uart.write("A")
		if self.uart.read() == "Z":
			self.conn = 1
			print "connection established"
		else:
			self.conn = 0
			print "connection failed"
	# dump image
	def eco_dump (self, root, isPrint, fm_type, fsize):
		now = time.time()
		if isPrint == 1:
			b_bar = prog_bar.pb(root, "dump image")
		if fm_type == "flash":
			self.uart.write("d")
		elif fm_type == "eeprom":
			self.uart.write("D")

		# send data length		
                high = fsize >> 8
                low = fsize & 0xff
                high = struct.pack("B", high)
                low = struct.pack("B", low)
                self.uart.write(high)
                self.uart.write(low)

		msg = ""
		c = ""
		self.dump_data = ""
		tmp_msg = ""
		turn = fsize / 16
		for i in range(turn):
		  	OO_count = 0
			ff_count = 0
			display = 1
			for j in range(18):
				c = self.uart.read()
				v = struct.unpack("B", c)
				if j == 0:
					msg = msg + "0000"
				if j == 2:
					 msg = msg + ": "
				if j < 2:
					msg = msg + "%02X" % v[0]
				else:
					msg = msg + "%02X " % v[0]
				if j >= 2:
					self.dump_data += "%02X" % v[0]
					if ("%02X" % v[0]) == "FF":
						ff_count = ff_count + 1
					elif ("%02X" % v[0]) == "00":
						OO_count = OO_count + 1;
					if OO_count == 16:
						display = 0
						tmp_msg = tmp_msg + "0x00 "
					elif ff_count == 16:
						display = 0
						tmp_msg = tmp_msg + "0xFF "
							
			if isPrint == 1:
				if display == 1:
			 		print msg
				if (i%5) == 0:
			 		b_bar.update(1.0 * i / turn)
			msg = ""
		if isPrint == 1:
		  	b_bar.close()
  			print tmp_msg
		prev = now
		now = time.time()
		if isPrint == 1:
		  	print "time elapsed: %.3f s" % (now - prev)
	# upload a hex file to the target Eco sensor
	# @image:  hex file
	# @root: root window
	def upload_hex (self, image, root, fm_type, fsize):
		import binascii
                now = time.time()
                print "upload the hex file"
                #read full file
		fin = open(image, "r")
                text = fin.read()
       		fin.close()
		
		b_bar = prog_bar.pb(root, "upload")
                total_data_len = 0
                self.ori_data = ""
		bin_data = ""
		#seperate file to lines
		if '\r' in text:
                	lines = text.split('\r\n')
        	else:
                	lines = text.split('\n')

        	for line in lines:
                	if line == '' or line[0] != ':':
                        	continue
                	data = line[1:] # discard ':'
                	bdata = binascii.unhexlify(data)     # hexstr=>bin
                	#do parsing
  			rec_len = struct.unpack("B", bdata[0])
			rec_type = struct.unpack("B", bdata[3])
			#end of hex
			if rec_type[0] == 01:
				break
			#read data, update total_data_len
  			total_data_len += rec_len[0]
			#store binary data
			for i in range(rec_len[0]):
				bin_data += bdata[4+i];

                
		send_data_len = 0
                len = fsize
                
		# send image to target sensor
		if fm_type == "eeprom":
                	self.uart.write("U")
		elif fm_type == "flash":
			self.uart.write("u")
                
  		# send data length
                high = total_data_len >> 8
                low = total_data_len & 0xff
                high = struct.pack("B", high)
                low = struct.pack("B", low)

                self.uart.write(high)
                self.uart.write(low)

		# send flash/eeprom size
                high = fsize >> 8
                low = fsize & 0xff
                high = struct.pack("B", high)
                low = struct.pack("B", low)
		
		self.uart.write(high)
		self.uart.write(low)


  		lc = total_data_len / 64
		lm = total_data_len % 64

  		#sen data to target sensor
  		for i in range(lc):
		  	for j in range(64):
                		self.uart.write(bin_data[i*64+j])
                		#b = self.uart.read()
                		b = struct.unpack("B",bin_data[i*64+j])
                		self.ori_data += "%02X" % b
			send_data_len += 64;
			b = self.uart.read()
			b_bar.update(1.0 * send_data_len / len)

		for j in range(lm):	
		  	self.uart.write(bin_data[lc*64+j])
			b = struct.unpack("B",bin_data[lc*64+j])
			self.ori_data += "%02X" % b
		
		send_data_len += lm;	
  		b = self.uart.read()
		b_bar.update(1.0 * send_data_len / len)


  		print "padding 0xFF"
		self.ori_data += "FF" * (len - send_data_len)

		for p in range(len - send_data_len):	
			b = self.uart.read()
			if b == "C":
				send_data_len += 64
				b_bar.update(1.0 * send_data_len / len)
			elif b == "D":
				break
		b_bar.close()
		prev = now
		now = time.time()
		print "time elapsed: %.3f s" % (now - prev)
  
        # upload a binary image to the target Eco sensor
        # @image: binary image
        # @root: root window
	def upload_bin (self, image, root, fm_type, fsize):
                now = time.time()
                print "upload the binary image"
                #read data
                f = open(image, "rb")
                data = f.read()
                f.close()

                b_bar = prog_bar.pb(root, "upload")
                data_len = 0
                tlen = fsize
                self.ori_data = ""

                # send image to target sensor
                if fm_type == "eeprom":
                        self.uart.write("U")
                elif fm_type == "flash":
                        self.uart.write("u")


                #data length
		dlen = len(data)
                high = dlen  >> 8
                low = dlen & 0xff
                high = struct.pack("B", high)
                low = struct.pack("B", low)
                
		self.uart.write(high)
                self.uart.write(low)

		# flash/eeprom size
                high = fsize  >> 8
                low = fsize & 0xff
                high = struct.pack("B", high)
                low = struct.pack("B", low)

		self.uart.write(high)
		self.uart.write(low)

  		lc = dlen / 64
  		lm = dlen % 64

                #send data
                for i in range(lc):
			for j in range(64):
                        	self.uart.write(data[i * 64 + j])
                        	#b = self.uart.read()
                        	b = struct.unpack("B", data[i * 64 + j])
                        	self.ori_data += "%02X" % b
			data_len += 64
  			b = self.uart.read()
                        b_bar.update(1.0 * data_len / tlen)
		
		for j in range(lm):
		  	self.uart.write(data[lc * 64 + j])
			b = struct.unpack("B", data[lc * 64 + j])
			self.ori_data += "%02X" % b

		data_len += lm
		b = self.uart.read()
		b_bar.update(1.0 * data_len / tlen)

  		print "padding 0xFF"
                self.ori_data += "FF" * (tlen - data_len)
                for p in range(tlen - data_len):
                        b = self.uart.read()
                        if b == "C":
                                data_len += 64
                                b_bar.update(1.0 * data_len / tlen)
                        elif b == "D":
                                break
                b_bar.close()
                prev = now
                now = time.time()
                print "time elapsed: %.3f s" % (now - prev)

	# verify - verify written data
	def verify (self, root, fm_type, fsize):
	  	now = time.time()
		if self.ori_data == "":
			print "binary image should be uploaded first"
			return
		# read written data
		self.eco_dump(root,1,fm_type,fsize)
		if self.ori_data == self.dump_data:
			print "result: consistent data"
		else:
			print "inconsistent data, dumping buffer"
			print "original data:"
			print self.ori_data
			print "dump data:"
			print self.dump_data
			print "result: error - inconsistent data"
		prev = now
		now = time.time()
              	print "time elapsed: %.3f s" % (now - prev)

	# blink - blink LED
	def blink (self):
		self.uart.write("B")
	# flash_erase - erase whole flash memory
	def flash_erase (self, root):
		now = time.time()
		self.uart.write("F")
		b = self.uart.read()
		if b == "D":
			print "flash erased"
		prev = now
		now = time.time()
		print "time elapsed: %.3f s" % (now - prev)
	# erase - erase whole EEPROM
	def erase (self, root, fsize):
		now = time.time()
		b_bar = prog_bar.pb(root, "erasing")
		total = fsize
		cur = 0
		self.uart.write("E")

                # flash/eeprom size
                high = fsize  >> 8
                low = fsize & 0xff
                high = struct.pack("B", high)
                low = struct.pack("B", low)
		self.uart.write(high)
		self.uart.write(low)

		while 1:
			b = self.uart.read()
			if b == "C":
				cur += 64
				b_bar.update(1.0 * (cur - 64)/ total)
			elif b == "D":
				print "EEPROM erased"
				break
		prev = now
		now = time.time()
		b_bar.close()
		print "time elapsed: %.3f s" % (now - prev)
	# status - get status register
	def status (self, root):
	  	self.uart.write("S")
		b = self.uart.read()
		b = struct.unpack("B", b)
		print "0x" + "%02X" % b



#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import re
import urllib
import zipfile
import struct
import time
import binascii

print "usage: convert.py [input file] [output file]"

if len(sys.argv) < 3:

	input_file = "paging2.hex"
	output_file = "paging3.hex"
	
else:
	input_file = sys.argv[1]
	output_file = sys.argv[2]


class convert:
    def __init__(self):
        
        #print "%s" %input_file
        #print "%s" %output_file
        
        f = open(input_file,'rb')
        temp_hex = f.read()
        f.close
        
        hex_file = temp_hex[0:13]
        hex_file = hex_file + "0F" + temp_hex[15:]   #0~12 + 13~14(byte 7) + 15~

#=======================================
        f1 = open(output_file, 'wb')
        f1.write(hex_file)
        f1.close
#=======================================
        
        print "Convert finish."
        
if __name__ == '__main__':
#    port = '2001'
    convert()
    
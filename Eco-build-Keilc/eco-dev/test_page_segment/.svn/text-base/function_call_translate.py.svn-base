#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author(s): Wei-Han Chen (Embedded Platform Lab, NTHU)
# Copyright (c) 2009 National Tsing Hua University (NTHU) 
# Permission to copy, modify, and distribute this program is granted 
# for noncommercial purposes, provided the author(s) and copyright
# notice are retained. All other uses require explicit written
# permission from NTHU. 
#
# Wei-Han Chen <xwaynec@gmail.com> 

import sys
import os
import re
INPUT_FILE = ''
OUTPUT_FILE = ''

SRC_FILE_NAME = ''

ECO_UTILIY_FUNCTION = ['_mdelay','eeprom_init','?C?IMUL','?C_STARTUP','_store_cpu_rate','eco_page_init','_rf_configure','_serial_init','rf_init']


def get_function_name():

    #global SRC_FILENAME
    print 'get_function_name'

    pattern_SRC_NAME = '[N][A][M][E]\s([\w]+)'

    f = open(INPUT_FILE,'r')
    for asm_line in f.readlines():
        reg_src_name = re.search(pattern_SRC_NAME,asm_line)
        if reg_src_name:
            print reg_src_name.group(1)
            SRC_FILE_NAME = reg_src_name.group(1)				
    f.close()
    print 'SRC_FILE_NAME = ',SRC_FILE_NAME	


def function_translate():
    print 'function_translate'

    pattern_PUBLIC = '[P][U][B][L][I][C]\s([\w]+)'
    pattern_EXTRN_CODE = '[E][X][T][R][N]\s[C][O][D][E]\s\(([\w]+)\)'
    
    f = open(INPUT_FILE,'r')
    asm_function_list = []


    for asm_line in f.readlines():
        #PUBLIC FUNCTION 
        reg_public = re.search(pattern_PUBLIC,asm_line)
        if reg_public:
            print reg_public.group(0)
            asm_function_list.append(reg_public.group(1))


    f.close()

    print asm_function_list, '\nfunction count = ' ,len(asm_function_list) ,'\n'

    asm_function_call_list = []

    #find 8051 LCALL FUNCTION instruction
    f = open(INPUT_FILE,'r')
    f_out = open(OUTPUT_FILE,'w')

    flag = True

    for asm_line in f.readlines():
        output_string = asm_line
        for l in asm_function_list:
            #reg_call = re.match('\tLCALL\s' + l+'\s',asm_line)
            reg_call = re.match('\tLCALL\s([\w]+)',asm_line)
            
            if reg_call:
                if not reg_call.group(1) in ECO_UTILIY_FUNCTION:
                    output_string = '\t;---------'+reg_call.group(0)+' start\n'
                    output_string += '\tMOV\tECO_PAGE_ADDR,#HIGH (%s)\n' %reg_call.group(1) 
                    output_string += '\tMOV\tECO_PAGE_ADDR+01H,#LOW (%s)\n' %reg_call.group(1) 
                    output_string += '\tLCALL\teco_page_manager\n' 
                    output_string += '\t;---------'+reg_call.group(0)+' end\n'
                    asm_function_call_list.append(reg_call.group(1))
           
            #EXTER CODE FUNCTION
            reg_code = re.search(pattern_EXTRN_CODE,asm_line)
            if reg_code:
                if flag:
                    print reg_code.group(1)
                    print '\tEXTRN\tCODE (eco_page_manager)\n'
                    f_out.writelines('\tEXTRN\tCODE (eco_page_manager)\n')
                    print '\tEXTRN\tDATA (ECO_PAGE_MANAGER)\n'
                    f_out.writelines('\tEXTRN\tDATA (ECO_PAGE_ADDR)\n')
                    flag = False

        f_out.writelines(output_string) 

    f.close()
    f_out.close()

    print 'asm_function_call_list = ' , asm_function_call_list


if __name__ == '__main__':
   
    #Function tranlate
    if len(sys.argv) == 2:
        #input file format

        INPUT_FILE = sys.argv[1] + '.back'

        #output file format
        OUTPUT_FILE = sys.argv[1]

        os.rename(OUTPUT_FILE,INPUT_FILE)

        #raw_input('Press any key to continue')
        
        get_function_name()	

        function_translate()

    else:
        print 'Error\n'




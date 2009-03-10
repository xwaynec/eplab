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
import string
INPUT_FILE = ''
OUTPUT_FILE = ''

SRC_FILE_NAME = ''

ECO_UTILIY_FUNCTION = ['mdelay','eeprom_init','?C?IMUL','?C_STARTUP','store_cpu_rate','eco_page_init','rf_configure','serial_init','main']


ECO_ASM_FUNCTION = []

#######################################
#   
#   get this asm source name
#
#######################################
def get_function_name():
    #global SRC_FILENAME
    print '---------------------------'
    print 'get_function_name'
    print '---------------------------'

    pattern_src_name = '[N][A][M][E]\s([\w]+)'

    f = open(INPUT_FILE,'r')
    for asm_line in f.readlines():
        reg_src_name = re.search(pattern_src_name,asm_line)
        if reg_src_name:
            print reg_src_name.group(1)
            SRC_FILE_NAME = reg_src_name.group(1)				
    f.close()
    print 'SRC_FILE_NAME = ',SRC_FILE_NAME	


#######################################
#   
#   parsing source asm code and translate
#   the LCALL instruction 
#
#######################################
def function_parse():
    print '---------------------------'
    print 'function_translate'
    print '---------------------------'
    
    pattern_src_funcs = '[\?]PR[\?]([\w]+)[\?]([\w]+)[\s]+SEGMENT[\s]+CODE'
    pattern_src_extern_code = 'EXTRN[\s]+CODE[\s]+\(([\w]+)\)'
    asm_funcs_list = []

    f = open(INPUT_FILE,'r')

    for asm_line in f.readlines():
        
        reg_src_funcs = re.search(pattern_src_funcs,asm_line)
        if reg_src_funcs:
             
            if not reg_src_funcs.group(1) in ECO_UTILIY_FUNCTION:
                ECO_ASM_FUNCTION.append(reg_src_funcs.group(1))
                print reg_src_funcs.group(1) + '\n'

        reg_src_extern_code = re.search(pattern_src_extern_code,asm_line)
        if reg_src_extern_code:
            if not reg_src_extern_code.group(1) in ECO_UTILIY_FUNCTION:
                ECO_ASM_FUNCTION.append(reg_src_extern_code.group(1))
                print reg_src_extern_code.group(1)
    f.close()



#######################################
#   
#   function translate 
#
#######################################
def function_translate():
    print '---------------------------'
    print 'function translate'
    print '---------------------------'
    print 'asm valid function =',ECO_ASM_FUNCTION
    
    #string template
    pattern_func_parameter = '\s+MOV[\s]+R([\d]),(.+)'
    
    #parse for c comment function call
    comment_template = string.Template(';[\s]+${func}\(([\w\s,]*)\)')


    pattern_src_extern_code = 'EXTRN[\s]+CODE[\s]+\(([\w]+)\)'


    asm_valid_funcs = []
    for i in range(len(ECO_ASM_FUNCTION)):
        if ECO_ASM_FUNCTION[i][0:1] == '_':
            asm_valid_funcs.append(comment_template.substitute(func = ECO_ASM_FUNCTION[i][1:]))
        else:
            asm_valid_funcs.append(comment_template.substitute(func = ECO_ASM_FUNCTION[i]))
    
    f = open(INPUT_FILE,'r')
    f_out = open(OUTPUT_FILE,'w')
    #extern only one time 
    extern_code_flag = True
    
    for asm_line in f:

        reg_extern_code = re.search(pattern_src_extern_code,asm_line)
        if reg_extern_code and extern_code_flag:
            print reg_extern_code.group(0)
            print '\tEXTRN\tCODE (eco_page_manager)\n'
            print '\tEXTRN\tDATA (ECO_PAGE_ADDR)\n'
            
            extern_code_flag = False
        
        for valid_func in asm_valid_funcs:

            #print 'template is ',s
            reg_func_test = re.search(valid_func,asm_line)
          
            #find c function
            if reg_func_test:
                print '\nfind c function ',reg_func_test.group(0)
                
                if reg_func_test.group(1):
                    print 'this function has parameter ',reg_func_test.group(0)
                    for asm_func_line in f:
                        #print asm_func_line
                        #regex for asm register parameter
                        reg_func_para = re.search(pattern_func_parameter,asm_func_line)
                        if reg_func_para:
                            print reg_func_para.group(0)

                            print '--------------------------'
                            print 'MOV  R0,#LOW (ECO_PAGE_REGISTER%d)' %int(reg_func_para.group(1))
                            print 'MOV  @R0,%s' %(reg_func_para.group(2)) 
                            print '--------------------------'
                        elif asm_func_line.find('LCALL') != -1:
                            reg_lcall = re.search('\s+LCALL\s+([\w]+)',asm_func_line)
                            if reg_lcall:
                                print '\t;----------'+reg_lcall.group(0)+' start----------'
                                print '\tMOV\tECO_PAGE_ADDR,#HIGH (%s)\n' %reg_lcall.group(1)
                                print '\tMOV\tECO_PAGE_ADDR,#LOW (%s)\n' %reg_lcall.group(1)
                                print '\tLCALL\teco_page_manager\n'
                                print '\t;----------'+reg_lcall.group(0)+' end----------'
                            print valid_func,' is over'
                            break 

                else:
                    print 'this function is no parameter'
                    for asm_func_line in f:
                        reg_lcall = re.search('\s+LCALL\s+([\w]+)',asm_func_line) 
                        if reg_lcall:
                            print '\t;----------'+reg_lcall.group(0)+' start----------'
                            print '\tMOV\tECO_PAGE_ADDR,#HIGH (%s)\n' %reg_lcall.group(1)
                            print '\tMOV\tECO_PAGE_ADDR,#LOW (%s)\n' %reg_lcall.group(1)
                            print '\tLCALL\teco_page_manager\n'
                            print '\t;----------'+reg_lcall.group(0)+' end----------'
                            break 
    f.close()


#######################################
#   
#   backup source file
#
#######################################
def backup_file(src_name,backup_name):
    print '---------------------------'
    print 'back up file from %s to %s' %(src_name,backup_name) 
    print '---------------------------'
    os.rename(src_name,backup_name) 


#######################################
#   
#   translate c to asm function list
#
#######################################
def make_asm_function():
    print '---------------------------'
    print ' translate c to asm func'
    print '---------------------------'
    for i in range(len(ECO_UTILIY_FUNCTION)):
        ECO_UTILIY_FUNCTION.append('_'+ECO_UTILIY_FUNCTION[i])

    print ECO_UTILIY_FUNCTION

#######################################
#   
#   program entry
#
#######################################
if __name__ == '__main__':
  
    make_asm_function()

    #Function tranlate
    if len(sys.argv) == 2:
        
        #input file format
        INPUT_FILE = sys.argv[1] + '.back'

        #output file format
        OUTPUT_FILE = sys.argv[1]

        #backup_file
        backup_file(sys.argv[1],sys.argv[1]+'.back')
        
        #get assembly code function name
        get_function_name()	

        function_parse()
        
        function_translate()
    else:
        print 'Error\n'




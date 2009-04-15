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


import os
import sys
import re
import string
import shutil


class SRCCall_Relocation:
    def __init__(self,src_file):
        self.src_file = src_file
        
        self.ECO_UTILITY_FUNC = ['mdelay','eeprom_init','?C?IMUL','?C_STARTUP','store_cpu_rate','eco_page_init','rf_configure','serial_init','main','rf_init']

        #get source file name
        self.PATTERN_SRC_NAME = 'NAME\s([\w]+)'
        self.SRC_NAME = ''

        #parse function call
        self.PATTERN_SRC_FUNC = '[\?]PR[\?]([\w]+)[\?]([\w]+)[\s]+SEGMENT[\s]+CODE'
        self.PATTERN_SRC_EXTERN_CODE = 'EXTRN[\s]+CODE[\s]+\(([\w]+)\)'
        self.ECO_ASM_FUNC = []
    
        #translate function call
        self.PATTERN_FUNC_PARAMETER = '\s+MOV[\s]+R([\d]),(.+)'
    
        self.asm_valid_funcs = []
   
        self._make_asm_function()
 
    #######################################
    #   
    #   backup source file
    #
    #######################################
    def backup_file(self,src,backup):
        print '---------------------------'
        print 'back up file from %s to %s' %(src,backup) 
        print '---------------------------'
        #os.system ("copy %s %s" % (src, backup))
        shutil.copy(src,backup)
        
        #change src to backup
        self.src_file = backup 
        print self.src_file


    #######################################
    #   
    #   get this asm source name
    #
    #######################################
    def get_src_name(self):
        print '---------------------------'
        print 'get_src_name'
        print '---------------------------'
        f = open(self.src_file,'r')
        for asm_line in f.readlines():
            reg_src_name = re.search(self.PATTERN_SRC_NAME,asm_line)
            if reg_src_name:
                print reg_src_name.group(1)
                self.SRC_NAME = reg_src_name.group(1)
        f.close()
        print 'self.SRC_NAME = ',self.SRC_NAME

    
    def _make_asm_function(self):
        for i in range(len(self.ECO_UTILITY_FUNC)):
            self.ECO_UTILITY_FUNC.append('_' + self.ECO_UTILITY_FUNC[i])    

   
    #######################################
    #   
    #   parsing source asm code and translate
    #   the LCALL instruction 
    #
    #######################################
    def parse_function_call(self):
        print '---------------------------'
        print 'parse_function_call'
        print '---------------------------'

        f = open(self.src_file,'r')

        for asm_line in f.readlines():
            reg_src_funcs = re.search(self.PATTERN_SRC_FUNC,asm_line)
            if reg_src_funcs:
                if not reg_src_funcs.group(1) in self.ECO_UTILITY_FUNC:
                    self.ECO_ASM_FUNC.append(reg_src_funcs.group(1))
                    print reg_src_funcs.group(1)

            reg_src_extern_code = re.search(self.PATTERN_SRC_EXTERN_CODE,asm_line)
            if reg_src_extern_code:
                if not reg_src_extern_code.group(1) in self.ECO_UTILITY_FUNC:
                    self.ECO_ASM_FUNC.append(reg_src_extern_code.group(1))
                    print reg_src_extern_code.group(1)

        f.close()

        print 'self.ECO_ASM_FUNC = ', self.ECO_ASM_FUNC 


    #######################################
    #   
    #   eco page manager segment insert 
    #
    #######################################
    def add_page_manager_segment(self):
        print '---------------------------'
        print 'add eco page manager segment'
        print '---------------------------'
    
        #parse c comment function call
        comment_template = string.Template(';[\s]+${func}\(([\w\s,]*)\)')

        for i in range(len(self.ECO_ASM_FUNC)):
            if self.ECO_ASM_FUNC[i][0:1] == '_':
                self.asm_valid_funcs.append(comment_template.substitute(func = self.ECO_ASM_FUNC[i][1:]))
            else:
                self.asm_valid_funcs.append(comment_template.substitute(func = self.ECO_ASM_FUNC[i])) 
   
       
        print self.asm_valid_funcs 
 


if __name__ == '__main__':
    src_file = sys.argv[1]
    
    src = SRCCall_Relocation(src_file)

    src.backup_file(src_file,src_file + '.back')

    src.get_src_name()

    src.parse_function_call()
     
    src.add_page_manager_segment() 
 

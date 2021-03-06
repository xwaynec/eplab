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
        self.out_file = src_file
        
        #self.ECO_UTILITY_FUNC = ['mdelay','eeprom_init','?C?IMUL','?C_STARTUP','store_cpu_rate','eco_page_init','rf_configure','serial_init','main','rf_init']
        self.ECO_UTILITY_FUNC = ['compute_W']

        #get source file name
        self.PATTERN_SRC_NAME = 'NAME\s([\w]+)'
        self.SRC_NAME = ''

        #parse function call
        self.PATTERN_SRC_FUNC = '[\?]PR[\?]([\w]+)[\?]([\w]+)[\s]+SEGMENT[\s]+CODE'
        self.PATTERN_SRC_REENTRANT_FUNC = '[\?]PR[\?][_][\?]([\w]+)[\?]([\w]+)[\s]+SEGMENT[\s]+CODE'
        self.PATTERN_SRC_EXTERN_CODE = 'EXTRN[\s]+CODE[\s]+\(([\?\w]+)\)'
        self.ECO_ASM_FUNC = []
    
        #translate function call
        self.PATTERN_FUNC_PARAMETER = '\s+MOV[\s]+R([\d]),(.+)'


        self.asm_valid_funcs = []
        self.asm_valid_lcall = []
        self.src_lines = [] 
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
            #self.PATTERN_SRC_FUNC = '[\?]PR[\?]([\w]+)[\?]([\w]+)[\s]+SEGMENT[\s]+CODE'
            reg_src_funcs = re.search(self.PATTERN_SRC_FUNC,asm_line)
            if reg_src_funcs:
                #if not reg_src_funcs.group(1) in self.ECO_UTILITY_FUNC:
                if reg_src_funcs.group(1) in self.ECO_UTILITY_FUNC:
                    self.ECO_ASM_FUNC.append(reg_src_funcs.group(1))
                    print reg_src_funcs.group(1)

            #self.PATTERN_SRC_EXTERN_CODE = 'EXTRN[\s]+CODE[\s]+\(([\?\w]+)\)'
            reg_src_extern_code = re.search(self.PATTERN_SRC_EXTERN_CODE,asm_line)
            if reg_src_extern_code:
                #if not reg_src_extern_code.group(1) in self.ECO_UTILITY_FUNC:
                if reg_src_extern_code.group(1) in self.ECO_UTILITY_FUNC:
                    self.ECO_ASM_FUNC.append(str(reg_src_extern_code.group(1)).replace('?','\?'))
                    print reg_src_extern_code.group(1)
            
            reg_src_reentrant_func = re.search(self.PATTERN_SRC_REENTRANT_FUNC,asm_line)
            if reg_src_reentrant_func:
                #if not reg_src_reentrant_func.group(1) in self.ECO_UTILITY_FUNC:
                if reg_src_reentrant_func.group(1) in self.ECO_UTILITY_FUNC:
                    self.ECO_ASM_FUNC.append('_\?' + reg_src_reentrant_func.group(1))
                    print '_\?' + reg_src_reentrant_func.group(1)

        f.close()

        print 'self.ECO_ASM_FUNC = ', self.ECO_ASM_FUNC 


    #######################################
    #   
    #   create asm function list 
    #
    #######################################
    def create_asm_fuctions_list(self):
        print '---------------------------'
        print 'create asm functions list'
        print '---------------------------'
    
        #parse c comment function call
        #comment_template = string.Template(';[\s]+${func}\(([\w\s,]*)\)')
        #comment_template = string.Template('${func}\(([\w\s,]*)\);')
        #comment_template = string.Template('[\s]${func}\(([\w\s,]*)\);')
        #comment_template = string.Template(';[=\(\w\s]*${func}\(([\w\s,]*)\)')
        comment_template = string.Template(';[=\(\w\s]*${func}\(([\(\)\+\*\w\s\>\<&,]*)\)')
        
        lcall_template = string.Template('LCALL[\s]+(${func})')

        for i in range(len(self.ECO_ASM_FUNC)):
            if self.ECO_ASM_FUNC[i][0:1] == '_':
                self.asm_valid_funcs.append(comment_template.substitute(func = self.ECO_ASM_FUNC[i][1:]))
            else:
                self.asm_valid_funcs.append(comment_template.substitute(func = self.ECO_ASM_FUNC[i])) 
  
        for i in range(len(self.ECO_ASM_FUNC)):
            self.asm_valid_lcall.append(lcall_template.substitute(func = self.ECO_ASM_FUNC[i])) 
        
 
        print self.asm_valid_lcall 


    #######################################
    #
    #   parse commnet c function 
    #
    #######################################
    def parse_lcall_function(self):
        print '---------------------------'
        print 'parse asm LCALL function'
        print '---------------------------'

        f = open(self.src_file,'r')
        asm_lines = f.readlines()
        #print asm_lines
        f.close()       

        modify_start_index = 0
        modify_end_index = 0
        parameter_flag = False
 
        #for line in asm_lines:
        for line_index in range(len(asm_lines)):
            #find valid LCALL function
            for valid_func in self.asm_valid_lcall:

                reg_lcall_function = re.search(valid_func,asm_lines[line_index])

                if reg_lcall_function and asm_lines[line_index].find('?C?') == -1:
                    
                    #print 'reg_lcall_function.group(1) = ',reg_lcall_function.group(1)
                    modify_end_index = line_index
                    for i in range(line_index,0,-1):
                        reg_c_function = re.search(self.asm_valid_funcs[self.asm_valid_lcall.index(valid_func)],asm_lines[i])
                        if reg_c_function:
                            if reg_c_function.group(1):
                                parameter_flag = True
                            else:
                                parameter_flag = False
                            modify_start_index = i
                            break
                    
                    #intern_lcall_flag = false
                     
                    if parameter_flag:
                        print 'YES modify_start_index = %d and modify_end_index = %d' %(modify_start_index,modify_end_index)
                        parameter_index = 0
                        for index in range(modify_end_index-1,modify_start_index-1,-1):
                            
                            #self.PATTERN_FUNC_PARAMETER = '\s+MOV[\s]+R([\d]),(.+)'
                            reg_func_para = re.search(self.PATTERN_FUNC_PARAMETER,asm_lines[index])

                            if str(asm_lines[index]).find('LCALL') != -1:
                                #print asm_lines[index]
                                #raw_input()
                                break 

                            if reg_func_para:
                                #print '\t;' + asm_lines[index]
                                #print '\tMOV\tR0,#LOW (ECO_PAGE_REGISTER%s)\n' %reg_func_para.group(1)
                                #print '\tMOV\t@R0,%s\n' %reg_func_para.group(2)
                                temp = '\t;----------start----------\r\n' 
                                temp += '\t;' + asm_lines[index] + '\r\n'
                                temp += '\tMOV\tR0,#LOW (ECO_PAGE_REGISTER%s)\r\n' %reg_func_para.group(1)
                                temp += '\tMOV\t@R0,%s\r\n' %reg_func_para.group(2)
                                temp += '\t;----------end----------\r\n' 
                                asm_lines.pop(index)
                                asm_lines.insert(index,temp)
                                

                        parameter_flag = False
                    
                        
                    temp = '\t;LCALL----------start----------\r\n' 
                    temp += ';' + asm_lines[modify_end_index] + '\r\n'
                    temp += '\tMOV\tECO_PAGE_SPI_CONN,SPI_CTRL\r\n'
                    temp += '\tMOV\tECO_PAGE_ADDR,#HIGH (%s)\r\n' %reg_lcall_function.group(1)
                    temp += '\tMOV\tECO_PAGE_ADDR+01H,#LOW (%s)\r\n' %reg_lcall_function.group(1)
                    temp += '\tLCALL\teco_page_manager\r\n'
                    temp += '\t;LCALL----------end----------\n\n'
                    asm_lines.pop(modify_end_index) 
                    asm_lines.insert(modify_end_index,temp)

        self.src_lines = asm_lines

    #######################################
    #
    #   print asm source code 
    #
    #######################################
    def print_asm_source(self):
        print '---------------------------'
        print 'print asm source code'
        print '---------------------------'
        for line in self.src_lines:
            print line

    #######################################
    #
    #   store asm source code 
    #
    #######################################
    def save_asm_source(self):
        f = open(self.out_file,'w')       
        for line in self.src_lines:
            f.writelines(line)
        
        f.close()

if __name__ == '__main__':
    src_file = sys.argv[1]
    
    src = SRCCall_Relocation(src_file)

    src.backup_file(src_file,src_file + '.back')

    src.get_src_name()

    src.parse_function_call()
     
    src.create_asm_fuctions_list()

    src.parse_lcall_function()
    
    src.print_asm_source() 
   
    src.save_asm_source()

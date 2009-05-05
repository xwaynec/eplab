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


class FunctCall_Relocation:
    def __init__(self,src_file):
        self.src_file = src_file 
        self.out_file = src_file

        #self.ECO_UTILITY_FUNC = ['mdelay','eeprom_init','?C?IMUL','?C_STARTUP','store_cpu_rate','eco_page_init','rf_configure','serial_init','main','rf_init']
        #self.ECO_UTILITY_FUNC = ['eeprom_init','?C?IMUL','?C_STARTUP','store_cpu_rate','eco_page_init','rf_configure','serial_init','main','rf_init']
        self.ECO_UTILITY_FUNC = ['rf_send','log_2','delta_compress']

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
        self._make_asm_function()
        print '---------------------------'
        print 'parse_function_call'
        print '---------------------------'
        
        f = open(self.src_file,'r')

        for asm_line in f.readlines():
            reg_src_funcs = re.search(self.PATTERN_SRC_FUNC,asm_line)
            if reg_src_funcs:
                #if not reg_src_funcs.group(1) in self.ECO_UTILITY_FUNC:
                if reg_src_funcs.group(1) in self.ECO_UTILITY_FUNC:
                    self.ECO_ASM_FUNC.append(reg_src_funcs.group(1))
                    print reg_src_funcs.group(1)

            reg_src_extern_code = re.search(self.PATTERN_SRC_EXTERN_CODE,asm_line)
            if reg_src_extern_code:
                #if not reg_src_extern_code.group(1) in self.ECO_UTILITY_FUNC:
                if reg_src_extern_code.group(1) in self.ECO_UTILITY_FUNC:
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

        f = open(self.src_file,'r')
        f_out = open(self.out_file + '.tmp','w')

        #extern only one time 
        extern_code_flag = True
        for asm_line in f:
            f_out.writelines(asm_line)
            reg_extern_code = re.search(self.PATTERN_SRC_EXTERN_CODE,asm_line)
            if reg_extern_code and extern_code_flag:
                print reg_extern_code.group(0)
                print '\tEXTRN\tCODE (eco_page_manager)'
                print '\tEXTRN\tDATA (ECO_PAGE_ADDR)'
                f_out.writelines('\tEXTRN\tCODE (eco_page_manager)\n')
                f_out.writelines('\tEXTRN\tDATA (ECO_PAGE_ADDR)\n')
                f_out.writelines('\tEXTRN\tDATA (ECO_PAGE_SPI_CONN)\n')
                f_out.writelines('\tEXTRN\tIDATA (ECO_PAGE_REGISTER1)\n')
                f_out.writelines('\tEXTRN\tIDATA (ECO_PAGE_REGISTER2)\n')
                f_out.writelines('\tEXTRN\tIDATA (ECO_PAGE_REGISTER3)\n')
                f_out.writelines('\tEXTRN\tIDATA (ECO_PAGE_REGISTER4)\n')
                f_out.writelines('\tEXTRN\tIDATA (ECO_PAGE_REGISTER5)\n')
                f_out.writelines('\tEXTRN\tIDATA (ECO_PAGE_REGISTER6)\n')
                f_out.writelines('\tEXTRN\tIDATA (ECO_PAGE_REGISTER7)\n')
                extern_code_flag = False
    
        f.close()
        f_out.close()
               
    #######################################
    #   
    #   translate function call
    #
    #######################################
    def translate_function_call(self):
        print '---------------------------'
        print 'translate function call'
        print '---------------------------'
        
        f = open(self.out_file + '.tmp','r')
        f_out = open(self.out_file,'w')

        for asm_line in f:
            
            #initialize the output line
            output_line = asm_line
            
            for valid_func in self.asm_valid_funcs:
                
                #print 'template is ',s
                reg_func_test = re.search(valid_func,asm_line)

                if reg_func_test:
                    print 'find c function ',reg_func_test.group(0)
                    
                    if reg_func_test.group(1):
                        print 'this funct has parameter ',reg_func_test.group(0)
                        
                        for asm_func_line in f:
                            reg_func_para = re.search(self.PATTERN_FUNC_PARAMETER,asm_func_line)
                            if reg_func_para:
                                print reg_func_para.group(0)

                                #comment the line like 'MOV R0,#LOW (msg)'
                                output_line += '\t;--------------------------\n'
                                output_line += '\t;' + asm_func_line 
                                output_line += '\tMOV\tR0,#LOW (ECO_PAGE_REGISTER%s)\n' %reg_func_para.group(1)
                                output_line += '\tMOV\t@R0,%s\n' %reg_func_para.group(2)
                                output_line += '\t;--------------------------\n\n'
    
                                print '\t--------------------------'
                                print '\tMOV  R0,#LOW (ECO_PAGE_REGISTER%d)' %int(reg_func_para.group(1))
                                print '\tMOV  @R0,%s' %(reg_func_para.group(2))
                                print '\t--------------------------'
   
                         
                            elif asm_func_line.find('LCALL') != -1:
                                reg_lcall = re.search('\s+LCALL\s+([\w]+)',asm_func_line)
    
                                if reg_lcall:
                                    print '\t;----------'+reg_lcall.group(0)+' start----------'
                                    print '\tMOV\tECO_PAGE_ADDR,#HIGH (%s)' %reg_lcall.group(1)
                                    print '\tMOV\tECO_PAGE_ADDR+01H,#LOW (%s)' %reg_lcall.group(1)
                                    print '\tLCALL\teco_page_manager'
                                    print '\t;----------'+reg_lcall.group(0)+' end----------'
                                    output_line += '\t;----------'+reg_lcall.group(0)+' start----------\n'
                                    output_line += '\tMOV\tECO_PAGE_SPI_CONN,SPI_CTRL\n'
                                    output_line += '\tMOV\tECO_PAGE_ADDR,#HIGH (%s)\n' %reg_lcall.group(1)
                                    output_line += '\tMOV\tECO_PAGE_ADDR+01H,#LOW (%s)\n' %reg_lcall.group(1)
                                    output_line += '\tLCALL\teco_page_manager\n'
                                    output_line += '\t;----------'+reg_lcall.group(0)+' end----------\n\n'
                                print valid_func,' is over'
    
                                #f_out.writelines(output_line)
                                break
                                #continue
                            else:
                                print asm_func_line
                                output_line += asm_func_line 

                    else:
                        print 'this function is no parameter'
                        for asm_func_line in f:
                            reg_lcall = re.search('\s+LCALL\s+([\w]+)',asm_func_line)
                            if reg_lcall:
                                output_line = '\t;----------'+reg_lcall.group(0)+' start----------\n'
                                output_line += '\tMOV\tECO_PAGE_SPI_CONN,SPI_CTRL\n'
                                output_line += '\tMOV\tECO_PAGE_ADDR,#HIGH (%s)\n' %reg_lcall.group(1)
                                output_line += '\tMOV\tECO_PAGE_ADDR+01H,#LOW (%s)\n' %reg_lcall.group(1)
                                output_line += '\tLCALL\teco_page_manager\n'
                                output_line += '\t;----------'+reg_lcall.group(0)+' end----------\n\n'
    
                                print '\t;----------'+reg_lcall.group(0)+' start----------'
                                print '\tMOV\tECO_PAGE_ADDR,#HIGH (%s)' %reg_lcall.group(1)
                                print '\tMOV\tECO_PAGE_ADDR+01H,#LOW (%s)' %reg_lcall.group(1)
                                print '\tLCALL\teco_page_manager'
                                print '\t;----------'+reg_lcall.group(0)+' end----------'
    
                                #f_out.writelines(output_line)
    
                                break
                                #continue 

            print 'write out'
            f_out.writelines(output_line)
        f.close()
        f_out.close()
 
 
if __name__ == '__main__':

    src_file = sys.argv[1]

    back_file = sys.argv[1] + '.back'

    out_file = sys.argv[1]
    
    funct = FunctCall_Relocation(src_file)

    funct.backup_file(src_file,back_file)

    funct.get_src_name() 
    
    funct.parse_function_call()

    funct.add_page_manager_segment()

    funct.translate_function_call()

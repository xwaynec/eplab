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
import shutil
import math

class FunctRelocation:
    def __init__(self,lines,page_size):
        self.lines = lines
        
        self.PATTERN_CODE = '(\w+)[\s]+(\w+)[\s]+(\w+)[\s]+([\w-]+)[\s]+([\w\.-]+)[\s]+([\w\.-]+)[\s]+([\w\.\?-]+)'
        self.code_memory_list = []
        self.code_memory_start = []
        self.code_memory_end = []
        self.code_memory_length = []
        self.code_memory_segment_name = []
        
        #eco page size
        self.ECO_PAGE_SIZE = page_size 
        self.ECO_PAGE_MASK = int(math.log(page_size,2))
        self.eco_page_vid = []
        #print 'Eco page size is %d bytes and mask is %d' % (self.ECO_PAGE_SIZE,self.ECO_PAGE_MASK)

        #eco reserved memory size
        #self.ECO_RESERVED_SIZE = 1280
        self.ECO_RESERVED_SIZE = 0
        
        self.SEG_DIRECTIVE = ''

    #######################################
    #   
    #   parse code memory map file 
    #
    #######################################
    def parse_code_memory(self):
        #print '---------------------------'
        #print 'parse code memory'
        #print '---------------------------' 
        #print self.lines
        code_memory_flag = False
        code_memory_counter = 0

        for map_line in self.lines:
            #reg = re.search(self.PATTERN_CODE_MEMORY,map_line)
            #if reg:
            #    print 'reg.group(0) = ', reg.group(0) 
            if map_line.find('*   C O D E   M E M O R Y   *') != -1:
                code_memory_flag = True
                continue

            if code_memory_counter >= 3 or map_line.find('*  X D A T A   M E M O R Y  *') != -1:
                #print 'code memory is over'
                code_memory_flag = False 
                break

            if code_memory_flag:
                #reg_code = re.search(self.PATTERN_CODE,map_line)
                reg_code = re.search(self.PATTERN_CODE,map_line)
                if reg_code:
                    print reg_code.group(0)
                    code_memory_counter = 0
                    self.code_memory_list.append(reg_code.group(0))
                    self.code_memory_start.append(reg_code.group(1))
                    self.code_memory_end.append(reg_code.group(2))
                    self.code_memory_length.append(reg_code.group(3))
                    self.code_memory_segment_name.append(reg_code.group(7))
                elif map_line == '\n':
                    code_memory_counter += 1                
                #print map_line 

        print 'Len = ',len(self.code_memory_list) 

    #######################################
    #   
    #   relocate code memory and generate segment script 
    #
    #######################################
    def relocate_code_memory(self):
        #print '---------------------------'
        #print 'relocate code memory'
        #print '---------------------------' 
        
        #start from reserved size 
        code_start_address = self.ECO_RESERVED_SIZE 
        
        #print self.code_memory_start
        #print self.code_memory_end 
        #print self.code_memory_length
        #print self.code_memory_segment_name

        for i in range(len(self.code_memory_list)):
            if self._check_segment(self.code_memory_segment_name[i]) and str(self.code_memory_segment_name[i]).find('MAIN') != -1:
                #print '----------------------------------------'
                print '%s can be relocated' %self.code_memory_segment_name[i]
                if (code_start_address/self.ECO_PAGE_SIZE) != ((code_start_address + int(self.code_memory_length[i][0:-1],16))/self.ECO_PAGE_SIZE):
                    #print 'cross page line'
                    code_start_address = (((code_start_address + int(self.code_memory_length[i][0:-1],16))/self.ECO_PAGE_SIZE) * self.ECO_PAGE_SIZE)
                    
                    if (code_start_address >> self.ECO_PAGE_MASK) not in self.eco_page_vid:
                        self.eco_page_vid.append(code_start_address >> self.ECO_PAGE_MASK)
                    
                    #print 'SEGMENTS\\(' + self.code_memory_segment_name[i] + '\\(C:' + hex(code_start_address) + '\\)\\)'
                    self.SEG_DIRECTIVE += ' SEGMENTS\\(' + self.code_memory_segment_name[i] + '\\(C:' + hex(code_start_address) + '\\)\\)'

                    #print '%s is located at %X' %(self.code_memory_segment_name[i],code_start_address) 
                      
                else:
                    #print 'still in page size'
                    
                    if (code_start_address >> self.ECO_PAGE_MASK) not in self.eco_page_vid:
                        self.eco_page_vid.append(code_start_address >> self.ECO_PAGE_MASK)

                    #print 'SEGMENTS\\(' + self.code_memory_segment_name[i] + '\\(C:' + hex(code_start_address) + '\\)\\)'
                    self.SEG_DIRECTIVE += ' SEGMENTS\\(' + self.code_memory_segment_name[i] + '\\(C:' + hex(code_start_address) + '\\)\\)'
                    
                    #print '%s is located at %X' %(self.code_memory_segment_name[i],code_start_address) 

                code_start_address = code_start_address + int(self.code_memory_length[i][0:-1],16)                 
                 
                #print '----------------------------------------'
 
        #print self.SEG_DIRECTIVE
        #print 'self.eco_page_vid len = %d' %(len(self.eco_page_vid))
        #print 'self.eco_page_vid = ', self.eco_page_vid  

    #######################################
    #   
    #   check this segment name  
    #
    #######################################
    def _check_segment(self,s_name):
        #print s_name 
        if s_name.find('?C_') != -1 or s_name.find('?C?') != -1:
            #print '\t\t%s is system c library' %s_name
            return False
        elif s_name.find('RF_CH1_RECV') != -1:
            return False
        elif s_name.find('?MAIN?') != -1:
            return False
        elif s_name.find('?CO?') != -1:
            #print '\t\t%s is constant data memory' %s_name
            return False
        elif s_name.find('TIMER0') != -1:
            return False
        else:
            reg_int = re.search('[\?][$\d]',s_name)
            if reg_int:
                return False
            elif s_name.find('ECO_PAGE') != -1:
                return False
            return True           


    #######################################
    #   
    #   check reserved space  
    #
    #######################################
    def _check_reserved_space(self,s_name):
        
        if s_name.find('?CO?') != -1:
            return False
        elif s_name.find('?MAIN?MAIN') != -1:
            return False
        elif s_name.find('TIMER0') != -1:
            return False
        elif s_name.find('?MAIN') != -1:
            return True
        else:
            return False
          
    #######################################
    #   
    #   calculate reserved space  
    #
    #######################################
    def calculate_reserved_space(self):
        print 'calculate reserved space'
        temp_code_memory = 0
        for i in range(len(self.code_memory_list)):
            #if not self._check_segment(self.code_memory_segment_name[i]):
            if not self._check_reserved_space(self.code_memory_segment_name[i]):
                #print self.code_memory_segment_name[i] 
                temp_code_memory += int(self.code_memory_length[i][0:-1],16)
            else:
                print self.code_memory_segment_name[i] 
                 
        print 'reserved code_memory = ',temp_code_memory   
 
        self.ECO_RESERVED_SIZE = int(math.ceil(temp_code_memory / float(self.ECO_PAGE_SIZE)) * self.ECO_PAGE_SIZE)

        print 'self.ECO_RESERVED_SIZE = ',self.ECO_RESERVED_SIZE


    #######################################
    #   
    #   get page offset  
    #
    #######################################
    def get_eco_page_offset(self):
        #print 'eco_page offset is %d' %(self.ECO_RESERVED_SIZE / self.ECO_PAGE_SIZE)
        return int(self.ECO_RESERVED_SIZE / self.ECO_PAGE_SIZE)

    
    #######################################
    #   
    #   get all relocation information  
    #
    #######################################
    def get_all_relocation_info(self):
        print '\033[1;34m---------------------------------------\033[1;m'
        print '\033[1;34m-\033[1;m'
        print '\033[1;34m-\033[1;m    \033[1;34mMakefile link srcipt\033[1;m'
        print '\033[1;34m-\033[1;m'
        print '\033[1;34m---------------------------------------\033[1;m'
        self.get_page_relocation_script()


        print '\033[1;34m---------------------------------------\033[1;m'
        print '\033[1;34m-\033[1;m'
        print '\033[1;34m-\033[1;m    \033[1;34mECO_PAGE_SIZE\033[1;m'
        print '\033[1;34m-\033[1;m'
        print '\033[1;34m---------------------------------------\033[1;m'
        print '\033[1;31mECO_PAGE_SIZE is \033[1;33m%d\033[1;m' %self.ECO_PAGE_SIZE 
        #print 'ECO_PAGE_OFFSET is %d' %(self.ECO_RESERVED_SIZE / self.ECO_PAGE_SIZE)


        print '\033[1;34m---------------------------------------\033[1;m'
        print '\033[1;34m-\033[1;m'
        print '\033[1;34m-\033[1;m    \033[1;34mECO_PAGE_OFFSET\033[1;m'
        print '\033[1;34m-\033[1;m'
        print '\033[1;34m---------------------------------------\033[1;m'
        print '\033[1;31mECO_PAGE_OFFSET is \033[1;33m%d\033[1;m' %self.get_eco_page_offset()


        print '\033[1;34m---------------------------------------\033[1;m'
        print '\033[1;34m-\033[1;m'
        print '\033[1;34m-\033[1;m    \033[1;34mECO_PAGE_TABLE initial value\033[1;m'
        print '\033[1;34m-\033[1;m'
        print '\033[1;34m---------------------------------------\033[1;m'
        print '\033[1;31mECO_PAGE_TABLE initial value \033[1;33m%s\033[1;m' %self.eco_page_vid


        print '\033[1;34m---------------------------------------\033[1;m'
        print '\033[1;34m-\033[1;m'
        print '\033[1;34m-\033[1;m    \033[1;34mECO_PAGE_TABLE initial value in hex format\033[1;m'
        print '\033[1;34m-\033[1;m'
        print '\033[1;34m---------------------------------------\033[1;m'
        for i in range(len(self.eco_page_vid)):
            print '%05X' %self.eco_page_vid[i]

    #######################################
    #   
    #   get relocation script  
    #
    #######################################
    def get_page_relocation_script(self):
        print self.SEG_DIRECTIVE
        
        
if __name__ == "__main__":
    print '__main__'
    
    file = open(sys.argv[1],'r')
    lines = file.readlines()

    func_relocate = FunctRelocation(lines,int(sys.argv[2]))

    func_relocate.parse_code_memory()
 
    func_relocate.calculate_reserved_space()

    func_relocate.get_eco_page_offset()

    func_relocate.relocate_code_memory() 
   
    func_relocate.get_all_relocation_info() 

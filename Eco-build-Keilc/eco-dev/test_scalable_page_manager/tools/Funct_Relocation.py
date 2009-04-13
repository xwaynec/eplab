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


class FunctRelocation:
    def __init__(self,lines):
        self.lines = lines
        
        self.PATTERN_CODE = '(\w+)[\s]+(\w+)[\s]+(\w+)[\s]+([\w-]+)[\s]+([\w\.-]+)[\s]+([\w\.-]+)[\s]+([\w\.\?-]+)'
        self.code_memory_list = []
        self.code_memory_start = []
        self.code_memory_end = []
        self.code_memory_length = []
        self.code_memory_segment_name = []
        
        #eco page size
        self.ECO_PAGE_SIZE = 128 
        #eco reserved memory size
        self.ECO_RESERVED_SIZE = 1024
        
        self.SEG_DIRECTIVE = ''

    def parse_code_memory(self):
        print '---------------------------'
        print 'parse code memory'
        print '---------------------------' 
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

            if code_memory_counter >= 3:
                print 'code memory is over'
                code_memory_flag = False 
                break

            if code_memory_flag:
                #reg_code = re.search(self.PATTERN_CODE,map_line)
                reg_code = re.search(self.PATTERN_CODE,map_line)
                if reg_code:
                    #print reg_code.group(0)
                    code_memory_counter = 0
                    self.code_memory_list.append(reg_code.group(0))
                    self.code_memory_start.append(reg_code.group(1))
                    self.code_memory_end.append(reg_code.group(2))
                    self.code_memory_length.append(reg_code.group(3))
                    self.code_memory_segment_name.append(reg_code.group(7))
                elif map_line == '\n':
                    code_memory_counter += 1                
                #print map_line 
                 

    def relocate_code_memory(self):
        print '---------------------------'
        print 'relocate code memory'
        print '---------------------------' 
        
        #start from reserved size 
        code_start_address = self.ECO_RESERVED_SIZE 
        
        #print self.code_memory_start
        #print self.code_memory_end 
        #print self.code_memory_length
        #print self.code_memory_segment_name

        for i in range(len(self.code_memory_list)):
            if self._check_segment(self.code_memory_segment_name[i]):
                print '----------------------------------------'
                print '%s can be relocated' %self.code_memory_segment_name[i]
                if (code_start_address/self.ECO_PAGE_SIZE) != ((code_start_address + int(self.code_memory_length[i][0:-1],16))/self.ECO_PAGE_SIZE):
                    print 'cross page line'
                    code_start_address = (((code_start_address + int(self.code_memory_length[i][0:-1],16))/self.ECO_PAGE_SIZE) * self.ECO_PAGE_SIZE)
                    
                    #print 'SEGMENTS\\(' + self.code_memory_segment_name[i] + '\\(C:' + hex(code_start_address) + '\\)\\)'
                    self.SEG_DIRECTIVE += ' SEGMENTS\\(' + self.code_memory_segment_name[i] + '\\(C:' + hex(code_start_address) + '\\)\\)'

                    print '%s is located at %X' %(self.code_memory_segment_name[i],code_start_address) 
                      
                else:
                    print 'still in page size'
                    
                    #print 'SEGMENTS\\(' + self.code_memory_segment_name[i] + '\\(C:' + hex(code_start_address) + '\\)\\)'
                    self.SEG_DIRECTIVE += ' SEGMENTS\\(' + self.code_memory_segment_name[i] + '\\(C:' + hex(code_start_address) + '\\)\\)'
                    
                    print '%s is located at %X' %(self.code_memory_segment_name[i],code_start_address) 
                code_start_address = code_start_address + int(self.code_memory_length[i][0:-1],16)                 
                 
                print '----------------------------------------'
 
        print self.SEG_DIRECTIVE
 
    def _check_segment(self,s_name):
        #print s_name 
        if s_name.find('?C_') != -1:
            #print '\t\t%s is system c library' %s_name
            return False
        elif s_name.find('?CO?') != -1:
            #print '\t\t%s is constant data memory' %s_name
            return False
        else:
            reg_int = re.search('[\?][$\d]',s_name)
            if reg_int:
                return False
            elif s_name.find('ECO_PAGE') != -1:
                return False
            return True           

if __name__ == "__main__":
    print '__main__'
    
    path = '/Users/waynec/Desktop/EPLab/Eco-build-Keilc/eco-dev/test_page_reload_seg/'
    
    file = open(sys.argv[1],'r')
    lines = file.readlines()

    func_relocate = FunctRelocation(lines)

    func_relocate.parse_code_memory()
 
    func_relocate.relocate_code_memory() 
    

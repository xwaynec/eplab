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

class EcoPage_Translation:
    def __init__(self,path,src):
        self.path = path           
        self.src = src
        self.out = src 
        self.PATTERN_EXTRN_CODE = 'EXTRN\sCODE\s\(([\w]+)\)'
        self.PATTERN_PRAGMA = '[#][p][r][a][g][m][a]\s[a][s][m]'


    def backup_file(self,src,back):
        print '---------------------------'
        print 'back up file from %s to %s' %(src,back) 
        print '---------------------------' 
        
        shutil.copy(src,back)
        
        self.src = back
        
    def translate_eco_page(self):
        print '---------------------------'
        print 'translate eco_page' 
        print '---------------------------' 
        f = open(self.src,'r')
        f2 = open(self.out,'w')

        flag = True

        for line in f.readlines():
            f2.writelines(line)
            reg_extrn = re.search(self.PATTERN_EXTRN_CODE,line)
            if reg_extrn:
                if flag:
                    print reg_extrn.group(0)
                    print '\tEXTRN\tCODE (?C?ICALL2)'
                    f2.writelines('\tEXTRN\tCODE (?C?ICALL2)\n')
                    flag = False
    
            reg_pragma = re.search(self.PATTERN_PRAGMA,line)
            if reg_pragma:
        
                #f2.writelines('MOV\tR0,#LOW (ECO_PAGE_REGISTER3)\n')
                for i in range(7):
                    line1 = '\tMOV\tR0,#LOW (ECO_PAGE_REGISTER%s)\n' %(i+1)
                    line2 = '\tMOV\tA,@R0\n'
                    line3 = '\tMOV\tR%s,A\n' %(i+1)
                    print line1
                    print line2
                    print line3
                    f2.writelines(line1)
                    f2.writelines(line2)
                    f2.writelines(line3)
    
                print '\tMOV\tSPI_CTRL,ECO_PAGE_SPI_CONN'
                f2.writelines('\tMOV\tSPI_CTRL,ECO_PAGE_SPI_CONN\n')
                print reg_pragma.group(0)
                f2.writelines('\tMOV\tDPH,ECO_PAGE_ADDR\n')
                print '\tMOV\tDPH,ECO_PAGE_ADDR\n'
                f2.writelines('\tMOV\tDPL,ECO_PAGE_ADDR+01H\n')
                print '\tMOV\tDPL,ECO_PAGE_ADDR+01H\n'
                f2.writelines('\tLCALL\t?C?ICALL2\n')
                print '\tLCALL\t?C?ICALL2\n'
				
        f.close()
        f2.close() 
        

if __name__ == '__main__':
    print 'Test EcoPage_Translation'
    
    path = '/Users/waynec/Desktop/EPLab/Eco-build-Keilc/eco-dev/test_page_reload_seg/'
    
    src_file = sys.argv[1]

    ecopage_trans = EcoPage_Translation(path,src_file)

    ecopage_trans.backup_file(sys.argv[1],sys.argv[1] + '.back')
    
    ecopage_trans.translate_eco_page()
     

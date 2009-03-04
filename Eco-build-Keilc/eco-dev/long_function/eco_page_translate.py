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

ECO_PAGE_FILE = 'eco_page.src'

def eco_page_translate():
    print '-----eco_page_translate-----\n'
    
    pattern_EXTRN_CODE = '[E][X][T][R][N]\s[C][O][D][E]\s\(([\w]+)\)'
    pattern_PRAGMA  = '[#][p][r][a][g][m][a]\s[a][s][m]' 


    f = open(INPUT_FILE,'r')
    f2 = open(OUTPUT_FILE,'w')
   
    flag = True

    for line in f.readlines():
        f2.writelines(line)
        reg_extrn = re.search(pattern_EXTRN_CODE,line)
        if reg_extrn:
            if flag:
                print reg_extrn.group(0)
                print '\tEXTRN\tCODE (?C?ICALL2)'
                f2.writelines('\tEXTRN\tCODE (?C?ICALL2)\n')
                flag = False

        reg_pragma = re.search(pattern_PRAGMA,line)
        if reg_pragma:
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
   
    #Function tranlate
    if len(sys.argv) == 2:
        #input file format
        INPUT_FILE = sys.argv[1]+'.back'

        os.rename(sys.argv[1],INPUT_FILE)

        #output file format
        OUTPUT_FILE = sys.argv[1]

        #raw_input('Press any key to continue')

        print len(sys.argv)
        eco_page_translate()    

    else:
        print 'Error\n'




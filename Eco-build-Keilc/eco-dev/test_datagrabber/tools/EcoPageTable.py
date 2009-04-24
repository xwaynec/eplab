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


class EcoPageTable:
    def __init__(self,src):
        self.src = src
        print self.src

    
    def parse_page_table(self):
        
        f = open(self.src,'r')

        
        
        f.close()

if __name__ == '__main__':
    print '__main__'

    
    src = sys.argv[1]

    tb = EcoPageTable(src)
    
    


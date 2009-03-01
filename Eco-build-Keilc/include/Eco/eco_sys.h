/*
 * Author(s): Min-Hua Chen (Embedded Platform Lab, NTHU)
 * Copyright (c) 2008 National Tsing Hua University (NTHU) 
 * Permission to copy, modify, and distribute this program is granted 
 * for noncommercial purposes, provided the author(s) and copyright
 * notice are retained. All other uses require explicit written
 * permission from NTHU. 
 *
 * Min-Hua Chen <orca.chen@gmail.com> 
 */
#ifndef _ECO_SYS_H_
#define	_ECO_SYS_H_

#include <Eco/reg24e1.h>

#define blink_led() P0 ^= 0x20

#define eco_dev_blink_led() P0 ^= 0x08

#endif 

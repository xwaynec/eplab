/*
 * Author(s): Wei-Han Chen (Embedded Platform Lab, NTHU)
 * Copyright (c) 2009 National Tsing Hua University (NTHU) 
 * Permission to copy, modify, and distribute this program is granted 
 * for noncommercial purposes, provided the author(s) and copyright
 * notice are retained. All other uses require explicit written
 * permission from NTHU. 
 *
 * Eco Paging Library
 *
 * Wei-Han Chen <xwaynec@gmail.com> 
 * 2009/2/13
 */

#ifndef	__ECO_PAGE_H
#define	__ECO_PAGE_H


#include "Eco/reg24e1.h"
#include "Eco/eco_sys.h"
#include "utils/utils.h"
#include "eeprom/eeprom.h"

#define EEPROM_HEADER 3
#define ECO_PAGE_ADDR_OFFSET        6
#define ECO_ADDR_SHIFT(x)       ((unsigned int)(x) + 3)


/*
static unsigned char ECO_PAGE_TABLE[10];

static unsigned int ECO_PAGE_ADDR;

static unsigned int ECO_PAGE_TABLE_INDEX;
*/

void eco_page_init();
void eco_page_manager();


#endif

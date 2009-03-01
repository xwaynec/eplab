/*
 * Author(s): Min-Hua Chen (Embedded Platform Lab, NTHU)
 * Copyright (c) 2008 National Tsing Hua University (NTHU) 
 * Permission to copy, modify, and distribute this program is granted 
 * for noncommercial purposes, provided the author(s) and copyright
 * notice are retained. All other uses require explicit written
 * permission from NTHU. 
 */
#ifndef _EEPROM_H_
#define _EEPROM_H_

/* instruction for eeprom AT25320A */
#define	EE_WREN		0x06
#define EE_WRDI		0x04
#define EE_RDSR		0x05
#define EE_WRSR		0x01
#define	EE_READ		0x03
#define	EE_WRITE	0x02
#define	ERASE_ALL	0x62	/* erase all page for flash memory */
/* the eeprom chip select is connected to P0_0, and
 * the eeprom is active when CS is set low */
#define	EE_CS		P0_0

void eeprom_init();
void eeprom_write(unsigned int addr, char byte);
char eeprom_read(unsigned int addr);
char eeprom_status();

#endif 

/* 
 * Author(s): Min-Hua Chen (Embedded Platform Lab, NTHU)
 * Copyright (c) 2008 National Tsing Hua University (NTHU) 
 * Permission to copy, modify, and distribute this program is granted 
 * for noncommercial purposes, provided the author(s) and copyright
 * notice are retained. All other uses require explicit written
 * permission from NTHU. 
 *
 * utils.c
 *
 * small utils, architecture dependent
 * the udelay is stolen from Linux kernel
 * Min-Hua Chen <orca.chen@gmail.com> 
 * 2007/10/22
 */
#include "Eco/reg24e1.h"
unsigned long MHZ;	/* system clock rate */

/* 
 * store_cpu_rate - store the cpu rate to the global variable MHZ
 * @mhz: default cpu rate (in MHz)
 */
void store_cpu_rate(int mhz)
{
	MHZ = mhz;	/* store clock rate */
}

/* 
 * mdelay - delay 1 msec
 * @msec: number of msec to delay
 * (HZ >> 20) instructions takes 1 usec
 * This function is not verified by oscilloscope
 */
void mdelay(unsigned int msec)
{
	int i, j, instr_per_msec;
	instr_per_msec = 43 * MHZ / 4;
	for (i = 0; i < msec; i++)	/* delay */
		for (j = 0; j < instr_per_msec; j++)
			;
}

/* 
 * wdt_load - load the watchdog timer (WDT), the WDT expires when
 * the number of ticks is 0. The counter decreases every 10 ms.
 * @cnt: number of cycles for the watchdog timer (max: 16-bits)
 */
void wdt_load(unsigned int cnt)
{
	while ((REGX_CTRL & 0x10))	/* wait until not busy */
		;
	REGX_MSB = cnt >> 8;
	REGX_LSB = cnt & 0xff;
	REGX_CTRL = 0x08;	/* op-code for write WTD */
}

/*
 * strncpy - copy n bytes of data from src to dst
 * @src: char pointer to source
 * @dst: char pointer to destination
 * @n: number of bytes of data
 */
void strncpy(char *src, char *dst, int n)
{
	int i;
	for (i = 0; i < n; i++) {
		*dst++ = *src++;
	}
}

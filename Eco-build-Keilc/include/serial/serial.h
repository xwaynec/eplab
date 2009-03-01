/*
 * Author(s): Min-Hua Chen (Embedded Platform Lab, NTHU)
 * Copyright (c) 2008 National Tsing Hua University (NTHU) 
 * Permission to copy, modify, and distribute this program is granted 
 * for noncommercial purposes, provided the author(s) and copyright
 * notice are retained. All other uses require explicit written
 * permission from NTHU. 
 */
#ifndef _SERIAL_H_
#define _SERIAL_H_

/* for SCON register */
#define SERIAL_MODE0	0x00	/* sync mode */
#define SERIAL_MODE1	(1 << 6)	/* async, full duplex mode */
#define SERIAL_MODE2	(2 << 6)	/* async, full duplex mode */ 
#define SERIAL_MODE3	(3 << 6)	/* async, full duplex mode */ 

#define SERIAL_CLK_D4		(1 << 5)

#define SERIAL_IO_PORT	(3 << 1)
#define RECV_ENABLE	(1 << 4)
#define TRAN_DONE	(1 << 1)
#define	RECV_DONE	1

/* for PCON register */
#define BAUD_DOUBLE	(1 << 7)

void serial_init(unsigned int baud);
void putc(char c);
void puts(char *s);
char getc();
void int_print(unsigned int val) reentrant;

#endif

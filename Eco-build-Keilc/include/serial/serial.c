/*
 * Author(s): Min-Hua Chen (Embedded Platform Lab, NTHU)
 * Copyright (c) 2008 National Tsing Hua University (NTHU) 
 * Permission to copy, modify, and distribute this program is granted 
 * for noncommercial purposes, provided the author(s) and copyright
 * notice are retained. All other uses require explicit written
 * permission from NTHU. 
 *
 * serial port driver
 *
 * Min-Hua Chen <orca.chen@gmail.com>
 * 2007/8/2
 */

#include "Eco/reg24e1.h"
#include "serial.h"
#include "timer/timer.h"

/* setup_baudrate - note that the CPU is 16M Hz
 * @baud: baudrate
 */
static int setup_baudrate(unsigned int baud)
{
	T2CON &= TIMER2_AUTO;	/* set auto-reload */
	TCLK = 1;	/* set transmit clock */
	RCLK = 1;	/* set receive clock */
	C_T2 = 0;	/* select timer function */
	T2CON |= TIMER2_ENABLE;	/* enable timer2 */

	P0 &= ~0x06;	/* clean [1:2] bits */
	P0_ALT |= SERIAL_IO_PORT;	/* select serial I/O port */

	switch (baud) {
	case 57600:
		RCAP2H = 0xFF;
		RCAP2L = 0xF7;
		break;
	case 19200:
		RCAP2H = 0xFF;
		RCAP2L = 0xE6;
		break;
	default:
		/* baudrate not supported */
		return 0;
	}
	return 1;
}

/* serial_init - setup baudrate 
 * NOTE: using timer 2 as baud generator @ CPU 16M Hz only 
 * @baud: baud rate
 */
void serial_init(unsigned int baud)
{
	/* SCON initial value: 0x00 */
	/* add more supported modes here */

	setup_baudrate(baud);
	SCON |= SERIAL_MODE1;	/* enable serial port mode 1 */
	SCON |= RECV_ENABLE;	/* enable receive */
}

/* serial_write - transmit one byte by serial port
 * @byte: writing byte
 */
static void serial_write(char byte)
{
	SBUF = byte;	/* write to serial buffer */
	while (!TI)	/* wait until done */
		;
	TI = 0;	/* clean transmit done bit */
}

/* serial_read - read one byte from serial port
 * @ret: read byte
 */
static char serial_read()
{
	while (!RI)	/* wait until done */
		;
	RI = 0;	/* clean receive bit */
	return SBUF;
}

/* wrappers for serial read/write interface */
void putc(char c)
{
	serial_write(c);
}

void puts(char *s)
{
	while (*s)
		serial_write(*s++);
}

char getc()
{
	return serial_read();
}

/* int_print - convert an unsigned int to a string then print it
 * max int is 65535
 * @val: int for printing
 */
void int_print(unsigned int val) reentrant
{
	if (val / 10)
		int_print(val / 10);
	putc((val % 10) + '0');
}


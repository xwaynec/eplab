/*
 * Author(s): Min-Hua Chen (Embedded Platform Lab, NTHU)
 * Copyright (c) 2008 National Tsing Hua University (NTHU) 
 * Permission to copy, modify, and distribute this program is granted 
 * for noncommercial purposes, provided the author(s) and copyright
 * notice are retained. All other uses require explicit written
 * permission from NTHU. 
 * 
 * SPI driver
 * Min-Hua Chen <orca.chen@gmail.com>
 * 2007/8/1
 */

#include "Eco/reg24e1.h"
#include "spi/spi.h"

/* spi_init - initialize SPI 
 * @conn_dev: specified device for SPI to connect to
 * @clk: specified clock rate for SPI
 */
void spi_init(char conn_dev, char clk)
{
	/* check data if necessary */
	SPI_CTRL = conn_dev;	/* connect SPI to device */
	SPICLK = clk;	/* setup clock rate */
}

/* spi_write_then_read - write 8-bits to the SPI to clock out and then 
 * return the clocked in data.
 * @byte: data write to SPI
 * @ret: clocked in data after clock out 8-bits
 */
char spi_write_then_read(char byte)
{
	EXIF &= ~SPI_READY;	/* clean the SPI done flag before write */
	SPI_DATA = byte;	/* send 8 bits */
	while (!(EXIF & SPI_READY))	/* wait until done */
		;
	return SPI_DATA;	/* return data */
}

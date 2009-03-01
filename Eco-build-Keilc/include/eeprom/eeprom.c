/*
 * Author(s): Min-Hua Chen (Embedded Platform Lab, NTHU)
 * Copyright (c) 2008 National Tsing Hua University (NTHU) 
 * Permission to copy, modify, and distribute this program is granted 
 * for noncommercial purposes, provided the author(s) and copyright
 * notice are retained. All other uses require explicit written
 * permission from NTHU. 
 *
 * eeprom driver
 * Min-Hua Chen <orca.chen@gmail.com> 
 * 2007/8/23
 * 2008/3/6
 */

#include "Eco/reg24e1.h"
#include "spi/spi.h"
#include "eeprom/eeprom.h"


/* Eco programmer mode, issue output signal as EE_CS signal 
 * to another Eco debugger board. With correct wire connection,
 * we can write date to another debugging board, check the manual
 * for the connection part
 */


#ifdef ECO_PROG_MODE
#undef EE_CS
/* I/O port as CS for Eco sensor node*/
#define EE_CS INT0_N
#endif 

#ifdef ECO_DEV_PROG_MODE
#undef EE_CS
/* I/O port as CS for new debugging boad */
#define EE_CS DIO7
#endif 

/* eeproom_init - init the eeprom, connect eeprom to the SPI
 * interface */
void eeprom_init()
{
	/* connect spi to eeprom and setup clock rate to 1/8 of CPU */
	spi_init(SPI_CONN_EEPROM, SPI_CLK_D8);
	/* set p0.0(EEPROM CSN) to output mode */
	P0_DIR &= ~0x01;
}

/* eeprom_status - read the status register */
char eeprom_status()
{
	char byte;
	EE_CS = 0;	/* active eeprom */
	spi_write_then_read(EE_RDSR);	/* send read-status-register
					   instruction to the eeprom */
	byte = spi_write_then_read(0);
	EE_CS = 1;	/* inactive eeprom */

	return byte;
}

/* eeprom_write - write a single byte to specified address
 * @addr: target address
 * @byte: writting byte of data
 */
void eeprom_write(unsigned int addr, char byte)
{
	while (eeprom_status() & 0x01)	/* wait until write cycle done */
		;
	EE_CS = 0;	/* active eeprom */
	spi_write_then_read(EE_WREN);	/* write-enable instruction */
	EE_CS = 1;	/* inactive eeprom */
	EE_CS = 0;	/* active eeprom */
	spi_write_then_read(EE_WRITE);	/* write instruction */
	spi_write_then_read(addr >> 8);	/* higher byte of addr */
	spi_write_then_read(addr & 0xff);	/* lower byte */
	spi_write_then_read(byte);	/* write data */
	EE_CS = 1;	/* inactive eeprom */
	EE_CS = 0;	/* active eeprom */
	spi_write_then_read(EE_WRDI);	/* write-disable instruction */
	EE_CS = 1;	/* inactive eeprom */
}

/* eeprom_read - read single byte from specified address
 * @addr: target address
 */
char eeprom_read(unsigned int addr)
{
	char byte = 0;
	while (eeprom_status() & 0x01)	/* wait until write cycle done */
		;
	EE_CS = 0;	/* active eeprom */
	spi_write_then_read(EE_READ);	/* read instruction */
	spi_write_then_read(addr >> 8);	/* higher byte of addr */
	spi_write_then_read(addr & 0xff);	/* lower byte */
	byte = spi_write_then_read(0); /* read data */
	EE_CS = 1;	/* inactive eeprom */
	return byte;
}

/* flash_erase_all - erase all pages on flash memory */
void flash_erase_all()
{
	while (eeprom_status() & 0x01)	/* wait until write cycle done */
		;
	EE_CS = 0;	/* enable SPI slave */
	spi_write_then_read(EE_WREN);	/* write-enable instruction */
	EE_CS = 1;	/* start erase operation */
	EE_CS = 0;	/* start erase operation */
	spi_write_then_read(ERASE_ALL);	/* read instruction */
	EE_CS = 1;	/* start erase operation */
	while (eeprom_status() & 0x00)	/* wait until erase done */
		;
	/* re-enable flash write operation */
	EE_CS = 0;	/* enable SPI slave */
	spi_write_then_read(EE_WREN);	/* write-enable instruction */
	EE_CS = 1;	/* start erase operation */
}

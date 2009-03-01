/*
 * Author(s): Min-Hua Chen (Embedded Platform Lab, NTHU)
 * Copyright (c) 2008 National Tsing Hua University (NTHU) 
 * Permission to copy, modify, and distribute this program is granted 
 * for noncommercial purposes, provided the author(s) and copyright
 * notice are retained. All other uses require explicit written
 * permission from NTHU. 
 */
#ifndef _SPI_H_
#define _SPI_H_

/* for SPI_CTRL register */
#define SPI_CONN_NONE   0x00
#define SPI_CONN_EEPROM 0x01
#define SPI_CONN_RADIO  0x02
#define SPI_CONN_RADIO2 0x03

/* for SPICLK register */
#define SPI_CLK_D8      0x00
#define SPI_CLK_D16     0x01
#define SPI_CLK_D32     0x02
#define SPI_CLK_D64     0x03

/* end of SPI read/write */
#define SPI_READY       (1 << 5)

void spi_init(char conn_dev, char clk);
char spi_write_then_read(char byte);

#endif 

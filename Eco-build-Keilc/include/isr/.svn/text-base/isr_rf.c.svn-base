/*
 * Author(s): Min-Hua Chen (Embedded Platform Lab, NTHU)
 * Copyright (c) 2008 National Tsing Hua University (NTHU) 
 * Permission to copy, modify, and distribute this program is granted 
 * for noncommercial purposes, provided the author(s) and copyright
 * notice are retained. All other uses require explicit written
 * permission from NTHU. 
 *
 * radio driver - ISR
 * Nordic transceiver subsystem
 * NOTE: DuoCeiver (two parallel independent channels) is not supported, 
 * hence only data channel 1 is used.
 *
 * note: This ISR only has basic function, users should modify this ISR
 * for his purpose. Users has to handle the timing to receive /
 * transmit.
 *
 * Min-Hua Chen <orca.chen@gmail.com> 
 * 2008/03/16
 *
 * *set the radio to low power mode after receiving data by set CE = 0
 * 2008/06/05
 */

#include <eco/reg24e1.h>
#include <isr/isr_rf.h>
#include <spi/spi.h>
struct radio_buffer rf_buf = { 0, {0}};

/* radio_init - basic initialization for radio
 * the radio should be configured by rf_configure after radio_init */
void rf_init()
{
	/* RADIO init value: 0x80;*/
	PWR_UP = 1;	/* turn on radio power */
	/* connect spi to radio and setup clock rate to 1/8 of CPU */
	spi_init(SPI_CONN_RADIO, SPI_CLK_D8);
	EA = 1;	/* enable global interrupt */
	EX4 = 1;	/* enable radio interrupt */
}

/* rf_configure - write configure data to radio subsystem, software 
 * should use construct the rf_config struct first
 * @*cfg: rf_config struct, which contains the configuration 
 * data for the radio subsystem.
 */
void rf_configure(struct rf_config *cfg)
{
	char *p;
	int i;

	CS = 1;	/* enter configure mode */

	p = (char *)cfg;
	/* write configure data to radio */
	for (i = 0; i < sizeof(*cfg); i++) {
		spi_write_then_read(*(p + i));
	}

	CS = 0;	/* back to standby mode */
}

/* 
 * radio_send - send payload to specified address
 * @*addr: receiver's address
 * @addr_len: receiver's address length (in bytes)
 * @*payload: payload to receiver
 * @pl_len: payload to receiver length (in bytes)
 */
void rf_send(char *addr, unsigned char addr_len,
		char *payload, unsigned char pl_len)
{
	int i;

	CE = 1;	/* enable on board processing */

	/* send address */
	for (i = 0; i < addr_len; i++)
		spi_write_then_read(*(addr + i));
	/* send payload */
	for (i = 0; i < pl_len; i++)
		spi_write_then_read(*(payload + i));

	CE = 0; /* enable transmission */
}

/* rf_ch1_recv - read a packet from radio channel 1 */
void rf_ch1_recv() interrupt 10
{
	int i = 0;
	/* 
	 * read the data and write the data to the buffer 
	 * DR1 is set to low when all data is clocked out 
	 */ 
	if (rf_buf.ready)
		goto out;
	while (DR1) {
		rf_buf.buffer[i++] = spi_write_then_read(0);
	}
	rf_buf.ready = 1;	/* data ready */
out:
	/* clean interrupt flag (or the interrupt is always on */ 
	EXIF &= ~0x40;
}

/* 
 * rf_wait_msg - wait for data packet
 */
void rf_wait_msg()
{
	CE = 1;	/* enable radio transceiver (ch1) */
	while (!rf_buf.ready)	/* wait for data */
		;
	CE = 0; /* disable radio to save power */
}

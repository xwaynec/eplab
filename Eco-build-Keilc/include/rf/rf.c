/*
 * Author(s): Min-Hua Chen (Embedded Platform Lab, NTHU)
 * Copyright (c) 2008 National Tsing Hua University (NTHU) 
 * Permission to copy, modify, and distribute this program is granted 
 * for noncommercial purposes, provided the author(s) and copyright
 * notice are retained. All other uses require explicit written
 * permission from NTHU. 
 *
 * radio driver
 * Nordic transceiver subsystem
 * NOTE: DuoCeiver (two parallel independent channels) is not supported, 
 * hence only data channel 1 is used.
 * Min-Hua Chen <orca.chen@gmail.com> 
 * 2007/8/1
 *
 * add a new API - rf_wait_msg
 * Reduce the code size and on function argument is needed now.
 * Min-Hua Chen <orca.chen@gmail.com> 
 * 2008/3/18
 */

#include <eco/reg24e1.h>
#include <rf/rf.h>
#include <spi/spi.h>
char rf_buf[RF_BUF_LEN];

/* radio_init - basic initialization for radio
 * the radio should be configured by rf_configure after radio_init */
void rf_init()
{
	/* RADIO init value: 0x80;*/
	PWR_UP = 1;	/* turn on radio power */
	/* connect spi to radio and setup clock rate to 1/8 of CPU */
	spi_init(SPI_CONN_RADIO, SPI_CLK_D8);
	//EX4 = 1;
	//EA = 1;
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

/* radio_send - send payload to specified address
 * @*addr: receiver's address
 * @addr_len: receiver's address length (in bytes)
 * @*payload: payload to receiver
 * @pl_len: payload to receiver length (in bytes)
 */
void rf_send(char *addr, unsigned char addr_len,
		char *payload, unsigned char pl_len)
{
	unsigned char i;

	CE = 1;	/* enter transmit mode */

	/* send address */
	for (i = 0; i < addr_len; i++)
		spi_write_then_read(*(addr + i));
	/* send payload */
	for (i = 0; i < pl_len; i++)
		spi_write_then_read(*(payload + i));

	CE = 0; /* back to standby mode */
}

/* 
 * rf_wait_msg - wait for rf data packets, and read the packet to the
 * buffer
 */
void rf_wait_msg()
{
	unsigned char i = 0;
	CE = 1;	/* enter receive mode */
	while (!DR1)	/* wait for data */
		;
	while (DR1) {
		rf_buf[i++] = spi_write_then_read(0);	/* clock in data */
	}

	CE = 0; /* back to standby mode */
}

/*
 * rf_wait_msg_timeout - timeout counter version
 * *p: a pointer to the timeout counter
 */
void rf_wait_msg_timeout(unsigned int *p)
{
	unsigned char i = 0;
	CE = 1;	/* enter receive mode */
	while (!DR1) {	/* wait for data */
		if (!(*p))
			return;
		(*p)--;
	}
	while (DR1) {
		rf_buf[i++] = spi_write_then_read(0);	/* clock in data */
	}

	CE = 0; /* back to standby mode */
}

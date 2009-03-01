/* 
 * Author(s): Min-Hua Chen (Embedded Platform Lab, NTHU)
 * Copyright (c) 2008 National Tsing Hua University (NTHU) 
 * Permission to copy, modify, and distribute this program is granted 
 * for noncommercial purposes, provided the author(s) and copyright
 * notice are retained. All other uses require explicit written
 * permission from NTHU. 
 */
#ifndef _RADIO_H_
#define _RADIO_H_

#define	RF_BUF_LEN	23	/* default rf buffer size */

/* RF configuration descriptor */
struct rf_config {
	/* data width (in bits) */
	unsigned char data2_width;
	unsigned char data1_width;
	/* address for two channels ,for only one channel, use addr1 */
	char addr2[5];
	char addr1[5];
	/* [7:2] is address width (in bits), [1:0] is for CRC control */
	char addr_and_crc;
	char rf_prog[2];	/* rf programming */
};

void rf_init();
void rf_configure(struct rf_config *cfg);
void rf_send(char *addr, unsigned char addr_len,
		char *payload, unsigned char pl_len);
void rf_wait_msg();
void rf_wait_msg_timeout(unsigned int *p);
#define rf_recv_msg(cfg) rf_wait_msg()

#endif 

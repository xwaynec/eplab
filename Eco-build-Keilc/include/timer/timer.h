/*
 * Author(s): Min-Hua Chen (Embedded Platform Lab, NTHU)
 * Copyright (c) 2008 National Tsing Hua University (NTHU) 
 * Permission to copy, modify, and distribute this program is granted 
 * for noncommercial purposes, provided the author(s) and copyright
 * notice are retained. All other uses require explicit written
 * permission from NTHU. 
 */
#ifndef _TIMER_H_
#define _TIMER_H_

/* for TMOD register */
#define TIMER1_AS_CNTR	(1 << 6)

#define TIMER0_AS_CNTR	(1 << 2)


#define TIMER1_MODE0	(0 << 4)	/* 13-bit counter */
#define TIMER1_MODE1	(1 << 4)	/* 16-bit counter */
#define TIMER1_MODE2	(2 << 4)	/* 8-bit counter, auto-reload */
#define TIMER1_MODE3	(3 << 4)	/* two 8-bit counters */

#define TIMER0_MODE0	0x00	/* 13-bit counter */
#define TIMER0_MODE1	0x01	/* 16-bit counter */
#define TIMER0_MODE2	0x10	/* 8-bit counter, auto-reload */
#define TIMER0_MODE3	0x11	/* two 8-bit counters */

/* for TCON register */
#define TIMER1_ENABLE	(1 << 6)
#define TIMER0_ENABLE	(1 << 4)

/* for T2CON register */
#define TIMER2_ENABLE	(1 << 2)
#define	TIMER2_AUTO	~0x01	/* auto-reload */

/* for CKCON register */
#define TIMER2_CLK_D4	(1 << 5)	/* 1/4 of CPU clock rate */
#define TIMER1_CLK_D4	(1 << 4)
#define TIMER0_CLK_D4	(1 << 3)

#endif 

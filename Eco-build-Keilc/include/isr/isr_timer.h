/*
 * Author(s): Min-Hua Chen (Embedded Platform Lab, NTHU)
 * Copyright (c) 2008 National Tsing Hua University (NTHU) 
 * Permission to copy, modify, and distribute this program is granted 
 * for noncommercial purposes, provided the author(s) and copyright 
 * notice are retained. All other uses require explicit written 
 * permission from NTHU. 
 *
 * A simple timer ISR for time 0
 *
 * Min-Hua Chen <orca.chen@gmail.com> 
 * 2008/03/17
 */
#include <eco/reg24e1.h>

void timer0() interrupt 1;
void do_timer();
int set_timer(unsigned int ticks, void (*p)());
void delay_ticks(unsigned int ticks);

/* timer status */
#define SET 1
#define UNSET 0

/*
 * If SYS_CLK is defined, timer interrupt must keep enabled. 
 */
/* #define	SYS_CLK */
#ifdef SYS_CLK
extern unsigned int jiffies[2];
/* disable macros to dynamically control timer0 */
#define ENABLE_TIMER0_INT() 
#define DISABLE_TIMER0_INT() 
/* timer0 init macro */
#define	init_timer0_int() \
	do {	\
		TMOD = 0x02;	\
		TH0 = 0xFF;	\
		EA = 1;		\
		ET0 = 1;	\
		TR0 = 1;	\
  	} while(0)
#else
/* disable macros to dynamically control timer0 */
#define ENABLE_TIMER0_INT() ET0 = 1
#define DISABLE_TIMER0_INT() ET0 = 0
/* timer0 init macro */
#define	init_timer0_int() \
	do {	\
		TMOD = 0x02;	\
		TH0 = 0xFF;	\
		EA = 1;		\
		TR0 = 1;	\
  	} while(0)
#endif 

/*
 * timer structure
 */
struct timer {
	unsigned char status;	/* timer status */
	unsigned int tick;	/* time to expire the timer */
	int (*p)();		/* function to execute */
};

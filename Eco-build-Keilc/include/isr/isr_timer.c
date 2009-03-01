/*
 * Author(s): Min-Hua Chen (Embedded Platform Lab, NTHU)
 * Copyright (c) 2008 National Tsing Hua University (NTHU) 
 * Permission to copy, modify, and distribute this program is granted 
 * for noncommercial purposes, provided the author(s) and copyright
 * notice are retained. All other uses require explicit written
 * permission from NTHU. 
 *
 * timer.c - ISR
 * timer interrupt simply update the system jiffies (32 bits)
 *
 * Min-Hua Chen <orca.chen@gmail.com> 
 * 2008/03/10
 */
#include <isr/isr_timer.h>

#ifdef SYS_CLK
unsigned int jiffies[2] = {0};
#endif 
struct timer timer = {0, 0, 0}; 

/*
 * do_timer - check timer routines, only 1 timer is allowed
 */
void do_timer()
{
	if (timer.status) {
		if (!--timer.tick) {
			/* timer expire */
			if (timer.p)
				timer.p();
			timer.status = UNSET;
			DISABLE_TIMER0_INT();
		}
	}
}

/*
 * do_timer - timer ISR, keep a 32-bit system clock
 */
void timer0() interrupt 1
{
#ifdef SYS_CLK
	/* update system jiffies */
	if (jiffies[0] == 0xffff) {
		jiffies[1]++;
	}
	jiffies[0]++;
#endif 
	do_timer();
}

/* 
 * set_timer - register a timer
 * @tick - expire time
 * @p - timer function pointer
 */
int set_timer(unsigned int ticks, void (*p)())
{
	if (!timer.status) {
		timer.tick = ticks;
		timer.p = p;
		timer.status = SET;
		ENABLE_TIMER0_INT();
		return 1;
	}
	return 0;
}

/*
 * delay_ticks - delay for given ticks
 * @ticks: delay time
 */
void delay_ticks(unsigned int ticks)
{
	set_timer(ticks, 0);
	/* wait for expire */
	while (timer.status)
		;
}

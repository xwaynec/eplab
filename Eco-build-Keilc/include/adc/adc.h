/* 
 * Author(s): Min-Hua Chen (Embedded Platform Lab, NTHU)
 * Copyright (c) 2008 National Tsing Hua University (NTHU) 
 * Permission to copy, modify, and distribute this program is granted 
 * for noncommercial purposes, provided the author(s) and copyright
 * notice are retained. All other uses require explicit written
 * permission from NTHU. 
 *
 * adc.h
 */

#ifndef _ADC_H_
#define	_ADC_H_

/* ADCCON register */
#define ADC_PWR_ON	(1 << 5)
#define	EXTREF		(1 << 4)

/* ADCSTATIC register */
#define	ADC_CLK_D32	(0 << 5)
#define	ADC_CLK_D8	(1 << 5)
#define	ADC_RES_6	0x00
#define	ADC_RES_8	0x01
#define	ADC_RES_10	0x02
#define	ADC_RES_12	0x03

/* the default value of ADCCON is 0x80, hence the H -> L -> H
 * sequence to start the ADC has L -> H left
 */
#define ADC_START()			\
	do {				\
		ADCCON &= ~0x80;	\
		ADCCON |= 0x80;		\
	} while (0)

#define ADC_EOC		(1 << 4)

/* pins connected to the accelerometer */
#define	X_AXIS		3
#define	Y_AXIS		4
#define Z_AXIS		6

void adc_init(char clk, char resol, char extref);
int adc_read(char in_pin);

#endif

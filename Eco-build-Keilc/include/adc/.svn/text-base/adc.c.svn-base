/*
 * Author(s): Min-Hua Chen (Embedded Platform Lab, NTHU)
 * Copyright (c) 2008 National Tsing Hua University (NTHU) 
 * Permission to copy, modify, and distribute this program is granted 
 * for noncommercial purposes, provided the author(s) and copyright 
 * notice are retained. All other uses require explicit written 
 * permission from NTHU. 
 *
 * A/D converter driver 
 * Min-Hua Chen <orca.chen@gmail.com> 
 * 2007/8/1
 */

#include <Eco/reg24e1.h>
#include <adc/adc.h>

/* adc_init - initialize A/D converter
 * @CLK: clock rate, 1/n of CPU clock rate
 * @resol: data resolution
 * @extref: internal or external reference voltage
 */
void adc_init(char clk, char resol, char extref)
{
	/* ADCCON init value: 0x80 */
	ADCCON |= ADC_PWR_ON;	/* power on */
	ADCCON |= extref;	/* use external reference */
	ADCSTATIC &= ~(1 << 5);	/* clean [5] bit */
	ADCSTATIC |= clk;	/* setup ADC clock */
	ADCSTATIC &= ~0x03;	/* clean [0:1] bits */
	ADCSTATIC |= resol;	/* 12-bit resolution */
}

static int p_adc_read()
{
	int resol = ADCSTATIC & 0x03;	/* get resolution */
	int val = 0;
	switch (resol) {
	case 0:
	case 1:
		/* data is in ADCDATAH only */
		val = ADCDATAH;
		break;
	case 2:
		/* data is ADCDATAH + ADCDATA[7:6] */
		val = (ADCDATAH << 2);
		val += (ADCDATAL >> 6);
	case 3:
		/* data is ADCDATAH + ADCDATA[7:4] */
		val = (ADCDATAH << 4);
		val += (ADCDATAL >> 4);
	}
	return val;
}

int adc_read(char in_pin)
{
	int ret = 0;
	/* check data if necessary */
	ADCCON &= ~0x07;	/* clean [0:2] bits */
	ADCCON |= in_pin;	/* select input pin */
	ADC_START();	/* start A/D conversion */

	while (!(EXIF & ADC_EOC))	/* wait until done */
		;

	ret = p_adc_read();	/* read ADCDATAH/L register */

	EXIF &= ~ADC_EOC;	/* clear EXIF.4 */
	return ret;
}

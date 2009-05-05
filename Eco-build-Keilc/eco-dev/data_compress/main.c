#include "Eco/reg24e1.h"
#include "Eco/eco_sys.h"
#include "utils/utils.h"
#include "serial/serial.h"
#include "isr/isr_rf.h"
#include "eeprom/eeprom.h"
#include "eco_page.h"
#include "adc/adc.h"
#include <math.h>

#define LEN 27
struct rf_config rf_data = { {0x00}, /* data2 width */
    {0xA0}, /* data1 width */ 
    {0x00, 0x00, 0x00, 0x00, 0x00}, /* addr2 */
    {0xF2, 0xF2, 0xF2, 0xF2, 0xF2}, /* addr1, host addr */
    {0x63}, /* 24-bit address, 16-bit CRC */
    {0x6f, 0xEC} };
struct rf_config *cfg = &rf_data;

//struct rf_config *cfg = &rf_data;
char dst_addr[3] = { 0xF1, 0xF1, 0xF1 };
char idata msg[54];

int log_2(int x){

	if( x > 0)
		return ((float)log(x))/(float)(log(2)) + 1;
	else if(x == 0)
		return 0;
	else
		return ((float)log(-x))/(float)(log(2)) + 2;
}

void delta_compress()
{
	int i,j;
	float idata delta;
	int now,prev;

	now = prev = (int)(msg[0]<<8) + msg[1];

	for(i=2,j=2;i<LEN*2;i+=2,j++)
	{
		prev = now;
		now = (int)(msg[i]<<8) + msg[i+1];
		delta = now - prev;
		/*
		   int_print(i);
		   puts(":");
		   int_print(prev);
		   puts(" ");
		   int_print(now);
		   puts(" ");

		   int_print(delta);
		   puts("\r\n");
		 */

		if(log_2(delta)>8)
			msg[j] = now;
		else
			msg[j] = delta;
	}
}


int main()
{

	int i;
	int accx;
	store_cpu_rate(16);
	/* init led */
	P0_DIR &= ~0x28;
	P0_ALT &= ~0x28;

	//serial_init(19200);

	for (i = 0; i < 6; i++) {
		blink_led();
		mdelay(400);
	}
	/* init adc */
	adc_init(ADC_CLK_D8, ADC_RES_12, EXTREF);

	/* rf */
	rf_init();
	rf_configure(cfg);


	while(1)
	{
		for(i=0;i<LEN*2;i+=2){
			accx = adc_read(X_AXIS);
			msg[i] = (accx >> 8);
			msg[i+1] = accx & 0xff;
			mdelay(5);
		}

		delta_compress();
		rf_send(dst_addr, 3, msg, 20);
		blink_led();
		mdelay(20);
	}

}



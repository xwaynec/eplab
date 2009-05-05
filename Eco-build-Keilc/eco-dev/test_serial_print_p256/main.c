#include "Eco/reg24e1.h"
#include "Eco/eco_sys.h"
#include "utils/utils.h"
#include "serial/serial.h"
#include "isr/isr_rf.h"
#include "eeprom/eeprom.h"
//#include "eco_page.h"
#include "adc/adc.h"
#include <math.h>

#define LEN 27
struct rf_config rf_data = { {0x00}, /* data2 width */
    {0xA0}, /* data1 width */ 
    {0x00, 0x00, 0x00, 0x00, 0x00}, /* addr2 */
    {0xF2, 0xF2, 0xF2, 0xF2, 0xF2}, /* addr1, host addr */
    {0x63}, /* 24-bit address, 16-bit CRC */
    {0x6f, 0xEC} };

//struct rf_config *cfg = &rf_data;
char dst_addr[3] = { 0xF1, 0xF1, 0xF1 };
char idata msg[54];

volatile unsigned int test_counter;
volatile unsigned int flag;
volatile unsigned int timer_counter;

void timer0() interrupt 1
{
	if(timer_counter < 5000)
	{
		timer_counter++;
	}
	else
	{
		timer_counter = 0;
		flag = 1;
		EA = 0;
	}	
	
}
int log_2(int x)
{
    //EA = 0;   
    if( x > 0)
    {   
		if (x < 0) log10(x);
        while(x--)
        ;
		return ;
    }   
    else if(x == 0)
    {   
        return ;
    }   
    else
    {   
        return ;    
    }
}

void delta_compress()
{
    int i,j;
    float idata delta;
    int now,prev;
    test_counter++;
    now = prev = (msg[0]<<8) + msg[1];

    for(i=2,j=2;i<54;i+=2,j++)
    {
        prev = now;
        now = (msg[i]<<8) + msg[i+1];
        delta = now - prev;
        log_2(delta);
        msg[j] = now;
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

	//eco_page_init();

	serial_init(19200);
	puts("test:");
	int_print(test_counter);
  	puts("\r\n");

	for (i = 0; i < 6; i++) {
		blink_led();
		mdelay(400);
	}
	/* init adc */
	adc_init(ADC_CLK_D8, ADC_RES_12, EXTREF);

	/* rf */
	rf_init();
	rf_configure(&rf_data);

	//volatile value for calculating 
	test_counter = 0;
	timer_counter = 0;
	flag = 0;
	/* init timer */
	// TMOD.1 TMOD.2 [1 0] 8-bit counter with auto-reload
	TMOD = 0x02;
	TH0 = 0x00;
	//enable interrupt
	EA = 1;
	//enable timer interrupt
	ET0 = 1;
	//set to 1 to enable counting on Timer 0.		
	TR0 = 1;	

	while(1)
	{
		for(i=0;i<LEN*2;i+=2)
		{
			accx = adc_read(X_AXIS);
			msg[i] = (accx >> 8);
			msg[i+1] = accx & 0xff;
		}

		delta_compress();
		
		if(flag == 1)
		{
			flag = 0;
			blink_led();
			int_print(test_counter);
		   	puts("\r\n");
			EA = 1;
		}
		
		rf_send(dst_addr, 3, msg, 20);
	}

}



#include "Eco/reg24e1.h"
#include "Eco/eco_sys.h"
#include "utils/utils.h"
#include "serial/serial.h"
#include "isr/isr_rf.h"
#include "eeprom/eeprom.h"
#include "eco_page.h"


struct rf_config rf_data = { {0x00}, /* data2 width */
	{0x38}, /* data1 width */ 
	{0x00, 0x00, 0x00, 0x00, 0x00}, /* addr2 */
	{0xF2, 0xF2, 0xF2, 0xF2, 0xF2}, /* addr1, host addr */
	{0x63}, /* 24-bit address, 16-bit CRC */
	{0x6f, 0xEC} };
struct rf_config *cfg = &rf_data;
char dst_addr[3] = {0xF1, 0xF1, 0xF1};
idata char msg[7];


extern unsigned char ECO_PAGE_SPI_CONN;
/* rf.c
void rf_init();
void rf_configure(struct rf_config);
void rf_send(char *, unsigned char, char *, unsigned char);
*/

/*int long_function(int time1,int time2,int time3,int time4)
{
	int i;

	for(i=0;i<time1;i++)
	{
		blink_led();
		mdelay(300);
	}

	for(i=0;i<time2;i++)
	{
		blink_led();
		mdelay(300);
	}

	for(i=0;i<time3;i++)
	{
		blink_led();
		mdelay(300);
	}
	
	for(i=0;i<time4;i++)
	{
		blink_led();
		mdelay(300);
	}

	msg[0] = 0x0A;
	msg[1] = 0x00;
	msg[2] = 0x02;
	msg[3] = 0xA0;
	msg[4] = 0x02;
	msg[5] = 0xDD;
	msg[6] = 0xCC;
	mdelay(1000);

	for(i=0;i<time1;i++)
	{
		blink_led();
		mdelay(300);
	}

	for(i=0;i<time2;i++)
	{
		blink_led();
		mdelay(300);
	}

	for(i=0;i<time3;i++)
	{
		blink_led();
		mdelay(300);
	}
	
	for(i=0;i<time4;i++)
	{
		blink_led();
		mdelay(300);
	}

	msg[0] = 0x0A;
	msg[1] = 0x00;
	msg[2] = 0x02;
	msg[3] = 0xA0;
	msg[4] = 0x02;
	msg[5] = 0xDD;
	msg[6] = 0xCC;
	mdelay(1000);
}
*/

void blink2()
{
	int i;
	for(i=0;i<4;i++)
	{
		blink_led();
		mdelay(400);
	}
	mdelay(1000);	
}
void blink4()
{
	int i;
	for(i=0;i<8;i++)
	{
		blink_led();
		mdelay(400);
	}	
	mdelay(1000);	
}
void blink6()
{
	int i;
	for(i=0;i<12;i++)
	{
		blink_led();
		mdelay(400);
	}	
	mdelay(1000);	
}

int main()
{
	unsigned char idx;
	unsigned int i = 0;
	store_cpu_rate(16);
	P0_DIR &= ~0x28;
	P0_ALT &= ~0x28;
	rf_init();
	rf_configure(cfg);
	serial_init(19200);	
	eco_page_init();
	
	//long_function(4,6,8,4);

	msg[0] = 0x0A;
	msg[1] = 0x00;
	/* ADDR */
	msg[2] = 0x02;
	msg[3] = 0xA0;
	/* LEN */
	msg[4] = 0x02;
	msg[5] = 0xDD;
	msg[6] = 0xCC;
	
	for(idx = 4; idx > 0; idx--)
	{
		blink_led();		
		mdelay(300);
	}

	mdelay(1000);	

	while(1)
	{
		blink4();
		rf_send(dst_addr, 3, msg, 7);
		blink2();
		mdelay(200);	
		blink6();
	}

	return 0;
}

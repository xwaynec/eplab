#include "Eco/reg24e1.h"
#include "Eco/eco_sys.h"
#include "utils/utils.h"
#include "serial/serial.h"
#include "isr/isr_rf.h"
#include "eeprom/eeprom.h"
#include "eco_page.h"
#include "adc/adc.h"


#include <math.h> /* for log */



struct rf_config rf_data = { {0x00}, /* data2 width */
	{0xA0}, /* data1 width */ 
	{0x00, 0x00, 0x00, 0x00, 0x00}, /* addr2 */
	{0xF2, 0xF2, 0xF2, 0xF2, 0xF2}, /* addr1, host addr */
	{0x63}, /* 24-bit address, 16-bit CRC */
	{0x6f, 0xEC} };
struct rf_config *cfg = &rf_data;
char dst_addr[3] = {0xF1, 0xF1, 0xF1};
char idata msg[20];


/*void blink2()
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
*/

void delta_compress(char *ptr)
{
			
}

int main()
{
	unsigned int i = 0;
	store_cpu_rate(16);
	P0_DIR &= ~0x20;
	P0_ALT &= ~0x20;

	adc_init(ADC_CLK_D8,ADC_RES_12,EXTREF);

	rf_init();
	rf_configure(cfg);
	//serial_init(19200);	
	eco_page_init();

	for(i=0;i<6;i++)
	{
		blink_led();
		mdelay(300);
	}
	
	mdelay(1000);

	while(1)
	{
		//blink4();
		int acc_x,acc_y,acc_z;
		acc_x = adc_read(X_AXIS);
		acc_y = adc_read(Y_AXIS);
		acc_z = adc_read(Z_AXIS);
		
		msg[0] = acc_x & 0x00FF;
		msg[1] = acc_x >> 8;

		msg[2] = acc_y & 0x00FF;
		msg[3] = acc_y >> 8;
		
		msg[4] = acc_z & 0x00FF;
		msg[5] = acc_z >> 8;
	
		delta_compress(msg);
	
		rf_send(dst_addr, 3, msg, 20);

		//blink2();
		mdelay(200);
		blink_led();
		//mdelay(200);
	}

	return 0;
}

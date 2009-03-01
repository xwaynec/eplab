#include "Eco/reg24e1.h"
#include "Eco/eco_sys.h"
#include "utils/utils.h"
#include "eeprom/eeprom.h"
#include "adc/adc.h"
#include "eco_page.h"
//#include "rf/rf.h"
#include "serial/serial.h"
#include "isr/isr_rf.h"

extern struct radio_buffer rf_buf;
struct rf_config rf_data = { 
	{0x00}, /* data2 width */
	{0xA8}, /* data1 width */
	{0x00, 0x00, 0x00, 0x00, 0x00}, /* addr2 */
	{0xF1, 0xF1, 0xF1, 0xF1, 0xF1}, /* addr1, host addr */
	{0xA3}, /* 24-bit address, 8-bit CRC */
	{0x6F, 0xEC} 
};
struct rf_config *cfg = &rf_data;
char dst_addr[5] = {0xF1, 0xF2, 0xF3, 0xF4, 0xF5};
char msg[6] = { 0x00, 0x01, 0x02, 0x04, 0x08, 0x0F};

void main()
{
	int i;

	store_cpu_rate(16);

	/* init led */
	P0_DIR &= ~0x28;
	P0_ALT &= ~0x28;

	for(i=0;i<6;i++)
	{
		blink_led();
		mdelay(300);
	}
	/* init adc */
	adc_init(ADC_CLK_D8, ADC_RES_12, EXTREF);
		   
	/* serial init */
    serial_init(19200);
	puts("rf guest program\n\r");

	/* rf init */
	rf_init();
	rf_configure(cfg);


	while(1)
	{
		int acc;
		
		acc = adc_read(X_AXIS);
		msg[0] = (acc >> 8);
		msg[1] = acc & 0xff;

		acc = adc_read(Y_AXIS);
		msg[2] = (acc >> 8);
		msg[3] = acc & 0xff;

		acc = adc_read(Z_AXIS);
		msg[4] = (acc >> 8);
		msg[5] = acc & 0xff;

		rf_send(dst_addr, 4, msg, 6);
		blink_led();
		mdelay(50);
	}
}




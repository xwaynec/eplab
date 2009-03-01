#include "Eco/reg24e1.h"
#include "Eco/eco_sys.h"
#include "utils/utils.h"
#include "eeprom/eeprom.h"
#include "adc/adc.h"
#include "eco_page.h"
#include "serial/serial.h"
//#include "rf/rf.h"
#include "isr/isr_rf.h"

//extern char rf_buf[RF_BUF_LEN];
extern struct radio_buffer rf_buf;
struct rf_config rf_data = { {0x00}, /* data2 width */
	{0xA8}, /* data1 width */
	{0x00, 0x00, 0x00, 0x00, 0x00}, /* addr2 */
	{0xF1, 0xF2, 0xF3, 0xF4, 0xF5}, /* addr1, host addr */
	{0xA3}, /* 24-bit address, 8-bit CRC */
	{0x6F, 0xED} };
struct rf_config *cfg = &rf_data;
char dst_addr[5] = {0x01, 0x01, 0x01};
/* utils.c */


int main()
{
	int i;
	int acc = 0;
	store_cpu_rate(16);
	/* init led */
	P0_DIR &= ~0x28;
	P0_ALT &= ~0x28;
	TMOD = 0x02;
    TH0 = 0xA4;
   	EA = 1;
    ET0 = 1;
    TR0 = 1;

	for (i = 0; i < 6; i++) {
		blink_led();
		mdelay(400);
	}
	
	/* init adc */
    adc_init(ADC_CLK_D8, ADC_RES_12, EXTREF);
	
	/* serial */
	serial_init(19200);
	puts("rf testing program starts\n\r");

	/* rf */
	rf_init();
	rf_configure(cfg);

	/* init IO port */
	//P0_ALT &= ~0x06;
	//P0_DIR &= ~0x06;

	while (1) {
		
		puts("rf recv:\n\r");
		rf_buf.ready = 0;
		rf_wait_msg();

		acc = rf_buf.buffer[1] + (rf_buf.buffer[0] << 8);
		puts("X:");
		int_print(acc);
		puts("    ");
		acc = rf_buf.buffer[3] + (rf_buf.buffer[2] << 8);
		puts("Y:");
		int_print(acc);
		puts("    ");
		acc = rf_buf.buffer[5] + (rf_buf.buffer[4] << 8);
		puts("Z:");
		int_print(acc);
		puts("\n\r");

		blink_led();
		mdelay(10);
	}


	return 0;
}


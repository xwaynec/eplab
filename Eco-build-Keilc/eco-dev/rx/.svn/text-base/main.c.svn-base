#include "Eco/reg24e1.h"
#include "Eco/eco_sys.h"
#include "utils/utils.h"
#include "spi/spi.h"
#include "isr/isr_rf.h"
#include "serial/serial.h"

struct rf_config rf_data = { {0x00}, /* data2 width */
	{0x38}, /* data1 width */ 
	{0x00, 0x00, 0x00, 0x00, 0x00}, /* addr2 */
	{0xF1, 0xF1, 0xF1, 0xF1, 0xF1}, /* addr1, host addr */
	{0x63}, /* 24-bit address, 16-bit CRC */
	{0x6f, 0xED} };
struct rf_config *cfg = &rf_data;


int main()
{
	unsigned char  idx;
		
	store_cpu_rate(16);
	P0_DIR &= ~0x28;
	P0_ALT &= ~0x28;
	EA = 1;		// Enable interrupts	
	rf_init();
	rf_configure(cfg);
	EX4 = 1;	// Enable interrupt 4(RADIO.DR1)
	CE = 1;		// Enable transmission/receive
	serial_init(19200);		
	
	for(idx = 4; idx > 0; idx--)
	{
		blink_led();
		mdelay(300);
	}	
	
	puts("test start\n\r");

	while(1)
	{		
		if(rf_buf.ready)
		{
			rf_buf.ready = 0;			
			putc('c');
		}			
	}
	return 0;
}


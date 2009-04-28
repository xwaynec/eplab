#include "Eco/reg24e1.h"
#include "Eco/eco_sys.h"
#include "utils/utils.h"
#include "serial/serial.h"
#include "isr/isr_rf.h"
#include "eeprom/eeprom.h"
//#include "eco_page.h"


int main()
{
	unsigned char idx;
	unsigned int i = 0;
	store_cpu_rate(16);
	P0_DIR &= ~0x28;
	P0_ALT &= ~0x28;
	//rf_init();
	//rf_configure(cfg);
	//serial_init(19200);	
	//eco_page_init();
	
	//long_function(4,6,8,4);

	
	for(idx = 4; idx > 0; idx--)
	{
		blink_led();		
		mdelay(300);
	}
	mdelay(1000);	

	eeprom_init();
	while(1)
	{
		unsigned char xdata *seg = (unsigned char xdata *)(0x800);
		
		//memory page is in ram

		for(i=0;i<256;i++)
		{
			*(seg+i) = eeprom_read(i);
		}
		blink_led();
		mdelay(300);
	}

	return 0;
}

#include "Eco/reg24e1.h"
#include "Eco/eco_sys.h"
#include "utils/utils.h"


int main()
{
	unsigned int i = 0;
	store_cpu_rate(16);

	P0_DIR &= ~0x28;
	P0_ALT &= ~0x28;


	while(1)
	{
		blink_led();
		mdelay(300);
	}
	
	return 0;
}

#include "Eco/reg24e1.h"
#include "Eco/eco_sys.h"
#include "utils/utils.h"
#include "eeprom/eeprom.h"
#include "eco_page.h"

//static unsigned char ECO_PAGE_TABLE[10];
//static unsigned int ECO_PAGE_ADDR;
//static unsigned int ECO_PAGE_TABLE_INDEX;

extern unsigned int ECO_PAGE_ADDR;


int blink_led_auto(int x,int y,int z,int w,int s)
{
	int i;

	for(i=0;i<x;i++)
	{
		blink_led();
		mdelay(y*100);
	}

	for(i=0;i<w;i++)
	{
		blink_led();
		mdelay(z*100);
	}

	mdelay(s*100);

	return x+y+z;
}

void blink_led_by_time(int times,int slot)
{
	int i;
	for(i=0;i<times;i++)
	{
		blink_led();
		mdelay(slot*100);
	}
}


void blink_fast()
{
	int i;
	mdelay(400);
	for(i=0;i<14;i++)	
	{
		blink_led();	
		mdelay(300);
	}
}
void blink_fast2()
{
	int i;
	mdelay(400);
	for(i=0;i<12;i++)	
	{
		blink_led();	
		mdelay(400);
	}
}

void main(void)
{
	int i;
	//unsigned char xdata *seg = (unsigned char xdata *)(0x500);

	//int auto_i;
	
	//init LED
	P0_DIR &= ~0x28;
	P0_ALT &= ~0x28;

	store_cpu_rate(16);

	for(i=0;i<6;i++)
	{
		//LED blink
		blink_led();
		mdelay(200);
	}

	mdelay(1000);	
		
	eeprom_init();
	
	//Get data from 0x1000 address
	//for(i=0;i<64;i++)
	//{
	//	*(seg+i) = eeprom_read(ECO_ADDR_SHIFT(4096) +i);
	//}	
	mdelay(1000);

	eco_page_init();		
	//ECO_PAGE_MANAGER();

	blink_fast2();	
	//MOV	ECO_PAGE_ADDR,#HIGH (blink_fast2)
	//MOV	ECO_PAGE_ADDR+01H,#LOW (blink_fast2)	
	//LCALL	eco_page_manager	
	
	mdelay(1000);		

	//blink_led_by_time(4,6);

	blink_fast();
	//MOV	ECO_PAGE_ADDR,#HIGH (blink_fast)
	//MOV	ECO_PAGE_ADDR+01H,#LOW (blink_fast)	
	//LCALL	eco_page_manager
	//mdelay(1000);
	
	//auto_i = blink_led_auto(4,4,5,6,2);
	//ECO_PAGE_MANAGER();
	
	mdelay(1000);
	
	blink_fast();
	//MOV	ECO_PAGE_ADDR,#HIGH (blink_fast)
	//MOV	ECO_PAGE_ADDR+01H,#LOW (blink_fast)	
	//LCALL	eco_page_manager	
	mdelay(1);	
}

#include "Eco/reg24e1.h"
#include "Eco/eco_sys.h"
#include "utils/utils.h"
#include "eeprom/eeprom.h"
#include "eco_page.h"

#define EEPROM_HEADER 3
#define ECO_PAGE_ADDR_OFFSET	6
#define ECO_ADDR_SHIFT(x)	((unsigned int)(x) + 3)

//static unsigned char ECO_PAGE_TABLE[10];

//extern ECO_PAGE_ADDR;



void ECO_PAGE_INIT()
{
	
	ECO_PAGE_TABLE_INDEX = 5;
		
	ECO_PAGE_TABLE[0] = -1;
	ECO_PAGE_TABLE[1] = -1;
	ECO_PAGE_TABLE[2] = 8;
	ECO_PAGE_TABLE[3] = -1;
	ECO_PAGE_TABLE[4] = -1;
	ECO_PAGE_TABLE[5] = -1;
	ECO_PAGE_TABLE[6] = -1;
	ECO_PAGE_TABLE[7] = -1;
	ECO_PAGE_TABLE[8] = -1;
	ECO_PAGE_TABLE[9] = -1; 

}

void ECO_PAGE_TABLE_UPDATE(int index,int page_number)
{
	ECO_PAGE_TABLE[index] = page_number;
}

void ECO_PAGE_SEGMENT_UPDATE()
{
	unsigned char xdata *seg = (unsigned char xdata *)(0x500);
	
}

void ECO_PAGE_MANAGER()
{
	unsigned int i,page_index = -1;	
		
	//Check POP instruction 
	for(i=0;i<10;i++)
	{	
		blink_led();
		mdelay(400);
	}	

	mdelay(1000);
		
	//Check Table	
	for(i=0;i<10;i++)
	{
		if(ECO_PAGE_ADDR == (ECO_PAGE_TABLE[i] << 8))
		{
			page_index = i;
			break;		
		}	
		
	}
	if(page_index != -1)
	{
		//memory page is in ram
		for(i=0;i<4;i++)
		{
			blink_led();
			mdelay(400);
		}
		ECO_PAGE_ADDR = (page_index + ECO_PAGE_ADDR_OFFSET) << 8;
		#pragma asm
		MOV	DPH,ECO_PAGE_ADDR
		MOV	DPL,ECO_PAGE_ADDR+01H
		//;LCALL	?C?ICALL2
		#pragma endasm
	}
	else
	{
		//page fault
		/* Move Data from EEPROM to iRAM */	
		unsigned char xdata *seg = (unsigned char xdata *)((ECO_PAGE_TABLE_INDEX + ECO_PAGE_ADDR_OFFSET)<<8);	
			
		for(i=0;i<256;i++)
		{
			*(seg+i) = eeprom_read(ECO_ADDR_SHIFT(ECO_PAGE_ADDR) +i);
		}

		//Update Page Table
		ECO_PAGE_TABLE[ECO_PAGE_TABLE_INDEX] = ECO_PAGE_ADDR >> 8;
		
		//Update Page Address
		ECO_PAGE_ADDR = ((ECO_PAGE_TABLE_INDEX + ECO_PAGE_ADDR_OFFSET) << 8);
	
		ECO_PAGE_TABLE_INDEX++;
	
		//Jump	to Function Address	
		
		#pragma asm
		MOV	DPH,ECO_PAGE_ADDR
		MOV	DPL,ECO_PAGE_ADDR+01H
		//;LCALL	?C?ICALL2		
		#pragma endasm
			
	}
	mdelay(1);
}

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

	ECO_PAGE_INIT();	
		
	//ECO_PAGE_MANAGER();

	blink_fast2();		
	//MOV	ECO_PAGE_ADDR,#HIGH (blink_fast2)
	//MOV	ECO_PAGE_ADDR+01H,#LOW (blink_fast2)	
	//LCALL	ECO_PAGE_MANAGER	
	
	mdelay(1000);		

	//blink_led_by_time(4,6);

	blink_fast();
	//MOV	ECO_PAGE_ADDR,#HIGH (blink_fast)
	//MOV	ECO_PAGE_ADDR+01H,#LOW (blink_fast)	
	//LCALL	ECO_PAGE_MANAGER	
	//mdelay(1000);
	
	//auto_i = blink_led_auto(4,4,5,6,2);
	//ECO_PAGE_MANAGER();
	
	mdelay(1000);
	
	blink_fast();
	//MOV	ECO_PAGE_ADDR,#HIGH (blink_fast)
	//MOV	ECO_PAGE_ADDR+01H,#LOW (blink_fast)	
	//LCALL	ECO_PAGE_MANAGER	
	mdelay(1);	
}

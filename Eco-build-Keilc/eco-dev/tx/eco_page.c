/*
 * Author(s): Wei-Han Chen (Embedded Platform Lab, NTHU)
 * Copyright (c) 2009 National Tsing Hua University (NTHU) 
 * Permission to copy, modify, and distribute this program is granted 
 * for noncommercial purposes, provided the author(s) and copyright
 * notice are retained. All other uses require explicit written
 * permission from NTHU. 
 *
 * Eco Paging Library 
 *
 * Wei-Han Chen <xwaynec@gmail.com> 
 * 2009/2/13
 */


#include "eco_page.h"
#include "eeprom/eeprom.h"
#include "isr/isr_rf.h"
//test

static unsigned char ECO_PAGE_TABLE[10];
static unsigned int ECO_PAGE_TABLE_INDEX;

unsigned int ECO_PAGE_ADDR;
unsigned char ECO_PAGE_SPI_CONN;

unsigned char ECO_PAGE_REGISTER3;
unsigned char ECO_PAGE_REGISTER2;
unsigned char ECO_PAGE_REGISTER1;
unsigned char ECO_PAGE_REGISTER5;

void eco_page_init()
{
	

	ECO_PAGE_TABLE_INDEX = 5;

	ECO_PAGE_ADDR = 0;

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


void eco_page_manager()
{
	unsigned int i;
	unsigned int page_index = -1; 

	//Check POP instruction 
	/*for(i=0;i<10;i++)
	{    
		blink_led();
		mdelay(200);
	}    

	mdelay(1000);
	*/
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
		/*for(i=0;i<4;i++)
		{   
			blink_led();
			mdelay(400);
		} 
		*/

		ECO_PAGE_ADDR = (page_index + ECO_PAGE_ADDR_OFFSET) << 8;
	
		rf_init();
		#pragma asm
		//eco_page_function_call
		//MOV     DPH,ECO_PAGE_ADDR
		//MOV     DPL,ECO_PAGE_ADDR+01H
		//LCALL	?C?ICALL2
		#pragma endasm
	}   
	else
	{
		//page fault
		/* Move Data from EEPROM to iRAM */
		unsigned char xdata *seg = (unsigned char xdata *)((ECO_PAGE_TABLE_INDEX + ECO_PAGE_ADDR_OFFSET)<<8);
		
		//memory page is in ram
		/*for(i=0;i<4;i++)
		{   
			blink_led();
			mdelay(400);
		}
		mdelay(1000);
*/
		eeprom_init();
		for(i=0;i<256;i++)
		{
			*(seg+i) = eeprom_read(ECO_ADDR_SHIFT(ECO_PAGE_ADDR) +i);
		}
		
		//memory page is in ram
		/*for(i=0;i<4;i++)
		{   
			blink_led();
			mdelay(300);
		}*/
		//mdelay(1000);

		//Update Page Table
		ECO_PAGE_TABLE[ECO_PAGE_TABLE_INDEX] = ECO_PAGE_ADDR >> 8;

		//Update Page Address
		ECO_PAGE_ADDR = ((ECO_PAGE_TABLE_INDEX + ECO_PAGE_ADDR_OFFSET) << 8);

		ECO_PAGE_TABLE_INDEX++;

		//Jump  to Function Address
		rf_init();
		#pragma asm
		//MOV     DPH,ECO_PAGE_ADDR
		//MOV     DPL,ECO_PAGE_ADDR+01H
		//LCALL        ?C?ICALL2               
		#pragma endasm

	}

	mdelay(1);

}

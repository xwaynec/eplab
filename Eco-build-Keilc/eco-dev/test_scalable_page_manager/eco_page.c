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

#define ECO_PAGE_SIZE 256
#define ECO_PAGE_ADDR_OFFSET	11	

#if ECO_PAGE_SIZE == 64
	
	#define ECO_PAGE_ENTRY	48
	#define ECO_PAGE_SHIFT	6
	#define ECO_PAGE_MASK	0x003F
	#define ECO_PAGE_MOV_MASK	0xFC00

	unsigned int idata ECO_PAGE_TABLE[63-ECO_PAGE_ADDR_OFFSET] = {0};
	//Eco page virtual address id
	unsigned int ECO_PAGE_PREV_VID;
	//Eco page physical address id 
	unsigned int ECO_PAGE_PREV_PID;

#elif ECO_PAGE_SIZE == 128
	
	#define ECO_PAGE_ENTRY 24	
	#define ECO_PAGE_SHIFT	7
	#define ECO_PAGE_MASK	0x007F
	#define ECO_PAGE_MOV_MASK	0xFE00

	//unsigned int idata ECO_PAGE_TABLE[32-ECO_PAGE_ADDR_OFFSET] = {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24};
	unsigned int idata ECO_PAGE_TABLE[31-ECO_PAGE_ADDR_OFFSET];
	//Eco page virtual address id
	unsigned int ECO_PAGE_PREV_VID;
	//Eco page physical address id 
	unsigned int ECO_PAGE_PREV_PID;

#elif ECO_PAGE_SIZE == 256
	
	#define ECO_PAGE_ENTRY 	(15-ECO_PAGE_ADDR_OFFSET)
	#define ECO_PAGE_SHIFT	8	
	#define ECO_PAGE_MASK	0x00FF
	#define ECO_PAGE_MOV_MASK	0xFF00
	

	unsigned int ECO_PAGE_TABLE[ECO_PAGE_ENTRY];
	//Eco page virtual address id
	unsigned char ECO_PAGE_PREV_VID;
	//Eco page physical address id 
	unsigned char ECO_PAGE_PREV_PID;

#endif

unsigned char ECO_PAGE_TABLE_INDEX;

unsigned int ECO_PAGE_ADDR;

unsigned char ECO_PAGE_SPI_CONN;

unsigned char idata ECO_PAGE_REGISTER1;
unsigned char idata ECO_PAGE_REGISTER2;
unsigned char idata ECO_PAGE_REGISTER3;
unsigned char idata ECO_PAGE_REGISTER4;
unsigned char idata ECO_PAGE_REGISTER5;
unsigned char idata ECO_PAGE_REGISTER6;
unsigned char idata ECO_PAGE_REGISTER7;


void eco_page_init()
{
	ECO_PAGE_TABLE_INDEX = 0;
	
	ECO_PAGE_ADDR = 0;
	ECO_PAGE_PREV_VID = 0;
	ECO_PAGE_PREV_PID = 0;

	/*
	ECO_PAGE_TABLE[0] = 0; 
	ECO_PAGE_TABLE[1] = 0; 
	ECO_PAGE_TABLE[2] = 0;
	ECO_PAGE_TABLE[3] = 0; 
	ECO_PAGE_TABLE[4] = 0; 
	ECO_PAGE_TABLE[5] = 0; 
	ECO_PAGE_TABLE[6] = 0; 
	ECO_PAGE_TABLE[7] = 0; 
	ECO_PAGE_TABLE[8] = 0; 
	ECO_PAGE_TABLE[9] = 0;
	ECO_PAGE_TABLE[10] = 0; 
	ECO_PAGE_TABLE[11] = 0; 
	ECO_PAGE_TABLE[12] = 0;
	*/	
}

//LRU page replacement
/*void eco_page_manager()
{
	unsigned int i;
	unsigned int page_index = -1;

	//if page id is the same with the last page id
	if(((ECO_PAGE_ADDR >> 8) & 0x7F) == (ECO_PAGE_PREV_PID & 0x7F))
	{
		//virtual address id + function offset
		ECO_PAGE_ADDR = (ECO_PAGE_PREV_VID << 8) + (ECO_PAGE_ADDR & 0x00FF);
		#pragma asm
		//eco_page_function_call	
		//MOV     DPH,ECO_PAGE_ADDR
		//MOV     DPL,ECO_PAGE_ADDR+01H
		//LCALL	?C?ICALL2
		#pragma endasm
		return ;
	}	
	
	//check page table
	for(i=0;i<ECO_PAGE_ENTRY;i++)
	{
		if((ECO_PAGE_ADDR >> 8) == ECO_PAGE_TABLE[i])
		{
			page_index = i;
			
			//set LRU bit is 1
			ECO_PAGE_TABLE[i] = ECO_PAGE_TABLE[i] | 0x80;
			break;
		}
	}

	if(page_index != -1)
	{
		//store function physical addres id 
		ECO_PAGE_PREV_PID = ECO_PAGE_ADDR >> 8;
	
		//memory page is in ram
		ECO_PAGE_ADDR = ((page_index + ECO_PAGE_ADDR_OFFSET) << 8) + (ECO_PAGE_ADDR & 0x00FF);

		//cache the virtual address id
		ECO_PAGE_PREV_VID = ECO_PAGE_ADDR >> 8;

		#pragma asm
		//eco_page_function_call
		//MOV     DPH,ECO_PAGE_ADDR
		//MOV     DPL,ECO_PAGE_ADDR+01H
		//LCALL	?C?ICALL2
		#pragma endasm

		return ;
	}	
	else
	{
		//page fault
		for(i=ECO_PAGE_TABLE_INDEX+1; ;i=(i+1)%10)
		{
			if((ECO_PAGE_TABLE[i] & 0x80) == 0x80)
			{
				//LRU bit is 1 and then set this bit is 0
				ECO_PAGE_TABLE[i] = ECO_PAGE_TABLE[i] & 0x7F;
			}
			else
			{
				unsigned char xdata *seg = (unsigned char xdata *)((i + ECO_PAGE_ADDR_OFFSET)<<8);
				unsigned int j;
				
				//memory page is in ram
				eeprom_init();

				//mov code from eeprom to external ram
				for(j=0;j<256;j++)
				{
					*(seg+j) = eeprom_read(ECO_ADDR_SHIFT(ECO_PAGE_ADDR & 0xFF00 ) +j);
				}
				
				//update page table to connect this physical address id with virtual address id 
				ECO_PAGE_TABLE[i] = ECO_PAGE_ADDR >> 8;

				//store physical address id
				ECO_PAGE_PREV_PID = ECO_PAGE_TABLE[i];

				//update page address e.g.  (page_id<<8) + page_offset
				ECO_PAGE_ADDR = ((i + ECO_PAGE_ADDR_OFFSET) << 8) + (ECO_PAGE_ADDR & 0x00FF);

				//store virtual address id 
				ECO_PAGE_PREV_VID = ECO_PAGE_ADDR >> 8;	

				//mov to the next index
				ECO_PAGE_TABLE_INDEX = i;

				//jump  to function address
				#pragma asm
				//eco_page_function_call
				//MOV     DPH,ECO_PAGE_ADDR
				//MOV     DPL,ECO_PAGE_ADDR+01H
				//LCALL        ?C?ICALL2               
				#pragma endasm
				
				return ;
				
			}
		}
			
	}
				
}
*/

void eco_page_manager()
{
	unsigned int i;
	unsigned int page_index = -1; 

	//Check POP instruction 
	//for(i=0;i<10;i++)
	//{    
	//	blink_led();
	//	mdelay(200);
	//}    
	//mdelay(1000);
	
	//if page id is the same with the last page id
	if((ECO_PAGE_ADDR >> ECO_PAGE_SHIFT) == ECO_PAGE_PREV_PID)
	{
		//virtual address id + function offset
		ECO_PAGE_ADDR = (ECO_PAGE_PREV_VID << 8) + (ECO_PAGE_ADDR & 0x00FF);
		#pragma asm
		//eco_page_function_call
		#pragma endasm
		return ;
	}	
				
	//Check Table   
	for(i=0;i<ECO_PAGE_ENTRY;i++)
	{   
		if((ECO_PAGE_ADDR >> ECO_PAGE_SHIFT) == ECO_PAGE_TABLE[i])
		{
			page_index = i;
			break;
		}
	}

	if(page_index != -1) 
	{  
		//store function physical addres id 
		ECO_PAGE_PREV_PID = ECO_PAGE_ADDR >> ECO_PAGE_SHIFT;
	
		//memory page is in ram
		ECO_PAGE_ADDR = ((page_index + ECO_PAGE_ADDR_OFFSET) << ECO_PAGE_SHIFT) + (ECO_PAGE_ADDR & ECO_PAGE_MASK);

		//cache the virtual address id
		ECO_PAGE_PREV_VID = ECO_PAGE_ADDR >> ECO_PAGE_SHIFT;

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
		// Move Data from EEPROM to iRAM 
		unsigned char xdata *seg = (unsigned char xdata *)((ECO_PAGE_TABLE_INDEX + ECO_PAGE_ADDR_OFFSET) << ECO_PAGE_SHIFT);
		
		//memory page is in ram
		eeprom_init();

		//mov code from eeprom to external ram
		for(i=0;i<ECO_PAGE_SIZE;i++)
		{
			*(seg+i) = eeprom_read(ECO_ADDR_SHIFT(ECO_PAGE_ADDR & ECO_PAGE_MOV_MASK) +i);
		}
		
		//update page table to connect this physical address id with virtual address id 
		ECO_PAGE_TABLE[ECO_PAGE_TABLE_INDEX] = ECO_PAGE_ADDR >> ECO_PAGE_SHIFT;

		//store physical address id
		ECO_PAGE_PREV_PID = ECO_PAGE_TABLE[ECO_PAGE_TABLE_INDEX];

		//update page address
		ECO_PAGE_ADDR = ((ECO_PAGE_TABLE_INDEX + ECO_PAGE_ADDR_OFFSET) << ECO_PAGE_SHIFT) + (ECO_PAGE_ADDR & ECO_PAGE_MASK);

		//store virtual address id 
		ECO_PAGE_PREV_VID = ECO_PAGE_ADDR >> ECO_PAGE_SHIFT;	

		//mov to the next index
		ECO_PAGE_TABLE_INDEX++;
			
		//jump  to function address
		#pragma asm
		//eco_page_function_call
		//MOV     DPH,ECO_PAGE_ADDR
		//MOV     DPL,ECO_PAGE_ADDR+01H
		//LCALL        ?C?ICALL2               
		#pragma endasm

	}

}


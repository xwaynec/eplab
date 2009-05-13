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

//control page replacement policy is LRU or Round-Robin
#define PAGE_REPLACEMENT 1

//#define ECO_PAGE_SIZE 256
//#define ECO_PAGE_ADDR_OFFSET 11 


//#define ECO_PAGE_SIZE 128
//#define ECO_PAGE_ADDR_OFFSET 23



//#define ECO_PAGE_SIZE 64
//#define ECO_PAGE_ADDR_OFFSET 47


#define ECO_PAGE_SIZE 128
#define ECO_PAGE_ADDR_OFFSET 26


#if ECO_PAGE_SIZE == 64
	
	#define ECO_PAGE_ENTRY	(64-ECO_PAGE_ADDR_OFFSET)
	#define ECO_PAGE_SHIFT	6
	#define ECO_PAGE_MASK	0x003F
	#define ECO_PAGE_MOV_MASK	0xFFC0

	unsigned int idata ECO_PAGE_TABLE[ECO_PAGE_ENTRY];
	//Eco page virtual address id
	unsigned int ECO_PAGE_PREV_VID;
	//Eco page physical address id 
	unsigned int ECO_PAGE_PREV_PID;

#elif ECO_PAGE_SIZE == 128
	
	#define ECO_PAGE_ENTRY (32-ECO_PAGE_ADDR_OFFSET)
	#define ECO_PAGE_SHIFT	7
	#define ECO_PAGE_MASK	0x007F
	#define ECO_PAGE_MOV_MASK	0xFF80

	unsigned int idata ECO_PAGE_TABLE[ECO_PAGE_ENTRY];
	//Eco page virtual address id
	unsigned int ECO_PAGE_PREV_VID;
	//Eco page physical address id 
	unsigned int ECO_PAGE_PREV_PID;

#elif ECO_PAGE_SIZE == 256
	
	#define ECO_PAGE_ENTRY 	(16-ECO_PAGE_ADDR_OFFSET)
	#define ECO_PAGE_SHIFT	8	
	#define ECO_PAGE_MASK	0x00FF
	#define ECO_PAGE_MOV_MASK	0xFF00

	//unsigned int ECO_PAGE_TABLE[ECO_PAGE_ENTRY]={13,14,15};
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
	//ECO_PAGE_TABLE_INDEX = ECO_PAGE_ENTRY - 1;
	ECO_PAGE_TABLE_INDEX = 0;	
	ECO_PAGE_ADDR = 0;
	ECO_PAGE_PREV_VID = 0;
	ECO_PAGE_PREV_PID = 0;
}


#if PAGE_REPLACEMENT == 0 
//LRU page replacement
void eco_page_manager()
{
	unsigned int i;
	unsigned int page_index = -1;

	//if page id is the same with the last page id
	if((ECO_PAGE_ADDR >> ECO_PAGE_SHIFT) == ECO_PAGE_PREV_PID)
	{
		//virtual address id + function offset
		ECO_PAGE_ADDR = (ECO_PAGE_PREV_VID << ECO_PAGE_SHIFT) + (ECO_PAGE_ADDR & ECO_PAGE_MASK);
		#pragma asm

		MOV R0,#LOW (ECO_PAGE_REGISTER1)
   		MOV A,@R0
		MOV	R1,A

		MOV R0,#LOW (ECO_PAGE_REGISTER2)
   		MOV A,@R0
		MOV	R2,A

		MOV R0,#LOW (ECO_PAGE_REGISTER3)
   		MOV A,@R0
		MOV	R3,A

		MOV R0,#LOW (ECO_PAGE_REGISTER4)
   		MOV A,@R0
		MOV	R4,A

		MOV R0,#LOW (ECO_PAGE_REGISTER5)
   		MOV A,@R0
		MOV	R5,A

		MOV R0,#LOW (ECO_PAGE_REGISTER6)
   		MOV A,@R0
		MOV	R6,A

		MOV R0,#LOW (ECO_PAGE_REGISTER7)
   		MOV A,@R0
		MOV	R7,A
	
		MOV	SPI_CTRL,ECO_PAGE_SPI_CONN
		MOV	DPH,ECO_PAGE_ADDR
		MOV	DPL,ECO_PAGE_ADDR+01H
				
		CLR	A
		JMP	@A+DPTR
		#pragma endasm
	}

	//Check Table   
	for(i=0;i<ECO_PAGE_ENTRY;i++)
	{   
		if((ECO_PAGE_ADDR >> ECO_PAGE_SHIFT) == (ECO_PAGE_TABLE[i] & 0x7FFF))
		{
			page_index = i;

			//set LRU bit is 1
			ECO_PAGE_TABLE[i] = ECO_PAGE_TABLE[i] | 0x8000;
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
		MOV R0,#LOW (ECO_PAGE_REGISTER1)
   		MOV A,@R0
		MOV	R1,A

		MOV R0,#LOW (ECO_PAGE_REGISTER2)
   		MOV A,@R0
		MOV	R2,A

		MOV R0,#LOW (ECO_PAGE_REGISTER3)
   		MOV A,@R0
		MOV	R3,A

		MOV R0,#LOW (ECO_PAGE_REGISTER4)
   		MOV A,@R0
		MOV	R4,A

		MOV R0,#LOW (ECO_PAGE_REGISTER5)
   		MOV A,@R0
		MOV	R5,A

		MOV R0,#LOW (ECO_PAGE_REGISTER6)
   		MOV A,@R0
		MOV	R6,A

		MOV R0,#LOW (ECO_PAGE_REGISTER7)
   		MOV A,@R0
		MOV	R7,A

		MOV	SPI_CTRL,ECO_PAGE_SPI_CONN
		MOV	DPH,ECO_PAGE_ADDR
		MOV	DPL,ECO_PAGE_ADDR+01H
				
		CLR	A
		JMP	@A+DPTR
		#pragma endasm

	}	
	else
	{
		//page fault
		for(i=(ECO_PAGE_TABLE_INDEX+1)%ECO_PAGE_ENTRY; ;i=(i+1)%ECO_PAGE_ENTRY)
		{
			if((ECO_PAGE_TABLE[i] & 0x8000) == 0x8000)
			{
				//LRU bit is 1 and then set this bit is 0
				ECO_PAGE_TABLE[i] = ECO_PAGE_TABLE[i] & 0x7FFF;
			}
			else
			{
				unsigned char xdata *seg = (unsigned char xdata *)((i + ECO_PAGE_ADDR_OFFSET) << ECO_PAGE_SHIFT);
				unsigned int j;
				
				//memory page is in ram
				eeprom_init();

				//mov code from eeprom to external ram
				for(j=0;j<ECO_PAGE_SIZE;j++)
				{
					*(seg+j) = eeprom_read(ECO_ADDR_SHIFT(ECO_PAGE_ADDR & ECO_PAGE_MOV_MASK ) +j);
				}
				
				//update page table to connect this physical address id with virtual address id 
				ECO_PAGE_TABLE[i] = ECO_PAGE_ADDR >> ECO_PAGE_SHIFT;

				//store physical address id
				ECO_PAGE_PREV_PID = ECO_PAGE_TABLE[i];

				//update page address e.g.  (page_id<<8) + page_offset
				ECO_PAGE_ADDR = ((i + ECO_PAGE_ADDR_OFFSET) << ECO_PAGE_SHIFT) + (ECO_PAGE_ADDR & ECO_PAGE_MASK);

				//store virtual address id 
				ECO_PAGE_PREV_VID = ECO_PAGE_ADDR >> ECO_PAGE_SHIFT;	

				//mov to the next index
				ECO_PAGE_TABLE_INDEX = i;
				#pragma asm

				MOV R0,#LOW (ECO_PAGE_REGISTER1)
   				MOV A,@R0
				MOV	R1,A

				MOV R0,#LOW (ECO_PAGE_REGISTER2)
   				MOV A,@R0
				MOV	R2,A

				MOV R0,#LOW (ECO_PAGE_REGISTER3)
   				MOV A,@R0
				MOV	R3,A

				MOV R0,#LOW (ECO_PAGE_REGISTER4)
   				MOV A,@R0
				MOV	R4,A

				MOV R0,#LOW (ECO_PAGE_REGISTER5)
   				MOV A,@R0
				MOV	R5,A

				MOV R0,#LOW (ECO_PAGE_REGISTER6)
   				MOV A,@R0
				MOV	R6,A

				MOV R0,#LOW (ECO_PAGE_REGISTER7)
   				MOV A,@R0
				MOV	R7,A

				MOV	SPI_CTRL,ECO_PAGE_SPI_CONN
				MOV	DPH,ECO_PAGE_ADDR
				MOV	DPL,ECO_PAGE_ADDR+01H
				
				CLR	A
				JMP	@A+DPTR
				#pragma endasm

			}
		}
			
	}
				
}

#else

void eco_page_manager()
{
	unsigned int idata i;
	unsigned int idata page_index = -1; 

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
		ECO_PAGE_ADDR = (ECO_PAGE_PREV_VID << ECO_PAGE_SHIFT) + (ECO_PAGE_ADDR & ECO_PAGE_MASK);
		#pragma asm

		MOV R0,#LOW (ECO_PAGE_REGISTER1)
   		MOV A,@R0
		MOV	R1,A

		MOV R0,#LOW (ECO_PAGE_REGISTER2)
   		MOV A,@R0
		MOV	R2,A

		MOV R0,#LOW (ECO_PAGE_REGISTER3)
   		MOV A,@R0
		MOV	R3,A

		MOV R0,#LOW (ECO_PAGE_REGISTER4)
   		MOV A,@R0
		MOV	R4,A

		MOV R0,#LOW (ECO_PAGE_REGISTER5)
   		MOV A,@R0
		MOV	R5,A

		MOV R0,#LOW (ECO_PAGE_REGISTER6)
   		MOV A,@R0
		MOV	R6,A

		MOV R0,#LOW (ECO_PAGE_REGISTER7)
   		MOV A,@R0
		MOV	R7,A

	
		MOV	SPI_CTRL,ECO_PAGE_SPI_CONN
		MOV	DPH,ECO_PAGE_ADDR
		MOV	DPL,ECO_PAGE_ADDR+01H
		
		CLR	A
		JMP	@A+DPTR
		#pragma endasm
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

		MOV R0,#LOW (ECO_PAGE_REGISTER1)
   		MOV A,@R0
		MOV	R1,A

		MOV R0,#LOW (ECO_PAGE_REGISTER2)
   		MOV A,@R0
		MOV	R2,A

		MOV R0,#LOW (ECO_PAGE_REGISTER3)
   		MOV A,@R0
		MOV	R3,A

		MOV R0,#LOW (ECO_PAGE_REGISTER4)
   		MOV A,@R0
		MOV	R4,A

		MOV R0,#LOW (ECO_PAGE_REGISTER5)
   		MOV A,@R0
		MOV	R5,A

		MOV R0,#LOW (ECO_PAGE_REGISTER6)
   		MOV A,@R0
		MOV	R6,A

		MOV R0,#LOW (ECO_PAGE_REGISTER7)
   		MOV A,@R0
		MOV	R7,A


		MOV	SPI_CTRL,ECO_PAGE_SPI_CONN
		MOV	DPH,ECO_PAGE_ADDR
		MOV	DPL,ECO_PAGE_ADDR+01H
		
		CLR	A
		JMP	@A+DPTR
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
		//ECO_PAGE_PREV_PID = ECO_PAGE_TABLE[ECO_PAGE_TABLE_INDEX];
		ECO_PAGE_PREV_PID = ECO_PAGE_ADDR >> ECO_PAGE_SHIFT;

		//update page address
		ECO_PAGE_ADDR = ((ECO_PAGE_TABLE_INDEX + ECO_PAGE_ADDR_OFFSET) << ECO_PAGE_SHIFT) + (ECO_PAGE_ADDR & ECO_PAGE_MASK);

		//store virtual address id 
		ECO_PAGE_PREV_VID = ECO_PAGE_ADDR >> ECO_PAGE_SHIFT;	

		//mov to the next index
		ECO_PAGE_TABLE_INDEX = (ECO_PAGE_TABLE_INDEX + 1) % ECO_PAGE_ENTRY;
			
		//jump  to function address
		#pragma asm

		MOV R0,#LOW (ECO_PAGE_REGISTER1)
   		MOV A,@R0
		MOV	R1,A

		MOV R0,#LOW (ECO_PAGE_REGISTER2)
   		MOV A,@R0
		MOV	R2,A

		MOV R0,#LOW (ECO_PAGE_REGISTER3)
   		MOV A,@R0
		MOV	R3,A

		MOV R0,#LOW (ECO_PAGE_REGISTER4)
   		MOV A,@R0
		MOV	R4,A

		MOV R0,#LOW (ECO_PAGE_REGISTER5)
   		MOV A,@R0
		MOV	R5,A

		MOV R0,#LOW (ECO_PAGE_REGISTER6)
   		MOV A,@R0
		MOV	R6,A

		MOV R0,#LOW (ECO_PAGE_REGISTER7)
   		MOV A,@R0
		MOV	R7,A
	
		MOV	SPI_CTRL,ECO_PAGE_SPI_CONN
		MOV	DPH,ECO_PAGE_ADDR
		MOV	DPL,ECO_PAGE_ADDR+01H
		
		CLR	A
		JMP	@A+DPTR
		#pragma endasm

	}

}

#endif

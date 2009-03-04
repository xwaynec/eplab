#include "Eco/reg24e1.h"
#include "Eco/eco_sys.h"
#include "utils/utils.h"
#include "eeprom/eeprom.h"

#include "eco_page.h"
#define EEPROM_HEADER 3
#define ECO_ADDR_SHIFT(x)	((unsigned int)(x) + 3)

static unsigned int PAGE_ADDR_L,PAGE_ADDR_H;
static unsigned int SP_ADDR_L,SP_ADDR_H;
static unsigned char ECO_PAGE_TABLE[10];
static unsigned int JUMP_ADDR;

void ECO_PAGE_MANAGER()
{
	unsigned int i;	

	#pragma asm
		;POP LCALL ADDR_HIGHT
		POP	SP_ADDR_H+01H
		MOV	SP_ADDR_H,#00H

		;POP LCALL ADDR_LOW	
		POP	SP_ADDR_L+01H
		MOV	SP_ADDR_L,#00H
		
		;POP Function Address
		POP	PAGE_ADDR_H+01H
		MOV	PAGE_ADDR_H,#00H

		POP	PAGE_ADDR_L+01H
		MOV  	PAGE_ADDR_L,#00H

	#pragma endasm	
	
	//Check POP instruction 
	for(i=0;i<PAGE_ADDR_H;i++)
	{	
		blink_led();
		mdelay(400);
	}	
	
	//Check Table	
		

	
	//Set Return Address Back
	#pragma asm

		CLR	A
		MOV	A,SP_ADDR_L	
		PUSH	ACC	

		CLR	A
		MOV	A,SP_ADDR_H
		PUSH	ACC

		RET	
	#pragma endasm
	
}

void blink_test()
{
	blink_led();
}

void blink_fast()
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
	unsigned char xdata *seg = (unsigned char xdata *)(0x500);
	
	//unsigned char xdata *jump_fp;

	//void(code *fp)();
	blink_test();
	ECO_PAGE_TABLE[0] = 2; 
	
	
	PAGE_ADDR_L = 10;
	PAGE_ADDR_H = 11;
	
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

	mdelay(800);	
		
	eeprom_init();
	
	//Get data from 0x1000 address
	for(i=0;i<64;i++)
	{
		*(seg+i) = eeprom_read(ECO_ADDR_SHIFT(4096) +i);
	}	
	mdelay(400);


	//function pointer to blink_fast() 
	//jump_fp = (unsigned char xdata *)((1280));	
	//((void (code *)(void))jump_fp)();	
	/*JUMP_ADDR = 0x500;
	#pragma asm
		MOV	A,JUMP_ADDR
		MOV	DPH,A
		MOV	A,JUMP_ADDR+01H
		MOV	DPL,A
		CLR	A
		JMP	@A+DPTR	
	#pragma endasm	
	*/


	blink_fast();	
	
	/*	
	#pragma asm
		//LCALL	0x500

		CLR	A	
		;ADDR_LOW
		MOV	A,#0CH
		PUSH	ACC	
	
		CLR	A
		;ADDR_HIGH	
		MOV	A,#0AH
		PUSH	ACC
	
	#pragma endasm
	*/

	//ECO_PAGE_MANAGER();
	
	mdelay(800);
	for(i=0;i<10;i++)
	{
		blink_led();
		mdelay(200);
	}
	mdelay(400);
	
}

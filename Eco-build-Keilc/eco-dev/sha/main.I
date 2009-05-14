
#line 1 ".\main.c" /0
  
#line 1 "../../INCLUDE\ECO/REG24E1.H" /0
 
 
 
 
 sfr P0			= 0x80 ;
 sfr SP			= 0x81 ;
 sfr DPL			= 0x82 ;
 sfr DPL0		= 0x82 ;
 sfr DPH			= 0x83 ;
 sfr DPH0		= 0x83 ;
 sfr DPL1		= 0x84 ;
 sfr DPH1		= 0x85 ;
 sfr DPS			= 0x86 ;
 sfr PCON		= 0x87 ;
 sfr TCON		= 0x88 ;
 sfr TMOD		= 0x89 ;
 sfr TL0			= 0x8A ;
 sfr TL1			= 0x8B ;
 sfr TH0			= 0x8C ;
 sfr TH1			= 0x8D ;
 sfr CKCON		= 0x8E ;
 sfr SPC_FNC		= 0x8F ;
 sfr P1      	= 0x90 ;
 sfr EXIF		= 0x91 ;
 sfr MPAGE		= 0x92 ;
 sfr P0_DIR		= 0x94 ;
 sfr P0_ALT		= 0x95 ;
 sfr P1_DIR		= 0x96 ;
 sfr P1_ALT		= 0x97 ;
 sfr SCON		= 0x98 ;
 sfr SBUF		= 0x99 ;
 sfr RADIO		= 0xA0 ;
 sfr ADCCON		= 0xA1 ;
 sfr ADCDATAH	= 0xA2 ;
 sfr ADCDATAL	= 0xA3 ;
 sfr ADCSTATIC	= 0xA4 ;
 sfr IE			= 0xA8 ;
 sfr PWMCON		= 0xA9 ;
 sfr PWMDUTY		= 0xAA ;
 sfr REGX_MSB	= 0xAB ;
 sfr REGX_LSB	= 0xAC ;
 sfr REGX_CTRL	= 0xAD ;
 sfr RSTREAS		= 0xB1 ;
 sfr SPI_DATA   	= 0xB2 ;
 sfr SPI_CTRL	= 0xB3 ;
 sfr SPICLK		= 0xB4 ;
 sfr TICK_DV		= 0xB5 ;
 sfr CK_CTRL		= 0xB6 ;
 sfr TEST_MODE	= 0xB7 ;
 sfr IP			= 0xB8 ;
 sfr T1_1V2		= 0xBC ;
 sfr T2_1V2		= 0xBD ;
 sfr DEV_OFFSET	= 0xBE ;
 sfr T2CON		= 0xC8 ;
 sfr RCAP2L		= 0xCA ;
 sfr RCAP2H		= 0xCB ;
 sfr TL2			= 0xCC ;
 sfr TH2			= 0xCD ;
 sfr PSW			= 0xD0 ;
 sfr EICON		= 0xD8 ;
 sfr ACC			= 0xE0 ;
 sfr EIE			= 0xE8 ;
 sfr B			= 0xF0 ;
 sfr EIP			= 0xF8 ;
 
 
 
 
 sbit P0_0	= 0x80 	;
 sbit DIO2	= 0x80 	;
 sbit P0_1	= 0x81 	;
 sbit RXD	= 0x81 	;
 sbit DIO3	= 0x81 	;
 sbit P0_2	= 0x82 	;
 sbit TXD	= 0x82 	;
 sbit DIO4	= 0x82 	;
 sbit P0_3	= 0x83 	;
 sbit INT0_N	= 0x83 	;
 sbit DIO5	= 0x83 	;
 sbit P0_4	= 0x84 	;
 sbit INT1_N	= 0x84 	;
 sbit DIO6	= 0x84 	;
 sbit P0_5	= 0x85 	;
 sbit T0		= 0x85 	;
 sbit DIO7	= 0x85 	;
 sbit P0_6	= 0x86 	;
 sbit T1		= 0x86 	;
 sbit DIO8	= 0x86 	;
 sbit P0_7	= 0x87 	;
 sbit PWM	= 0x87 	;
 sbit DIO9	= 0x87 	;
 
 
 sbit IT0	= 0x88 ;
 sbit IE0	= 0x89 ;
 sbit IT1	= 0x8A ;
 sbit IE1	= 0x8B ;
 sbit TR0	= 0x8C ;
 sbit TF0	= 0x8D ;
 sbit TR1	= 0x8E ;
 sbit TF1	= 0x8F ;
 
 
 sbit P1_0	= 0x90 ;
 sbit T2		= 0x90 ;
 sbit DIO0	= 0x90 ;
 sbit P1_1	= 0x91 ;
 sbit DIO1	= 0x91 ;
 sbit P1_2	= 0x92 ;
 sbit DIN0	= 0x92 ;
 
 
 sbit RI		= 0x98 ;
 sbit TI		= 0x99 ;
 sbit RB8	= 0x9A ;
 sbit TB8	= 0x9B ;
 sbit REN	= 0x9C ;
 sbit SM2	= 0x9D ;
 sbit SM1	= 0x9E ;
 sbit SM0	= 0x9F ;
 
 
 sbit DATA	= 0xA0 ;
 sbit CLK1	= 0xA1 ;
 sbit DR1	= 0xA2 ;
 sbit CS		= 0xA3 ;
 sbit DOUT2	= 0xA4 ;
 sbit CLK2	= 0xA5 ;
 sbit DR2_CE	= 0xA6 ;
 sbit DR2	= 0xA6 ;
 sbit CE		= 0xA6 ;
 sbit PWR_UP	= 0xA7 ;
 
 
 sbit EX0	= 0xA8 ;
 sbit ET0	= 0xA9 ;
 sbit EX1	= 0xAA ;
 sbit ET1	= 0xAB ;
 sbit ES		= 0xAC ;
 sbit ET2	= 0xAD ;
 sbit EA		= 0xAF ;
 
 
 sbit PX0	= 0xB8 ;
 sbit PT0	= 0xB9 ;
 sbit PX1	= 0xBA ;
 sbit PT1	= 0xBB ;
 sbit PS		= 0xBC ;
 sbit PT2	= 0xBD ;
 
 
 sbit CP_RL2	= 0xC8 ;
 sbit CPRL2	= 0xC8 ;
 sbit C_T2	= 0xC9 ;
 sbit CT2	= 0xC9 ;
 sbit TR2	= 0xCA ;
 sbit EXEN2	= 0xCB ;
 sbit TCLK	= 0xCC ;
 sbit RCLK	= 0xCD ;
 sbit EXF2	= 0xCE ;
 sbit TF2	= 0xCF ;
 
 
 sbit P		= 0xD0 ;
 sbit F1		= 0xD1 ;
 sbit OV		= 0xD2 ;
 sbit RS0	= 0xD3 ;
 sbit RS1	= 0xD4 ;
 sbit F0		= 0xD5 ;
 sbit AC		= 0xD6 ;
 sbit CY		= 0xD7 ;
 
 
 sbit WDTI	= 0xDB ;
 
 
 sbit EX2	= 0xE8 ;
 sbit EX3	= 0xE9 ;
 sbit EX4	= 0xEA ;
 sbit EX5	= 0xEB ;
 sbit EWDI	= 0xEC ;
 
 
 sbit PX2	= 0xF8 ;
 sbit PX3	= 0xF9 ;
 sbit PX4	= 0xFA ;
 sbit PX5	= 0xFB ;
 sbit PWDI	= 0xFC ;
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
#line 1 ".\main.c" /0
 
  
#line 1 "../../INCLUDE\ECO/ECO_SYS.H" /0









 
 
 
 
  
#line 1 "../../INCLUDE\ECO/REG24E1.H" /0
 
#line 2 "../../INCLUDE\ECO/REG24E1.H" /1
  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  
  
  
  
  
 
 
  
  
  
  
  
  
  
  
 
  
  
 
 
  
  
  
  
  
 
 
#line 14 "../../INCLUDE\ECO/ECO_SYS.H" /0
#line 14 "../../INCLUDE\ECO/ECO_SYS.H" /0
 
 
 
 
 
 
 
#line 2 ".\main.c" /0
 
  
#line 1 "../../INCLUDE\UTILS/UTILS.H" /0












 
 
 void store_cpu_rate(int mhz);
 void mdelay(unsigned int msec);
 void wdt_load(unsigned int cnt);
 void strncpy(char *src, char *dst, int n);
#line 3 ".\main.c" /0
 
  
#line 1 "../../INCLUDE\SERIAL/SERIAL.H" /0







 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 void serial_init(unsigned int baud);
 void putc(char c);
 void puts(char *s);
 char getc();
 void int_print(unsigned int val) reentrant;
 
 
#line 4 ".\main.c" /0
 
 
  
#line 1 "../../INCLUDE\EEPROM/EEPROM.H" /0







 
 
 
 
 
 
 
 
 
 
 
 

 
 
 
 void eeprom_init();
 void eeprom_write(unsigned int addr, char byte);
 char eeprom_read(unsigned int addr);
 char eeprom_status();
 
 
#line 6 ".\main.c" /0
 
  
#line 1 "eco_page.h" /0












 
 
 
 
 
 
  
#line 1 "../../INCLUDE\ECO/REG24E1.H" /0
 
#line 2 "../../INCLUDE\ECO/REG24E1.H" /1
  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  
  
  
  
  
 
 
  
  
  
  
  
  
  
  
 
  
  
 
 
  
  
  
  
  
 
 
#line 19 "eco_page.h" /0
#line 19 "eco_page.h" /0
 
  
#line 1 "../../INCLUDE\ECO/ECO_SYS.H" /0









 
 
#line 12 "../../INCLUDE\ECO/ECO_SYS.H" /1
  
 
  
 
  
 
  
 
 
#line 20 "eco_page.h" /0
#line 20 "eco_page.h" /0
 
  
#line 1 "../../INCLUDE\UTILS/UTILS.H" /0












 
 
 void store_cpu_rate(int mhz);
 void mdelay(unsigned int msec);
 void wdt_load(unsigned int cnt);
 void strncpy(char *src, char *dst, int n);
#line 21 "eco_page.h" /0
 
  
#line 1 "../../INCLUDE\EEPROM/EEPROM.H" /0







 
 
#line 10 "../../INCLUDE\EEPROM/EEPROM.H" /1
  
 
 
  
  
  
  
  
  
  

 
  
 
 
 
 
 
 
 
#line 22 "eco_page.h" /0
#line 22 "eco_page.h" /0
 
 
 
 
 
 






 
 
 void eco_page_init();
 void eco_page_manager();
 
 
 
#line 7 ".\main.c" /0
 
 
 
 
 


 
 
 typedef struct SHA1Context
 {
 unsigned Message_Digest[5];  
 
 unsigned Length_Low;         
 unsigned Length_High;        
 
 unsigned char Message_Block[64];  
 char Message_Block_Index;     
 
 int Computed;                
 int Corrupted;               
 } SHA1Context;
 
 
 void SHA1ProcessMessageBlock(SHA1Context idata *context)
 {
 idata unsigned K[] =             
 {
 0x5A827999,
 0x6ED9EBA1,
 0x8F1BBCDC,
 0xCA62C1D6
 };
 idata int         t;                   
 idata unsigned    temp;                
 xdata unsigned    W[80];               
 idata unsigned    A, B, C, D, E;       
 


 
 for(t = 0; t < 16; t++)
 {
 W[t] = ((unsigned) context->Message_Block[t * 4]) << 24;
 W[t] |= ((unsigned) context->Message_Block[t * 4 + 1]) << 16;
 W[t] |= ((unsigned) context->Message_Block[t * 4 + 2]) << 8;
 W[t] |= ((unsigned) context->Message_Block[t * 4 + 3]);
 }
 
 for(t = 16; t < 80; t++)
 {
 W[t] = ((((W[t-3] ^ W[t-8] ^ W[t-14] ^ W[t-16]) << (1)) & 0xFFFFFFFF) | ((W[t-3] ^ W[t-8] ^ W[t-14] ^ W[t-16]) >> (32-(1))));
 }
 
 A = context->Message_Digest[0];
 B = context->Message_Digest[1];
 C = context->Message_Digest[2];
 D = context->Message_Digest[3];
 E = context->Message_Digest[4];
 
 for(t = 0; t < 20; t++)
 {
 temp =  ((((A) << (5)) & 0xFFFFFFFF) | ((A) >> (32-(5)))) +
 ((B & C) | ((~B) & D)) + E + W[t] + K[0];
 temp &= 0xFFFFFFFF;
 E = D;
 D = C;
 C = ((((B) << (30)) & 0xFFFFFFFF) | ((B) >> (32-(30))));
 B = A;
 A = temp;
 }
 
 for(t = 20; t < 40; t++)
 {
 temp = ((((A) << (5)) & 0xFFFFFFFF) | ((A) >> (32-(5)))) + (B ^ C ^ D) + E + W[t] + K[1];
 temp &= 0xFFFFFFFF;
 E = D;
 D = C;
 C = ((((B) << (30)) & 0xFFFFFFFF) | ((B) >> (32-(30))));
 B = A;
 A = temp;
 }
 
 for(t = 40; t < 60; t++)
 {
 temp = ((((A) << (5)) & 0xFFFFFFFF) | ((A) >> (32-(5)))) +
 ((B & C) | (B & D) | (C & D)) + E + W[t] + K[2];
 temp &= 0xFFFFFFFF;
 E = D;
 D = C;
 C = ((((B) << (30)) & 0xFFFFFFFF) | ((B) >> (32-(30))));
 B = A;
 A = temp;
 }
 
 for(t = 60; t < 80; t++)
 {
 temp = ((((A) << (5)) & 0xFFFFFFFF) | ((A) >> (32-(5)))) + (B ^ C ^ D) + E + W[t] + K[3];
 temp &= 0xFFFFFFFF;
 E = D;
 D = C;
 C = ((((B) << (30)) & 0xFFFFFFFF) | ((B) >> (32-(30))));
 B = A;
 A = temp;
 }
 
 context->Message_Digest[0] =
 (context->Message_Digest[0] + A) & 0xFFFFFFFF;
 context->Message_Digest[1] =
 (context->Message_Digest[1] + B) & 0xFFFFFFFF;
 context->Message_Digest[2] =
 (context->Message_Digest[2] + C) & 0xFFFFFFFF;
 context->Message_Digest[3] =
 (context->Message_Digest[3] + D) & 0xFFFFFFFF;
 context->Message_Digest[4] =
 (context->Message_Digest[4] + E) & 0xFFFFFFFF;
 
 context->Message_Block_Index = 0;
 
 }
 
 
 void SHA1Reset(SHA1Context idata *context)
 {
 context->Length_Low             = 0;
 context->Length_High            = 0;
 context->Message_Block_Index    = 0;
 
 context->Message_Digest[0]      = 0x67452301;
 context->Message_Digest[1]      = 0xEFCDAB89;
 context->Message_Digest[2]      = 0x98BADCFE;
 context->Message_Digest[3]      = 0x10325476;
 context->Message_Digest[4]      = 0xC3D2E1F0;
 
 context->Computed   = 0;
 context->Corrupted  = 0;
 }
 
 
 void SHA1PadMessage(SHA1Context idata *context)
 {





 
 if (context->Message_Block_Index > 55)
 {
 context->Message_Block[context->Message_Block_Index++] = 0x80;
 while(context->Message_Block_Index < 64)
 {
 context->Message_Block[context->Message_Block_Index++] = 0;
 }
 
 SHA1ProcessMessageBlock(context);
 
 while(context->Message_Block_Index < 56)
 {
 context->Message_Block[context->Message_Block_Index++] = 0;
 }
 }
 else
 {
 context->Message_Block[context->Message_Block_Index++] = 0x80;
 while(context->Message_Block_Index < 56)
 {
 context->Message_Block[context->Message_Block_Index++] = 0;
 }
 }
 


 
 context->Message_Block[24] = (context->Length_High >> 24) & 0xFF;
 context->Message_Block[25] = (context->Length_High >> 16) & 0xFF;
 context->Message_Block[26] = (context->Length_High >> 8) & 0xFF;
 context->Message_Block[27] = (context->Length_High) & 0xFF;
 context->Message_Block[28] = (context->Length_Low >> 24) & 0xFF;
 context->Message_Block[29] = (context->Length_Low >> 16) & 0xFF;
 context->Message_Block[30] = (context->Length_Low >> 8) & 0xFF;
 context->Message_Block[31] = (context->Length_Low) & 0xFF;
 
 SHA1ProcessMessageBlock(context);
 }
 
 
 int SHA1Result(SHA1Context idata *context)
 {
 
 if (context->Corrupted)
 {
 return 0;
 }
 
 if (!context->Computed)
 {
 SHA1PadMessage(context);
 context->Computed = 1;
 }
 
 return 1;
 }
 
 
 void SHA1Input(SHA1Context idata *context,unsigned char idata *message_array,unsigned idata length)
 {
 if (!length)
 {
 return;
 }
 
 if (context->Computed || context->Corrupted)
 {
 context->Corrupted = 1;
 return;
 }
 
 while(length-- && !context->Corrupted)
 {
 context->Message_Block[context->Message_Block_Index++] =(*message_array & 0xFF);
 
 context->Length_Low += 8;
 
 context->Length_Low &= 0xFFFFFFFF;
 if (context->Length_Low == 0)
 {
 context->Length_High++;
 
 context->Length_High &= 0xFFFFFFFF;
 if (context->Length_High == 0)
 {
 
 context->Corrupted = 1;
 }
 }
 
 if (context->Message_Block_Index == 32)
 {
 SHA1ProcessMessageBlock(context);
 }
 
 message_array++;
 }
 }
 
 
 void main()
 {
 
 idata char i;
 idata SHA1Context sha;
 
 store_cpu_rate(16);
 
 P0_DIR &= ~0x28;
 P0_ALT &= ~0x28;
 
 serial_init(19200);
 
 
 for(i=0;i<6;i++)
 {
  P0 ^= 0x20;
 mdelay(400);
 }	
 
 while(1)
 {
 SHA1Reset(&sha);
 SHA1Input(&sha, (const unsigned char *) "abc", 3);
 
 SHA1Result(&sha);
  P0 ^= 0x20;	
 }	
 
 }
 
 

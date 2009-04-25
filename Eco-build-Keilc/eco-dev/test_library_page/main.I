
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
 
  
#line 1 "../../INCLUDE\ISR/ISR_RF.H" /0







 
 
 
 
 
 
 
 struct rf_config {
 
 unsigned char data2_width;
 unsigned char data1_width;
 
 char addr2[5];
 char addr1[5];
 
 char addr_and_crc;
 char rf_prog[2];	 
 };
 
 
 struct radio_buffer {
 unsigned char ready;
 unsigned char buffer[23];
 };
 
 void rf_init();
 void rf_configure(struct rf_config *cfg);
 void rf_send(char *addr, unsigned char addr_len,
 char *payload, unsigned char pl_len);
 void rf_wait_msg();
 
 extern struct radio_buffer rf_buf;
 
 
#line 5 ".\main.c" /0
 
  
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
 
 
 
 struct rf_config rf_data = { {0x00},  
 {0x38},  
 {0x00, 0x00, 0x00, 0x00, 0x00},  
 {0xF2, 0xF2, 0xF2, 0xF2, 0xF2},  
 {0x63},  
 {0x6f, 0xEC} };
 struct rf_config *cfg = &rf_data;
 char dst_addr[3] = {0xF1, 0xF1, 0xF1};
 idata char msg[7];
 
 
 extern unsigned char ECO_PAGE_SPI_CONN;




 
 






































































 
 
 void blink2()
 {
 int i;
 for(i=0;i<4;i++)
 {
  P0 ^= 0x20;
 mdelay(400);
 }
 mdelay(1000);	
 }
 void blink4()
 {
 int i;
 for(i=0;i<8;i++)
 {
  P0 ^= 0x20;
 mdelay(400);
 }	
 mdelay(1000);	
 }
 void blink6()
 {
 int i;
 for(i=0;i<12;i++)
 {
  P0 ^= 0x20;
 mdelay(400);
 }	
 mdelay(1000);	
 }
 
 int main()
 {
 unsigned char idx;
 unsigned int i = 0;
 store_cpu_rate(16);
 P0_DIR &= ~0x28;
 P0_ALT &= ~0x28;
 rf_init();
 rf_configure(cfg);
 serial_init(19200);	
 eco_page_init();
 
 
 
 msg[0] = 0x0A;
 msg[1] = 0x00;
 
 msg[2] = 0x02;
 msg[3] = 0xA0;
 
 msg[4] = 0x02;
 msg[5] = 0xDD;
 msg[6] = 0xCC;
 
 for(idx = 4; idx > 0; idx--)
 {
  P0 ^= 0x20;		
 mdelay(300);
 }
 
 mdelay(1000);
 
 while(1)
 {
 blink4();
 rf_send(dst_addr, 3, msg, 7);
 blink2();
 mdelay(200);	
 blink6();
 }
 
 return 0;
 }

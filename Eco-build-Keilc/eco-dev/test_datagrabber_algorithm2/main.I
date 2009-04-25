
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
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
#line 46 ".\main.c" /0
 
  
#line 1 "../../INCLUDE\ECO/ECO_SYS.H" /0









 
 
 
 
  
#line 1 "../../INCLUDE\ECO/REG24E1.H" /0
 
#line 2 "../../INCLUDE\ECO/REG24E1.H" /1
  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  
  
  
  
  
 
 
  
  
  
  
  
  
  
  
 
  
  
 
 
  
  
  
  
  
 
 
#line 14 "../../INCLUDE\ECO/ECO_SYS.H" /0
#line 14 "../../INCLUDE\ECO/ECO_SYS.H" /0
 
 
 
 
 
 
 
#line 47 ".\main.c" /0
 
  
#line 1 "../../INCLUDE\UTILS/UTILS.H" /0












 
 
 void store_cpu_rate(int mhz);
 void mdelay(unsigned int msec);
 void wdt_load(unsigned int cnt);
 void strncpy(char *src, char *dst, int n);
#line 48 ".\main.c" /0
 
  
#line 1 "../../INCLUDE\SERIAL/SERIAL.H" /0







 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 void serial_init(unsigned int baud);
 void putc(char c);
 void puts(char *s);
 char getc();
 void int_print(unsigned int val) reentrant;
 
 
#line 49 ".\main.c" /0
 
  
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
 
 
#line 50 ".\main.c" /0
 
  
#line 1 "../../INCLUDE\EEPROM/EEPROM.H" /0







 
 
 
 
 
 
 
 
 
 
 
 

 
 
 
 void eeprom_init();
 void eeprom_write(unsigned int addr, char byte);
 char eeprom_read(unsigned int addr);
 char eeprom_status();
 
 
#line 51 ".\main.c" /0
 
  
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
 
 
 
#line 52 ".\main.c" /0
 
  
#line 1 "C:\KEIL\C51\INC\MATH.H" /0






 
 
 
 
 
 #pragma SAVE
 #pragma REGPARMS
 extern char  cabs  (char  val);
 extern int    abs  (int   val);
 extern long  labs  (long  val);
 extern float fabs  (float val);
 extern float sqrt  (float val);
 extern float exp   (float val);
 extern float log   (float val);
 extern float log10 (float val);
 extern float sin   (float val);
 extern float cos   (float val);
 extern float tan   (float val);
 extern float asin  (float val);
 extern float acos  (float val);
 extern float atan  (float val);
 extern float sinh  (float val);
 extern float cosh  (float val);
 extern float tanh  (float val);
 extern float atan2 (float y, float x);
 
 extern float ceil  (float val);
 extern float floor (float val);
 extern float modf  (float val, float *n);
 extern float fmod  (float x, float y);
 extern float pow   (float x, float y);
 
 #pragma RESTORE
 
 
#line 53 ".\main.c" /0
 
 
 
 
 
 
 
 
 










 
 










 
 










 
 xdata int in[64];            
 xdata unsigned int amplitude[32];    
 xdata unsigned int harmonic[32];     
 xdata int work[128];         
 
  unsigned char scale;
  unsigned char i_r, i_i, ip_r, ip_i;
  unsigned char pass, di, dip, dk, k, rot;
 int sink, cosk;
 int x0, x1, x2, x3, x4, x5;
 int real, imag;
 
 void fft_int(void);                                  
  unsigned int longroot(unsigned long radic);     
 int mult(int x, int y);          
 
 main()
 {
  unsigned char i;
 
 
 





 




 
 
 
 
 fft_int();    
 
 while(1);
 }
 





















 
 void fft_int()
 {
  unsigned char i,j;                 
 bit done;                  
  unsigned int f1;                   
  unsigned int adjust;               
 int workipr, workipi;      
 
 
 for(i=0;i<64;i++){
 j= move[i];
 work[j]= in[i];
 work[64+j]= 0;      
 }
 
 scale= 0;
 di= 2;
 dip= 1;
 dk= 32;
 
 for(pass=0;pass<6;pass++){
 k= 0;
 for(rot=1;rot<=dip;rot++,k+=dk){
 sink= sine[k];
 cosk= cosine[k];
 for(i_r=rot-1;i_r<64;i_r+=di){
 ip_r= i_r + dip;
 i_i= i_r + 64;
 ip_i= i_i + dip;
 workipr= work[ip_r];
 workipi= work[ip_i];
 done= 0;
 do{
 x1= mult(workipr,cosk);
 x2= mult(workipi,sink);
 real= x1 + x2;
 


 
 
 
 x1= mult(workipi,cosk);
 x2= mult(workipr,sink);
 imag= x1 - x2;
 
 x1= work[i_r];
 x2= x1 + real;
 
 x3= work[i_i];
 x4= x3 + imag;
 
 x5= x1 - real;                 
 
 x0= x3 - imag;
 
 
 work[ip_i]= x0;
 work[ip_r]= x5;
 work[i_r]= x2;
 work[i_i]= x4;
 done= 1;
 }
 while(!done);
 }
 }
 
 dk= dk >> 1;
 dip= di;
 di= di << 1;
 }
 
 f1= 0;
 for(i=0;i<32;i++){
 x1= abs(work[i]);
 x2= abs(work[i+64]);
 


 
 
 if((x1<8) && (x2<8)) x3= 0;       
 else if(x1 < (x2 >> 5)) x3= x2;   
 else if(x2 < (x1 >> 5)) x3= x1;   
 else x3= longroot((unsigned long) x1*x1 + (unsigned long) x2*x2);
 
 if(i==1){ f1= x3; adjust= x3 >> 1;}
 else if(f1 != 0) harmonic[i]= (adjust + x3 * 1000L) / f1;
 
 if(scale) x3= x3 << scale;
 amplitude[i]= x3;
 }
 }
 
 void scaling()          
 {
  unsigned char i;
  unsigned int x;
 
 scale++;
 for(i=0;i<128;i++){
 x= work[i];
 if(x>0) x++;
 if(x>16383) x--;
 x= x >> 1;
 work[i]= x;
 }
 }
 
 
 
  unsigned int longroot(unsigned long radic)
 {
  unsigned int result;
  unsigned int mask, masknot;
 unsigned long acu;
 
 radic= radic << 2;     
 result= 0;
 mask= 0x8000;
 do{
 masknot= ~mask;
 result |= mask;
 acu= result;
 acu*= result;
 if(acu > radic){
 result &= masknot;
 }
 mask= mask >> 1;
 }
 while(!(mask & 1));
 
 
 result++;
 result= result >> 1;
 return result;
 }
 
 
 int mult(int x, int y)
 {
 long temp;
  unsigned char templo;
  unsigned int  temphi;
 
 temp= (long) x * y;
 temphi= *((unsigned int *) (&temp));          
 templo= *((unsigned char *) (&temp) + 2);     
 temphi= temphi << 2;
 if(templo & 0x80) temphi |= 2;
 if(templo & 0x40) temphi |= 1;
 return temphi;
 }
 
 

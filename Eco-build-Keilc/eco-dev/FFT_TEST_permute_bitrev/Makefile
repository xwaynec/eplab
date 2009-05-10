# Makefile for Memory Paging
#
# Wei-Han Chen <xwaynec@gmail.com>

SOURCE = main

TARGET = main

CC = wine /Users/waynec/Library/Application\ Support/CrossOver/Bottles/winxp/dosdevices/c:/Keil/C51/BIN/C51.exe
AC = wine /Users/waynec/Library/Application\ Support/CrossOver/Bottles/winxp/dosdevices/c:/Keil/C51/BIN/AX51.exe
LX = wine /Users/waynec/Library/Application\ Support/CrossOver/Bottles/winxp/dosdevices/c:/Keil/C51/BIN/LX51.exe
OX = wine /Users/waynec/Library/Application\ Support/CrossOver/Bottles/winxp/dosdevices/c:/Keil/C51/BIN/OHX51.exe

#CC = C51.exe
#AC = AX51.exe
#LX = LX51.exe
#OX = OHX51.exe


INCLUDE = ../../Include
CFLAG 	= BROWSE DEBUG CODE LISTINCLUDE SYMBOLS PREPRINT 
AFLAG	= EP DEBUG SYMBOLS
LFLAG	= CODE NOOL

vpath %.h ../../include/Eco
vpath %.c ../../include/utils
vpath %.c ../../include/eeprom
vpath %.c ../../include/serial
vpath %.c ../../include/adc
#vpath %.c ../../include/rf
vpath %.c ../../include/spi
vpath %.c ../../include/isr


vpath %.LIB /cygdrive/c/Keil/C51/INC 
vpath %.LIB /cygdrive/c/Keil/C51/LIB

all: main
main: main.obj isr_rf.obj utils.obj serial.obj spi.obj eeprom.obj adc.obj eco_page.obj 
	#$(LX) main.obj , isr_rf.obj , eco_page.obj , adc.obj , utils.obj , serial.obj , spi.obj, eeprom.obj , C51S.LIB TO $(TARGET) SEGMENTS\(?PR?P_ADC_READ?ADC\(C:0x700\)\) SEGMENTS\(?PR?_PUTC?SERIAL\(C:0x74d\)\) SEGMENTS\(?PR?_MDELAY?UTILS\(C:0x750\)\) SEGMENTS\(?PR?_STRNCPY?UTILS\(C:0x799\)\) SEGMENTS\(?PR?_SETUP_BAUDRATE?SERIAL\(C:0x800\)\) SEGMENTS\(?PR?_EEPROM_WRITE?EEPROM\(C:0x83d\)\) SEGMENTS\(?PR?_?INT_PRINT?SERIAL\(C:0x900\)\) SEGMENTS\(?PR?_RF_CONFIGURE?ISR_RF\(C:0x945\)\) SEGMENTS\(?PR?_EEPROM_READ?EEPROM\(C:0x986\)\) SEGMENTS\(?PR?_PUTS?SERIAL\(C:0xa00\)\) SEGMENTS\(?PR?FLASH_ERASE_ALL?EEPROM\(C:0xa30\)\) SEGMENTS\(?PR?_ADC_READ?ADC\(C:0xa7d\)\) SEGMENTS\(?PR?_ADC_INIT?ADC\(C:0xaa1\)\) SEGMENTS\(?PR?_WDT_LOAD?UTILS\(C:0xab4\)\) SEGMENTS\(?PR?EEPROM_STATUS?EEPROM\(C:0xac6\)\) SEGMENTS\(?PR?RF_INIT?ISR_RF\(C:0xb00\)\) SEGMENTS\(?PR?_STORE_CPU_RATE?UTILS\(C:0xb1b\)\) SEGMENTS\(?PR?_SPI_WRITE_THEN_READ?SPI\(C:0xb28\)\) SEGMENTS\(?PR?EEPROM_INIT?EEPROM\(C:0xb35\)\) SEGMENTS\(?PR?_SERIAL_INIT?SERIAL\(C:0xb4d\)\) SEGMENTS\(?PR?RF_WAIT_MSG?ISR_RF\(C:0xb60\)\) SEGMENTS\(?PR?_SERIAL_WRITE?SERIAL\(C:0xb69\)\) SEGMENTS\(?PR?SERIAL_READ?SERIAL\(C:0xb71\)\) SEGMENTS\(?PR?_SPI_INIT?SPI\(C:0xb79\)\) SEGMENTS\(?PR?GETC?SERIAL\(C:0xb7e\)\) SEGMENTS\(?PR?_RF_SEND?ISR_RF\(C:0xc00\)\) SEGMENTS\(?PR?BLINK2?MAIN\(C:0xc81\)\) SEGMENTS\(?PR?BLINK4?MAIN\(C:0xcb7\)\) SEGMENTS\(?PR?BLINK6?MAIN\(C:0xd00\)\)
	#$(LX) main.obj , isr_rf.obj , eco_page.obj , adc.obj , utils.obj , serial.obj , spi.obj, eeprom.obj , C51S.LIB TO $(TARGET) 
	
	#page size is 256
	#$(LX) main.obj , isr_rf.obj , eco_page.obj , adc.obj , utils.obj , serial.obj , spi.obj, eeprom.obj , C51S.LIB TO $(TARGET) SEGMENTS\(?PR?_rf_send?ISR_RF\(C:0x1000\)\) SEGMENTS\(?PR?BLINK2?MAIN\(C:0x1100\)\) SEGMENTS\(?PR?BLINK4?MAIN\(C:0x1155\)\) SEGMENTS\(?PR?BLINK6?MAIN\(C:0x11AA\)\)
	
	#page size is 128
	#$(LX) main.obj , isr_rf.obj , eco_page.obj , adc.obj , utils.obj , serial.obj , spi.obj, eeprom.obj , C51S.LIB TO $(TARGET) SEGMENTS\(?PR?_rf_send?ISR_RF\(C:0x1000\)\) SEGMENTS\(?PR?BLINK2?MAIN\(C:0x1080\)\) SEGMENTS\(?PR?BLINK4?MAIN\(C:0x10A9\)\) SEGMENTS\(?PR?BLINK6?MAIN\(C:0x10D2\)\)
	
	#page size is 64
	#$(LX) main.obj , isr_rf.obj , eco_page.obj , adc.obj , utils.obj , serial.obj , spi.obj, eeprom.obj , C51S.LIB TO $(TARGET) SEGMENTS\(?PR?_rf_send?ISR_RF\(C:0x1000\)\) SEGMENTS\(?PR?BLINK2?MAIN\(C:0x10C0\)\) SEGMENTS\(?PR?BLINK4?MAIN\(C:0x1080\)\) SEGMENTS\(?PR?BLINK6?MAIN\(C:0x10A8\)\)
	

	#$(LX) main.obj , isr_rf.obj , eco_page.obj , adc.obj , utils.obj , serial.obj , spi.obj, eeprom.obj , C51S.LIB TO $(TARGET) SEGMENTS\(?PR?_rf_send?ISR_RF\(C:0x1000\)\) SEGMENTS\(?PR?_long_function?MAIN\(C:0x1200\)\) SEGMENTS\(?PR?_long_function_2?MAIN\(C:0x1300\)\)

	#page size is 128	
	#$(LX) main.obj , isr_rf.obj , eco_page.obj , adc.obj , utils.obj , serial.obj , spi.obj, eeprom.obj , C51S.LIB TO $(TARGET) SEGMENTS\(?PR?_rf_send?ISR_RF\(C:0x1000\)\) SEGMENTS\(?PR?_adc_init?ADC\(C:0x1080\)\) SEGMENTS\(?PR?_adc_read?ADC\(C:0x10A0\)\)

	#$(LX) main.obj , isr_rf.obj , eco_page.obj , adc.obj , utils.obj , serial.obj , spi.obj, eeprom.obj , C51S.LIB , C51FPL.LIB  TO $(TARGET) 
	#$(LX) main.obj , isr_rf.obj , adc.obj , utils.obj , serial.obj , spi.obj , C51S.LIB , C51FPL.LIB  TO $(TARGET) SEGMENTS\(?PR?_FFT?MAIN\(C:0x1200\)\) SEGMENTS\(?PR?_BITREV?MAIN\(C:0x1000\)\)
	#$(LX) main.obj , isr_rf.obj , eco_page.obj , adc.obj , utils.obj , serial.obj , spi.obj , eeprom.obj , C51S.LIB , C51FPL.LIB  TO $(TARGET) SEGMENTS\(?PR?_BITREV?MAIN\(C:0x1000\)\) SEGMENTS\(?PR?_LOG_2?MAIN\(C:0x1055\)\) SEGMENTS\(?PR?_COMPUTE_W?MAIN\(C:0x1100\)\) SEGMENTS\(?PR?_EEPROM_WRITE?EEPROM\(C:0x3000\)\) SEGMENTS\(?PR?ECO_PAGE_INIT?ECO_PAGE\(C:0x303B\)\) SEGMENTS\(?PR?_SERIAL_WRITE?SERIAL\(C:0x3047\)\) SEGMENTS\(?PR?RF_WAIT_MSG?ISR_RF\(C:0x304F\)\) SEGMENTS\(?PR?RF_CH1_RECV?ISR_RF\(C:0x3058\)\) SEGMENTS\(?PR?FLASH_ERASE_ALL?EEPROM\(C:0x30B8\)\)
	$(LX) main.obj , isr_rf.obj , eco_page.obj , adc.obj , utils.obj , serial.obj , spi.obj , eeprom.obj , C51S.LIB , C51FPL.LIB  TO $(TARGET) SEGMENTS\(?PR?_FFT?MAIN\(C:0x1500\)\) SEGMENTS\(?PR?_RF_SEND?ISR_RF\(C:0x1800\)\) SEGMENTS\(?PR?ECO_PAGE_INIT?ECO_PAGE\(C:0x193B\)\) SEGMENTS\(?PR?_SERIAL_WRITE?SERIAL\(C:0x1947\)\) SEGMENTS\(?PR?RF_WAIT_MSG?ISR_RF\(C:0x194F\)\) SEGMENTS\(?PR?RF_CH1_RECV?ISR_RF\(C:0x1958\)\) SEGMENTS\(?PR?FLASH_ERASE_ALL?EEPROM\(C:0x19B8\)\)
#SEGMENTS\(?PR?blink_fast?PAGING\(C:0x1000\)\) SEGMENTS\(?PR?blink_fast2?PAGING\(C:0x800\)SEGMENTS\(?PR?_BITREV?MAIN\(C:0x1800\)\)

	$(OX) "MAIN" HEX
	#./eeprepbat.bat
	python eeprep.py MAIN.hex main2.hex
	python convert.py main2.hex main3.hex

eco_page.obj: eco_page.src
	$(AC) ./$< $(AFLAG) OJ\(./$@\) PR\(./eco_page.ls1\)

isr_rf.obj: isr_rf.src
	$(AC) ./$< $(AFLAG) OJ\(./$@\) PR\(./eco_page.ls1\)

adc.obj : adc.src
	$(AC) ./$< $(AFLAG) OJ\(./$@\) PR\(./adc.ls1\)

utils.obj : utils.src 
	$(AC) ./$< $(AFLAG) OJ\(./$@\) PR\(./utils.ls1\)

serial.obj : serial.src 
	$(AC) ./$< $(AFLAG) OJ\(./$@\) PR\(./utils.ls1\)

spi.obj : spi.src 
	$(AC) ./$< $(AFLAG) OJ\(./$@\) PR\(./spi.ls1\)

#rf.obj : rf.src 
#	$(AC) ./$< $(AFLAG) OJ\(./$@\) PR\(./eeprom.ls1\)

eeprom.obj : eeprom.src 
	$(AC) ./$< $(AFLAG) OJ\(./$@\) PR\(./eeprom.ls1\)

main.obj : main.src
	$(AC) ./$< $(AFLAG) OJ\(./$@\) PR\(./main.ls1\)


eco_page.src : eco_page.c
	$(CC) ./$< $(CFLAG) ROM\(LARGE\) INCDIR\($(INCLUDE)\) SRC \(./$@\) 

#rf.src : rf.c
#	$(CC) ./$< $(CFLAG) INCDIR\($(INCLUDE)\) SRC \(./$@\) 

serial.src : serial.c
	$(CC) ./$< $(CFLAG) INCDIR\($(INCLUDE)\) SRC \(./$@\) 

isr_rf.src : isr_rf.c
	$(CC) ./$< $(CFLAG) INCDIR\($(INCLUDE)\) SRC \(./$@\) 

main.src : main.c
	$(CC) ./$< $(CFLAG) ROM\(LARGE\) INCDIR\($(INCLUDE)\) SRC \(./$@\) 

utils.src : utils.c
	$(CC) ../../include/utils/utils.c $(CFLAG) INCDIR\($(INCLUDE)\) PRINT\(./utils.lst\) PREPRINT\(./utils.i\) SRC\(./$@\) 

spi.src : spi.c
	$(CC) ../../include/spi/spi.c $(CFLAG) INCDIR\($(INCLUDE)\) PRINT\(./spi.lst\) PREPRINT\(./spi.i\) SRC\(./$@\) 

eeprom.src : eeprom.c
	$(CC) ../../include/eeprom/eeprom.c $(CFLAG) INCDIR\($(INCLUDE)\) PRINT\(./eeprom.lst\) PREPRINT\(./eeprom.i\) SRC\(./$@\) 

adc.src : adc.c
	$(CC) ../../include/adc/adc.c $(CFLAG) INCDIR\($(INCLUDE)\) PRINT\(./adc.lst\) PREPRINT\(./adc.i\) SRC\(./$@\) 

ts:
	python ./tools/func.py main.src
	python ./tools/eco_page_translate.py eco_page.src

asm:
	$(AC) ./eco_page.src $(AFLAG) OJ\(./eco_page.obj\) PR\(./eco_page.ls1\) 
	$(AC) ./$(SOURCE).src $(AFLAG) OJ\(./$(SOURCE).obj\) PR\(./$(SOURCE).ls1\)


link:	
	#$(LX) main.obj , isr_rf.obj , eco_page.obj , adc.obj , utils.obj , serial.obj , spi.obj, eeprom.obj , C51S.LIB TO $(TARGET) 
	$(LX) main.obj , isr_rf.obj , eco_page.obj , adc.obj , utils.obj , serial.obj , spi.obj, eeprom.obj , C51S.LIB TO $(TARGET) SEGMENTS\(?PR?_rf_send?ISR_RF\(C:0x1000\)\)
	
	$(OX) "MAIN" HEX
	#wine ./eeprepbat.bat
	python eeprep.py MAIN.hex main2.hex
	python convert.py main2.hex main3.hex


clean:
	rm -f *.obj *.hex *.lst *.i *.SBR *.MAP *.I *.ls1
	rm -f utils.* eeprom.* spi.* adc.* serial.* isr_rf.*
	rm -f main.LST main.OBJ MAIN 
	rm -f main.src eco_page.src

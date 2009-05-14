# Makefile for Memory Paging
#
# Wei-Han Chen <xwaynec@gmail.com>

SOURCE = main

TARGET = main

#CC = wine /Users/xwaynec/Library/Application\ Support/CrossOver/Bottles/winxp/dosdevices/c:/Keil/C51/BIN/C51.exe
#AC = wine /Users/xwaynec/Library/Application\ Support/CrossOver/Bottles/winxp/dosdevices/c:/Keil/C51/BIN/AX51.exe
#LX = wine /Users/xwaynec/Library/Application\ Support/CrossOver/Bottles/winxp/dosdevices/c:/Keil/C51/BIN/LX51.exe
#OX = wine /Users/xwaynec/Library/Application\ Support/CrossOver/Bottles/winxp/dosdevices/c:/Keil/C51/BIN/OHX51.exe

CC = wine /Users/eplab/Library/Application\ Support/CrossOver/Bottles/winxp/dosdevices/c:/Keil/C51/BIN/C51.exe
AC = wine /Users/eplab/Library/Application\ Support/CrossOver/Bottles/winxp/dosdevices/c:/Keil/C51/BIN/AX51.exe
LX = wine /Users/eplab/Library/Application\ Support/CrossOver/Bottles/winxp/dosdevices/c:/Keil/C51/BIN/LX51.exe
OX = wine /Users/eplab/Library/Application\ Support/CrossOver/Bottles/winxp/dosdevices/c:/Keil/C51/BIN/OHX51.exe
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
	#$(LX) main.obj , eco_page.obj , utils.obj , spi.obj, eeprom.obj , isr_rf , C51S.LIB TO $(TARGET) ASSIGN\(ECO_PAGE_TABLE_INDEX \(16\)\) SEGMENTS\(?PR?blink_fast?PAGING\(C:0x1000\)\) SEGMENTS\(?PR?blink_fast2?PAGING\(C:0x800\)\)
	$(LX) main.obj , isr_rf.obj , eco_page.obj , adc.obj , utils.obj , serial.obj , spi.obj, eeprom.obj , C51S.LIB TO $(TARGET) ASSIGN\(ECO_PAGE_TABLE_INDEX \(16\)\) #SEGMENTS\(?PR?blink_fast?PAGING\(C:0x1000\)\) SEGMENTS\(?PR?blink_fast2?PAGING\(C:0x800\)

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
	$(CC) ./$< $(CFLAG) INCDIR\($(INCLUDE)\) SRC \(./$@\) 

#rf.src : rf.c
#	$(CC) ./$< $(CFLAG) INCDIR\($(INCLUDE)\) SRC \(./$@\) 

serial.src : serial.c
	$(CC) ./$< $(CFLAG) INCDIR\($(INCLUDE)\) SRC \(./$@\) 

isr_rf.src : isr_rf.c
	$(CC) ./$< $(CFLAG) INCDIR\($(INCLUDE)\) SRC \(./$@\) 

main.src : main.c
	$(CC) ./$< $(CFLAG) INCDIR\($(INCLUDE)\) SRC \(./$@\) 

utils.src : utils.c
	$(CC) ../../include/utils/utils.c $(CFLAG) INCDIR\($(INCLUDE)\) PRINT\(./utils.lst\) PREPRINT\(./utils.i\) SRC\(./$@\) 

spi.src : spi.c
	$(CC) ../../include/spi/spi.c $(CFLAG) INCDIR\($(INCLUDE)\) PRINT\(./spi.lst\) PREPRINT\(./spi.i\) SRC\(./$@\) 

eeprom.src : eeprom.c
	$(CC) ../../include/eeprom/eeprom.c $(CFLAG) INCDIR\($(INCLUDE)\) PRINT\(./eeprom.lst\) PREPRINT\(./eeprom.i\) SRC\(./$@\) 

adc.src : adc.c
	$(CC) ../../include/adc/adc.c $(CFLAG) INCDIR\($(INCLUDE)\) PRINT\(./adc.lst\) PREPRINT\(./adc.i\) SRC\(./$@\) 

ts:
	python ./tools/function_call_translate.py main.src
	python ./tools/eco_page_translate.py eco_page.src

asm:
	$(AC) ./eco_page.src $(AFLAG) OJ\(./eco_page.obj\) PR\(./eco_page.ls1\) 
	$(AC) ./$(SOURCE).src $(AFLAG) OJ\(./$(SOURCE).obj\) PR\(./$(SOURCE).ls1\)


link:	
	$(LX) main.obj , eco_page.obj , adc.obj , utils.obj , serial.obj , spi.obj, eeprom.obj , C51S.LIB TO $(TARGET) ASSIGN\(ECO_PAGE_TABLE_INDEX \(16\)\) #SEGMENTS\(?PR?blink_fast?PAGING\(C:0x1000\)\) SEGMENTS\(?PR?blink_fast2?PAGING\(C:0x800\)\)
	
	$(OX) "MAIN" HEX
	#wine ./eeprepbat.bat
	python eeprep.py MAIN.hex main2.hex
	python convert.py main2.hex main3.hex


clean:
	rm -f *.obj *.hex *.lst *.i *.SBR *.MAP *.I *.ls1
	rm -f utils.* eeprom.* spi.* adc.* serial.* isr_rf.*
	rm -f main.LST main.OBJ MAIN 
	rm -f main.src eco_page.src

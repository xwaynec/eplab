# Makefile for Memory Paging
#
# Wei-Han Chen <xwaynec@gmail.com>

SOURCE = paging

TARGET = paging

CC = wine /Users/xwaynec/Library/Application\ Support/CrossOver/Bottles/winxp/dosdevices/c:/Keil/C51/BIN/C51.exe
AC = wine /Users/xwaynec/Library/Application\ Support/CrossOver/Bottles/winxp/dosdevices/c:/Keil/C51/BIN/AX51.exe
LX = wine /Users/xwaynec/Library/Application\ Support/CrossOver/Bottles/winxp/dosdevices/c:/Keil/C51/BIN/LX51.exe
OX = wine /Users/xwaynec/Library/Application\ Support/CrossOver/Bottles/winxp/dosdevices/c:/Keil/C51/BIN/OHX51.exe

#CC = C51.exe
#AC = AX51.exe
#LX = LX51.exe
#OX = OHX51.exe


INCLUDE = ../../Include
CFLAG 	= BROWSE DEBUG CODE LISTINCLUDE SYMBOLS PREPRINT 
AFLAG	= EP DEBUG SYMBOLS
LFLAG	= CODE

vpath %.h ../../include/Eco
vpath %.c ../../include/utils
vpath %.c ../../include/eeprom
vpath %.c ../../include/serial
vpath %.c ../../include/adc
vpath %.c ../../include/rf
vpath %.c ../../include/spi

vpath %.LIB /cygdrive/c/Keil/C51/INC 
vpath %.LIB /cygdrive/c/Keil/C51/LIB

all: main
main: paging.obj utils.obj spi.obj eeprom.obj adc.obj
	$(LX) paging.obj , utils.obj , spi.obj, eeprom.obj ,C51S.LIB TO $(TARGET) ASSIGN\(ECO_PAGE_TABLE_INDEX \(16\)\) SEGMENTS\(?PR?blink_fast?__PAGING\(C:0x1000\)\) SEGMENTS\(?PR?blink_fast2?__PAGING\(C:0x800\)\)

#	$(LX) paging.obj , utils.obj , spi.obj, eeprom.obj ,C51S.LIB TO $(TARGET) ASSIGN\(ECO_PAGE_TABLE_INDEX \(16\)\) 
	$(OX) "PAGING" HEX
	#./eeprepbat.bat	
	python eeprep.py PAGING.hex paging2.hex
	python convert.py paging2.hex paging3.hex

adc.obj : adc.src
	$(AC) ./$< $(AFLAG) OJ\(./$@\) PR\(./adc.ls1\)

utils.obj : utils.src 
	$(AC) ./$< $(AFLAG) OJ\(./$@\) PR\(./utils.ls1\)

spi.obj : spi.src 
	$(AC) ./$< $(AFLAG) OJ\(./$@\) PR\(./spi.ls1\)

eeprom.obj : eeprom.src 
	$(AC) ./$< $(AFLAG) OJ\(./$@\) PR\(./eeprom.ls1\)

paging.obj : paging.src
	$(AC) ./$< $(AFLAG) OJ\(./$@\) PR\(./paging.ls1\)


#paging.src : paging.c
#	$(CC) ./$< $(CFLAG) INCDIR\($(INCLUDE)\) SRC \(./$@\) 

utils.src : utils.c
	$(CC) ../../include/utils/utils.c $(CFLAG) INCDIR\($(INCLUDE)\) PRINT\(./utils.lst\) PREPRINT\(./utils.i\) SRC\(./$@\) 

spi.src : spi.c
	$(CC) ../../include/spi/spi.c $(CFLAG) INCDIR\($(INCLUDE)\) PRINT\(./spi.lst\) PREPRINT\(./spi.i\) SRC\(./$@\) 

eeprom.src : eeprom.c
	$(CC) ../../include/eeprom/eeprom.c $(CFLAG) INCDIR\($(INCLUDE)\) PRINT\(./eeprom.lst\) PREPRINT\(./eeprom.i\) SRC\(./$@\) 

adc.src : adc.c
	$(CC) ../../include/adc/adc.c $(CFLAG) INCDIR\($(INCLUDE)\) PRINT\(./adc.lst\) PREPRINT\(./adc.i\) SRC\(./$@\) 

asm:
	$(AC) ./$(SOURCE).src $(AFLAG) OJ\(./$(SOURCE).obj\) PR\(./$(SOURCE).ls1\)	

link:	
	$(LX) paging.obj , utils.obj , spi.obj, eeprom.obj ,C51S.LIB TO $(TARGET) ASSIGN\(ECO_PAGE_TABLE_INDEX \(16\)\) SEGMENTS\(?PR?blink_fast?__PAGING\(C:0x1000\)\) SEGMENTS\(?PR?blink_fast2?__PAGING\(C:0x800\)\)
	$(OX) "PAGING" HEX
	#wine ./eeprepbat.bat
	python eeprep.py PAGING.hex paging2.hex
	python convert.py paging2.hex paging3.hex

clean:
	rm -f *.obj *.hex *.lst *.i *.SBR *.MAP *.I *.ls1
	rm -f utils.* eeprom.* spi.* adc.*
	rm -f paging.LST paging.OBJ PAGING

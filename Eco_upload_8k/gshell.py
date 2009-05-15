# Min-Hua Chen <orca.chen@gmail.com> 

import Tkinter
import tkFileDialog
import prog_bar
import time
import serial
import eco_uart

root = Tkinter.Tk()
root.withdraw()

# setup serial port
uart = eco_uart.eco_uart(19200)

while 1:
        print "LE1/e - nRF24LE1 programmer"
        print "LU1/u - nRF24LU1 programmer"
        print "exit/bye/quit/q - exit this program"
        str = raw_input("Eco:$ ")

        if str == "q" or str == "bye" or str == "exit" or str == "quit":
                break
        elif str == "LE1" or str == "e":
                while 1:
                        #print "======= E1 programmer command list ======="
                        #print "blink/b - blink led"
                        #print "erase/e - erase whole EEPROM"
                        #print "uart_connect/c - connect to Eco by UART interface"
                        #print "upload_bin/u - upload bin image to Eco"
                        #print "upload_hex/x - upload hex file to Eco"
                        #print "dump_img/d - dump image of Eco"
                        #print "help/h - print this message"
                        #print "verify/v - verify written data"
                        #print "exit/bye/quit/q - return to main menu"

                        str = raw_input("Eco:$ ")

                        if str == "uart_connect" or str == "c":
                                uart.eco_test()
                        elif str == "upload_bin" or str == "u":
                                if uart.conn == 0:
                                        print "serial connection is not available"
                                        continue
                                print "upload image to Eco"
                                img = tkFileDialog.askopenfilename(title =
                                                                   "select a binary image", filetypes =
                                                                   [("binary file", "*.bin")])
                                print "uploading %s" % img
                                uart.upload_bin(img, root, "eeprom",8192)
                                print "upload successfully"
                        elif str == "upload_hex" or str == "x":
                                if uart.conn == 0:
                                        print "serial connection is not available"
                                        continue
                                print "upload hex to Eco"
                                img = tkFileDialog.askopenfilename(title =
                                                                   "select a hex file", filetypes =
                                                                   [("hex file", "*.hex")])
                                print "uploading %s" % img
                                uart.upload_hex(img, root, "eeprom", 8192)
                                print "upload successfully"
                        elif str == "dump_img" or str == "d":
                                if uart.conn == 0:
                                        print "serial connection is not available"
                                        continue
                                print "dump image"
                                uart.eco_dump(root,1,"eeprom",8192)
                        elif str == "help" or str == "h":
                                print "======= LE1 programmer command list ======="
                                print "blink/b - blink led"
                                print "erase/e - erase whole EEPROM"
                                print "uart_connect/c - connect to Eco by UART interface"
                                print "upload_bin/u - upload bin image to Eco"
                                print "upload_hex/v - upload hex file to Eco"
                                print "dump_img/d - dump image of Eco"
                                print "help/h - print this message"
                                print "verify/v - verify written data"
                                print "exit/bye/quit/q - return to main menu"
                        elif str == "q" or str == "bye" or str == "exit" or str == "quit":
                                break
                        elif str == "verify" or str == "v":
                                if uart.conn == 0:
                                        print "serial connection is not available"
                                        continue
                                print "verify written data"
                                uart.verify(root,"eeprom",8192)
                        elif str == "b" or str == "blink":
                                if uart.conn == 0:
                                        print "serial connection is not available"
                                        continue
                                print "blink led"
                                uart.blink()
                        elif str == "e" or str == "erase":
                                if uart.conn == 0:
                                        print "serial connection is not available"
                                        continue
                                print "erase EEPROM..."
                                uart.erase(root,8192)


        elif str == "LU1" or str == "u":
                while(1):
                        #print "======= LU1 programmer command list ======="
                        #print "blink/b - blink led"
                        #print "flash_erase/f - erase whole flash"
                        #print "uart_connect/c - connect to Eco by UART interface"
                        #print "upload_bin/u - upload bin image to Eco"
                        #print "upload_hex/v - upload hex file to Eco"
                        #print "dump_img/d - dump image of Eco"
                        #print "help/h - print this message"
                        #print "verify/v - verify written data"
                        #print "exit/bye/quit/q - return to main menu"

                        str = raw_input("Eco:$ ")

                        if str == "uart_connect" or str == "c":
                                uart.eco_test()
                        elif str == "upload_bin" or str == "u":
                                if uart.conn == 0:
                                        print "serial connection is not available"
                                        continue
                                print "upload image to Eco"
                                img = tkFileDialog.askopenfilename(title =
                                                                   "select a binary image", filetypes =
                                                                   [("binary file", "*.bin")])
                                print "uploading %s" % img
                                uart.upload_bin(img, root, "flash",16384)
                                print "upload successfully"
                        elif str == "upload_hex" or str == "x":
                                if uart.conn == 0:
                                        print "serial connection is not available"
                                        continue
                                print "upload hex to Eco"
                                img = tkFileDialog.askopenfilename(title =
                                                                   "select a hex file", filetypes =
                                                                   [("hex file", "*.hex")])
                                print "uploading %s" % img
                                uart.upload_hex(img, root, "flash",16384)
                                print "upload successfully"
                        elif str == "dump_img" or str == "d":
                                if uart.conn == 0:
                                        print "serial connection is not available"
                                        continue
                                print "dump image"
                                uart.eco_dump(root,1,"flash",16384)
                        elif str == "help" or str == "h":
                                print "======= LU1 programmer command list ======="
                                print "blink/b - blink led"
                                print "flash_erase/f - erase whole flash"
                                print "uart_connect/c - connect to Eco by UART interface"
                                print "upload_bin/u - upload bin image to Eco"
                                print "upload_hex/v - upload hex file to Eco"
                                print "dump_img/d - dump image of Eco"
                                print "help/h - print this message"
                                print "verify/v - verify written data"
                                print "exit/bye/quit/q - return to main menu"
                        elif str == "q" or str == "bye" or str == "exit" or str == "quit":
                                break
                        elif str == "verify" or str == "v":
                                if uart.conn == 0:
                                        print "serial connection is not available"
                                        continue
                                print "verify written data"
                                uart.verify(root,"flash",16384)
                        elif str == "b" or str == "blink":
                                if uart.conn == 0:
                                        print "serial connection is not available"
                                        continue
                                print "blink led"
                                uart.blink()
                        elif str == "f" or str == "flash_erase":
                                if uart.conn == 0:
                                        print "serial connection is not available"
                                        continue
                                print "erase flash pages..."
                                uart.flash_erase(root)
                        elif str == "status" or str == "s":
                                if uart.conn == 0:
                                        print "serial connection is not available"
                                        continue
                                print "status register:"
                                uart.status(root)



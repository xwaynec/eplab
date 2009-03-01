#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author(s): Wei-Han Chen (Embedded Platform Lab, NTHU)
# Copyright (c) 2008 National Tsing Hua University (NTHU) 
# Permission to copy, modify, and distribute this program is granted 
# for noncommercial purposes, provided the author(s) and copyright
# notice are retained. All other uses require explicit written
# permission from NTHU. 
#
# Wei-Han Chen <xwaynec@gmail.com> 

import sys
import os
import re
import urllib
import zipfile
import struct
import time
import serial
import pango
import gobject
import binascii

try:
    import pygtk
    pygtk.require("2.0")
except:
    print 'error import pygtk'
try:
    import gtk
    import gtk.glade
except:
    print "You need to install pyGTK or GTKv2 ",
    print "or set your PYTHONPATH correctly."
    sys.exit(1)



ECO_SERVER = "http://epl.cs.nthu.edu.tw/EcoKit/"
ECO_MEM_FORMAT = "EEPROM"  #EEPROM or FLASH
ECO_MEM_SIZE = 8192


def insert_web_row(model, parent, firstcolumn, secondcolumn, thirdcolumn):
    myiter=model.insert_after(parent, None)
    model.set_value(myiter, 1, firstcolumn)
    model.set_value(myiter, 2, secondcolumn)
    model.set_value(myiter, 3, thirdcolumn)


def insert_local_row(model, parent, firstcolumn, secondcolumn, thirdcolumn):
    myiter=model.insert_after(parent, None)
    model.set_value(myiter, 0, firstcolumn)
    model.set_value(myiter, 1, secondcolumn)
    model.set_value(myiter, 2, thirdcolumn)

    return myiter


def scan_serialprot():
    available = []
    for i in range(256):
        try:
            if os.name == "nt":
                s = serial.Serial(i)
                available.append((i,s.portstr))
                s.close()
            elif os.name == "posix":
                ser_name = '/dev/tty.SLAB_USBtoUART'
                s = serial.Serial(ser_name)
                available.append((i,s.portstr))
                s.close()
		break
            else:
                pass
        except serial.SerialException:
            pass
    return available


#-------- for color textview ---------
#-------------------------------------
PANGO_SCALE=1024

def insert_one_tag_into_buffer(buffer, name, *params):
    tag = gtk.TextTag(name)
    while(params):
        tag.set_property(params[0], params[1])
        params = params[2:]
    table = buffer.get_tag_table()
    table.add(tag)

    
def create_tags (buffer):
    
  insert_one_tag_into_buffer(buffer, "blue_foreground", "foreground", "blue")
  
  insert_one_tag_into_buffer(buffer, "red_foreground", "foreground", "red")

  insert_one_tag_into_buffer(buffer, "red_background", "background", "red")
  
  insert_one_tag_into_buffer(buffer, "blue_background", "background", "blue")
  
  
def insert_text (buffer, string):
    
    #iter = buffer.get_iter_at_offset (0)
    iter = buffer.get_end_iter()

    buffer.insert_with_tags_by_name(iter, string, "red_foreground")

def insert_text_blue (buffer, string):
    
    #iter = buffer.get_iter_at_offset (0)
    iter = buffer.get_end_iter()

    buffer.insert_with_tags_by_name(iter, string, "blue_foreground")
#-------------------------------------
#-------------------------------------


class ComfirmDialog:
    def __init__(self,gladefile,filename):
        self.gladefile = gladefile
        self.filename = filename
        self.dialogboxname = "comfirmdialog1"
        self.wTree = gtk.glade.XML(self.gladefile,self.dialogboxname)
        self.dlg = self.wTree.get_widget(self.dialogboxname)
        self.result = False
        label = self.wTree.get_widget("label6")
        content = 'Comfirmed to Update '+str(filename)+' ?'
        label.set_text(content)

        dic = {\
            "on_manager_destroy" : \
            gtk.main_quit,
            "on_button5_activate" : \
            self.on_button5_activate,
            "on_button5_clicked" : \
            self.on_button5_clicked
        }

        self.wTree.signal_autoconnect(dic)

    def on_button5_clicked(self,widget):
        self.result = True
        print 'on_button5_clicked'

    def on_button5_activate(self,widget):
        print 'on_button5_activate'

    def run(self):
        #self.result = self.dlg.run()
        self.dlg.run()
        self.dlg.destroy()

        #return the result
        return self.result    



class EEPROMDialog:
    def __init__(self,gladefile):
        self.gladefile = gladefile
        self.dialogboxname = "eepromdialog"
        self.wTree = gtk.glade.XML(self.gladefile,self.dialogboxname)
        self.dlg = self.wTree.get_widget(self.dialogboxname)
        self.result = False
        label = self.wTree.get_widget("label8")
        content = 'Config to EEPROM ?'
        label.set_text(content)

        dic = {\
            "on_manager_destroy" : \
            gtk.main_quit,
            "on_button9_activate" : \
            self.on_button9_activate,
            "on_button9_clicked" : \
            self.on_button9_clicked
        }

        self.wTree.signal_autoconnect(dic)

    def on_button9_clicked(self,widget):
        self.result = True
        print 'on_button9_clicked'
        #--------------------------
        global ECO_MEM_FORMAT
        global ECO_MEM_SIZE
        ECO_MEM_FORMAT = "EEPROM"
        ECO_MEM_SIZE = 4096
        #--------------------------
        print 'Config EEPROM 4K'

    def on_button9_activate(self,widget):
        print 'on_button9_activate'
        #--------------------------
        global ECO_MEM_FORMAT
        global ECO_MEM_SIZE
        ECO_MEM_FORMAT = "EEPROM"
        ECO_MEM_SIZE = 4096
        #--------------------------
        print 'Config EEPROM 4K'

    def run(self):
        
        #self.result = self.dlg.run()
        self.dlg.run()
        self.dlg.destroy()

        #return the result
        return self.result    

    
class FLASHDialog:
    def __init__(self,gladefile):
        self.gladefile = gladefile
        self.dialogboxname = "flashdialog"
        self.wTree = gtk.glade.XML(self.gladefile,self.dialogboxname)
        self.dlg = self.wTree.get_widget(self.dialogboxname)
        self.result = False
        label = self.wTree.get_widget("label9")
        content = 'Config to FLASH ?'
        label.set_text(content)

        dic = {\
            "on_manager_destroy" : \
            gtk.main_quit,
            "on_button11_activate" : \
            self.on_button11_activate,
            "on_button11_clicked" : \
            self.on_button11_clicked
        }

        self.wTree.signal_autoconnect(dic)

    def on_button11_clicked(self,widget):
        self.result = True
        print 'on_button11_clicked'
        #--------------------------
        global ECO_MEM_FORMAT
        global ECO_MEM_SIZE
        ECO_MEM_FORMAT = "FLASH"
        ECO_MEM_SIZE = 65536
        #--------------------------
        print 'Config FLASH 64K'

    def on_button11_activate(self,widget):
        print 'on_button11_activate'
        #--------------------------
        global ECO_MEM_FORMAT
        global ECO_MEM_SIZE
        ECO_MEM_FORMAT = "FLASH"
        ECO_MEM_SIZE = 65536
        #--------------------------
        print 'Config FLASH 64K'

    def run(self):
        
        #self.result = self.dlg.run()
        self.dlg.run()
        self.dlg.destroy()

        #return the result
        return self.result
    

class DeleteFileDialog:
    def __init__(self,gladefile,filename):
        self.gladefile = gladefile
        self.filename = filename
        self.dialogboxname = "deletedialog1"
        self.wTree = gtk.glade.XML(self.gladefile,self.dialogboxname)
        self.dlg = self.wTree.get_widget(self.dialogboxname)
        self.result = False
        label = self.wTree.get_widget("label5")
        content = 'Comfirmed to Delete '+str(filename)+' ?'
        label.set_text(content)

        dic = {\
            "on_manager_destroy" : \
            gtk.main_quit,
            "on_button3_activate" : \
            self.on_button3_activate,
            "on_button3_clicked" : \
            self.on_button3_clicked
        }

        self.wTree.signal_autoconnect(dic)

    def on_button3_clicked(self,widget):
        self.result = True
        print 'on_button3_clicked'

    def on_button3_activate(self,widget):
        print 'on_button3_activate'

    def run(self):
        #self.result = self.dlg.run()
        self.dlg.run()
        self.dlg.destroy()

        #return the result
        return self.result

class ConfigSerialPortDialog:
    def __init__(self,gladefile):
        self.gladefile = gladefile
        self.dialogboxname = "configureserialdialog1"
        self.wTree = gtk.glade.XML(self.gladefile,self.dialogboxname)
        self.dlg = self.wTree.get_widget(self.dialogboxname)
        self.result = [False,""]

        combobox = self.wTree.get_widget("combobox1")
        liststore = gtk.ListStore(str)
        cell = gtk.CellRendererText()
        combobox.pack_start(cell)
        combobox.add_attribute(cell, 'text', 0)
        combobox.set_wrap_width(1)


        s = scan_serialprot()
        print s
        ser = []

        for i in range(len(s)):
            print s[i][1]
            liststore.append([s[i][1]])

        combobox.set_model(liststore)
        combobox.connect('changed', self.changed_combobox)
        combobox.set_active(0)

        #initialize return value 
        if len(s) > 0:
            self.result[1] = str(s[0][1])
            print 'initial return value = ',self.result

        dic = {\
            "on_manager_destroy" : \
            gtk.main_quit,
            "on_button1_clicked" : \
            self.on_button1_clicked,
            "on_button2_clicked" : \
            self.on_button2_clicked
        }

        self.wTree.signal_autoconnect(dic)

    def on_button1_clicked(self,widget):
        self.result[0] = True

    def on_button2_clicked(self,widget):
        self.result[0] = False

    def changed_combobox(self,combobox):
        model = combobox.get_model()
        index = combobox.get_active()
        if index > -1:
            self.result[1] = model[index][0]
            print model[index][0], 'selected'
        return

    def run(self):

        self.dlg.run()
        self.dlg.destroy()

        return self.result

class AboutDialog:
    def __init__(self,gladefile):
        self.gladefile = gladefile
        self.dialogboxname = "aboutdialog1"
    def run(self):
        self.wTree = gtk.glade.XML(self.gladefile, self.dialogboxname)
        self.dlg = self.wTree.get_widget(self.dialogboxname)
        self.result = self.dlg.run()
        self.dlg.destroy()

        #return the result
        return self.result

class ProgressBar:
    def __init__(self,gladefile,bar_name):
        self.gladefile = gladefile
        self.dialogboxname = "progressbar_dialog1"
        self.bar_name = bar_name

    def run(self):
        self.wTree = gtk.glade.XML(self.gladefile,self.dialogboxname)
        self.progressbar = self.wTree.get_widget(self.dialogboxname)
        self.bar = self.wTree.get_widget("progressbar1")
        self.bar.set_text(self.bar_name)

    def close(self):
        self.progressbar.destroy()


    def set_fraction(self,val):
        if val <= 1.0 and val >= 0.0:
            self.bar.set_fraction(val)
        else:
            self.bar.set_fraction(1.0)
        #http://faq.pygtk.org/index.py?req=show&file=faq23.020.htp
        while gtk.events_pending():
            gtk.main_iteration()

class EcoManager:
    def __init__(self):

        #Set Glade File
        self.gladefile = "Eco_Manager.glade"
        #window Title Name
        self.windowname = "Eco Manager"
        self.wTree = gtk.glade.XML(self.gladefile,self.windowname)

        #critical section for component button
        self.component_critical = 1

        # Web List
        import gobject
        self.webview = self.wTree.get_widget("treeview1")
        self.webmodel = gtk.TreeStore(gobject.TYPE_BOOLEAN,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING)
        self.webview.set_model(self.webmodel)
        self.webview.set_headers_visible(True)

        # The toggle cellrenderer is setup and we allow it to be
        # changed (toggled) by the user.
        renderer = gtk.CellRendererToggle()
        renderer.set_property('activatable', True)
        renderer.connect('toggled',self.weblist_toggled_cb,self.webmodel)
        column = gtk.TreeViewColumn("Check",renderer)
        #column.add_attribute(renderer,"active",1)
        column.set_attributes(renderer, active=0)
        self.webview.append_column(column)

        #Create the text cellrenderer
        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn("Name",renderer,text = 1)
        column.set_resizable(True)
        self.webview.append_column(column)

        #Create the text cellrenderer
        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn("Description", renderer, text = 2)
        column.set_resizable(True)
        self.webview.append_column(column)

        #Create the text cellrenderer
        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn("Status",renderer,text = 3)
        column.set_resizable(True)
        self.webview.append_column(column)

        #Local List
        self.localview = self.wTree.get_widget("treeview2")
        #self.localmodel = gtk.TreeStore(gobject.TYPE_BOOLEAN,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING)
        self.localmodel = gtk.TreeStore(gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING)
        self.localview.set_model(self.localmodel)
        self.localview.set_headers_visible(True)

        #Create the text cellrenderer
        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn("Name",renderer,text = 0)
        column.set_resizable(True)
        self.localview.append_column(column)

        #Create the text cellrenderer
        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn("Size", renderer, text = 1)
        column.set_resizable(True)
        self.localview.append_column(column)


        #Create the text cellrenderer
        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn("Time",renderer,text = 2)
        column.set_resizable(True)
        self.localview.append_column(column)


        package_path = os.getcwd() + '/package'
        package_list = os.listdir(package_path)
        print package_list

        #Get current local package list and put them to list 
        for i in range(len(package_list)):
            reg = re.search('([-a-zA-Z0-9]+)_([-a-zA-Z0-9]+)_([-a-zA-Z0-9]+)_([\d]+).zip',package_list[i])
            if reg:
                print reg.group(3),'list =',reg.group()

                #self.local_list_zip.append(reg.group())
                #self.local_list.append(reg.group(1) + reg.group(2))
                #self.local_list_version.append(reg.group(3))

                myinter = insert_local_row(self.localmodel,None,reg.group(0),os.path.getsize(package_path+'/'+reg.group(0)),reg.group(4))
                print 'zip_file = ',package_path + '/' + reg.group(0)
                zip_file = zipfile.ZipFile(package_path + '/' + reg.group(0))
                for zip_info in zip_file.infolist():
                    print 'zip_info = ',zip_info.filename,zip_info.date_time,zip_info.file_size

                    reg_zip = re.search('[-\/\w]+.(hex)',zip_info.filename)
                    if reg_zip:
                        insert_local_row(self.localmodel,myinter,reg_zip.group(0),zip_info.file_size,'')


        self.webview.show()


        #initialize serial port 
        self.connect_port = ''
        self.ser = serial.Serial()

        #initialize message log textview
        self.message = self.wTree.get_widget("textview1")
        self.messagebuf = self.message.get_buffer()
        self.message.modify_font(pango.FontDescription("Courier 10"))

        create_tags(self.messagebuf)
        
        #Create dictionary and connect to event handle function
        dic = {\
            "on_manager_destroy" : \
            self.eco_manager_quit,
            "on_imagemenuitem5_activate" : \
            gtk.main_quit,
            "on_tb1_connect_clicked" : \
            self.on_connect_server_clicked,
            "on_imagemenuitem10_activate" : \
            self.on_about_activate,
            "on_eepromdialog_activate" : \
            self.on_eeprom_activate,
            "on_flashdialog_activate" : \
            self.on_flash_activate,
            "on_tb2_configure_clicked" : \
            self.on_serial_configure_clicked,
            "on_tb1_download_clicked" : \
            self.on_server_download_clicked,
            "on_tb2_reload_clicked" : \
            self.on_locallist_reload_clicked,
            "on_tb2_delete_clicked" : \
            self.on_locallist_delete_clicked,
            "on_tb2_connect_clicked" : \
            self.on_serial_connect_clicked,
            "on_tb2_dump_clicked" : \
            self.on_locallist_dump_clicked,
            "on_tb2_erase_clicked" : \
            self.on_locallist_erase_clicked,
            "on_tb2_upload_clicked" : \
            self.on_locallist_upload_clicked,
            "on_tb2_verify_clicked" : \
            self.on_locallist_verify_clicked,
            "on_tb2_Hex_clicked" : \
            self.on_locallist_Hex_clicked,
            "on_tb2_version_clicked" : \
            self.on_locallist_version_clicked
        }

        self.wTree.signal_autoconnect(dic)
        return

    def eco_manager_quit(self,widget):
        if self.ser.isOpen():
            print 'Serial Connection is close'
            self.messagebuf.insert(self.messagebuf.get_end_iter(),'Connection is close!\n')
            self.message.scroll_mark_onscreen(self.messagebuf.get_insert())
            self.ser.close()
        gtk.main_quit()

    def weblist_toggled_cb(self,cell, path, model ):
        self.webmodel[path][0] = not self.webmodel[path][0]
        print "Toggle '%s' to: %s" % (model[path][1], model[path][0],)
        return


    def on_locallist_delete_clicked(self,widget):
        print 'on_locallist_delete_clicked'
        select_item = self.localview.get_selection()
        (model,iter) = select_item.get_selected()
        if iter:
            path = model.get_path(iter)
            print 'path = ',path
            if len(path) == 1:
                delete_path = os.getcwd() + '/package/' + self.localmodel[path][0]
                print 'Delete ',delete_path
                DeleteDlg = DeleteFileDialog(self.gladefile,self.localmodel[path][0])
                if DeleteDlg.run():
                    print 'DeleteDlg True'
                    os.remove(delete_path)


    def on_locallist_reload_clicked(self,widget):
        package_path = os.getcwd() + '/package'
        package_list = os.listdir(package_path)
        print package_list
        self.localmodel.clear()
        #Get current local package list and put them to list 
        for i in range(len(package_list)):
            reg = re.search('([-a-zA-Z0-9]+)_([-a-zA-Z0-9]+)_([-a-zA-Z0-9]+)_([\d]+).zip',package_list[i])
            if reg:
                print reg.group(3),'list =',reg.group()

                #self.local_list_zip.append(reg.group())
                #self.local_list.append(reg.group(1) + reg.group(2))
                #self.local_list_version.append(reg.group(3))
                myinter = insert_local_row(self.localmodel,None,reg.group(0),os.path.getsize(package_path+'/'+reg.group(0)),reg.group(4))
                print 'zip_file = ',package_path + '/' + reg.group(0)
                zip_file = zipfile.ZipFile(package_path + '/' + reg.group(0))
                for zip_info in zip_file.infolist():
                    print 'zip_info = ',zip_info.filename,zip_info.date_time,zip_info.file_size

                    reg_zip = re.search('[-\/\w]+.(hex)',zip_info.filename)
                    if reg_zip:
                        insert_local_row(self.localmodel,myinter,reg_zip.group(0),zip_info.file_size,'')

        print 'on_locallist_reload_clicked'

    def on_serial_configure_clicked(self,widget):
        ConfigSerialDlg = ConfigSerialPortDialog(self.gladefile)
        #self.connect_port = ConfigSerialDlg.run()

        flag , self.connect_port = ConfigSerialDlg.run()
        if flag == True:
            print 'on_serial_configure_clicked = ' , self.connect_port
            self.Connect_widget = self.wTree.get_widget("Connect")
            self.messagebuf.insert(self.messagebuf.get_end_iter(),'Open '+ self.connect_port +'\n')
            self.message.scroll_mark_onscreen(self.messagebuf.get_insert())
            self.Connect_widget.set_sensitive(True)
        else:
            self.Connect_widget = self.wTree.get_widget("Connect")
            self.Connect_widget.set_sensitive(False)


    def on_locallist_dump_clicked(self,widget):
        
        print 'on_locallist_dump_clicked'
        self.messagebuf.insert(self.messagebuf.get_end_iter(),'Dump Eco hex file\n')
        #print self.message.scroll_to_iter(self.messagebuf.get_end_iter(),0)
        self.message.scroll_mark_onscreen(self.messagebuf.get_insert())

        #timestamp for now time
        now_time = time.time()
        try:
            self.Dump_widget.set_sensitive(False)
            self.Upload_widget.set_sensitive(False)
            self.Verify_widget.set_sensitive(False)
            self.Erase_widget.set_sensitive(False)
            self.Version_widget.set_sensitive(False)
            self.Hex_widget.set_sensitive(False)
            if ECO_MEM_FORMAT == "EEPROM":
                #flush input buffer
                self.ser.flushInput()
                #flush output buffer
                self.ser.flushOutput()
                self.ser.write("D")
            elif ECO_MEM_FORMAT == "FLASH":
                #flush input buffer
                self.ser.flushInput()
                #flush output buffer
                self.ser.flushOutput()
                self.ser.write("d")

            mem_high = ECO_MEM_SIZE >> 8
            mem_low = ECO_MEM_SIZE & 0xff

            mem_high = struct.pack("B",mem_high)
            mem_low = struct.pack("B",mem_low)

            self.ser.write(mem_high)
            self.ser.write(mem_low)

            bar = ProgressBar(self.gladefile,"Dump")
            bar.run()

            mem_content0 = ""
            mem_content = ""
            self.dump_mem_data = ""
            row = ECO_MEM_SIZE / 16
            for i in range(row):
                for j in range(18):

                    c = self.ser.read()

                    v = struct.unpack("B",c)
                    #print 'v = ',v
                    if j == 0:
                        mem_content0 = mem_content0 + "0000"
                    if j == 2:
                        mem_content0 = mem_content0 + ": "
                    if j < 2:
                        mem_content0 = mem_content0 + "%02X" % v[0]
                    if j >= 2:
                        mem_content = mem_content + "%02X " % v[0]
                        self.dump_mem_data += "%02X" % v[0]

                if (i % 5) == 0:
                    bar.set_fraction(1.0 * i/ row)

                #self.messagebuf.insert(self.messagebuf.get_end_iter(),mem_content + "\n")
                #self.messagebuf.insert(self.messagebuf.get_end_iter(),mem_content0)
                insert_text_blue(self.messagebuf, mem_content0)
                insert_text(self.messagebuf, mem_content + "\n")
                
                self.message.scroll_mark_onscreen(self.messagebuf.get_insert())
                #self.message.scroll_to_iter(self.messagebuf.get_end_iter(),0)
                #rint mem_content
                #clear read data
                mem_content0 = ""
                mem_content = ""

            bar.close()
            prev_time = now_time
            now_time = time.time()
            self.Dump_widget.set_sensitive(True)
            self.Upload_widget.set_sensitive(True)
            self.Verify_widget.set_sensitive(True)
            self.Erase_widget.set_sensitive(True)
            self.Version_widget.set_sensitive(True)
            self.Hex_widget.set_sensitive(True)

            self.messagebuf.insert(self.messagebuf.get_end_iter(),"time elapsed: %.3f s\n" % (now_time - prev_time))
            self.message.scroll_mark_onscreen(self.messagebuf.get_insert())

        except:
            if bar:
                bar.close()
            self.Dump_widget.set_sensitive(True)
            self.Upload_widget.set_sensitive(True)
            self.Verify_widget.set_sensitive(True)
            self.Erase_widget.set_sensitive(True)
            self.Version_widget.set_sensitive(True)
            self.Hex_widget.set_sensitive(True)
            #self.messagebuf.insert(self.messagebuf.get_end_iter(),'Error!\n')
            insert_text(self.messagebuf, 'Error!\n')
            self.message.scroll_mark_onscreen(self.messagebuf.get_insert())



    def on_locallist_version_clicked(self,widget):
        print 'on_locallist_version_clicked'

        version = ""
        try:
            self.Dump_widget.set_sensitive(False)
            self.Upload_widget.set_sensitive(False)
            self.Verify_widget.set_sensitive(False)
            self.Erase_widget.set_sensitive(False)
            self.Version_widget.set_sensitive(False)
            self.Hex_widget.set_sensitive(False)

            self.ser.write("g")

            for i in range(5):
                b = self.ser.read()
                version = version + b

            self.Dump_widget.set_sensitive(True)
            self.Upload_widget.set_sensitive(True)
            self.Verify_widget.set_sensitive(True)
            self.Erase_widget.set_sensitive(True)
            self.Version_widget.set_sensitive(True)
            self.Hex_widget.set_sensitive(True)
            self.messagebuf.insert(self.messagebuf.get_end_iter(),'Dev. Board Firmware Version : ' + version + '\n')
            self.message.scroll_mark_onscreen(self.messagebuf.get_insert())
        except:
            self.Dump_widget.set_sensitive(True)
            self.Upload_widget.set_sensitive(True)
            self.Verify_widget.set_sensitive(True)
            self.Erase_widget.set_sensitive(True)
            self.Version_widget.set_sensitive(True)
            self.Hex_widget.set_sensitive(True)
            self.messagebuf.insert(self.messagebuf.get_end_iter(),'Error!\n')
            self.message.scroll_mark_onscreen(self.messagebuf.get_insert())

    def on_locallist_erase_clicked(self,widget):
        print 'on_locallist_erase_clicked'

        now_time = time.time()
        bar = ProgressBar(self.gladefile,"Erase")
        bar.run()
        total = ECO_MEM_SIZE
        cur = 0

        try:
            self.Dump_widget.set_sensitive(False)
            self.Upload_widget.set_sensitive(False)
            self.Verify_widget.set_sensitive(False)
            self.Erase_widget.set_sensitive(False)
            self.Version_widget.set_sensitive(False)
            self.Hex_widget.set_sensitive(False)
            self.ser.write("E")

            # flash/eeprom size
            mem_high = ECO_MEM_SIZE  >> 8
            mem_low = ECO_MEM_SIZE & 0xff
            mem_high = struct.pack("B", mem_high)
            mem_low = struct.pack("B", mem_low)
            self.ser.write(mem_high)
            self.ser.write(mem_low)

            while 1:
                b = self.ser.read()
                if b == "C":
                    cur += 64
                    bar.set_fraction(1.0 * (cur - 64)/ total)
                elif b == "D":
                    print "EEPROM erased"
                    break

            prev_time = now_time
            now_time = time.time()
            bar.close()
            self.Dump_widget.set_sensitive(True)
            self.Upload_widget.set_sensitive(True)
            self.Verify_widget.set_sensitive(True)
            self.Erase_widget.set_sensitive(True)
            self.Version_widget.set_sensitive(True)
            self.Hex_widget.set_sensitive(True)
            self.messagebuf.insert(self.messagebuf.get_end_iter(),"time elapsed: %.3f s\n" % (now_time - prev_time))
            self.message.scroll_mark_onscreen(self.messagebuf.get_insert())

        except:
            if bar:
                bar.close()
            self.Dump_widget.set_sensitive(True)
            self.Upload_widget.set_sensitive(True)
            self.Verify_widget.set_sensitive(True)
            self.Erase_widget.set_sensitive(True)
            self.Version_widget.set_sensitive(True)
            self.Hex_widget.set_sensitive(True)
            self.messagebuf.insert(self.messagebuf.get_end_iter(),'Error!\n')
            self.message.scroll_mark_onscreen(self.messagebuf.get_insert())

    def on_locallist_Hex_clicked(self,widget):
        print 'on_locallist_Hex_clicked'
        file_dialog = gtk.FileChooserDialog("Select Hex File", \
                                            None, \
                                            gtk.FILE_CHOOSER_ACTION_OPEN, \
                                            (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN, gtk.RESPONSE_OK) \
                                            )
        file_dialog.set_default_response(gtk.RESPONSE_OK)

        file_filter = gtk.FileFilter()
        file_filter.set_name("Hex Files")
        file_filter.add_pattern("*.hex")
        file_dialog.add_filter(file_filter)

        response = file_dialog.run()

        selected_filename = ""
        selected_ok = False
        if response == gtk.RESPONSE_OK:
            	selected_ok = True
	    	print file_dialog.get_filename(), 'selected'
            	selected_filename = u'%s' %file_dialog.get_filename()
			
        else:
            print 'Closed, no files selected'



        file_dialog.destroy()

        if selected_ok:
            try:

                f = open(selected_filename,'r')
                hex_file = f.read()
                f.close()
                self.ori_data = ""
                total_data_len = 0
                bin_data = ""

                now_time = time.time()

                #seperate file to lines
                if '\r' in hex_file:
                    upload_lines = hex_file.split('\r\n')
                else:
                    upload_lines = hex_file.split('\n')

                for line in upload_lines:
                    if line == '' or line[0] != ":":
                        continue

                    #discard ':'
                    data = line[1:]

                    #hex string to binary
                    temp_data = binascii.unhexlify(data)

                    #parsing
                    rec_len = struct.unpack("B", temp_data[0])
                    rec_type = struct.unpack("B", temp_data[3])

                    #end of hex
                    if rec_type[0] == 01:
                        break

                    #read data, update total_data_len
                    total_data_len += rec_len[0]
                    #store binary data
                    for i in range(rec_len[0]):
                        bin_data += temp_data[4+i];


                #send image to eco
                if ECO_MEM_FORMAT == "EEPROM":
                    self.ser.write("U")
                elif ECO_MEM_FORMAT == "FLASH":
                    self.ser.write("u")
                    #send info page config
                    t = struct.pack("B", 0xFF)
                    self.ser.write(t)  #DAEN
                    t = struct.pack("B", 0xFF)
                    self.ser.write(t) #NUPP
                    t = struct.pack("B", 0x00)
                    self.ser.write(t)  #STP
                    #read ready signal
                    self.ser.read()


                # send data length
                mem_high = total_data_len >> 8
                mem_low = total_data_len & 0xff
                mem_high = struct.pack("B", mem_high)
                mem_low = struct.pack("B", mem_low)

                self.ser.write(mem_high)
                self.ser.write(mem_low)

                # send flash/eeprom size
                mem_high = ECO_MEM_SIZE >> 8
                mem_low = ECO_MEM_SIZE & 0xff
                mem_high = struct.pack("B", mem_high)
                mem_low = struct.pack("B", mem_low)

                self.ser.write(mem_high)
                self.ser.write(mem_low)


                lc = total_data_len / 64
                lm = total_data_len % 64

                bar = ProgressBar(self.gladefile,"Upload")
                bar.run()

                send_data_len = 0
                #sen data to target sensor
                for i in range(lc):
                    for j in range(64):
                        self.ser.write(bin_data[i*64+j])
                        #b = self.uart.read()
                        b = struct.unpack("B",bin_data[i*64+j])
                        self.ori_data += "%02X" % b
                    send_data_len += 64;
                    b = self.ser.read()
                    bar.set_fraction(1.0 * send_data_len / ECO_MEM_SIZE)

                for j in range(lm):     
                    self.ser.write(bin_data[lc*64+j])
                    b = struct.unpack("B",bin_data[lc*64+j])
                    self.ori_data += "%02X" % b

                send_data_len += lm;    
                b = self.ser.read()
                #bar.set_fraction(1.0 * send_data_len / ECO_MEM_SIZE)


                print "padding 0xFF"
                self.ori_data += "FF" * (ECO_MEM_SIZE - send_data_len)

                for p in range(ECO_MEM_SIZE - send_data_len):   
                    b = self.ser.read()
                    if b == "C":
                        send_data_len += 64
                        bar.set_fraction(1.0 * send_data_len / ECO_MEM_SIZE)
                    elif b == "D":
                        break

                bar.close()
                self.Dump_widget.set_sensitive(True)
                self.Upload_widget.set_sensitive(True)
                self.Verify_widget.set_sensitive(True)
                self.Erase_widget.set_sensitive(True)
                self.Version_widget.set_sensitive(True)
                self.Hex_widget.set_sensitive(True)
                prev_time = now_time
                now_time = time.time()

                self.messagebuf.insert(self.messagebuf.get_end_iter(),hex_file + '\n')
                self.messagebuf.insert(self.messagebuf.get_end_iter(),"time elapsed: %.3f s\n" % (now_time - prev_time))
                self.message.scroll_mark_onscreen(self.messagebuf.get_insert())


            except:
                if bar:
                    bar.close()
                self.Dump_widget.set_sensitive(True)
                self.Upload_widget.set_sensitive(True)
                self.Verify_widget.set_sensitive(True)
                self.Erase_widget.set_sensitive(True)
                self.Version_widget.set_sensitive(True)
                self.Hex_widget.set_sensitive(True)
                self.messagebuf.insert(self.messagebuf.get_end_iter(),'Error!\n')
                self.message.scroll_mark_onscreen(self.messagebuf.get_insert())

        else:
            print 'Closed, no files selected'





    def on_locallist_upload_clicked(self,widget):
        print 'on_locallist_upload_clicked'
        sel = self.localview.get_selection()
        (model, iter) = sel.get_selected()

        if iter:
            path = model.get_path(iter)
            #print model[path][0]
            file_extension = re.search('[-\/\w]+.(hex)',model[path][0])

            if len(path) > 1:
                #print model[path][0]
                if file_extension:
                    #print file_extension.group(1)
                    if file_extension.group(1) == "hex":
                        try:
                            self.Dump_widget.set_sensitive(False)
                            self.Upload_widget.set_sensitive(False)
                            self.Verify_widget.set_sensitive(False)
                            self.Erase_widget.set_sensitive(False)
                            self.Version_widget.set_sensitive(False)
                            self.Hex_widget.set_sensitive(False)

                            root_path , leaf_path = model.get_path(iter)

                            self.messagebuf.insert(self.messagebuf.get_end_iter(),'Upload ' + model[path][0]+ ' to Eco\n')
                            self.message.scroll_mark_onscreen(self.messagebuf.get_insert())

                            #root_path = str(path).split(':')
                            #print 'path = ',path
                            #print 'root path = ',root_path[0]

                            print 'root = ',root_path
                            print 'leaf = ',leaf_path
                            print model[root_path][0]

                            package_path = os.getcwd() + '/package'
                            print package_path + '/' + model[root_path][0]

                            zip_file = zipfile.ZipFile(package_path + '/' + model[root_path][0],'r')

                            upload_file = zip_file.read(model[path][0])
                            #print upload_file
                            zip_file.close()

                            self.ori_data = ""
                            total_data_len = 0
                            bin_data = ""

                            now_time = time.time()

                            #seperate file to lines
                            if '\r' in upload_file:
                                upload_lines = upload_file.split('\r\n')
                            else:
                                upload_lines = upload_file.split('\n')

                            for line in upload_lines:
                                if line == '' or line[0] != ":":
                                    continue

                                #discard ':'
                                data = line[1:]

                                #hex string to binary
                                temp_data = binascii.unhexlify(data)

                                #parsing
                                rec_len = struct.unpack("B", temp_data[0])
                                rec_type = struct.unpack("B", temp_data[3])

                                #end of hex
                                if rec_type[0] == 01:
                                    break

                                #read data, update total_data_len
                                total_data_len += rec_len[0]
                                #store binary data
                                for i in range(rec_len[0]):
                                    bin_data += temp_data[4+i];


                            #send image to eco
                            if ECO_MEM_FORMAT == "EEPROM":
                                self.ser.write("U")
                            elif ECO_MEM_FORMAT == "FLASH":
                                self.ser.write("u")
                                #send info page config
                                t = struct.pack("B", 0xFF)
                                self.ser.write(t)  #DAEN
                                t = struct.pack("B", 0xFF)
                                self.ser.write(t) #NUPP
                                t = struct.pack("B", 0x00)
                                self.ser.write(t)  #STP
                                #read ready signal
                                self.ser.read()


                            # send data length
                            mem_high = total_data_len >> 8
                            mem_low = total_data_len & 0xff
                            mem_high = struct.pack("B", mem_high)
                            mem_low = struct.pack("B", mem_low)

                            self.ser.write(mem_high)
                            self.ser.write(mem_low)

                            # send flash/eeprom size
                            mem_high = ECO_MEM_SIZE >> 8
                            mem_low = ECO_MEM_SIZE & 0xff
                            mem_high = struct.pack("B", mem_high)
                            mem_low = struct.pack("B", mem_low)

                            self.ser.write(mem_high)
                            self.ser.write(mem_low)


                            lc = total_data_len / 64
                            lm = total_data_len % 64

                            bar = ProgressBar(self.gladefile,"Upload")
                            bar.run()

                            send_data_len = 0
                            #sen data to target sensor
                            for i in range(lc):
                                for j in range(64):
                                    self.ser.write(bin_data[i*64+j])
                                    #b = self.uart.read()
                                    b = struct.unpack("B",bin_data[i*64+j])
                                    self.ori_data += "%02X" % b
                                send_data_len += 64;
                                b = self.ser.read()
                                bar.set_fraction(1.0 * send_data_len / ECO_MEM_SIZE)

                            for j in range(lm): 
                                self.ser.write(bin_data[lc*64+j])
                                b = struct.unpack("B",bin_data[lc*64+j])
                                self.ori_data += "%02X" % b

                            send_data_len += lm;        
                            b = self.ser.read()
                            #bar.set_fraction(1.0 * send_data_len / ECO_MEM_SIZE)


                            print "padding 0xFF"
                            self.ori_data += "FF" * (ECO_MEM_SIZE - send_data_len)

                            for p in range(ECO_MEM_SIZE - send_data_len):       
                                b = self.ser.read()
                                if b == "C":
                                    send_data_len += 64
                                    bar.set_fraction(1.0 * send_data_len / ECO_MEM_SIZE)
                                elif b == "D":
                                    break

                            bar.close()
                            self.Dump_widget.set_sensitive(True)
                            self.Upload_widget.set_sensitive(True)
                            self.Verify_widget.set_sensitive(True)
                            self.Erase_widget.set_sensitive(True)
                            self.Version_widget.set_sensitive(True)
                            self.Hex_widget.set_sensitive(True)
                            prev_time = now_time
                            now_time = time.time()

                            self.messagebuf.insert(self.messagebuf.get_end_iter(),upload_file + '\n')
                            self.messagebuf.insert(self.messagebuf.get_end_iter(),"time elapsed: %.3f s\n" % (now_time - prev_time))
                            self.message.scroll_mark_onscreen(self.messagebuf.get_insert())


                        except:
                            if bar:
                                bar.close()
                            self.Dump_widget.set_sensitive(True)
                            self.Upload_widget.set_sensitive(True)
                            self.Verify_widget.set_sensitive(True)
                            self.Erase_widget.set_sensitive(True)
                            self.Version_widget.set_sensitive(True)
                            self.Hex_widget.set_sensitive(True)
                            self.messagebuf.insert(self.messagebuf.get_end_iter(),'Error!\n')
                            self.message.scroll_mark_onscreen(self.messagebuf.get_insert())

    def on_locallist_verify_clicked(self,widget):
        print 'on_locallist_verify_clicked'
        #sel = self.localview.get_selection()
        #(model, iter) = sel.get_selected()
        #if iter:
            #path = model.get_path(iter)
            #if len(path) > 1:

        #print model[path][0]
        #self.messagebuf.insert(self.messagebuf.get_end_iter(),'Verify Eco hex file is the same with '+ model[path][0]+'\n')

        #Dump Data from eco

        try:
            self.Dump_widget.set_sensitive(False)
            self.Upload_widget.set_sensitive(False)
            self.Verify_widget.set_sensitive(False)
            self.Erase_widget.set_sensitive(False)
            self.Version_widget.set_sensitive(False)
            self.Hex_widget.set_sensitive(False)
            if ECO_MEM_FORMAT == "EEPROM":
                self.ser.write("D")
            elif ECO_MEM_FORMAT == "FLASH":
                self.ser.write("d")

            mem_high = ECO_MEM_SIZE >> 8
            mem_low = ECO_MEM_SIZE & 0xff

            mem_high = struct.pack("B",mem_high)
            mem_low = struct.pack("B",mem_low)

            self.ser.write(mem_high)
            self.ser.write(mem_low)

            self.dump_mem_data = ""
            row = ECO_MEM_SIZE / 16



            bar = ProgressBar(self.gladefile,"Verify")
            bar.run()

            for i in range(row):
                for j in range(18):
                    c = self.ser.read()
                    v = struct.unpack("B",c)
                    if j >= 2:
                        self.dump_mem_data += "%02X" % v[0]

                if (i % 5) == 0:
                    bar.set_fraction(1.0 * i/ row)

            bar.close()
            self.Dump_widget.set_sensitive(True)
            self.Upload_widget.set_sensitive(True)
            self.Verify_widget.set_sensitive(True)
            self.Erase_widget.set_sensitive(True)
            self.Version_widget.set_sensitive(True)
            self.Hex_widget.set_sensitive(True)

            #self.messagebuf.insert(self.messagebuf.get_end_iter(),mem_content + "\n")

            if self.dump_mem_data == self.ori_data:
                print "result: consistent data"
                self.messagebuf.insert(self.messagebuf.get_end_iter(),"result: consistent data\n")
                self.message.scroll_mark_onscreen(self.messagebuf.get_insert())
            else:
                print "inconsistent data, dumping buffer"
                print "original data:"
                print self.ori_data
                print "dump data:"
                print self.dump_mem_data
                print "result: error - inconsistent data"
                self.messagebuf.insert(self.messagebuf.get_end_iter(),"result: inconsistent data\n")
                self.message.scroll_mark_onscreen(self.messagebuf.get_insert())

        except:
            if bar:
                bar.close()
            self.Dump_widget.set_sensitive(True)
            self.Upload_widget.set_sensitive(True)
            self.Verify_widget.set_sensitive(True)
            self.Erase_widget.set_sensitive(True)
            self.Version_widget.set_sensitive(True)
            self.Hex_widget.set_sensitive(True)
            self.messagebuf.insert(self.messagebuf.get_end_iter(),"Error!\n")
            self.message.scroll_mark_onscreen(self.messagebuf.get_insert())

    def on_serial_connect_clicked(self,widget):
        if self.connect_port:
            self.Serial_widget = self.wTree.get_widget("Connect")
            if self.Serial_widget.get_label() == 'Connect':
                print 'Serial Connect'

                try:
                    self.ser = serial.Serial(self.connect_port,19200)
                    self.ser.timeout = 5
                    self.ser.open()
                    print self.ser
                    self.messagebuf.insert(self.messagebuf.get_end_iter(),'Connect to '+ self.connect_port + ' success!\n')
                    self.message.scroll_mark_onscreen(self.messagebuf.get_insert())
                    self.Dump_widget = self.wTree.get_widget("Dump")
                    self.Upload_widget = self.wTree.get_widget("Upload")
                    self.Verify_widget = self.wTree.get_widget("Verify")
                    self.Erase_widget = self.wTree.get_widget("Erase")
                    self.Version_widget = self.wTree.get_widget("Version")
                    self.Hex_widget = self.wTree.get_widget("Hex")
                    self.Dump_widget.set_sensitive(True)
                    self.Upload_widget.set_sensitive(True)
                    self.Verify_widget.set_sensitive(True)
                    self.Erase_widget.set_sensitive(True)
                    self.Version_widget.set_sensitive(True)
                    self.Hex_widget.set_sensitive(True)
                    self.Serial_widget.set_label("Stop")
                    #self.ser.close()
                    #self.messagebuf.insert(self.messagebuf.get_end_iter(),'Connection close!\n')
                except serial.SerialException:
                    self.messagebuf.insert(self.messagebuf.get_end_iter(),'Connection error!\n')
                    self.message.scroll_mark_onscreen(self.messagebuf.get_insert())
                    pass
            else:
                if self.ser.isOpen():
                    self.ser.close()
                    print 'Serial Connection is close'
                    self.Dump_widget.set_sensitive(False)
                    self.Upload_widget.set_sensitive(False)
                    self.Verify_widget.set_sensitive(False)
                    self.Erase_widget.set_sensitive(False)
                    self.Version_widget.set_sensitive(False)
                    self.Hex_widget.set_sensitive(False)
                    self.messagebuf.insert(self.messagebuf.get_end_iter(),'Connection is close!\n')
                    self.message.scroll_mark_onscreen(self.messagebuf.get_insert())
                self.Serial_widget.set_label("Connect")


    def on_connect_server_clicked(self,widget):
        print 'connect_server_clicked\n'

        server_html = urllib.urlopen(ECO_SERVER)
        server_content = server_html.read()
        server_html.close()
        print server_content

        #clear webmodel list
        self.webmodel.clear()

        package_path = os.getcwd() + '/package'
        package_list = os.listdir(package_path)
        print package_list
        self.local_list_zip = []
        self.local_list = []
        self.local_list_version = []

        #Get current local package list and put them to list 
        for i in range(len(package_list)):
            reg = re.search('([-a-zA-Z0-9]+)_([-a-zA-Z0-9]+)_([-a-zA-Z0-9]+)_([\d]+).zip',package_list[i])
            if reg:
                print reg.group(3),'list =',reg.group()
                self.local_list_zip.append(reg.group())
                self.local_list.append(reg.group(1) + reg.group(2))
                self.local_list_version.append(reg.group(3))

        self.web_package_zip = []
        self.web_package = ''
        self.web_package_version = ''
        for lines in server_content.splitlines():
            reg = re.search('([-a-zA-Z0-9]+)_([-a-zA-Z0-9]+)_([-a-zA-Z0-9]+)_([\d]+).zip',lines)
            if reg:
                state = ''
                self.web_package_zip.append(reg.group())
                self.web_package = reg.group(1) + reg.group(2)
                self.web_package_version = reg.group(3)
                if self.web_package in self.local_list:
                    i = self.local_list.index(self.web_package)
                    if self.local_list_version[i] == self.web_package_version:
                        state = 'Local package is the latest'
                    else:
                        state = 'Local package is the not latest'
                else:
                    state = 'Package is not in local list'
                insert_web_row(self.webmodel,None,reg.group(0),'Coming soon',state)


        print '\nserver_html_get\n'
        print 'web_package_zip = ',self.web_package_zip

    def on_server_download_clicked(self,widget):
        package_path = os.getcwd() + '/package'
        package_list = os.listdir(package_path)
        print package_list
        print "len(self.webmodel) = ",len(self.webmodel)

        if len(self.webmodel):
            for i in range(len(self.webmodel)):
                if self.webmodel[i][0]:
                    print self.webmodel[i][1]
                    reg = re.search('([-a-zA-Z0-9]+)_([-a-zA-Z0-9]+)_([-a-zA-Z0-9]+)_([\d]+).zip',self.webmodel[i][1])
                    self.web_package = reg.group(1) + reg.group(2)
                    self.web_package_version = reg.group(3)
                    print self.web_package , ' version = ',self.web_package_version
                    if self.web_package in self.local_list:
                        j = self.local_list.index(self.web_package)
                        if self.local_list_version[j] == self.web_package_version:
                            print 'Local package is the latest'

                        else:
                            comfirm = ComfirmDialog(self.gladefile,self.webmodel[i][1])
                            if comfirm.run():
                                print 'Kill the local package and download the latest'
                                print package_path+'/'+self.local_list_zip[j]
                                os.remove(package_path+'/'+self.local_list_zip[j])
                                path = package_path + '/' + self.webmodel[i][1]
                                print 'path = ',path
                                zipfile = open(path,'wb')
                                url_file = urllib.urlopen(ECO_SERVER + '/' + self.webmodel[i][1])
                                url_zip_content = url_file.read()
                                url_file.close()
                                zipfile.write(url_zip_content)
                                zipfile.close()

                    else:
                        comfirm = ComfirmDialog(self.gladefile,self.webmodel[i][1])
                        if comfirm.run():
                            print 'Directly download'
                            path =  package_path + '/' + self.webmodel[i][1]
                            print path
                            zipfile = open(path,'wb')
                            url_file = urllib.urlopen(ECO_SERVER + '/' + self.webmodel[i][1])
                            url_zip_content = url_file.read()
                            url_file.close()
                            zipfile.write(url_zip_content)
                            zipfile.close()

            self.on_connect_server_clicked(widget)



    def on_about_activate(self,widget):
        AboutDlg = AboutDialog(self.gladefile)
        AboutDlg.run()

    
    def on_eeprom_activate(self,widget):
        EEPROMDlg = EEPROMDialog(self.gladefile)
        EEPROMDlg.run()
        
    def on_flash_activate(self,widget):
        FLASHDlg = FLASHDialog(self.gladefile)
        FLASHDlg.run()
        
        

if __name__ == "__main__":
    manager = EcoManager()
    gtk.main()


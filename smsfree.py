#!/usr/bin/env python
# -*- coding: latin-1 -*-

# smsfree.py by Kalasni (31-3-09)

import pygtk
pygtk.require("2.0")
import gtk
import urllib
import urllib2

class SmsFree(object):
    
    def on_mainWindow_destroy(self, widget, data=None):
        gtk.main_quit()
        
    def on_sendButton_clicked(self, widget, data=None):
        self.send()
        
    def on_clearButton_clicked(self, widget, data=None):
        self.clear()
    
    def on_about_menu_item(self, widget, data=None):
        
        authors = [
        "d3hydr8 <d3hydr8@gmail.com>",
        "Adapted to pyGtk by:",
        "Kalasni <kalasni@gmail.com>"
        ]
        
        aboutDlg = gtk.AboutDialog()
        aboutDlg.set_transient_for(self.window) # Shows dialog on mainWindow 
        aboutDlg.set_name("Send Free SMS")
        aboutDlg.set_version("1.0")
        aboutDlg.set_authors(authors)
        aboutDlg.set_logo_icon_name(gtk.STOCK_EDIT)
        aboutDlg.show()
        aboutDlg.connect("response", lambda d,response: d.destroy())


    def send(self):
        
        adr = self.fromEntry.get_text()
        n1 = self.entry1.get_text()
        n2 = self.entry2.get_text()
        n3 = self.entry3.get_text()
        buffer = self.textview.get_buffer()
        start = buffer.get_start_iter()
        end = buffer.get_end_iter()
        
        # get txt in textview from start to end
        txt = buffer.get_text(start, end)
        host = "http://www.txtdrop.com/"
        
        if len(txt) > 120:
            self.textview.get_buffer().set_text(
                "Message Length Over (Max:120 characters)")
        elif len(n1) != 3 or len(n2) != 3 or len(n3) != 4:
            self.textview.get_buffer().set_text("Misformed Number!")
            self.entry1.set_text("")
            self.entry2.set_text("")
            self.entry3.set_text("")
        else:
            login_form_seq = [ 
                ('emailfrom',adr), 
                ('npa',n1), 
                ('exchange',n2), 
                ('number',n3), 
                ('body',txt), 
                ('submitted','1'), 
                ('submit','Send')]
            login_form_data = urllib.urlencode(login_form_seq) 
            opener = urllib2.build_opener()
            try:
                opener.addheaders = [('User-agent', 'Mozilla/5.0')] 
                opener.open(host, login_form_data)
                msj = "From: "+adr+ "\nNumber: "+ n1+n2+n3+ "\nText: "+txt
                self.textview.get_buffer().set_text(msj+"\nMessage sent!")
            except(urllib2.URLError):
                self.textview.get_buffer().set_text("\nMessage failed! ")
                
    
    def clear(self):
        self.fromEntry.set_text("")
        self.entry1.set_text("")
        self.entry2.set_text("")
        self.entry3.set_text("")
        self.textview.get_buffer().set_text("")

   
    def __init__(self):

        builder = gtk.Builder()
        builder.add_from_file("smsfree.xml")
        self.window = builder.get_object("mainWindow")
        
        #variables
        self.fromEntry = builder.get_object("fromEntry")
        self.entry1 = builder.get_object("entry1")
        self.entry2 = builder.get_object("entry2")
        self.entry3 = builder.get_object("entry3")
        self.textview = builder.get_object("textview")
        builder.connect_signals(self)
        
        
    def main(self):
        self.window.show()
        gtk.main()
        
        
if __name__ == "__main__":
	app = SmsFree()
	app.main()

    


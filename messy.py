# Copyright (C) 2012 Sibi <sibi@psibi.in>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
# Created:  Feb 25, 2012
# Author:   Sibi <sibi@psibi.in>

#!/usr/bin/python
import gtk
import pygtk
from client import sms_client
class messy:
    def __init__(self):
        gladefile="messy.xml"
        builder=gtk.Builder()
        self.sms = sms_client()
        builder.add_from_file(gladefile)
        self.window=builder.get_object("main_window")
        self.send_window=builder.get_object("send_window")
        self.mobno=builder.get_object("mobno_send")
        self.message=builder.get_object("message")
        self.username=builder.get_object("username")
        self.password=builder.get_object("password")
        self.msgtext=builder.get_object("msg")
        self.char_entry=builder.get_object("char_entry")
        self.counter=0
        self.counts=48
        builder.connect_signals(self)
        
    def on_main_window_destroy(self, widget, data=None):
        gtk.main_quit()

    def on_login_button_clicked(self,widget,data=None):
        user=self.username.get_text()
        pword=self.password.get_text()
        perror=self.sms.authenticate_site(user,pword)
        valid = self.login_validate()
        if valid is False:
            dlg=gtk.MessageDialog(self.window,gtk.DIALOG_DESTROY_WITH_PARENT,gtk.MESSAGE_ERROR,gtk.BUTTONS_OK,"Data Incorrect")
            dlg.run()
            dlg.destroy()
            return False
        if perror is False:
            dlg=gtk.MessageDialog(self.window,gtk.DIALOG_DESTROY_WITH_PARENT,gtk.MESSAGE_ERROR,gtk.BUTTONS_OK,"Password Error")
            dlg.run()
            dlg.destroy()
            return False
        self.window.hide()
        self.send_window.show()

    def on_msg_changed(self,widget,data=None):
        total_length = 140
        startiter, enditer = self.msgtext.get_bounds()
        text = self.msgtext.get_text(startiter,enditer,False)
        remaining_length = total_length - len(text)
        if remaining_length >= 0:
            self.char_entry.set_text(str(remaining_length))
        else:
            text = text[0:139]
            self.char_entry.set_text(str(0))
            self.msgtext.set_text(text)            

    def on_send_button_clicked(self,widget,data=None):
        if self.sendsms_validate() is False:
            dlg=gtk.MessageDialog(self.window,gtk.DIALOG_DESTROY_WITH_PARENT,gtk.MESSAGE_ERROR,gtk.BUTTONS_OK,"Data Incorrect")
            dlg.run()
            dlg.destroy()
            return False
        if self.counter!=0:
            user=self.username.get_text()
            pword=self.password.get_text()
            self.sms.authenticate_site(user,pword)
        self.counter = self.counter + 1
        mobno = self.mobno.get_text()
        startiter, enditer = self.msgtext.get_bounds()
        text=self.msgtext.get_text(startiter,enditer,False)
        self.sms.send_sms(mobno,text)
        self.sms.logout()
        dlg=gtk.MessageDialog(self.window,gtk.DIALOG_DESTROY_WITH_PARENT,gtk.MESSAGE_INFO,gtk.BUTTONS_OK,"Message Sent!")
        dlg.run()
        dlg.destroy()

    def login_validate(self):
        if self.username.get_text_length()!=10:
            return False
        elif self.password.get_text_length()==0:
            return False
        else:
            return True

    def sendsms_validate(self):
        if self.mobno.get_text_length()!=10:
            return False
        else:
            return True

    def on_send_window_destroy(self,widget,data=None):
        gtk.main_quit()

if __name__=="__main__":
    window=messy()
    gtk.main()

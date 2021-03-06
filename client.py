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
import mechanize
import cookielib

br=mechanize.Browser()

class sms_client:
    """Basic class accessingg features of 160by2.com"""
    def __init__(self):
        cj = cookielib.LWPCookieJar()
        br.set_cookiejar(cj)
        br.set_handle_equiv(True)
        br.set_handle_gzip(True)
        br.set_handle_redirect(True)
        br.set_handle_referer(True)
        br.set_handle_robots(False)
        br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        
    def authenticate_site(self,user,pword):
        br.open("http://www.160by2.com")
        br.select_form(nr=0)
        br.form['username']=user
        br.form['password']=pword
        br.submit()
        s = br.geturl()
        #Check for Valid password here
        if s.find('Login') != -1:
            return False #returns false on password error
        link = s.split("?")
        self.id = link[1]
        return True
     
    def open_sendpage(self):
        action="SendSMS"
        s = self.get_weburl(action)
        br.open(s)
        br.select_form(nr=0)

    def send_sms(self,mobile_no,msg):
        self.open_sendpage()
        action="SendSMSAction"
        s = self.get_weburl(action)
        br.form['mobile1']=mobile_no
        br.form['msg1']=msg
        br.form.action = s
        try:
            br.submit()
        except Exception:
            pass #ignore the response exception

    def logout(self):
        self.open_sendpage()
        action="Logout"
        s = self.get_weburl(action)
        br.form.action = s
        br.submit()
   
    def get_weburl(self,action):
        weburl = "http://www.160by2.com/" + action + ".action?" + self.id
        return weburl
 
if __name__=="__main__":
    pass
    #client = sms_client()
    #client.authenticate_site('7200120343','xxx')
    #client.send_sms('948xxx94',"Hello World)
    #client.logout()

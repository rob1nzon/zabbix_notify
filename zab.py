from PyQt4.QtGui import *
from PyQt4.QtCore import *
import twill
import os
from twill.commands import *
from HTMLParser import HTMLParser
import sys, dbus
import thread,time
global tlist
knotify = dbus.SessionBus().get_object("org.kde.knotify", "/Notify")

# icons :3


# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    def handle_data(self, data):
       #print data
       self.output.append(data)
    def feed(self, data):
        self.output = []
        HTMLParser.feed(self, data)
# instantiate the parser and fed it some HTML
def ChkUpd(tlist):
	while 1:
		tlistnew=[]
		ParsPages(tlistnew)
		#import pdb; pdb.set_trace()
		u=1;
		for x in tlistnew:
			for y in tlist:
				if (x==y):
					u=0
					break
			if (u==1):
				print x
				if (x.count('/video')==0):
					knotify.event("warning", "kde", [], 'Zabbix', x, [], [], 0, 0,dbus_interface="org.kde.KNotify")
			if (u==0):
				break		
		tlist=tlistnew
		time.sleep(10)

def ParsPages(llist):
	pages =['1','2']
	for i in pages:
		go("tr_status.php?ddreset=1&sid=3a062a1cfae47a78&sort=lastchange&sortorder=DESC&page="+i)
		h=show()
		p.feed(h)
		AckPrint(p,llist)
def AckPrint(p,f):
	s=0
	n=0
	for x in p.output:
		if (x=='Acknowledged'): 
			s=1 # start parsing
		if (s==1):
			if (x=='Disaster') or (x=='Average') or (x=='High'): 
				n=1
				sl=''
		if (n==8):
			sl+=x+' '
			n=0
			#knotify.event("warning", "kde", [], 'title', sl, [], [], 0, 0,dbus_interface="org.kde.KNotify")
			f.append(sl)
			#print sl
		if (n==7):
			sl+=x+' '
			n=8
		if (n==6):
			#sl+=x+' '
			n=7
		if (n==5):
			#sl+=x+' '
			n=6
		if (n==4):
			#sl+=x+' '
			n=5
		if (n==3):
			sl+=x+' '
			n=4
		if (n==2):
			sl+=x+' '
			n=3
			if (x=='OK'):
				sl=''
				n=0
		if (n==1):
			sl+=x+' '
			n=2;
p = MyHTMLParser()
f = open(os.devnull,"w") # log off
twill.set_output(f) 
go('http://zabbixext')
fv("1", "name", "dchencov")
fv("1", "password", "qwerty")
submit('5')
tlist=[]
ParsPages(tlist)
#t = threading.Timer(60.0, ChkUpd(tlist))
#t.start() 
thread.start_new_thread(ChkUpd(tlist),())
#ChkUpd(tlist)


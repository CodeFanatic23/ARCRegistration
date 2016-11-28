#!/usr/bin/env python
import subprocess
import socket
import os
def startServer(port):
	f = os.popen('ifconfig eth0 | grep "inet\ addr" | cut -d: -f2 | cut -d" " -f1')
	a=(f.read()).strip()
	p = subprocess.Popen("cd bin; source activate; cd ..;cd arcreg; python manage.py runserver %s:%s --insecure;"%(a,port),shell=True,executable="/bin/bash")
	p.communicate()

def check(port):
	if port != '':
		port = int(port)
		if port > 1000 and port < 10000:
			return False
		else:
			return True
	else:
		startServer(8000)
		return False
try:
	flag = True
	b=0
	while(flag):
		b = raw_input("Enter the port to use for server.Leave blank to use default '8000':\n")
		flag = check(b)
		if flag == True:
			print("Value must be between 1001 and 9999\n")
	startServer(b)	
except Exception as e:
	print(e)
	quit()
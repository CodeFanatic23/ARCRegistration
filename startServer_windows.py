#!/usr/bin/env python
import subprocess
import socket
def startServer(port):
	a = socket.gethostbyname(socket.gethostname())
	p = subprocess.Popen("cd arc_registration& cd Scripts& activate.bat& cd ../arcreg& python manage.py runserver %s:%d --insecure&"%(a,port),shell=True)
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
		b = input("Enter the port to use for server.Leave blank to use default '8000':\n")
		flag = check(b)
		if flag == True:
			print("Value must be between 1001 and 9999\n")
	startServer(int(b))	
	
except Exception as e:
	print(e)
	quit()


#!/usr/bin/env python
import subprocess
import socket
import os
def install():

	p = subprocess.check_call("virtualenv arc_registration& ls& mv arcreg arc_registration& cd arc_registration& cd Scripts& ls& activate.bat& cd ..& cd arcreg& python -m pip install -r requirements.txt& cd ../..& cp -r registration arc_registration/Lib/site-packages&",shell=True)
	
	# p = subprocess.check_call("cd arc_registration& cd arcreg& ls&",shell=True)

	# files = [f for f in os.listdir(os.path.join(os.curdir,'arc_registration','arcreg'))]# if os.path.isfile(f)]
	# print(files)
	# start=''
	# for f in files:
	# 	print(f)
	# 	if f != 'db.sqlite3':
	# 		print("no migrations")
	# 		start = True
	# 		break
	# 	else:
	# 		print("new setup")
	# 		start = False
	# 		break
	# if start == True:
	# 	subprocess.check_call('cd arc_registration& cd arcreg& ls& python startServer_windows.py&',shell=True)
	# else:
	# 	subprocess.check_call('cd arc_registration& cd arcreg& ls& python manage.py makemigrations& python manage.py migrate& python startServer_windows.py&',shell=True)


install()
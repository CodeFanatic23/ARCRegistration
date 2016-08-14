import os,shutil,re
from django.conf import settings

class Clean_folder():
	"Used to remove previous xls sheet from xls_sheet folder when new xls_sheet entered in next sem"
	

	def remove_files(self,location):
		os.remove(location)
		print("deleting:" + location)

	def move(self,old,new):
		shutil.move(old,new)

	def remove_dir(self,location):
		os.rmdir(location)
		print("deleting:" + location)

	def clean(self,request, obj, form):
		path_xls_sheet = os.path.join(os.path.dirname(settings.BASE_DIR),"media","xls_sheets")
		

		#cleaning the folders
		path, dirs, files = next(os.walk(os.path.join(path_xls_sheet,"Capacity")))
		for f in files:	
			self.remove_files(os.path.join(path_xls_sheet,"Capacity",f))
		#path, dirs, files = next(os.walk(os.path.join(path_xls_sheet,"Elective_list")))
		# for f in files:	
		# 	self.remove_files(os.path.join(path_xls_sheet,"Elective_list",f))
		path, dirs, files = next(os.walk(os.path.join(path_xls_sheet,"FD_Priority_number")))
		for f in files:	
			self.remove_files(os.path.join(path_xls_sheet,"FD_Priority_number",f))
		path, dirs, files = next(os.walk(os.path.join(path_xls_sheet,"HD_Priority_number")))
		for f in files:	
			self.remove_files(os.path.join(path_xls_sheet,"HD_Priority_number",f))
		path, dirs, files = next(os.walk(os.path.join(path_xls_sheet,"Pre_requisite_senate")))
		for f in files:	
			self.remove_files(os.path.join(path_xls_sheet,"Pre_requisite_senate",f))
		path, dirs, files = next(os.walk(os.path.join(path_xls_sheet,"Time_Table_Semester_Wise")))
		for f in files:	
			self.remove_files(os.path.join(path_xls_sheet,"Time_Table_Semester_Wise",f))
		path, dirs, files = next(os.walk(os.path.join(path_xls_sheet,"Registration_data")))
		for f in files:	
			self.remove_files(os.path.join(path_xls_sheet,"Registration_data",f))
		


		# # print path_xls_sheet
		# # xls_sheet_name = []
		
		# # xls_sheet_name.append(request.FILES['Capacity'].name)
		# # xls_sheet_name.append(request.FILES['Elective_list'].name)
		# # xls_sheet_name.append(request.FILES['FD_Priority_number'].name)
		# # xls_sheet_name.append(request.FILES['HD_Priority_number'].name)
		# # xls_sheet_name.append(request.FILES['Pre_requisite_senate'].name)
		# # xls_sheet_name.append(request.FILES['Time_Table_Semester_Wise'].name)
		
		
		# path, dirs, files = next(os.walk(path_xls_sheet))
		# for f in files:	
		# 	self.remove_files(os.path.join(path_xls_sheet,f))

		#in linux space is replaced by _ , but in database the name of file contains spaces
		#so we use re.sub(" ", "_", line) 
		
		Capacity = str(re.sub(" ","_",request.FILES['Capacity'].name))
		#Elective_list = str(re.sub(" ","_",request.FILES['Elective_list'].name))
		FD_Priority_number = str(re.sub(" ","_",request.FILES['FD_Priority_number'].name))
		HD_Priority_number = str(re.sub(" ","_",request.FILES['HD_Priority_number'].name))
		Pre_requisite_senate = str(re.sub(" ","_",request.FILES['Pre_requisite_senate'].name))
		Time_Table_Semester_Wise = str(re.sub(" ","_",request.FILES['Time_Table_Semester_Wise'].name))
		Registration_data = str(re.sub(" ","_",request.FILES['Registration_data'].name))
		Registration_data =  str(re.sub("\)","",str(re.sub("\(","",Registration_data))))

		self.move(os.path.join(path_xls_sheet,"Capacity","temporary",Capacity),os.path.join(path_xls_sheet,"Capacity",Capacity))
		#self.move(os.path.join(path_xls_sheet,"Elective_list","temporary",Elective_list),os.path.join(path_xls_sheet,"Elective_list",Elective_list))
		self.move(os.path.join(path_xls_sheet,"FD_Priority_number","temporary",FD_Priority_number),os.path.join(path_xls_sheet,"FD_Priority_number",FD_Priority_number))
		self.move(os.path.join(path_xls_sheet,"HD_Priority_number","temporary",HD_Priority_number),os.path.join(path_xls_sheet,"HD_Priority_number",HD_Priority_number))
		self.move(os.path.join(path_xls_sheet,"Pre_requisite_senate","temporary",Pre_requisite_senate),os.path.join(path_xls_sheet,"Pre_requisite_senate",Pre_requisite_senate))
		self.move(os.path.join(path_xls_sheet,"Time_Table_Semester_Wise","temporary",Time_Table_Semester_Wise),os.path.join(path_xls_sheet,"Time_Table_Semester_Wise",Time_Table_Semester_Wise))
		self.move(os.path.join(path_xls_sheet,"Registration_data","temporary",Registration_data),os.path.join(path_xls_sheet,"Registration_data",Registration_data))

		
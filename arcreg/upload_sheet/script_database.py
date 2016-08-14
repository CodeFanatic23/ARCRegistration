from django.conf import settings
import xlrd
import os,re
from .models import *
from django.db import connection
from datetime import time,date

class Create_database():
	"create database from the given xls sheet"
	PATH_XLS_SHEET = os.path.join(os.path.dirname(settings.BASE_DIR),"media","xls_sheets")
	
	def create_Pre_requisite_senate_database(self,request):
		Pre_requisite_senate_name = str(re.sub(" ","_",request.FILES['Pre_requisite_senate'].name))
		
		#deleting all enteries in database
		Pre_requisite_senate.objects.all().delete()

		Pre_requisite_senate_path = os.path.join(self.PATH_XLS_SHEET,"Pre_requisite_senate")
		book = xlrd.open_workbook(os.path.join(Pre_requisite_senate_path,Pre_requisite_senate_name),logfile=open(os.devnull, 'w'))
		first_sheet = book.sheet_by_index(0)

		i=3
		while(True):
			try:
				cells = first_sheet.row_slice(rowx=i,start_colx=0,end_colx=26)
			except IndexError:
				break	
			prereq = Pre_requisite_senate(Cata_log = cells[2].value.replace(" ", ""),
											preq1 =cells[6].value.replace(" ", ""),
											condition1 = cells[9].value.replace(" ", ""),
											preq2 = cells[12].value.replace(" ", ""),
											condition2 = cells[15].value.replace(" ", ""),
											preq3 = cells[18].value.replace(" ", ""),
											condition3 = cells[22].value.replace(" ", ""),
											preq4 = cells[25].value.replace(" ", "")
											)
			prereq.save()
			i+=1	
			

	def create_capacity_database(self,request):
		#name of xls files
		#TODO: remove first row from capacity.xls and than change the code

		Capacity_name = str(re.sub(" ","_",request.FILES['Capacity'].name))
		
		#deleting all enteries in database
		Capacity.objects.all().delete()

		capacity_sheet_path = os.path.join(self.PATH_XLS_SHEET,"Capacity")
		book = xlrd.open_workbook(os.path.join(capacity_sheet_path,Capacity_name),logfile=open(os.devnull, 'w'))
		first_sheet = book.sheet_by_index(0)
		no_rows = int(first_sheet.cell(0,1).value)


		for i in range(2,no_rows+2):
			cells = first_sheet.row_slice(rowx=i,start_colx=0,end_colx=10)
			capacity = Capacity(Course_id= str(cells[0].value).strip(),
				Subject=str(cells[1].value).strip(),
				catalog_course_no=str(cells[2].value).strip(),
				descr=str(cells[3].value).strip(),
				Section=str(cells[4].value).strip(),
				Cap_enrl=int(cells[5].value ),
				Tot_enrl=int(cells[6].value),
				class_nbr= int(cells[8].value))

			Course_id = models.IntegerField(null=False)
			Subject = models.CharField(max_length=10,null=False)
			catalog_course_no = models.CharField(max_length=7,null=False)
			descr = models.CharField(max_length=70,null=False)
			Section = models.CharField(max_length=5,null=False)
			Cap_enrl = models.IntegerField(null=False)
			Tot_enrl = models.IntegerField(null=False)
			#Component = models.CharField(max_length=7,null=False)	
			class_nbr = models.IntegerField(null=False)
			#enrl_stat = models.CharField(max_length=5,null=False)

			capacity.save()

	def create_FD_priority_number(self,request):
		#name of xls files
		FD_Priority_number_name = str(re.sub(" ","_",request.FILES['FD_Priority_number'].name))
		
		#deleting all enteries in database
		FD_priority_number.objects.all().delete()

		FD_Priority_number_sheet_path = os.path.join(self.PATH_XLS_SHEET,"FD_Priority_number")

		book = xlrd.open_workbook(os.path.join(FD_Priority_number_sheet_path,FD_Priority_number_name),logfile=open(os.devnull, 'w'))
		first_sheet = book.sheet_by_index(0)

		i=1
		while(True):
			try:
				cells = first_sheet.row_slice(rowx=i,start_colx=0,end_colx=10)
			except IndexError:
				break	
			FD_P = FD_priority_number(erp_id= int(cells[0].value),
				campus_id=str(cells[1].value).strip(),
				name=str(cells[2].value).strip(),
				# strm=int(cells[3].value ),
				priority_number=int(cells[4].value ))
			FD_P.save()
			i+=1
	
	def create_HD_priority_number(self,request):
		#name of xls files
		HD_Priority_number_name = str(re.sub(" ","_",request.FILES['HD_Priority_number'].name))
		
		#deleting all enteries in database
		HD_priority_number.objects.all().delete()

		HD_Priority_number_sheet_path = os.path.join(self.PATH_XLS_SHEET,"HD_Priority_number")

		book = xlrd.open_workbook(os.path.join(HD_Priority_number_sheet_path,HD_Priority_number_name),logfile=open(os.devnull, 'w'))
		first_sheet = book.sheet_by_index(0)

		i=1
		while(True):
			try:
				cells = first_sheet.row_slice(rowx=i,start_colx=0,end_colx=10)
			except IndexError:
				break	
			HD_P = HD_priority_number(erp_id= int(cells[0].value),
				campus_id=str(cells[1].value).strip(),
				name=str(cells[2].value).strip(),
				#strm=int(cells[3].value ),
				priority_number=int(cells[4].value ))
			HD_P.save()
			i+=1
	
	def create_Time_Table_Semester_Wise(self,request):
		#name of xls files
		Time_Table_Semester_Wise_name = str(re.sub(" ","_",request.FILES['Time_Table_Semester_Wise'].name))
		
		#deleting all enteries in database
		Time_Table_Semester_Wise.objects.all().delete()
		Time_Table_Semester_Wise_path = os.path.join(self.PATH_XLS_SHEET,"Time_Table_Semester_Wise")
		
		book = xlrd.open_workbook(os.path.join(Time_Table_Semester_Wise_path,Time_Table_Semester_Wise_name),logfile=open(os.devnull, 'w'))
		first_sheet = book.sheet_by_index(0)

		#TODO: remove first row from time_table_semester_wise and than change the code
		i = 2	
		while(True):
			try:
				cells = first_sheet.row_slice(rowx=i,start_colx=0,end_colx=16)
			except IndexError:
				break
			try:
				print (cells[8].value)
				t = xlrd.xldate_as_tuple(cells[8].value, book.datemode)
				index_8 = time(*t[3:])
			except ValueError:
				l = (1111, 1, 1, 0, 0, 0)
				t1 = time(*l[3:])
				index_8 = t1
			except TypeError :
				l = (1111, 1, 1, 0, 0, 0)
				t1 = time(*l[3:])
				index_8 = t1
			try:
				t = xlrd.xldate_as_tuple(cells[9].value,  book.datemode)
				index_9 =  time(*t[3:])
			except ValueError:
				l = (1111, 1, 1, 0, 0, 0)
				#print l
				t1 = time(*l[3:])
				index_9 = t1
			except TypeError:
				l = (1111, 1, 1, 0, 0, 0)
				#print l
				t1 = time(*l[3:])
				index_9 = t1

			Ttsw = Time_Table_Semester_Wise(Course_id = int(cells[0].value),
				Subject = str(cells[1].value).strip(),
				catalog_course_no = str(cells[2].value).strip(),
				course_title = str(cells[3].value).strip(),
				class_nbr = int(cells[4].value),
				Section = str(cells[5].value).strip(),
				room = str(cells[6].value).strip(),
				class_pattern = str(cells[7].value).strip(),
				mtg_start_time = index_8,	
				end_time = index_9,
				#idc =  str(cells[10].value).strip(),
				display_name =  str(cells[11].value).strip(),
				)
			Ttsw.save()
			i=i+1

	def create_Elective_list(self,request):
		Elective_list_name = str(re.sub(" ","_",request.FILES['Elective_list'].name))
		
		
		#deleting all enteries in database
		Elective_list.objects.all().delete()

		Elective_list_sheet_path = os.path.join(self.PATH_XLS_SHEET,"Elective_list")

		book = xlrd.open_workbook(os.path.join(Elective_list_sheet_path,Elective_list_name),logfile=open(os.devnull, 'w'))
		first_sheet = book.sheet_by_index(0)

		i=1
		while(True):
			
			try:
				cells = first_sheet.row_slice(rowx=i,start_colx=0,end_colx=10)
			except IndexError:
				break	
			index_0 = cells[0].value.replace(" ","")
			index_1 = cells[1].value.replace(" ", "")
			index_2 = cells[2].value.replace(" ", "")
			index_3 = cells[3].value.replace(" ", "")
			try:
				t = xlrd.xldate_as_tuple(cells[4].value, book.datemode)
				index_4 = time(*t[3:])
			except ValueError:
				l = (1111, 1, 1, 0, 0, 0)
				t1 = time(*l[3:])
				index_4 = t1
			try:
				t = xlrd.xldate_as_tuple(cells[5].value, book.datemode)
				index_5 = time(*t[3:])
				
			except ValueError:
				l = (1111, 1, 1, 0, 0, 0)
				t1 = time(*l[3:])
				index_5 = t1

			Elective_list_object = Elective_list(Campus_ID = index_0,
					Catalog = index_1,
					Course_Title = 	index_2,
					Class_Pattern = index_3,
					Mtg_Start = index_4,
					End_time = index_5
				)
			Elective_list_object.save()

			i+=1

	def create_Registration_data(self,request):
		Registration_data_name = str(re.sub(" ","_",request.FILES['Registration_data'].name))
		Registration_data_name = str(re.sub("\)","",str(re.sub("\(","",Registration_data_name))))

		
		#deleting all enteries in database
		Registration_data.objects.all().delete()

		Registration_data_sheet_path = os.path.join(self.PATH_XLS_SHEET,"Registration_data")

		book = xlrd.open_workbook(os.path.join(Registration_data_sheet_path,Registration_data_name),logfile=open(os.devnull, 'w'))
		first_sheet = book.sheet_by_index(0)

		i=1
		while(True):
			try:
				cells = first_sheet.row_slice(rowx=i,start_colx=0,end_colx=16)
			except IndexError:
				break
			if cells[7].value == '' or cells[7].value == None:
				cells[7].value = -99
			Registration_data_P = Registration_data(
				Campus_ID = cells[2].value.replace(" ", ""),
				erp_ID = int(cells[3].value),
				Name = cells[4].value,
				Subject = cells[5].value.replace(" ", ""),
				Catalog = cells[6].value.replace(" ", ""),
				Course_ID =   int(cells[7].value),
				Lecture_Section_No = cells[8].value.replace(" ",""),
				Practical_Section_No = cells[9].value.replace(" ", ""),
				Tutorial_Section_No = cells[10].value.replace(" ", ""),
				Project_Section_No = cells[11].value.replace(" ", ""),
				Thesis_section = cells[12].value.replace(" ",""),
				Graded_Component = cells[13].value.replace(" ", ""),
				Grade_In = cells[14].value.replace(" ", "")
				)
			Registration_data_P.save()
			i+=1
	

	def start_script(self,request):
		self.create_capacity_database(request)
		self.create_FD_priority_number(request)
		self.create_HD_priority_number(request)
		self.create_Time_Table_Semester_Wise(request)
		self.create_Pre_requisite_senate_database(request)
		# self.create_Elective_list(request)
		self.create_Registration_data(request)
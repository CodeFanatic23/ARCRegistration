from django.db import models
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible
import os
# Create your models here.
class Upload_file(models.Model):
	# Capacity = models.FileField(upload_to='xls_sheets/Capacity/temporary', blank=True, null=False,default=os.path.join(settings.MEDIA_ROOT,'xls_sheets','Capacity','capacity.xls'))
	# #Elective_list = models.FileField(upload_to='xls_sheets/Elective_list/temporary', blank=True, null=False,default=os.path.join(settings.MEDIA_ROOT,'xls_sheets','','capacity.xls'))
	# FD_Priority_number = models.FileField(upload_to='xls_sheets/FD_Priority_number/temporary', blank=True, null=False,default=os.path.join(settings.MEDIA_ROOT,'xls_sheets','FD_Priority_Number','FD_Priority_Number.xls'))
	# HD_Priority_number = models.FileField(upload_to='xls_sheets/HD_Priority_number/temporary', blank=True, null=False,default=os.path.join(settings.MEDIA_ROOT,'xls_sheets','HD_Priority_number','HD_Priority_number.xls'))
	# #Pre_requisite_senate = models.FileField(upload_to='xls_sheets/Pre_requisite_senate/temporary', blank=True, null=False,default=os.path.join(settings.MEDIA_ROOT,'xls_sheets','Pre_requisite_senate','capacity.xls'))
	# Time_Table_Semester_Wise = models.FileField(upload_to='xls_sheets/Time_Table_Semester_Wise/temporary', blank=True, null=False,default=os.path.join(settings.MEDIA_ROOT,'xls_sheets','Time_Table_Semester_Wise','Time_Table_Semester_Wise.xls'))
	# Registration_data = models.FileField(upload_to='xls_sheets/Registration_data/temporary', blank=True, null=False,default=os.path.join(settings.MEDIA_ROOT,'xls_sheets','Registration_data','Registration_data.xls'))
	# nikhil_data = models.FileField(upload_to='xls_sheets/nikhil_data/temporary', blank=False, null=False)
	# Capacity = models.FileField(upload_to='xls_sheets/Capacity/temporary', blank=True, null=False,default=os.path.join(settings.MEDIA_ROOT,'capacity.xls'))
	# #Elective_list = models.FileField(upload_to='xls_sheets/Elective_list/temporary', blank=True, null=False,default=os.path.join(settings.MEDIA_ROOT,'xls_sheets','','capacity.xls'))
	# FD_Priority_number = models.FileField(upload_to='xls_sheets/FD_Priority_number/temporary', blank=True, null=False,default=os.path.join(settings.MEDIA_ROOT,'FD_Priority_Number.xls'))
	# HD_Priority_number = models.FileField(upload_to='xls_sheets/HD_Priority_number/temporary', blank=True, null=False,default=os.path.join(settings.MEDIA_ROOT,'HD_Priority_number.xls'))
	# #Pre_requisite_senate = models.FileField(upload_to='xls_sheets/Pre_requisite_senate/temporary', blank=True, null=False,default=os.path.join(settings.MEDIA_ROOT,'xls_sheets','Pre_requisite_senate','capacity.xls'))
	# Time_Table_Semester_Wise = models.FileField(upload_to='xls_sheets/Time_Table_Semester_Wise/temporary', blank=True, null=False,default=os.path.join(settings.MEDIA_ROOT,'Time_Table_Semester_Wise.xls'))
	# Registration_data = models.FileField(upload_to='xls_sheets/Registration_data/temporary', blank=True, null=False,default=os.path.join(settings.MEDIA_ROOT,'Registration_data.xls'))
	Parse_data = models.BooleanField(default=True,null=False,blank=True,help_text="Please add files to media folder to parse data")
	added_on = models.DateTimeField(blank=True,auto_now_add=True)

class Capacity(models.Model):
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

class FD_priority_number(models.Model):
	erp_id = models.BigIntegerField(blank=True,null=True)
	campus_id = models.CharField(max_length=14,null=False)
	name = models.CharField(max_length=70,null=False)
	#strm = models.IntegerField(null=False)
	priority_number = models.IntegerField(null=True)

class HD_priority_number(models.Model):
	erp_id = models.BigIntegerField(blank=True,null=True)
	campus_id = models.CharField(max_length=14,null=False)
	name = models.CharField(max_length=70,null=False)
	#strm = models.IntegerField(null=False)
	priority_number = models.IntegerField(null=True)

@python_2_unicode_compatible
class Time_Table_Semester_Wise(models.Model):
	Course_id = models.IntegerField(null=True,blank=True)
	Subject = models.CharField(max_length=7,null=True,blank=True)
	catalog_course_no = models.CharField(max_length=7,null=True,blank=True)
	course_title = models.CharField(max_length=50,null=True,blank=True)
	class_nbr = models.IntegerField(null=True,blank=True)
	Section = models.CharField(max_length=5,null=True,blank=True)
	room = models.CharField(max_length=6,null=True,blank=True)
	class_pattern = models.CharField(max_length=6,null=True,blank=True)
	mtg_start_time = models.TimeField(null=True,blank=True)
	end_time = models.TimeField(null=True,blank=True)
	#idc = models.CharField(max_length=12,null=True,blank=True)
	display_name = models.CharField(max_length=70,null=True,blank=True)
	#role = models.CharField(max_length=5,null=True,blank=True)
	#exam_tm_cond = models.CharField(max_length=10,null=True,blank=True)
	#exam_date = models.DateTimeField(input_formats="%Y-%m-%dT-%H-%M-%S")
	#exam_date = models.DateField(null=True,blank=True)
	#course_admin = models.CharField(max_length=8,null=True,blank=True)
	# class Meta:
	# 	ordering = ['class_nbr']
	def __str__(self):
		return self.course_title + '-' + str(self.class_nbr)


class Pre_requisite_senate(models.Model):
	Cata_log = models.CharField(max_length=7,null=True,blank=True)
	preq1 = models.CharField(max_length=7,null=True,blank=True)
	condition1 = models.CharField(max_length=5,null=True,blank=True)
	preq2 = models.CharField(max_length=7,null=True,blank=True)
	condition2 = models.CharField(max_length=5,null=True,blank=True)
	preq3 = models.CharField(max_length=7,null=True,blank=True)
	condition3 = models.CharField(max_length=5,null=True,blank=True)
	preq4 = models.CharField(max_length=7,null=True,blank=True)

class Elective_list(models.Model):
	Campus_ID = models.CharField(max_length=13,null=True,blank=True)
	Catalog = models.CharField(max_length=6,null=True,blank=True)
	Course_Title = 	models.CharField(max_length=100,null=True,blank=True)
	Class_Pattern = models.CharField(max_length=6,null=True,blank=True)
	Mtg_Start = models.TimeField(null=True,blank=True)
	End_time = models.TimeField(null=True,blank=True)

class Registration_data(models.Model):
	Campus_ID = models.CharField(max_length=13,null=True,blank=True)
	erp_ID = models.BigIntegerField(null=True,blank=True)
	Name = models.CharField(max_length=70,null=True,blank=True)
	Subject =  models.CharField(max_length=13,null=True,blank=True)
	Catalog = models.CharField(max_length=13,null=True,blank=True)
	Course_ID =  models.IntegerField(null=True,blank=True)
	Lecture_Section_No = models.CharField(max_length=5,null=True,blank=True)
	Practical_Section_No = models.CharField(max_length=5,null=True,blank=True)
	Tutorial_Section_No = models.CharField(max_length=5,null=True,blank=True)
	Project_Section_No = models.CharField(max_length=5,null=True,blank=True)
	Thesis_section = models.CharField(max_length=5,null=True,blank=True)
	Graded_Component = models.CharField(max_length=5,null=True,blank=True)
	Grade_In = models.CharField(max_length=5,null=True,blank=True)

# class nikhil(models.Model):
# 	one = models.IntegerField(null=True,blank=True)
# 	two = models.IntegerField(null=True,blank=True)
# 	three = models.IntegerField(null=True,blank=True)
# 	four = models.IntegerField(null=True,blank=True)
# 	five = models.IntegerField(null=True,blank=True)
# 	six = models.IntegerField(null=True,blank=True)
# 	seven = models.IntegerField(null=True,blank=True)

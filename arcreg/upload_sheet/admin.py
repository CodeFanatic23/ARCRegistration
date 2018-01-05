from django.contrib import admin
from .models import *
from .clean_xls_sheet_folder import Clean_folder
from .forms import UploadSheetForm
from .script_database import Create_database
from django.http import HttpResponse
from django.shortcuts import render


# Register your models here.
class UploadSheetAdmin(admin.ModelAdmin):
	# list_display = ['Capacity', 'FD_Priority_number', 'HD_Priority_number', 'Time_Table_Semester_Wise','Registration_data',]
	# # list_editable = ["event_name"]
	# form = UploadSheetForm
	list_display = ['added_on']


	
	def save_model(self, request, obj, form, change=False):
		obj.save()
		# Clean = Clean_folder()
		# Clean.clean(request,obj,form)
		# try:
		create_database = Create_database()
		create_database.start_script(request)
		# except Exception as e:
		# 	response = HttpResponse("Here's the text of the Web page.")
		# 	print e
		# 	return render(request,"about.html")
		
class TimeTableAdmin(admin.ModelAdmin):
	list_display = ['course_title','Course_id','class_nbr']
	search_fields = ['Course_id','course_title','class_nbr','Section']
	
	
	model = Time_Table_Semester_Wise

	
admin.site.register(Time_Table_Semester_Wise,TimeTableAdmin)


admin.site.register(Upload_file, UploadSheetAdmin)

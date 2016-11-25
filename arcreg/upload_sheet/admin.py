from django.contrib import admin
from .models import *
from .clean_xls_sheet_folder import Clean_folder
from .forms import UploadSheetForm
from .script_database import Create_database
from django.http import HttpResponse
from django.shortcuts import render


# Register your models here.
class UploadSheetAdmin(admin.ModelAdmin):
	list_display = ['Capacity', 'FD_Priority_number', 'HD_Priority_number', 'Pre_requisite_senate', 'Time_Table_Semester_Wise','Registration_data',]
	# list_editable = ["event_name"]
	form = UploadSheetForm


	
	def save_model(self, request, obj, form, change=False):
		obj.save()
		Clean = Clean_folder()
		Clean.clean(request,obj,form)
		# try:
		create_database = Create_database()
		create_database.start_script(request)
		# except Exception as e:
		# 	response = HttpResponse("Here's the text of the Web page.")
		# 	print e
		# 	return render(request,"about.html")
		



admin.site.register(Upload_file, UploadSheetAdmin)

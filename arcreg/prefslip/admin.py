from django.contrib import admin
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import *
from .forms import *
from .export import *


class AddCourseAdmin(admin.ModelAdmin):
	list_display=['name','ID_no','course_no','course_title','course_id','priority','pr_no']
	search_fields = ['name','ID_no','course_title','class_nbr','priority']
	#actions = ['export_xls','export_xlsx','export_csv']

	# For refactoring
	rem = ExportAddCourses()
	funcs = {'export_xls':rem.export_csv,'export_csv':rem.export_xlsx,'export_xlsx':rem.export_xls}
	actions = [funcs['export_xls'],funcs['export_xlsx'],funcs['export_csv']]
	
	
	model=AddCourses

admin.site.register(AddCourses,AddCourseAdmin)

class CourseSelectorAdmin(admin.ModelAdmin):
	list_display = ['discipline']
	raw_id_fields = ['available']
	model = Discipline

	
admin.site.register(Discipline,CourseSelectorAdmin)


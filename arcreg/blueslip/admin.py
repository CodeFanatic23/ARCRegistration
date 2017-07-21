from django.contrib import admin
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import *
from .forms import *

# Register your models here.
class RemoveCasesAdmin(admin.ModelAdmin):
	list_display=['name','ID_no','course_no','course_id','class_nbr','course_title','lecture_no','tutorial_no','practical_no']
	search_fields = ['name','ID_no','course_title','class_nbr']
	actions = ['export_xls','export_xlsx','export_csv']
	
	def export_csv(modeladmin, request, queryset):
		import csv
		from django.utils.encoding import smart_str
		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename=REMOVE_CASES.csv'
		writer = csv.writer(response, csv.excel)
		response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
		writer.writerow([
		    smart_str(u"ID"),
		    smart_str(u"Name"),
		    smart_str(u"ID_no"),
		    smart_str(u"Course ID"),
		    smart_str(u"Class No."),
		    smart_str(u"Course Title"),
		    smart_str(u"Lecture"),
		    smart_str(u"Tutorial"),
		    smart_str(u"Practical"),
		])
		for obj in queryset:
		    writer.writerow([
		        smart_str(obj.pk),
		        smart_str(obj.name),
		        smart_str(obj.ID_no),
		        smart_str(obj.course_id),
		        smart_str(obj.class_nbr),
		        smart_str(obj.course_title),
		        smart_str(obj.lecture_no),
		        smart_str(obj.tutorial_no),
		        smart_str(obj.practical_no),
		    ])
		return response
	export_csv.short_description = u"Export CSV"

	def export_xls(modeladmin, request, queryset):
		import xlwt
		response = HttpResponse(content_type='application/ms-excel')
		response['Content-Disposition'] = 'attachment; filename=REMOVE_CASES.xls'
		wb = xlwt.Workbook(encoding='utf-8')
		ws = wb.add_sheet("REMOVE_CASES")

		row_num = 0

		columns = [
		    (u"ID", 2000),
		    (u"Name", 6000),
		    (u"ID No.", 8000),
		    (u"Course ID", 8000),
		    (u"Class No.", 8000),
		    (u"Course Title", 8000),
		    (u"Lecture", 8000),
		    (u"Tutorial", 8000),
		    (u"Practical", 8000),
		]

		font_style = xlwt.XFStyle()
		font_style.font.bold = True

		for col_num in range(len(columns)):
		    ws.write(row_num, col_num, columns[col_num][0], font_style)
		    # set column width
		    ws.col(col_num).width = columns[col_num][1]

		font_style = xlwt.XFStyle()
		font_style.alignment.wrap = 1

		for obj in queryset:
		    row_num += 1
		    row = [
		        obj.pk,
		        obj.name,
		        obj.ID_no,
		        obj.course_id,
		        obj.class_nbr,
		        obj.course_title,
		        obj.lecture_no,
		        obj.tutorial_no,
		        obj.practical_no,
		    ]
		    for col_num in range(len(row)):
		        ws.write(row_num, col_num, row[col_num], font_style)
		        
		wb.save(response)
		return response

	export_xls.short_description = u"Export XLS"
	def export_xlsx(modeladmin, request, queryset):
		import openpyxl
		from openpyxl.cell import get_column_letter
		response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
		response['Content-Disposition'] = 'attachment; filename=REMOVE_CASES.xlsx'
		wb = openpyxl.Workbook()
		ws = wb.get_active_sheet()
		ws.title = "REMOVE_CASES"

		row_num = 0

		columns = [
		    (u"ID", 15),
		    (u"Name", 70),
		    (u"ID No.", 70),
		    (u"Course ID", 70),
		    (u"Class No.", 70),
		    (u"Course Title", 70),
		    (u"Lecture", 70),
		    (u"Tutorial", 70),
		    (u"Practical", 70),
		]

		for col_num in range(len(columns)):
		    c = ws.cell(row=row_num + 1, column=col_num + 1)
		    c.value = columns[col_num][0]
		    c.style.font.bold = True
		    # set column width
		    ws.column_dimensions[get_column_letter(col_num+1)].width = columns[col_num][1]

		for obj in queryset:
		    row_num += 1
		    row = [
		        obj.pk,
		        obj.name,
		        obj.ID_no,
		        obj.course_id,
		        obj.class_nbr,
		        obj.course_title,
		        obj.lecture_no,
		        obj.tutorial_no,
		        obj.practical_no,
		    ]
		    for col_num in range(len(row)):
		        c = ws.cell(row=row_num + 1, column=col_num + 1)
		        c.value = row[col_num]
		        c.style.alignment.wrap_text = True

		wb.save(response)
		return response

	export_xlsx.short_description = u"Export XLSX"
	model=Remove

admin.site.register(Remove,RemoveCasesAdmin)

class AddCasesAdmin(admin.ModelAdmin):
	list_display=['name','ID_no','course_no','course_id','class_nbr','course_title','lecture_no','tutorial_no','practical_no']
	search_fields = ['name','ID_no','course_title','class_nbr']
	
	actions = ['export_xls','export_xlsx','export_csv']
	
	def export_csv(modeladmin, request, queryset):
		import csv
		from django.utils.encoding import smart_str
		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename=ADD_CASES.csv'
		writer = csv.writer(response, csv.excel)
		response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
		writer.writerow([
		    smart_str(u"ID"),
		    smart_str(u"Name"),
		    smart_str(u"ID_no"),
		    smart_str(u"Course ID"),
		    smart_str(u"Class No."),
		    smart_str(u"Course Title"),
		    smart_str(u"Lecture"),
		    smart_str(u"Tutorial"),
		    smart_str(u"Practical"),
		])
		for obj in queryset:
		    writer.writerow([
		        smart_str(obj.pk),
		        smart_str(obj.name),
		        smart_str(obj.ID_no),
		        smart_str(obj.course_id),
		        smart_str(obj.class_nbr),
		        smart_str(obj.course_title),
		        smart_str(obj.lecture_no),
		        smart_str(obj.tutorial_no),
		        smart_str(obj.practical_no),
		    ])
		return response
	export_csv.short_description = u"Export CSV"

	def export_xls(modeladmin, request, queryset):
		import xlwt
		response = HttpResponse(content_type='application/ms-excel')
		response['Content-Disposition'] = 'attachment; filename=ADD_CASES.xls'
		wb = xlwt.Workbook(encoding='utf-8')
		ws = wb.add_sheet("ADD_CASES")

		row_num = 0

		columns = [
		    (u"ID", 2000),
		    (u"Name", 6000),
		    (u"ID No.", 8000),
		    (u"Course ID", 8000),
		    (u"Class No.", 8000),
		    (u"Course Title", 8000),
		    (u"Lecture", 8000),
		    (u"Tutorial", 8000),
		    (u"Practical", 8000),
		]

		font_style = xlwt.XFStyle()
		font_style.font.bold = True

		for col_num in range(len(columns)):
		    ws.write(row_num, col_num, columns[col_num][0], font_style)
		    # set column width
		    ws.col(col_num).width = columns[col_num][1]

		font_style = xlwt.XFStyle()
		font_style.alignment.wrap = 1

		for obj in queryset:
		    row_num += 1
		    row = [
		        obj.pk,
		        obj.name,
		        obj.ID_no,
		        obj.course_id,
		        obj.class_nbr,
		        obj.course_title,
		        obj.lecture_no,
		        obj.tutorial_no,
		        obj.practical_no,
		    ]
		    for col_num in range(len(row)):
		        ws.write(row_num, col_num, row[col_num], font_style)
		        
		wb.save(response)
		return response

	export_xls.short_description = u"Export XLS"
	def export_xlsx(modeladmin, request, queryset):
		import openpyxl
		from openpyxl.cell import get_column_letter
		response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
		response['Content-Disposition'] = 'attachment; filename=ADD_CASES.xlsx'
		wb = openpyxl.Workbook()
		ws = wb.get_active_sheet()
		ws.title = "ADD_CASES"

		row_num = 0

		columns = [
		    (u"ID", 15),
		    (u"Name", 70),
		    (u"ID No.", 70),
		    (u"Course ID", 70),
		    (u"Class No", 70),
		    (u"Course Title", 70),
		    (u"Lecture", 70),
		    (u"Tutorial", 70),
		    (u"Practical", 70),
		]

		for col_num in range(len(columns)):
		    c = ws.cell(row=row_num + 1, column=col_num + 1)
		    c.value = columns[col_num][0]
		    c.style.font.bold = True
		    # set column width
		    ws.column_dimensions[get_column_letter(col_num+1)].width = columns[col_num][1]

		for obj in queryset:
		    row_num += 1
		    row = [
		        obj.pk,
		        obj.name,
		        obj.ID_no,
		        obj.course_id,
		        obj.class_nbr,
		        obj.course_title,
		        obj.lecture_no,
		        obj.tutorial_no,
		        obj.practical_no,
		    ]
		    for col_num in range(len(row)):
		        c = ws.cell(row=row_num + 1, column=col_num + 1)
		        c.value = row[col_num]
		        c.style.alignment.wrap_text = True

		wb.save(response)
		return response

	export_xlsx.short_description = u"Export XLSX"
	model=Add

admin.site.register(Add,AddCasesAdmin)


class UserDataAdmin(admin.ModelAdmin):
	list_display=['name','ID_no','phone_no','submit','message']
	list_editable=['message']
	search_fields = ["name","ID_no"]
	
	model=Registered_User
	def save_model(self, request, obj, form, change=False):
		print("hello before saving")
		obj.message_status = False
		obj.save()
		print("Saved!")

	def submit(self,obj):
		return obj.submit_status
		

admin.site.register(Registered_User,UserDataAdmin)

class InstructionAdmin(admin.ModelAdmin):
	list_display=['instruction']
	list_display_links=['instruction']
	model = Instruction

admin.site.register(Instruction,InstructionAdmin)

class Generate_UserAdmin(admin.ModelAdmin):
	list_display = ['username','password']

	form = Generate_UserForm
	model = Generate_User

	def username(self,obj):
		return obj.no_of_users_to_generate

	def password(self,obj):
		return obj.username_pattern
	
	def response_add(self, request, obj, post_url_continue=None):
		return HttpResponseRedirect(reverse("admin:blueslip_generated_user_changelist"))

	# def response_add(self, request, obj, post_url_continue=None):
 #    """This makes the response go to the newly created model's change page
 #    without using reverse"""
 #    return HttpResponseRedirect("../%s" % obj.id])

class Generated_UserAdmin(admin.ModelAdmin):
	list_display_links=None
	list_display=['username','password']
	actions=['export_xls','export_xlsx','export_csv']

	class Media:
		js = ('/static/actions.min.js','http://forms.viewflow.io/static/material/admin/js/admin_init.js')
	def username(self,obj):
		return obj.usrname

	def password(self,obj):
		return obj.pwd

	def has_add_permission(self,request):
		return False

	def export_xls(modeladmin, request, queryset):
		import xlwt
		response = HttpResponse(content_type='application/ms-excel')
		response['Content-Disposition'] = 'attachment; filename=BULK_USERS.xls'
		wb = xlwt.Workbook(encoding='utf-8')
		ws = wb.add_sheet("BULK_USERS")

		row_num = 0

		columns = [
		    (u"ID", 2000),
		    (u"Username", 6000),
		    (u"Password", 8000),
		]

		font_style = xlwt.XFStyle()
		font_style.font.bold = True

		for col_num in range(len(columns)):
		    ws.write(row_num, col_num, columns[col_num][0], font_style)
		    # set column width
		    ws.col(col_num).width = columns[col_num][1]

		font_style = xlwt.XFStyle()
		font_style.alignment.wrap = 1

		for obj in queryset:
		    row_num += 1
		    row = [
		        obj.pk,
		        obj.usrname,
		        obj.pwd,
		    ]
		    for col_num in range(len(row)):
		        ws.write(row_num, col_num, row[col_num], font_style)
		        
		wb.save(response)
		return response

	export_xls.short_description = u"Export XLS"
	def export_xlsx(modeladmin, request, queryset):
		import openpyxl
		from openpyxl.cell import get_column_letter
		response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
		response['Content-Disposition'] = 'attachment; filename=BULK_USERS.xlsx'
		wb = openpyxl.Workbook()
		ws = wb.get_active_sheet()
		ws.title = "BULK_USERS"

		row_num = 0

		columns = [
		    (u"ID", 15),
		    (u"Username", 70),
		    (u"Password", 70),
		]

		for col_num in range(len(columns)):
		    c = ws.cell(row=row_num + 1, column=col_num + 1)
		    c.value = columns[col_num][0]
		    c.style.font.bold = True
		    # set column width
		    ws.column_dimensions[get_column_letter(col_num+1)].width = columns[col_num][1]

		for obj in queryset:
		    row_num += 1
		    row = [
		        obj.pk,
		        obj.usrname,
		        obj.pwd,
		      
		    ]
		    for col_num in range(len(row)):
		        c = ws.cell(row=row_num + 1, column=col_num + 1)
		        c.value = row[col_num]
		        c.style.alignment.wrap_text = True

		wb.save(response)
		return response

	export_xlsx.short_description = u"Export XLSX"

	def export_csv(modeladmin, request, queryset):
		import csv
		from django.utils.encoding import smart_str
		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename=BULK_USERS.csv'
		writer = csv.writer(response, csv.excel)
		response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
		writer.writerow([
		    smart_str(u"ID"),
		    smart_str(u"Username"),
		    smart_str(u"Password"),
		])
		for obj in queryset:
		    writer.writerow([
		        smart_str(obj.pk),
		        smart_str(obj.usrname),
		        smart_str(obj.pwd),
		    ])
		return response
	export_csv.short_description = u"Export CSV"

class ControlAdmin(admin.ModelAdmin):
	list_display = ['__str__']

	model = Control

	def has_add_permission(self,request):
		if self.model.objects.count() >= 1:
			return False
		else:
			return True
admin.site.register(Control,ControlAdmin)

admin.site.register(Generated_User,Generated_UserAdmin)
admin.site.register(Generate_User,Generate_UserAdmin)

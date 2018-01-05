from django.shortcuts import render, get_object_or_404
from .forms import *
from .models import *
from blueslip.models import Registered_User
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponseBadRequest, Http404
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.conf import settings
from django.contrib.auth.decorators import login_required
import json
import traceback
from blueslip.views import getMyData, clashWithOwnCheck, str_to_bool
from upload_sheet.models import FD_priority_number


@login_required	
def available_courses(request,disp):
	courses = Discipline.objects.filter(discipline=disp)
	l = []
	obj = Registered_User.objects.get(user__username__iexact=str(request.user))
	chk = request.session['chk']
	form = AvailForm(request.POST or None)
	for i in courses:
		l.append(i.available)
	if request.method == 'POST':
		if form.is_valid():#cleaned_data is available only when is_valid is called
			data = request.POST['available'].split(',')
			priority = form.cleaned_data.get('priority')
			my_pref = AddCourses.objects.filter(Q(ID_no__iexact=obj.ID_no) & Q(priority=priority) & Q(discipline=disp))
			if len(my_pref) == 0:
				#check for clash
				my_tt = getMyData(obj.ID_no,str(request.user),chk)

				clash_with = clashWithOwnCheck(int(data[0]),'1','1','1',my_tt)

				clash_with = clash_with.split('/')
				can_take = clash_with[-1]
				can_take = str_to_bool(can_take)
				if can_take:
					add_data = AddCourses(ID_no=obj.ID_no,name=obj.name,
									course_no=data[3],
									course_id=data[0],
									class_nbr=data[2],
									course_title=data[1],
									priority=priority,
									discipline=disp,
									userid=str(request.user))
					add_data.save()
					context = {
					'new_course':data[1]+ ' ' + data[3],
					'discipline':disp,
					}
					return HttpResponseRedirect('/avail/'+disp)
				else:
					i = 'Clashes with '+clash_with[0]
					info = '<title>Error</title> <link href="/static/css/bootstrap.min.css" rel="stylesheet"><script>function redirect(){window.history.go(-1);}</script><h1>'+i+'<br><button type="button" class="btn btn-danger" onClick="redirect();">Back</button>'
					return HttpResponse(info)
			info = '<title>Error</title> <link href="/static/css/bootstrap.min.css" rel="stylesheet"><script>function redirect(){var url = "/prefstatus";window.location = url;}</script><h1>Priority Already present, Remove the existing priority added to continue.<br><button type="button" class="btn btn-danger" onClick="redirect();">Click to change priority</button>'
			return HttpResponse(info)

	context = {
		'courses':l,
		'avail':form,
		'submit_status':request.session['subm'],
		'discipline':disp,
	}
	return render(request,'prefslipTemplates/available.html',context)

def prefstatus(request):
	obj = Registered_User.objects.get(user__username__iexact=str(request.user))
	request.session['ID'] = obj.ID_no
	my_pref = AddCourses.objects.filter(ID_no__iexact=obj.ID_no)
	print(my_pref)
	context = {
	'my_pref':my_pref,
	'stuobj':obj,
	'title':'STATUS',
	}

	return render(request,'prefslipTemplates/prefstatus.html',context)

@login_required
def prefdelete(request,priority,discipline):
	ID = request.session['ID']
	a = get_object_or_404(AddCourses,priority=priority,userid=str(request.user),discipline=discipline)
	if a.ID_no == ID:
		a.delete()
		print("Deleted:",a.course_title,"ID:",ID)
	
	return HttpResponseRedirect("/prefstatus/")

def offers(request):
	courses = Discipline.objects.all().distinct('discipline')

	return render(request,'prefslipTemplates/avail_list.html',{'courses':courses})

def pr(request):
	q = AddCourses.objects.all()
	for i in q:
		pr_no = FD_priority_number.objects.get(campus_id__iexact=i.ID_no)
		AddCourses.objects.filter(ID_no__iexact=i.ID_no).update(pr_no=pr_no.priority_number)

	return HttpResponse("DONE")
from django.shortcuts import render, get_object_or_404
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.db.models import Q
from upload_sheet.models import *
from django.http import HttpResponseRedirect, HttpResponseBadRequest, Http404
from django.http import HttpResponse
from difflib import SequenceMatcher
from django.core.serializers.json import DjangoJSONEncoder
from django.conf import settings
from django.contrib.auth.decorators import login_required
import json
import traceback


#ADD CLASH CHECKING USERS HERE
clashCheckers = ['clash','clash1','awesome']
tts = True


@login_required
def add(request):
	try:
		if request.is_ajax() or request.method == 'POST':
			add = AddForm(request.POST)
			if add.is_valid():
				chk = request.session['chk']
				check,created = Checks.objects.update_or_create(id_no=str(str(request.user.id)),defaults={})
				a,b = Checks.objects.update_or_create(id_no=str(request.user.id))
				
				c = Checks.objects.get(id_no=str(request.user.id))
				obj = Registered_User.objects.get(user__username__iexact=str(request.user))

				present_check = False
				can_take = True
				cbn = ''
				#Check for no. of additions
				if c.no_of_adds <= 5000:
					print("Checked for no. of adds!")
					#Check for previous additions

					for x in Add.objects.filter(ID_no__iexact=obj.ID_no):
						if request.POST['add_courses'] == x.course_no:
							present_check = True
							can_take = False
							break					
					
					if present_check == False:
						print("Checked for previous additions!")
					 
						pr_data = ''
						try:
							print(request.POST["add_courses"])
							if not str(obj.ID_no)[4] == 'H':
								print("FD")
								pr_data = FD_priority_number.objects.get(campus_id__iexact=obj.ID_no)
								print(pr_data.erp_id)
							else:
								print("HD")
								pr_data = HD_priority_number.get(campus_id__iexact=obj.ID_no)
						except Exception as e:
							print(e)


						try:
						# 	q = Time_Table_Semester_Wise.objects.filter(Q(Course_id=request.POST['add_courses']) & (Q(Section="L"+add.cleaned_data.get('lecture_no')) | 
						# 	 	Q(Section="T"+add.cleaned_data.get('tutorial_no')) | Q(Section="P"+add.cleaned_data.get('practical_no'))))
							q = getDataFromTT(request.POST['add_courses'],'L'+add.cleaned_data.get('lecture_no'),'T'+add.cleaned_data.get('tutorial_no'),'P'+add.cleaned_data.get('practical_no'))
							if len(q) == 0 and (int(add.cleaned_data.get('tutorial_no')) > 2 or int(add.cleaned_data.get('lecture_no')) > 2 or int(add.cleaned_data.get('practical_no')) > 2):
								cbn = False
								can_take = False
							elif len(q) != 0 or (int(add.cleaned_data.get('tutorial_no')) <=2 or int(add.cleaned_data.get('lecture_no')) <=2 or int(add.cleaned_data.get('practical_no')) <=2):
								try:
									q[0]
								except Exception as e:
									print("Combination not found...Error:",e)

								#NEW
								
								my_tt = getMyData(obj.ID_no,str(request.user),chk)

								clash_with = clashWithOwnCheck(request.POST['add_courses'],add.cleaned_data.get('lecture_no'),add.cleaned_data.get('tutorial_no'),add.cleaned_data.get('practical_no'),my_tt)

								
								clash_with = clash_with.split('/')
								print("CLASHES WITH:",clash_with[0])
								print("NEW CAN TAKE=",clash_with[-1])
								can_take = str_to_bool(clash_with[-1])
								print(can_take)
								print(q)
								print(q[0].course_title)
						except Exception as e:
							print(e)
							pass
						
						print("Final Result..can take?....",can_take)
						
							
						if can_take == True:
							print("Checked for time clash!")
							sec1 = ''
							sec2 = ''
							for i in q:
								if i.Section in ['R1','I1']:
									sec1 = i.Section
								else:
									sec2 = i.Section
								add_data = Add(erp_id=pr_data.erp_id,
									ID_no=obj.ID_no,name=pr_data.name,
									PR_no=pr_data.priority_number,
									course_no=request.POST['add_courses'],
									course_id=i.Subject+" "+i.catalog_course_no,
									class_nbr=i.class_nbr,
									course_title=i.course_title,
									lecture_no=add.cleaned_data.get('lecture_no'),
									tutorial_no=add.cleaned_data.get('tutorial_no'),
									practical_no=add.cleaned_data.get('practical_no'),
									graded_comp = sec2,
									project_section = sec1,
									userid=str(request.user))
								add_data.save()
								a.no_of_adds = F('no_of_adds')+1
								a.save()

		
					add_status = ''
					if present_check == True:
						add_status = "Already present in the addition queue!"
					elif cbn == False:
						add_status = "This combination does not exist"
					elif can_take == True:
						add_status = "Requested for addition!"
					elif can_take == False:
						add_status = "Cannot Add! Clashes with  "+clash_with[0]
					context={
					'add_status':add_status,
					}
					return HttpResponse(json.dumps(context),content_type="application/json")
				else:
					context={
					'add_status':"Cannot add more than 5 courses!",
					}
					return HttpResponse(json.dumps(context),content_type="application/json")

		else:
			return HttpResponse("<title>Warning</title><link href='/static/css/bootstrap.min.css' rel='stylesheet'><style>body{background-color:#F0D8D8;</style><div class='container'><h1 style='border: 1px solid;font-family:Helvetica;background-color:#f7f7f7;'>Bad Request...<p><strong>WARNING!</strong><br>Sending Too many bad requests will result in deregistration</p></h1></div>")		
	except Exception as e:
		print(e)

@login_required					
def remove(request):
	try:
		if request.is_ajax() or request.method == 'POST':
			remove = RemoveForm(request.POST)
			if remove.is_valid():
				
				check,created = Checks.objects.update_or_create(id_no=str(request.user.id),defaults={})
				a,b = Checks.objects.update_or_create(id_no=str(request.user.id))
				obj = Registered_User.objects.get(user__username__iexact=str(request.user))
				c = Checks.objects.get(id_no=str(request.user.id))
				print(request.POST["rem"])
				if not str(obj.ID_no)[4] == 'H':
					print("FD")
					pr_data = FD_priority_number.objects.get(campus_id__iexact=obj.ID_no)
					print(pr_data.erp_id)
				else:
					print("HD")
					pr_data = HD_priority_number.get(campus_id__iexact=obj.ID_no)
				
				print(obj.ID_no)
				course_no = int(request.POST['rem'])
				print(course_no)
				lec_data = Registration_data.objects.filter(Campus_ID__iexact=obj.ID_no,Course_ID=course_no)

				lecture_no = ''
				practical_no = ''
				tutorial_no = ''
				grad_comp = ''
				proj_sec = ''
				print(lec_data)
				for i in lec_data:
					if not i.Lecture_Section_No == '':
						lecture_no = i.Lecture_Section_No
					if not i.Practical_Section_No == '':
						practical_no = i.Practical_Section_No
					if not i.Tutorial_Section_No == '':
						tutorial_no = i.Tutorial_Section_No
					if not i.Project_Section_No == '':
						proj_sec = i.Project_Section_No
					if not i.Graded_Component == '':
						grad_comp = i.Graded_Component
					 
				q = Time_Table_Semester_Wise.objects.filter(Q(Course_id=request.POST['rem']) & (Q(Section=lecture_no) | Q(Section=tutorial_no) | Q(Section=practical_no) | Q(Section='I1') | Q(Section='R1') | Q(Section='G1'))).distinct('class_nbr')
				print(q[0].course_title)
				print(lecture_no)
				print(practical_no)
				print(tutorial_no)
				
				
				#Check for already present removals
				present_check = False
				rem_objs = Remove.objects.filter(ID_no__iexact=obj.ID_no)
				for x in rem_objs:
					if request.POST['rem'] == x.course_no:
						present_check = True
						break

				if c.no_of_removes <= 5000:
					print("Checked!")
					if present_check == False:
						for i in q:
							cont = False
							remove_data = Remove(erp_id=pr_data.erp_id,
								ID_no=obj.ID_no,name=pr_data.name,
								course_no= int(request.POST['rem']),
								course_title=i.course_title,
								course_id=i.Subject+" "+i.catalog_course_no,
								class_nbr=i.class_nbr,
								lecture_no=lecture_no,
								tutorial_no=tutorial_no,
								practical_no=practical_no,
								graded_comp = grad_comp,
								project_section = proj_sec,
								userid=str(request.user))
							
							remove_data.save()
							a.no_of_removes = F('no_of_removes')+1
							a.save()

						remove_status = "Requested for removal!"
						context={
						"remove_status":remove_status,
						}
						return HttpResponse(json.dumps(context),content_type="application/json")
					else:
						remove_status = "Already present in the removal queue!"
						context={
						"remove_status":remove_status,
						}
						return HttpResponse(json.dumps(context),content_type="application/json")
				else:
					remove_status = "Cannot Remove More than 5 courses"
					context={
					"remove_status":remove_status,
					}
					return HttpResponse(json.dumps(context),content_type="application/json")
		else:
			return HttpResponse("<title>Warning</title><link href='/static/css/bootstrap.min.css' rel='stylesheet'><style>body{background-color:#F0D8D8;</style><div class='container'><h1 style='border: 1px solid;font-family:Helvetica;background-color:#f7f7f7;'>Bad Request...<p><strong>WARNING!</strong><br>Sending Too many bad requests will result in deregistration</p></h1></div>")		
	except Exception as e:
				print(e)

def home(request):
	if request.user.is_active:
		
		if Control.objects.all().count() > 0:
			chk = Control.objects.all()[0].disable_checks #chk = disable checks or not
		else:
			chk = False
		print(chk)
		request.session['chk'] = chk

		print("Checks...",not chk)
		try:
			first_login = Registered_User.objects.get(user__username__iexact=str(request.user))
			if first_login.submit_status == False:
				add = AddForm(request.POST or None)
				remove = RemoveForm(request.POST or None)
						
				obj = Registered_User.objects.get(user__username__iexact=str(request.user))
				request.session['subm'] = obj.submit_status
				print("Searching:",obj.ID_no)
				my_data = Registration_data.objects.filter(Campus_ID__iexact=obj.ID_no)
				if len(my_data) > 0:
					message = obj.message
					
					a=[]
					my_courses = []
					course_no = []
					my_classes = []
					for i in my_data:
						a.append(i.Course_ID)
					my_courses = list(set(a))
					for i in my_courses:
						k=0
						t = Time_Table_Semester_Wise.objects.filter(Course_id=i)
						course_no.append(t[0].course_title)
					
					print("TIME TABLE")
					my_tt = getMyData(obj.ID_no,str(request.user),chk)
					
				
					instruction =[]
					ind = 0
					index=[]
					for i in Instruction.objects.all():
						ind+=1
						instruction.append(i.instruction)
						index.append(ind)
					
					courses = Time_Table_Semester_Wise.objects.all().order_by('class_nbr').distinct()
					all_courses = []
					add_courses = []
					for l in courses:
						if l.Course_id not in all_courses:
							all_courses.append(l.Course_id)
							add_courses.append(l.course_title+"-"+l.Subject+" "+l.catalog_course_no)
				 
				
					context={
					'add':add,
					'remove':remove,
					'rem_dropdown':zip(my_courses,course_no),
					'add_dropdown':zip(all_courses,add_courses),
					'message':message +' ' + obj.name,
					'message_status':obj.message_status,
					'instructions':zip(index,instruction),
					'submit_status':obj.submit_status,
					'title':'HOME',
					}
					return render(request,"material/home.html",context)

				else:
				
					info = ''
					if str(request.user).lower() in clashCheckers:
						info = '<title>Error</title> <link href="/static/css/bootstrap.min.css" rel="stylesheet"><script>function redirect(){var url = "/2638hjsbd3245347";window.location = url;}</script><h1>Student is not eligible(ID not found).Make sure you entered correct <strong>BITSID</strong>.BITSID is 20XXXX[XX/PS]XXXXG.<br>Please contact ARC for more information.<br><button type="button" class="btn btn-danger" onClick="redirect();">Go Back</button>'
					else:
						info = '<title>Error</title> <link href="/static/css/bootstrap.min.css" rel="stylesheet"><h1>Student is not eligible(ID not found).Make sure you entered correct <strong>BITSID</strong>.BITSID is 20XXXX[XX/PS]XXXXG.<br>Please contact ARC for more information.'
					return HttpResponse(info)
			else:
				obj = Registered_User.objects.get(user__username__iexact=str(request.user))
				message = obj.message
				instruction =[]
				ind = 0
				index=[]
				for i in Instruction.objects.all():
					ind+=1
					instruction.append(i.instruction)
					index.append(ind)
				context={				
				'message':message+' '+obj.name,
				'message_status':obj.message_status,
				'instructions':zip(index,instruction),
				'submit_status':obj.submit_status,
				'title':'HOME',
				}
				return render(request,"material/home.html",context)
	
		except Exception as e:
			traceback.print_exc()
			if request.user.is_staff or str(request.user) in clashCheckers:
				general = ClashForm(request.POST or None)
			else:
				general = GeneralForm(request.POST or None)
			ind = 0
			index=[]
			instruction =[]
			for i in Instruction.objects.all():
				ind+=1
				instruction.append(i.instruction)
				index.append(ind)
			if request.method == 'POST':
				if general.is_valid():
					if request.user.is_staff or str(request.user) in clashCheckers:
						a = Registered_User(semester=0,
							name='GOD_MODE',
							ID_no=(request.POST['ID_no']).upper(),
							phone_no='-1',
							user_id=str(request.user.id))
						a.save()							
					else:
						a = Registered_User(semester=request.POST['semester'],
							name=(request.POST['name']).upper(),
							ID_no=(request.POST['ID_no']).upper(),
							phone_no=request.POST['phone_no'],
							user_id=str(request.user.id))
						a.save()

					return HttpResponseRedirect('/home')

	
			context = {
			'form':general,
			'instructions':zip(index,instruction),
			'title':'HOME',
			}
			
			return render(request,"material/home_first.html",context)
			

	else:
		return render(request,"material/home.html")

@login_required
def update(request):
	if request.is_ajax():
		print("working")
		obj = Registered_User.objects.get(user__username__iexact=str(request.user))
		if obj.message_status == False:
			obj.message_status = True
			obj.save()
			print("Changed")
		print(obj.message_status)
		return HttpResponseBadRequest()
	else:
		raise Http404

@login_required
def status(request):
	if request.user.is_active:
		try:
			obj = Registered_User.objects.get(user__username__iexact=str(request.user))
			a = Add.objects.filter(ID_no=obj.ID_no)
			r = Remove.objects.filter(ID_no=obj.ID_no)
			
			context={
			'add':a,
			'remove':r,
			'message_status':obj.message_status,
			'message':obj.message+' ' + obj.name,
			'stuobj':obj,
			'title':'STATUS',
			}
			return render(request,"status.html",context)
		except Exception as e:
			print(e)
			return HttpResponseRedirect('/home/')
	else:
		return render(request,"status.html")
@login_required
def submit(request):
	obj = Registered_User.objects.get(user__username__iexact=str(request.user))
	obj.submit_status = True
	obj.save()
	return HttpResponseRedirect('/home/')

def instructions(request):
	instruction =[]
	ind = 0
	index=[]
	for i in Instruction.objects.all():
		ind+=1
		instruction.append(i.instruction)
		index.append(ind)
	context = {
	'data':zip(index,instruction)
	}
	return render(request,"instructions.html",context)
@login_required
def adelete(request,id):
	try:
		obj = Registered_User.objects.get(user__username__iexact=str(request.user))
		a = get_object_or_404(Add,id=id)
		if a.ID_no == obj.ID_no:
			a.delete()
			print("Deleted:",a.course_title,"ID:",a.ID_no)
			return HttpResponseRedirect("/status/")
		else:
			return HttpResponse("<title>Error</title><link href='/static/css/bootstrap.min.css' rel='stylesheet'><h1>You do not have sufficient permissions to perform this operation")

	except Exception as e:
		traceback.print_exc()
		raise Http404

@login_required
def rdelete(request,id):
	if request.user.is_active:
		try:
			obj = Registered_User.objects.get(user__username__iexact=str(request.user))
			a = get_object_or_404(Remove,id=id)
			if a.ID_no == obj.ID_no:
				a.delete()
				print("Deleted:",a.course_title,"ID:",a.ID_no)
				return HttpResponseRedirect("/status/")
			else:
				return HttpResponse("<title>Error</title><link href='/static/css/bootstrap.min.css' rel='stylesheet'><h1>You do not have sufficient permissions to perform this operation")

		except Exception as e:
			traceback.print_exc()
			raise Http404
	else:
		raise Http404

def clash(request):
	try:
		obj = Registered_User.objects.get(user__username__iexact=str(request.user))
		print(str(request.user))
		if str(request.user).lower() in clashCheckers:
			for i in Add.objects.filter(ID_no=obj.ID_no,userid=str(request.user)):
				print(i.id)
				i.delete()
			for j in Remove.objects.filter(ID_no=obj.ID_no,userid=str(request.user)):
				j.delete()			
			obj.delete()
			print("Deleted user")
			return HttpResponseRedirect('/home/')
		else:
			return HttpResponse("<title>Error</title><link href='/static/css/bootstrap.min.css' rel='stylesheet'><h1>You do not have sufficient permissions to perform this operation")	
	except Exception as e:
		print(e)
		pass
def buildWeekInfo(info,formatted):
	days = {'M':'Monday','T':'Tuesday','W':'Wednesday','TH':'Thursday','F':'Friday','S':'Saturday'}
	pat = info.class_pattern

	if pat == 'MWF':
		formatted[days['M']][info.mtg_start_time] = info
		formatted[days['W']][info.mtg_start_time] = info
		formatted[days['F']][info.mtg_start_time] = info
	elif pat == 'TTHS':
		formatted[days['T']][info.mtg_start_time] = info
		formatted[days['TH']][info.mtg_start_time] = info
		formatted[days['S']][info.mtg_start_time] = info
	elif pat in ['M','W','F','T','TH','S']:
		formatted[days[pat]][info.mtg_start_time] = info
	elif pat == 'MW':
		formatted[days['M']][info.mtg_start_time] = info
		formatted[days['W']][info.mtg_start_time] = info
	elif pat == 'WF':
		formatted[days['W']][info.mtg_start_time] = info
		formatted[days['F']][info.mtg_start_time] = info
	elif pat == 'TTH':
		formatted[days['T']][info.mtg_start_time] = info
		formatted[days['TH']][info.mtg_start_time] = info
	elif pat == 'TS':
		formatted[days['T']][info.mtg_start_time] = info
		formatted[days['S']][info.mtg_start_time] = info
	elif pat == 'THS':
		formatted[days['TH']][info.mtg_start_time] = info
		formatted[days['S']][info.mtg_start_time] = info
	elif pat == 'MT':
		formatted[days['M']][info.mtg_start_time] = info
		formatted[days['T']][info.mtg_start_time] = info
	elif pat == 'MTH':
		formatted[days['M']][info.mtg_start_time] = info
		formatted[days['TH']][info.mtg_start_time] = info
	elif pat == 'MS':
		formatted[days['M']][info.mtg_start_time] = info
		formatted[days['S']][info.mtg_start_time] = info
	elif pat == 'WTH':
		formatted[days['W']][info.mtg_start_time] = info
		formatted[days['TH']][info.mtg_start_time] = info
	elif pat == 'WS':
		formatted[days['W']][info.mtg_start_time] = info
		formatted[days['S']][info.mtg_start_time] = info
	elif pat == 'TW':
		formatted[days['T']][info.mtg_start_time] = info
		formatted[days['W']][info.mtg_start_time] = info
	elif pat == 'TF':
		formatted[days['T']][info.mtg_start_time] = info
		formatted[days['F']][info.mtg_start_time] = info
	elif pat == 'FS':
		formatted[days['F']][info.mtg_start_time] = info
		formatted[days['S']][info.mtg_start_time] = info


def formatTTData(data):
	from collections import defaultdict
	formatted = defaultdict(dict)
	for i in data:
		if i != None:
			buildWeekInfo(i,formatted)
	# for i in formatted:
	# 	print(i,"\t",end="")
	# 	print(printDict(formatted[i]))
	return formatted

def printDict(dictionary):
	for i in dictionary:
		print(dictionary[i].course_title +"\t|",end="")

@login_required
def timetable(request):
	try:
		obj = Registered_User.objects.get(user__username__iexact=str(request.user))
		chk = request.session['chk']
		formatted = formatTTData(getMyData(obj.ID_no,str(request.user),chk))
	
		context = {
		'data':formatted,
		'bitsID':obj.ID_no,
		'title':'TIMETABLE',
		}
		return render(request,"tt.html",context)
	except Exception as e:
		print(e)
		return HttpResponseRedirect('/home')



def str_to_bool(s):
    if s == 'True':
         return True
    elif s == 'False':
         return False
    else:
         raise ValueError

def getMyData(ID,uid,checks):
	#checks in is terms of disable checks or not..checks=true means disable checks = true
	try:
		my_data = []
		data = Registration_data.objects.filter(Campus_ID__iexact=ID)
		add = Add.objects.filter(ID_no=ID,userid=uid)
		rem = Remove.objects.filter(ID_no=ID,userid=uid)
	
		print('+---------------------------------------+')
		print('|Course no\t|Lect no|Prac no|Tut no.|')
		print('|---------------------------------------|')
		print('+---------------------------------------------------------------+')
		print('|Course no\t|Start Time\t|End Time\t|Class Pattern\t|')
		print('|---------------------------------------------------------------|')
		if not checks:
			for i in data:
				#print("|",i.Course_ID,"\t|",i.Lecture_Section_No,"\t|",i.Practical_Section_No,"\t|",i.Tutorial_Section_No,"\t|")
				
				my_data = my_data + getDataFromTT(i.Course_ID,i.Lecture_Section_No,i.Tutorial_Section_No,i.Practical_Section_No)
				
		#else only courses currently being added or removed courses will be in my_data
		for i in rem:
			print("REMOVNG--------------")
			my_data = updateOwnTimeTable(i,my_data,False)		#False for removing
			# i.updated = True
			# i.save()

		for i in add:
			my_data = my_data + getDataFromTT(i.course_no,'L'+i.lecture_no,'T'+i.tutorial_no,'P'+i.practical_no)
			# i.updated = True
			# i.save()
		
		print('+---------------------------------------------------------------+')
		#print('|---------------------------------------|')
		#print('+---------------------------------------+')
		return my_data


	except Exception as e:
		print(e)
		pass
def getDataFromTT(course_id,L_section,T_section,P_section):
	tt_data = Time_Table_Semester_Wise.objects.filter(Q(Course_id=course_id) & (Q(Section=L_section) | Q(Section=T_section) | Q(Section=P_section) | Q(Section='I1') | Q(Section='R1') | Q(Section='G1'))).distinct('class_nbr')
	ret_data = []
	prev_time=None
	for i in tt_data:
		if i.mtg_start_time != prev_time:
			print("|",i.Course_id,"\t|",i.mtg_start_time,"\t|",i.end_time,"\t|",i.class_pattern,"\t\t|",i.Section)
			prev_time = i.mtg_start_time
			ret_data.append(i)

	return ret_data

def clashWithOwnCheck(course_id,L_section,T_section,P_section,my_tt):
	can_take = None
	req_course = getDataFromTT(course_id,'L'+L_section,'T'+T_section,'P'+P_section)
	
	clash_with = ''
	
	for i in my_tt:
		for j in req_course:
			print('Checking Course ID...')
			if i.Course_id == j.Course_id:
				can_take = False
				clash_with = i.course_title+':'+i.Section+':'+i.class_pattern
				print("Already Present:",clash_with,"Can take:",can_take)
				return clash_with+'/'+str(can_take)
			else:
				print("Course id not matched!..checking for other clashes")
				prob = SequenceMatcher(None,i.class_pattern,j.class_pattern).ratio()
				tth = (i.class_pattern == 'T' and j.class_pattern == 'TH') or (i.class_pattern == 'TH' and j.class_pattern == 'T')
				if i.Section in ['G1','I1','R1']:
					print('General Section/ Project..No need to check')
					can_take = True
				elif (prob >= 0.3) and (not tth):
						print('Class Pattern Matched...checking times')
						if i.mtg_start_time <= j.mtg_start_time:
							print('Start Times matching('+str(i.mtg_start_time)+' <='+str(j.mtg_start_time)+')..checking for end times')
							if i.end_time <= j.mtg_start_time:
							# if(i.end_time < j.end_time ):
								can_take = True
								print("Times OK...",can_take)
							else:
								can_take = False
								clash_with = i.course_title+' [ '+i.Subject+' '+i.catalog_course_no+' ] , Section '+i.Section+' On '+i.class_pattern
								print("Times Clashing:",str(i.mtg_start_time)+' >'+str(j.mtg_start_time),clash_with,"Can take:",can_take)
								return clash_with+'/'+str(can_take)
						elif i.mtg_start_time >= j.mtg_start_time:
							print('Start Times matching('+str(i.mtg_start_time)+' >='+str(j.mtg_start_time)+')..checking for end times')
							if j.end_time <= i.mtg_start_time:
							# if(i.end_time > j.end_time):

								can_take = True
								print("Times OK...",can_take)
							else:
								can_take = False
								clash_with = i.course_title+':'+i.Section+':'+i.class_pattern
								print("Times Clashing:",str(i.mtg_start_time)+' <'+str(j.mtg_start_time),clash_with,"Can take:",can_take)
								return clash_with+'/'+str(can_take)
				else:
					can_take = True
					print("Pattern Not Matching...PROB:",prob,"--T-TH:",tth)
	print(can_take)

	return clash_with+'/'+str(can_take)

def updateOwnTimeTable(new_class,my_tt,add_or_remove):
	temp = []
	if add_or_remove:
		my_tt.append(new_class)
	else:
		for i in my_tt:
			if str(i.Course_id) != new_class.course_no:				
				temp.append(i)
	return temp



def mat(request):
	# form = RegistrationForm(request.POST or None)
	# context={
	# 'form':form,
	# }
	return render(request,'material/base_al.html')
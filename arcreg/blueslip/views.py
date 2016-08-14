from django.shortcuts import render
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.db.models import Q
from upload_sheet.models import *
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.http import HttpResponse
from difflib import SequenceMatcher
from django.core.serializers.json import DjangoJSONEncoder
from django.conf import settings
from django.contrib.auth.decorators import login_required
import json
import traceback

# Create your views here.
@login_required
def add(request):
	try:
		if request.is_ajax() or request.method == 'POST':
			add = AddForm(request.POST)
			if add.is_valid() and request.session['chk'] == False:
				check,created = Checks.objects.update_or_create(id_no=request.user.id,defaults={})
				a,b = Checks.objects.update_or_create(id_no=request.user.id)
				
				c = Checks.objects.get(id_no=request.user.id)
				# obj = Registered_User.objects.get(user__username__iexact=request.user)
				obj = Registered_User.objects.get(user__username__iexact=request.user)

				present_check = False
				can_take = True
				cbn = ''
				#Check for no. of additions
				if c.no_of_adds <= 50:
					print("Checked for no. of adds!")
					#Check for previous additions

					for x in Add.objects.filter(ID_no__iexact=obj.ID_no):
						if request.POST['add_courses'] == x.course_no:
							present_check = True
							can_take = False
							break					
					
					if present_check == False:
						print("Checked for previous additions!")

						#Check for capacity
						available = ''
						abc = Control.objects.last()
						if abc.enable_capacity == True:
							capacity = Capacity.objects.filter(Q(Course_id=request.POST['add_courses']) & (Q(Section="L"+add.cleaned_data.get('lecture_no')) | 
								 	Q(Section="T"+add.cleaned_data.get('tutorial_no')) | Q(Section="P"+add.cleaned_data.get('practical_no'))))
							for item in capacity:
								if item.Tot_enrl >= item.Cap_enrl + abc.capacity_buffer:
									available = False
									can_take = False
								else:
									available = True
									can_take = True
									item.Tot_enrl = item.Tot_enrl + 1
									item.save()
						else:
							available = True
						if available == True:
							print("Checked For Capacity")
					 
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

							my_classes_new = request.session['my_classes_new']
							my_courses = request.session['my_courses']
							my_start_time = request.session['my_start_time']
							my_end_time = request.session['my_end_time']
							my_class_pattern = request.session['my_class_pattern']
							
							my_start_time_prcsd = []
							my_end_time_prcsd = []
							my_start_time_prcsd = my_start_time.split('"')
							my_end_time_prcsd = my_end_time.split('"')
							for itr1 in my_start_time_prcsd:
								if itr1.strip() == ',' or '[' or ']':
									my_start_time_prcsd.remove(itr1)
							print(my_start_time_prcsd)

							for itr2 in my_end_time_prcsd:
								if itr2.strip() == ',' or '[' or ']':
									my_end_time_prcsd.remove(itr2)
							print(my_end_time_prcsd)

							print("______________________________________________________________________________________________________________")
							print(len(my_start_time_prcsd))
							print(len(my_end_time_prcsd))
							print(len(my_class_pattern))
							print("______________________________________________________________________________________________________________")

							print(obj.ID_no)
							print(request.POST['add_courses'])
							print(add.cleaned_data.get('lecture_no'))
							print(add.cleaned_data.get('tutorial_no'))
							try:
								q = Time_Table_Semester_Wise.objects.filter(Q(Course_id=request.POST['add_courses']) & (Q(Section="L"+add.cleaned_data.get('lecture_no')) | 
								 	Q(Section="T"+add.cleaned_data.get('tutorial_no')) | Q(Section="P"+add.cleaned_data.get('practical_no'))))
								if len(q) == 0 and (int(add.cleaned_data.get('tutorial_no')) > 2 or int(add.cleaned_data.get('lecture_no')) > 2 or int(add.cleaned_data.get('practical_no')) > 2):
									cbn = False
									can_take = False
								elif len(q) != 0 or (int(add.cleaned_data.get('tutorial_no')) <=2 or int(add.cleaned_data.get('lecture_no')) <=2 or int(add.cleaned_data.get('practical_no')) <=2):
									try:
										q[0]
									except Exception as e:
										print("Combination not found...Error:",e)
										q = Time_Table_Semester_Wise.objects.filter(Q(Course_id=request.POST['add_courses']))
									start_time = []
									end_time = []
									class_pattern = []
									course_id = []
									#GET TIME OF REQUESTED COURSE
									for i in q:
										start_time.append((i.mtg_start_time).strftime("%H:%M:%S"))
										end_time.append((i.end_time).strftime("%H:%M:%S"))
										class_pattern.append(i.class_pattern)
										course_id.append(i.Course_id)
							
									print("End time",end_time)
									print("Class pattern",class_pattern)
				
									alpha = 0	
									break_status = False						
									print("##########....Working Level 1....##########")
									for x in range(0,len(my_start_time_prcsd)):
										beta = 0
										print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
										for y in range(0,len(start_time)):
											prob = SequenceMatcher(None,my_class_pattern[alpha],class_pattern[beta]).ratio()
											
											print("My Pattern(pat=",my_class_pattern[alpha],")    Req Class Pattern(",course_id[beta],")",",pat=",class_pattern[beta])
											print("Class pattern probablity..... ",prob)
											if prob >= 0.3:
												print("______________________________________________________________________________________________________________")
												print("Pattern Matched...Checking for start time.....")
												print("My Start Time(",my_start_time_prcsd[alpha],")....Req Start Time(",start_time[beta],")")
												if start_time[beta] == my_start_time_prcsd[alpha]:
													print("Start time Matched!....Checking for end time")
													print("My End Time(",my_end_time_prcsd[alpha],")....Req End Time(",end_time[beta],")")
													can_take = False
													print("Can Take?.....",can_take)
													break_status = True
													break

												elif end_time[beta] == my_end_time_prcsd[alpha]:
													print("______________________________________________________________________________________________________________")
													print("Start time not matching...Checking for End time....\n..... Matched!")
													can_take = False
													print("Can Take?.....",can_take)
													break_status = True
													break
												else:
													print("______________________________________________________________________________________________________________")
													can_take = True
													print("Neither Start nor end time match!")
													print("Can Take?.....",can_take)
											else:
												print("______________________________________________________________________________________________________________")
												print("Pattern not matching!")
												print("Can Take?.....",can_take)
											beta+=1
										if break_status == True:
											break
										alpha+=1
										print("alpha  ",alpha)
										print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")


									#GET TIME OF ALREADY PRESENT COURSES
									q2 = []
									add_start_time = []
									add_end_time = []
									add_class_pattern = []
									add_course_id = []
									for i in Add.objects.filter(ID_no=obj.ID_no):
										print(i.course_no)
										q2 = Time_Table_Semester_Wise.objects.filter(Q(Course_id=i.course_no) & (Q(Section="L"+i.lecture_no) | 
										 	Q(Section="T"+i.tutorial_no) | Q(Section="P"+i.practical_no)))
									
										for i in q2:
											add_start_time.append((i.mtg_start_time).strftime("%H:%M:%S"))
											add_end_time.append((i.end_time).strftime("%H:%M:%S"))
											add_class_pattern.append(i.class_pattern)
											add_course_id.append(i.Course_id)

									# print(add_start_time)
									# print(add_end_time)
									# print(add_class_pattern)
									print(len(add_start_time))
									print(len(add_end_time))
									print(len(add_class_pattern))
									print(len(add_course_id))

									if can_take == False:
										print("Can Take?...",can_take,"...Skipping level 2")
									else:
										alpha = 0	
										break_status = False						
										print("##########....Working Level 2....##########")
										for x in range(0,len(add_start_time)):
											beta = 0
											print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
											for y in range(0,len(start_time)):
												prob = SequenceMatcher(None,add_class_pattern[alpha],class_pattern[beta]).ratio()
												
												print("My Pattern(pat=",add_class_pattern[alpha],")    Req Class Pattern(",course_id[beta],")",",pat=",class_pattern[beta])
												print("Class pattern probablity..... ",prob)
												if prob >= 0.3:
													print("______________________________________________________________________________________________________________")
													print("Pattern Matched...Checking for start time.....")
													print("My Start Time(",add_start_time[alpha],")....Req Start Time(",start_time[beta],")")
													if start_time[beta] == add_start_time[alpha]:
														print("Start time Matched!....Checking for end time")
														print("My End Time(",add_end_time[alpha],")....Req End Time(",end_time[beta],")")
														can_take = False
														print("Can Take?.....",can_take)
														break_status = True
														break

													elif end_time[beta] == add_end_time[alpha]:
														print("______________________________________________________________________________________________________________")
														print("Start time not matching...Checking for End time....\n..... Matched!")
														can_take = False
														print("Can Take?.....",can_take)
														break_status = True
														break
													else:
														print("______________________________________________________________________________________________________________")
														can_take = True
														print("Neither Start nor end time match!")
														print("Can Take?.....",can_take)
												else:
													print("______________________________________________________________________________________________________________")
													print("Pattern not matching!")
													print("Can Take?.....",can_take)
												beta+=1
											if break_status == True:
												break
											alpha+=1
											print("alpha  ",alpha)
											print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")



									print(q[0].course_title)
							except Exception as e:
								print(e)
								pass
							
							print("Final Result..can take?....",can_take)
							
								
							if can_take == True:
								print("Checked for time clash!")
								add_data = Add(erp_id=pr_data.erp_id,
									ID_no=obj.ID_no,name=pr_data.name,
									PR_no=pr_data.priority_number,
									course_no=request.POST['add_courses'],
									course_id=q[0].Subject+" "+q[0].catalog_course_no,
									class_nbr=q[0].class_nbr,
									course_title=q[0].course_title,
									lecture_no=add.cleaned_data.get('lecture_no'),
									tutorial_no=add.cleaned_data.get('tutorial_no'),
									practical_no=add.cleaned_data.get('practical_no'))
								add_data.save()
								a.no_of_adds = F('no_of_adds')+1
								a.save()

					add_status = ''
					if present_check == True:
						add_status = "Already present in the addition queue!"
					elif cbn == False:
						add_status = "This combination does not exist"
					elif available == False:
						add_status = "Capacity Full,No Seats available!"
					elif can_take == True:
						add_status = "Requested for addition!"
					elif can_take == False:
						add_status = "Cannot Add! Clashes with current timetable!"
					context={
					'add_status':add_status,
					}
					return HttpResponse(json.dumps(context),content_type="application/json")
				else:
					context={
					'add_status':"Cannot add more than 5 courses!",
					}
					return HttpResponse(json.dumps(context),content_type="application/json")


			elif request.session['chk'] == True:
				obj = Registered_User.objects.get(user__username__iexact=request.user)
				#Check for previous additions
				present_check = False
				can_take = True
				add_status = ''
				cbn = ''
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
						q = Time_Table_Semester_Wise.objects.filter(Q(Course_id=request.POST['add_courses']) & (Q(Section="L"+add.cleaned_data.get('lecture_no')) | 
						 	Q(Section="T"+add.cleaned_data.get('tutorial_no')) | Q(Section="P"+add.cleaned_data.get('practical_no'))))
						
						if len(q) == 0 and (int(add.cleaned_data.get('tutorial_no')) > 2 or int(add.cleaned_data.get('lecture_no')) > 2 or int(add.cleaned_data.get('practical_no')) > 2):
							cbn = False
							can_take = False

						elif len(q) != 0 or (int(add.cleaned_data.get('tutorial_no')) <= 2 or int(add.cleaned_data.get('lecture_no')) <= 2 or int(add.cleaned_data.get('practical_no')) <= 2):
							try:
								q[0]
							except Exception as e:
								print("Combination not found...Error:",e)
								q = Time_Table_Semester_Wise.objects.filter(Q(Course_id=request.POST['add_courses']))
							start_time = []
							end_time = []
							class_pattern = []
							course_id = []
							#GET TIME OF REQUESTED COURSE
							for i in q:
								start_time.append((i.mtg_start_time).strftime("%H:%M:%S"))
								end_time.append((i.end_time).strftime("%H:%M:%S"))
								class_pattern.append(i.class_pattern)
								course_id.append(i.Course_id)
							#GET TIME OF ALREADY PRESENT COURSES
							q2 = []
							add_start_time = []
							add_end_time = []
							add_class_pattern = []
							add_course_id = []
							for i in Add.objects.filter(ID_no=obj.ID_no):
								q2 = Time_Table_Semester_Wise.objects.filter(Q(Course_id=i.course_no) & (Q(Section="L"+i.lecture_no) | 
								 	Q(Section="T"+i.tutorial_no) | Q(Section="P"+i.practical_no)))

								for i in q2:
									add_start_time.append((i.mtg_start_time).strftime("%H:%M:%S"))
									add_end_time.append((i.end_time).strftime("%H:%M:%S"))
									add_class_pattern.append(i.class_pattern)
									add_course_id.append(i.Course_id)

							print(len(add_start_time))
							print(len(add_end_time))
							print(len(add_class_pattern))
							print(len(add_course_id))

	

							if can_take == False:
								print("Can Take?...",can_take,"...Skipping level 2")
							else:
								alpha = 0	
								break_status = False						
								print("##########....Working Level 2....##########")
								for x in range(0,len(add_start_time)):
									beta = 0
									print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
									for y in range(0,len(start_time)):
										prob = SequenceMatcher(None,add_class_pattern[alpha],class_pattern[beta]).ratio()
										
										print("My Pattern(pat=",add_class_pattern[alpha],")    Req Class Pattern(",course_id[beta],")",",pat=",class_pattern[beta])
										print("Class pattern probablity..... ",prob)
										if prob >= 0.3:
											print("______________________________________________________________________________________________________________")
											print("Pattern Matched...Checking for start time.....")
											print("My Start Time(",add_start_time[alpha],")....Req Start Time(",start_time[beta],")")
											if start_time[beta] == add_start_time[alpha]:
												print("Start time Matched!....Checking for end time")
												print("My End Time(",add_end_time[alpha],")....Req End Time(",end_time[beta],")")
												can_take = False
												print("Can Take?.....",can_take)
												break_status = True
												break

											elif end_time[beta] == add_end_time[alpha]:
												print("______________________________________________________________________________________________________________")
												print("Start time not matching...Checking for End time....\n..... Matched!")
												can_take = False
												print("Can Take?.....",can_take)
												break_status = True
												break
											else:
												print("______________________________________________________________________________________________________________")
												can_take = True
												print("Neither Start nor end time match!")
												print("Can Take?.....",can_take)
										else:
											print("______________________________________________________________________________________________________________")
											print("Pattern not matching!")
											print("Can Take?.....",can_take)
										beta+=1
									if break_status == True:
										break
									alpha+=1
									print("alpha  ",alpha)
									print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

								print(q[0].course_title)
							print("Final Result..can take?....",can_take)

						if can_take == True:	
							add_data = Add(erp_id=pr_data.erp_id,
								ID_no=obj.ID_no,name=pr_data.name,
								PR_no=pr_data.priority_number,
								course_no=request.POST['add_courses'],
								course_id=q[0].Subject+" "+q[0].catalog_course_no,
								class_nbr=q[0].class_nbr,
								course_title=q[0].course_title,
								lecture_no=add.cleaned_data.get('lecture_no'),
								tutorial_no=add.cleaned_data.get('tutorial_no'),
								practical_no=add.cleaned_data.get('practical_no'))
							add_data.save()

						
						
					except Exception as e:
						traceback.print_exc()
						# q1 = Time_Table_Semester_Wise.objects.get(Course_id=request.POST['add_courses'])
						# q = []
						# q.append(q1)
						# print(q[0].course_title)
				if present_check == True:
					add_status = "Already present in the addition queue!"
				elif cbn == False:
					add_status = "This combination does not exist"
				elif can_take == True:
					add_status = "Requested for addition!"
				elif can_take == False:
					add_status = "Cannot Add! Clashes with current timetable!"
					
				context={
				'add_status':add_status,
				}
				return HttpResponse(json.dumps(context),content_type="application/json")

	except Exception as e:
		print(e)
					
def remove(request):
	try:
		if request.is_ajax() or request.method == 'POST':
			remove = RemoveForm(request.POST)
			if remove.is_valid():
				
				check,created = Checks.objects.update_or_create(id_no=request.user.id,defaults={})
				a,b = Checks.objects.update_or_create(id_no=request.user.id)
				obj = Registered_User.objects.get(user__username__iexact=request.user)
				c = Checks.objects.get(id_no=request.user.id)
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
				for i in lec_data:
					if not i.Lecture_Section_No == '':
						lecture_no = i.Lecture_Section_No
					if not i.Practical_Section_No == '':
						practical_no = i.Practical_Section_No
					if not i.Tutorial_Section_No == '':
						tutorial_no = i.Tutorial_Section_No
				q = Time_Table_Semester_Wise.objects.filter(Course_id=request.POST['rem'])
				print(q[0].course_title)
				print(lecture_no)
				print(practical_no)
				print(tutorial_no)
				
				#Check for already present removals
				present_check = False
				for x in Remove.objects.filter(ID_no__iexact=obj.ID_no):
					if request.POST['rem'] == x.course_no:
						present_check = True
						break

				if c.no_of_removes <= 50:
					print("Checked!")
					if present_check == False:
						remove_data = Remove(erp_id=pr_data.erp_id,
							ID_no=obj.ID_no,name=pr_data.name,
							course_no= int(request.POST['rem']),
							course_title=q[0].course_title,
							course_id=q[0].Subject+" "+q[0].catalog_course_no,
							class_nbr=q[0].class_nbr,
							lecture_no=lecture_no,
							tutorial_no=tutorial_no,
							practical_no=practical_no)
						remove_data.save()
						a.no_of_removes = F('no_of_removes')+1
						a.save()
						#Check for capacity
						capacity = Capacity.objects.filter	(Q(Course_id=request.POST['rem']) & ((Q(Section=lecture_no)) | 
							 	Q(Section=tutorial_no) | Q(Section=practical_no)))
						for item2 in capacity:
							item2.Tot_enrl = item2.Tot_enrl - 1
							item2.save()
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

	except Exception as e:
				print(e)

def home(request):
	if request.user.is_active:
		
		if Control.objects.all().count() > 0:
			chk = Control.objects.all()[0].disable_checks
		else:
			chk = False
		print(chk)
		request.session['chk'] = chk
		if chk == False:
			print("Enabling Checks...")
			try:
				first_login = Registered_User.objects.get(user__username__iexact=request.user)
				if first_login.submit_status == False:
					add = AddForm(request.POST)
					remove = RemoveForm(request.POST)
							
					obj = Registered_User.objects.get(user__username__iexact=request.user)
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
							for p in t:
								my_classes.append(p.class_nbr)

						#GET OWN TIME TABLE

						my_lect=[]
						my_prac = []
						my_tut = []
						count = []
						cnt=0
					
						for u in my_courses:
							my_db = Registration_data.objects.filter(Campus_ID__iexact=obj.ID_no, Course_ID=u)
							for i in my_db:
								
								if not i.Graded_Component == "G1":
									cnt+=1
									if not i.Lecture_Section_No == '':
										my_lect.append(i.Lecture_Section_No)
						
									if not i.Practical_Section_No == '':
										my_lect.append(i.Practical_Section_No)
										
									if not i.Tutorial_Section_No == '':
										my_lect.append(i.Tutorial_Section_No)
							count.append(cnt)
						var = 0
						s=0
						g=0
						my_time_table = {}
						for u in my_courses:
							s = count[g]
							aw=[]
							for op in range(var,count[g]):
								aw.append(my_lect[op])
							my_time_table[u]=aw
					
							var = s
							g+=1
						print(my_time_table)

						#GET OWN TIME
						for key in my_time_table:
							# if my_time_table[key][0].startswith('T'):
							# 	if not len(my_time_table[key][0]) == 1:
							# 		my_time_table[key].insert(0,0)
							# if my_time_table[key][0].startswith('P'):
							# 	if len(my_time_table[key][0]) == 1:
							# 		my_time_table[key].insert(0,0)
							# 		my_time_table[key].insert(0,0)
							for ab in range(3-len(my_time_table[key])):
								my_time_table[key].append(0)						
							
						print(my_time_table)
					
						my_start_time = []
						my_end_time = []
						my_class_pattern = []
						my_classes_new = []
						for key in my_time_table:
							q = Time_Table_Semester_Wise.objects.filter(Q(Course_id=key) & (Q(Section__iexact=my_time_table[key][0]) | 
								Q(Section__iexact=my_time_table[key][1]) | Q(Section__iexact=my_time_table[key][2])))
							q1 = q[0].class_nbr
							q2 = q[0].class_pattern
							my_classes_new.append(key)
							my_start_time.append(q[0].mtg_start_time)
							my_end_time.append(q[0].end_time)
							my_class_pattern.append(q[0].class_pattern)
							for a1 in q:
								if not a1.class_nbr == q1 or  not a1.class_pattern == q2:
									my_start_time.append(a1.mtg_start_time)
									my_end_time.append(a1.end_time)
									my_class_pattern.append(a1.class_pattern)
									q1 = a1.class_nbr
									q2 = a1.class_pattern
									
						print(my_class_pattern)
						print(my_classes_new)
								
						#GET ALL THE COURSE IDs THAT ARE NOT IN ONE'S TIME-TABLE
						q = object()
						l=[]
						q = Time_Table_Semester_Wise.objects.filter(~Q(Course_id=my_courses[0]))
						k =1
						while k < len(my_courses):
							q = q.filter(~Q(Course_id=my_courses[k]))
							k+=1
						
						#GET THE CLASS NUMBERS FOR COURSES THAT ARE NOT ONE'S OWN
						all_classes = []
						a=0
						for i in q:
							all_classes.append(i.class_nbr)
							a+=1
				
						all_classes = list(set(all_classes))
						all_courses = []
						available_courses = []
						for i in all_classes:
							q = Time_Table_Semester_Wise.objects.filter(class_nbr=i)
							all_courses.append(q[0].Course_id)
						all_courses = list(set(all_courses))
						print(len(all_courses))
						
						add_courses = []
						for i in all_courses:
							k = 0
							b = Time_Table_Semester_Wise.objects.filter(Course_id=i)
							add_courses.append(b[0].course_title+"-"+b[0].Subject+" "+b[0].catalog_course_no)
							k+=1
						print(len(add_courses))
					
						instruction =[]
						ind = 0
						index=[]
						for i in Instruction.objects.all():
							ind+=1
							instruction.append(i.instruction)
							index.append(ind)
						
						request.session['my_classes_new'] = my_classes_new
						request.session['my_classes'] = my_classes
						request.session['my_courses'] = my_courses
						request.session['my_start_time'] = json.dumps(my_start_time, cls=DjangoJSONEncoder)
						request.session['my_end_time'] = json.dumps(my_end_time, cls=DjangoJSONEncoder)
						request.session['my_class_pattern'] = my_class_pattern

						context={
						'add':add,
						'remove':remove,
						'rem_dropdown':zip(my_courses,course_no),
						'add_dropdown':zip(all_courses,add_courses),
						'message':message,
						'message_status':obj.message_status,
						'instructions':zip(index,instruction),
						'submit_status':obj.submit_status,
						}
						return render(request,"home_V2.html",context)
					else:
						return HttpResponse('<h1>Student is either not eligible(ID not found).Please contact ARC for more information')
				else:
					obj = Registered_User.objects.get(user__username__iexact=request.user)
					message = obj.message
					instruction =[]
					ind = 0
					index=[]
					for i in Instruction.objects.all():
						ind+=1
						instruction.append(i.instruction)
						index.append(ind)
					context={				
					'message':message,
					'message_status':obj.message_status,
					'instructions':zip(index,instruction),
					'submit_status':obj.submit_status,
					}
					return render(request,"home_V2.html",context)
		
			except Exception as e:
				traceback.print_exc()
				general = GeneralForm(request.POST)
				ind = 0
				index=[]
				instruction =[]
				for i in Instruction.objects.all():
					ind+=1
					instruction.append(i.instruction)
					index.append(ind)
				if request.method == 'POST':
					if general.is_valid():
						
						a = Registered_User(semester=request.POST['semester'],
							name=(request.POST['name']).upper(),
							ID_no=(request.POST['ID_no']).upper(),
							phone_no=request.POST['phone_no'],
							user_id=request.user.id)
						a.save()

						return HttpResponseRedirect('/home')

		
				context = {
				'general':general,
				'instructions':zip(index,instruction),
				}
				
				return render(request,"home_first.html",context)
		else:
			#EMPTY LIST STUFF
			print("Disabling Checks...")
			try:
				first_login = Registered_User.objects.get(user__username__iexact=request.user)
				if first_login.submit_status == False:
					add = AddForm(request.POST)
										
					obj = Registered_User.objects.get(user__username__iexact=request.user)
					print("Searching:",obj.ID_no)
					
					er = Registration_data.objects.filter(Campus_ID__iexact=obj.ID_no)
					if len(er) > 0:
					
						message = obj.message	
						
						courses = Time_Table_Semester_Wise.objects.all().order_by('Course_id').distinct()
						all_courses = []
						add_courses = []
						for l in courses:
							if l.Course_id not in all_courses:
								all_courses.append(l.Course_id)
								add_courses.append(l.course_title+"-"+l.Subject+" "+l.catalog_course_no)

						instruction =[]
						ind = 0
						index=[]
						for i in Instruction.objects.all():
							ind+=1
							instruction.append(i.instruction)
							index.append(ind)				

						context={
						'add':add,
						'add_dropdown':zip(all_courses,add_courses),
						'message':message,
						'message_status':obj.message_status,
						'instructions':zip(index,instruction),
						'submit_status':obj.submit_status,
						}
						return render(request,"home_V3.html",context)
					else:
						return HttpResponse("<h1>Student is either not eligible(ID not found).Please contact ARC for more information</h1>")
				else:
					obj = Registered_User.objects.get(user__username__iexact=request.user)
					message = obj.message
					instruction =[]
					ind = 0
					index=[]
					for i in Instruction.objects.all():
						ind+=1
						instruction.append(i.instruction)
						index.append(ind)
					context={				
					'message':message,
					'message_status':obj.message_status,
					'instructions':zip(index,instruction),
					'submit_status':obj.submit_status,
					}
					return render(request,"home_V2.html",context)
		
			except Exception as e:
				print(e)
				general = GeneralForm(request.POST)
				ind = 0
				index=[]
				instruction =[]
				for i in Instruction.objects.all():
					ind+=1
					instruction.append(i.instruction)
					index.append(ind)
				if request.method == 'POST':
					if general.is_valid():
						a = Registered_User(semester=request.POST['semester'],
							name=(request.POST['name']).upper(),
							ID_no=(request.POST['ID_no']).upper(),
							phone_no=request.POST['phone_no'],
							user_id=request.user.id)
						a.save()
		
				context = {
				'general':general,
				'instructions':zip(index,instruction),
				}
				
				return render(request,"home_first.html",context)
			

	else:
		return render(request,"home_V2.html")


def update(request):
	if request.is_ajax():
		print("working")
		obj = Registered_User.objects.get(user__username__iexact=request.user)
		if obj.message_status == False:
			obj.message_status = True
			obj.save()
			print("Changed")
		print(obj.message_status)
		return HttpResponseBadRequest()
	else:
		raise Http404

def status(request):
	if request.user.is_active:
		try:
			obj = Registered_User.objects.get(user__username__iexact=request.user)
			a = Add.objects.filter(ID_no=obj.ID_no)
			r = Remove.objects.filter(ID_no=obj.ID_no)
			
			context={
			'add':a,
			'remove':r,
			'message_status':obj.message_status,
			'message':obj.message,
			'stuobj':obj,
			}
			return render(request,"status.html",context)
		except Exception as e:
			return HttpResponseRedirect('/home/')
	else:
		return render(request,"status.html")

def submit(request):
	obj = Registered_User.objects.get(user__username__iexact=request.user)
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
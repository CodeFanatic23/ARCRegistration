from django.db import models
from upload_sheet.models import Time_Table_Semester_Wise

# Create your models here.
class Available_Courses(models.Model):
	course_no = models.CharField(max_length = 12, blank = False, null = True,default=0)
	course_id = models.CharField(max_length = 12, blank = False, null = True,default=0)
	class_nbr = models.CharField(max_length=10,blank=False,null=True,default=0)
	course_title = models.CharField(max_length = 80, blank = False, null = True)

	def __str__(self):
		return self.course_title + ' ' + str(self.class_nbr)
	
class Discipline(models.Model):
	discipline = models.CharField(max_length=20,blank=False,null=True)
	available = models.ForeignKey(Time_Table_Semester_Wise,related_name='TimeTable')

class AddCourses(models.Model):
	ID_no = models.CharField(max_length = 14, blank = False, null = True)
	name = models.CharField(max_length = 80, blank = False, null = True)
	course_no = models.CharField(max_length = 12, blank = False, null = True,default=0)
	course_id = models.CharField(max_length = 12, blank = False, null = True,default=0)
	priority = models.IntegerField(null=True,default = 1)
	pr_no = models.IntegerField(null=True,default = 1)
	class_nbr = models.CharField(max_length=10,blank=False,null=True,default=0)
	course_title = models.CharField(max_length = 80, blank = False, null = True)
	discipline = models.CharField(max_length = 10, blank = False, null = True)
	userid = models.CharField(max_length=20,blank=False,default='-1')

	class Meta:
		verbose_name_plural = "Add courses"


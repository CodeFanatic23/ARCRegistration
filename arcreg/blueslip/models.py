from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.db.models import signals
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.mail import EmailMessage
from django.conf import settings
from django.db import transaction,IntegrityError
from django.utils.encoding import python_2_unicode_compatible
import string
import random



# Create your models here.
class Add(models.Model):
	erp_id = models.IntegerField(blank=True,null=True)
	ID_no = models.CharField(max_length = 14, blank = False, null = True)
	name = models.CharField(max_length = 80, blank = False, null = True)
	PR_no = models.IntegerField(null=True)
	course_no = models.CharField(max_length = 12, blank = False, null = True,default=0)
	course_id = models.CharField(max_length = 12, blank = False, null = True,default=0)
	class_nbr = models.CharField(max_length=10,blank=False,null=True,default=0)
	course_title = models.CharField(max_length = 80, blank = False, null = True)
	lecture_no = models.CharField(max_length = 2, blank = False, default=0)
	tutorial_no = models.CharField(max_length = 2,blank = False, default=0)
	practical_no = models.CharField(max_length = 2,blank = False, default=0)

	class Meta:
		verbose_name_plural = "Additions"

class Remove(models.Model):
	erp_id = models.IntegerField(blank=True,null=True)
	ID_no = models.CharField(max_length = 14, blank = False, null = True)
	name = models.CharField(max_length = 80, blank = False, null = True)
	course_no = models.CharField(max_length = 12, blank = False, null = True,default=0)
	course_id = models.CharField(max_length = 12, blank = False, null = True,default=0)
	class_nbr = models.CharField(max_length=10,blank=False,null=True,default=0)
	course_title = models.CharField(max_length = 80, blank = False, null = True)
	lecture_no = models.CharField(max_length = 2, blank = False, default=0)
	tutorial_no = models.CharField(max_length = 2,blank = False, default=0)
	practical_no = models.CharField(max_length = 2,blank = False, default=0)

	class Meta:
		verbose_name_plural = "Removals"


class Registered_User(models.Model):
	user = models.OneToOneField(User,related_name='add_or_remove') 
	semester = models.DecimalField(max_digits = 1, decimal_places = 0, null = True, blank = False)
	ID_no = models.CharField(max_length = 14, blank = False, null = True)
	name = models.CharField(max_length = 80, blank = False, null = True)
	phone_no = models.DecimalField(max_digits=10,decimal_places=0,blank = True, null = True)
	message = models.CharField(max_length=500,blank=True,null=True,default="Hello!")
	# prev_message = models.CharField(max_length=500,blank=True,null=True,default="Hello!")
	message_status = models.BooleanField(default=False)
	submit_status = models.BooleanField(default=False)

	class Meta:
		verbose_name_plural = "Registered Users"

User.profile = property(lambda u:Registered_User.objects.get_or_create(user=u)[0])

class Checks(models.Model):
	id_no = models.CharField(max_length=4,null=False)
	no_of_adds = models.IntegerField(null=True,default=0)
	no_of_removes = models.IntegerField(null=True,default=0)

class Instruction(models.Model):
	instruction = models.CharField(max_length=200,blank=True,null=True)


class Generated_User(models.Model):
	usrname = models.CharField(max_length=30,blank=False,null=True)
	pwd = models.CharField(max_length=10,blank=False,null=True)

	class Meta:
		verbose_name_plural = "Bulk Users' Data"

class Generate_User(models.Model):
	no_of_users_to_generate = models.IntegerField(validators=[MaxValueValidator(1000),MinValueValidator(1)],blank=False,null=True)
	username_pattern = models.CharField(max_length=20,blank=True,null=True,default="blueslip_user")
	usrpass=models.ForeignKey(Generated_User,default=1)

	class Meta:
		verbose_name_plural = "Generate new users"
@python_2_unicode_compatible
class Control(models.Model):
	disable_checks = models.BooleanField(default=False,verbose_name='Disable')
	enable_capacity = models.BooleanField(default=False,verbose_name='Enable Capacity Check')
	capacity_buffer = models.IntegerField(validators=[MaxValueValidator(100),MinValueValidator(0)],default=0)

	class Meta:
		verbose_name_plural = 'Disable/Enable Checks'

	def __str__(self):

		return "Edit Checks"


def generate_users(sender,instance,**kwargs):
	try:
		with transaction.atomic():
			for i in range(0,instance.no_of_users_to_generate):
				passvar = pass_generator()
				print(instance.username_pattern)
				if instance.username_pattern == '':
					random.seed(random.randint(0,100))
					instance.username_pattern = 'bits'+str(random.randint(0,1000))
				usrpass=Generated_User(usrname=instance.username_pattern+"_"+str(i+1),pwd=passvar)
				usrpass.save()
				User.objects.create_user(instance.username_pattern+"_"+str(i+1), 'email@email.com', passvar)
				obj = Generate_User(id=None,no_of_users_to_generate=instance.no_of_users_to_generate,
					username_pattern=instance.username_pattern,
					usrpass=usrpass)
				obj.save()
				print(passvar)
	except IntegrityError:
		pass

def pass_generator(size=6, chars=string.ascii_uppercase + string.digits):
	print(''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(8)))
	return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(8))

signals.pre_save.connect(generate_users,sender=Generate_User)

def update_email(sender,instance,**kwargs):
	try:
		user = instance.user
		if user.email != "f" + instance.ID_no[0:3] + instance.ID_no[-4:-1] + "@goa.bits-pilani.ac.in":
			user.email = "f" + instance.ID_no[0:3] + instance.ID_no[-4:-1] + "@goa.bits-pilani.ac.in"
			user.first_name = instance.name
			user.save()

		if instance.message == 'Hello!':
			pass

		else:
			subject = "ARC BLUESLIP"
			from_email = settings.EMAIL_HOST_USER
			to_email = [user.email]
			print("To Email:",to_email)
			print("From:",from_email)

			text = "This is a test message.\nText and html."
			html = """
			<html>
			  <head></head>
			  <body>
			  <div style="background-color:#200;">
			    <p>This is a test message.</p>
			    <img src = "https://www.google.co.in/logos/doodles/2016/r-d-burmans-77th-birthday-4882888807940096.2-hp.png" alt="image">
			    <br>
			    <p>Text and HTML</p>
			    </div>
			  </body>
			</html>
			"""

			contact_message ="Dear,\n %s,%sFrom:\n %s \tcontact:%s"%(
				instance.name, 
				instance.message, 
				from_email,
				str("ARC_CONTACT"),)
			msg = EmailMessage(subject,contact_message,to=to_email)
			msg.send()
			msg.attach(content=text,mimetype='text/html')
			msg.attach(content=html,mimetype='text/html')

	except Exception as e:
		print(e)

signals.pre_save.connect(update_email,sender=Registered_User)



	
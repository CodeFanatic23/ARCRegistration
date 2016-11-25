from django import forms
from .models import *


class AddForm(forms.Form):
	
	lecture_no = forms.CharField(required=True,widget=forms.NumberInput(attrs={'min': '1', 'max': '20'}))
	tutorial_no = forms.CharField(required=True,widget=forms.NumberInput(attrs={'min': '1', 'max': '20'}))
	practical_no = forms.CharField(required=True,widget=forms.NumberInput(attrs={'min': '1', 'max': '20'}))

	# def checks(request):
	# 	no_of_adds = Checks.objects.get(id_no=request.user.id).no_of_adds
	# 	print(no_of_adds)

	# 	if no_of_adds > 5:
	# 		raise ValidationError("Cannot Add more than 5 courses")
		

class RemoveForm(forms.Form):
	
	def checks(request):
		no_of_removes = Checks.objects.get(id_no=request.user.id).no_of_adds
		if no_of_removes > 5:
			raise ValidationError("Cannot Add more than 5 courses")

class GeneralForm(forms.ModelForm):
	
	class Meta:
		model = Registered_User
		fields = [ 'semester', 'ID_no', 'name', 'phone_no']
		def __init__(self,*args,**kwargs):
			self.fields['phone_no'].widget = forms.NumberInput(attrs={'min':'1','max':'9999999999'})
			self.fields['phone_no'].label = "Contact Number"
			self.fields['ID_no'].label = "ID Number"
			super(GeneralForm, self).__init__(*args, **kwargs)

class ClashForm(forms.ModelForm):
	
	class Meta:
		model = Registered_User
		fields = ['ID_no']
		def __init__(self,*args,**kwargs):
			self.fields['ID_no'].label = "ID Number"
			super(ClashForm, self).__init__(*args, **kwargs)


class Generate_UserForm(forms.ModelForm):

	no_of_users_to_generate = forms.CharField(required=True)
	username_pattern = forms.CharField(required=False)
	class Meta:
		model = Generate_User
		fields = ['no_of_users_to_generate','username_pattern']


class RegistrationForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField(label="Email Address")
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm password")
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    gender = forms.ChoiceField(choices=((None, ''), ('F', 'Female'), ('M', 'Male'), ('O', 'Other')))
    receive_news = forms.BooleanField(required=False, label='I want to receive news and special offers')
    agree_toc = forms.BooleanField(required=True, label='I agree with the Terms and Conditions')


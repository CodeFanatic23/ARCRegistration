from django import forms
from .models import *

class AvailForm(forms.Form):
	CHOICES = (('1',1),
			('2',2),
			('3',3),
			('4',4))
	priority = forms.ChoiceField(choices=CHOICES,required=True)
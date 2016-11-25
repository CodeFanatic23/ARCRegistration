from django import forms
from .models import *

class UploadSheetForm(forms.ModelForm):
	description = forms.CharField(widget=forms.Textarea,required=False)
	class Meta:
 		model = Upload_file
 		widgets = {
 		'description':forms.Textarea(attrs={'cols': 150, 'rows': 20}),}
 		fields = ['Capacity','FD_Priority_number', 'HD_Priority_number','Time_Table_Semester_Wise','Registration_data',]
		
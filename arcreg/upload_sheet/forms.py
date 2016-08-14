from django import forms
from .models import *

class UploadSheetForm(forms.ModelForm):
	description = forms.CharField(widget=forms.Textarea)
	class Meta:
 		model = Upload_file
 		widgets = {
 		'description':forms.Textarea(attrs={'cols': 150, 'rows': 20}),}
 		fields = ['Capacity', 'Elective_list', 'FD_Priority_number', 'HD_Priority_number', 'Pre_requisite_senate', 'Time_Table_Semester_Wise','Registration_data',]
		
from django import forms
from ckeditor.widgets import CKEditorWidget
from assignment.models import Assignment, Submission

# Esta clase genera la 
# estructura del formulario 
# para crear nuevas tareas
class NewAssignmentForm(forms.ModelForm):
	title = forms.CharField(widget=forms.TextInput(attrs={'class': 'validate'}), required=True)
	content = forms.CharField(widget=CKEditorWidget())
	points = forms.IntegerField(max_value=100, min_value=1)
	due = forms.DateField(widget=forms.TextInput(attrs={'class': 'datepicker'}), required=True) 
	files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

	class Meta:
		model = Assignment
		fields = ('title', 'content', 'points', 'due', 'files')

# Esta clase genera la 
# estructura del formulario para 
# crear nuevas respuestas de tarea
class NewSubmissionForm(forms.ModelForm):
	file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': False}), required=True)

	class Meta:
		model = Submission
		fields = ('file',)
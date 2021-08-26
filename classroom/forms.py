from django import forms
from ckeditor.widgets import CKEditorWidget

from classroom.models import Course, Category, Grade,Submission


# Esta clase genera la estructura del formulario para crear nuevos cursos
class NewCourseForm(forms.ModelForm):
	picture = forms.ImageField(required=False)
	title = forms.CharField(widget=forms.TextInput(attrs={'class': 'validate'}), required=True)
	description = forms.CharField(widget=forms.TextInput(attrs={'class': 'validate'}), required=True)
	day = forms.ChoiceField(choices=Course.DAY_CHOICES, required=True)
	time_start = forms.TimeField(widget=forms.TimeInput(format='%H:%M'), required=True)
	time_end = forms.TimeField(widget=forms.TimeInput(format='%H:%M'), required=True)
	category = forms.ModelChoiceField(queryset=Category.objects.all())
	syllabus = forms.CharField()

	class Meta:
		model = Course
		fields = ('picture', 'title', 'description', 'day', 'time_start', 'time_end', 'category', 'syllabus')

# Esta clase genera la estructura del formulario para crear nuevas notas
class NewGradeForm(forms.ModelForm):
	grade = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'validate'}))

	class Meta:
		model = Grade
		fields = ('grade',)
# Esta clase genera la estructura del formulario para asignar notas de tareas
class PointsSubmissionForm(forms.ModelForm):
	points = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'validate'}))

	class Meta:
		model = Submission
		fields = ('points',)

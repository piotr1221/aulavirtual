from django import forms
from ckeditor.widgets import CKEditorWidget
from page.models import Page

# Esta clase genera la estructura
# del formulario para crear una nueva pagina
class NewPageForm(forms.ModelForm):
	title = forms.CharField(widget=forms.TextInput(attrs={'class': 'validate'}), required=True)
	content = forms.CharField(widget=CKEditorWidget())
	files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

	class Meta:
		model = Page
		fields = ('title', 'content', 'files')
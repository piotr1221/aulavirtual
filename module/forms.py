from django import forms
from module.models import Module

# Esta clase genera la estructura
# del formulario para crear un nuevo modulo
class NewModuleForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'validate'}), required=True)
    hours = forms.CharField(widget=forms.TextInput(attrs={'class': 'validate'}), required=True)

    class Meta:
        model = Module
        fields = ('title', 'hours',)

from django import forms
from .models import ProjectVersion

class ProjectVersionForm(forms.ModelForm):
    class Meta:
        model = ProjectVersion
        fields = ['version']

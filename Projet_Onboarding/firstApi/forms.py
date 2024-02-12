from django import forms
from .models import ProjectVersion , Event
from datetime import datetime


class ProjectVersionForm(forms.ModelForm):
    class Meta:
        model = ProjectVersion
        fields = ['version']

class EventForm(forms.ModelForm):
                class Meta:
                    model = Event
                    fields = ['user_group', 'event', 'userinfo', 'feature', 'action_type']
            
                def save(self, commit=True):
                    event = super().save(commit=False)
                    event.created = datetime.now()
                    if commit:
                        event.save()
                    return event
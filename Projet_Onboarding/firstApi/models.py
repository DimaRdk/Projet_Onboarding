from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

class ProjectVersion (models.Model):
    version = models.CharField(max_length=10)
    def __str__(self) -> str:
        return self.version


    
    
class Event(models.Model):
    user= models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    user_group = models.CharField(max_length=255)
    event = models.CharField(max_length=255)
    created = models.DateTimeField()
    userinfo = models.CharField(max_length=255, null=True, blank=True)
    feature = models.CharField(max_length=255)
    action_type = models.CharField(max_length=50, choices=[
                ('CREATE', 'CREATE'),
                ('DELETE', 'DELETE'),
                ('MODIF', 'MODIF'),
                ('ASKMEYA', 'ASKMEYA'),
                ('NAVIGATE', 'NAVIGATE'),
                ('CHOOSE', 'CHOOSE'),
                ('DISCONNECT', 'DISCONNECT')
            ])

    def __str__(self):
        return f"{self.user} - {self.event} - {self.created}"


    


from django.db import models



class ProjectVersion (models.Model):
    version = models.CharField(max_length=10)
    def __str__(self) -> str:
        return self.version


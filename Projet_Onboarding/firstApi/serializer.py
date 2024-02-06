from rest_framework import serializers
from .models import  ProjectVersion
from django.contrib.auth.models import User



class ProjectVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectVersion
        fields = ['version']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email'] 
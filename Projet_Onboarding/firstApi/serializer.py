from rest_framework import serializers
from .models import  ProjectVersion
from django.contrib.auth.models import User



class ProjectVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectVersion
        fields = ['version']

class UserCountSerializer(serializers.Serializer):
    users = serializers.SerializerMethodField()

    def get_users(self, obj):
        return {"count": obj['userCount']}
from rest_framework import serializers
from .models import  ProjectVersion
from django.contrib.auth.models import User



class ProjectVersionSerializer(serializers.ModelSerializer):
    version_verbose = serializers.SerializerMethodField()
    class Meta:
        model = ProjectVersion
        fields = ['version','version_verbose']

    def get_version_verbose(self, obj):
        # Récupère la phrase du contexte, avec une valeur par défaut si nécessaire
        return self.context.get('version_verbose', 'Version descriptive par défaut')


class UserCountSerializer(serializers.Serializer):
    users = serializers.SerializerMethodField()
    user_count_verbose = serializers.CharField(read_only=True)

    def get_users(self, obj):
        return {"count": obj.get('userCount')}
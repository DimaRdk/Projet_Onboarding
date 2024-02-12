from rest_framework import serializers
from .models import  ProjectVersion ,Event
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
    

class EventSerializer(serializers.ModelSerializer):

    user = serializers.CharField(required=False, allow_blank=True, max_length=100)
    class Meta:
        model = Event
        fields = ['user','user_group','event','created','userinfo','feature','action_type']
        read_only_fields = ['user']


    def create(self, validated_data):
        print(validated_data)
        if validated_data['user'] == '':
            user = None
        else:
            user = User.objects.get(id=validated_data['user'])
        event = Event.objects.create(
            user = user,
            user_group = validated_data['user_group'],
            event = validated_data['event'],
            created = validated_data['created'],
            userinfo = validated_data['userinfo'],
            feature = validated_data['feature'],
            action_type = validated_data['action_type']
            
            )
        return event
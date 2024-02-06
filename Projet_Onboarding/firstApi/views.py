from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .models import ProjectVersion
from .serializer import UserSerializer, ProjectVersionSerializer
from rest_framework import status




class ProjectVersionAPIView(APIView):
    def get(self, request):
        version = ProjectVersion.objects.last()  
        if version is None:
            return Response({'error': 'Project version not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProjectVersionSerializer(version)
        return Response(serializer.data)
    
class UserListAPIView(APIView):
    def get(self, request):
        users = User.objects.all()
        if users is None:
            return Response({'error': 'Users not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
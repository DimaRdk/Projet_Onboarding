from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .models import ProjectVersion
from .serializer import UserSerializer, ProjectVersionSerializer
from rest_framework import status
from django.shortcuts import render
from .forms import ProjectVersionForm
from django.shortcuts import redirect



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
    


def change_version_view(request):
    if request.method == 'POST':
        form = ProjectVersionForm(request.POST)
        if form.is_valid():
            
            version_instance, created = ProjectVersion.objects.update_or_create(
                id=1, 
                defaults={'version': form.cleaned_data['version']},
            )
            return redirect('firstApi:dashboard')  
    else:
        form = ProjectVersionForm()
        
        current_version = ProjectVersion.objects.first()
        if current_version:
            form = ProjectVersionForm(instance=current_version)

    return render(request, 'firstApi/change_version.html', {'form': form})


def dashboard_view(request):
    return render(request, 'firstApi/dashboard.html')

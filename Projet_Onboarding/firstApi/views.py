from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .models import ProjectVersion
from .serializer import UserCountSerializer, ProjectVersionSerializer
from rest_framework import status
from django.shortcuts import render
from .forms import ProjectVersionForm
from django.shortcuts import redirect
from rest_framework.reverse import reverse
from rest_framework.parsers import JSONParser
import requests
from django.contrib.auth.models import User

class ProjectVersionAPIView(APIView):
    def get(self, request):
        version = ProjectVersion.objects.last()  
        if version is None:
            return Response({'error': 'Project version not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProjectVersionSerializer(version)
        return Response(serializer.data)
    
class UserListAPIView(APIView):
      def get(self, request):
        user_count = User.objects.count()
      
        serializer = UserCountSerializer({'userCount': user_count})
        return Response(serializer.data)
    
    

def project_version_view(request):
    api_url = reverse('firstApi:project-version',request = request)
    response = requests.get(api_url)
    if response.status_code == 200:
        version_data = response.json()
        version = version_data.get('version', 'Inconnue')
    else:
        version = 'Erreur lors de la récupération de la version'

    return render(request, 'firstApi/display_version.html', {'version': version})


def project_user_view(request):
    api_url = reverse('firstApi:user-list',request = request)
    response = requests.get(api_url)
    if response.status_code == 200:
        count_data = response.json()
        count = count_data.get('users', {}).get('count', 'Inconnue')
    else:
        count = 'Erreur lors de la récupération du nombre d\'utilisateurs' 

    return render(request, 'firstApi/display_count.html', {'count': count})



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

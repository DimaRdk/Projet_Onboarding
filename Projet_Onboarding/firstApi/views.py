from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .models import ProjectVersion , Event
from .serializer import UserCountSerializer, ProjectVersionSerializer, EventSerializer
from rest_framework import status
from django.shortcuts import render
from .forms import ProjectVersionForm , EventForm
from django.shortcuts import redirect
from rest_framework.reverse import reverse
import requests
from django.contrib.auth.models import User 
from llm_core.assistants import OpenAIAssistant , Analyst
from dataclasses import dataclass
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .permissions import IsUserAllowedToAccessUsers, IsUserAllowedToAccessVersion,IsUserAllowedToGetEvents , IsUserAllowedToPostEvent
from rest_framework.authtoken.models import Token
import json

model = "gpt-3.5-turbo-0613"
assistant = OpenAIAssistant


@dataclass
class VersionRequette:
    system_prompt  = "You are a system helper"
    prompt = "Write me a short, professional sentence to present the project version | I need you to answear me in {lang} |  the actual version is {version}"
    version_verbose: str



@dataclass 
class UserCountRequette:
    system_prompt  = "You are a system helper"
    prompt = "Write me a short, professional sentence to present number of users | I need you to answear me in {lang} |  the actual number of users is {user_count} "
    user_count_verbose: str


class EventView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsUserAllowedToPostEvent]
    def post(self, request):
       
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventListAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsUserAllowedToGetEvents]
    def get(self, request, format=None):
        data = json.loads(request.body)
        request_type = data.get('request')
        user = data.get('user')
        date = data.get('date')
        event = data.get('event')
        action_type  = data.get('action_type')

        queryset = Event.objects.all()

        if request_type == 'all':
            pass
        elif request_type == 'user':
            queryset = queryset.filter(user=user)
        elif request_type == 'date':
            queryset = queryset.filter(created__date=date)
        elif request_type == 'event':
            queryset = queryset.filter(event=event)
        elif request_type == 'action_type':
            queryset = queryset.filter(action_type=action_type)
        else:
            return Response({'error': 'Invalid request type'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = EventSerializer(queryset, many=True)
        return Response(serializer.data)


class ProjectVersionAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsUserAllowedToAccessVersion]
    def get(self, request):
        version = ProjectVersion.objects.last()  
        if version is None:
            return Response({'error': 'Project version not found'}, status=status.HTTP_404_NOT_FOUND)
        
        with OpenAIAssistant(VersionRequette,model) as assistant:
            resp = assistant.process(version=version.version, lang="en")
        version_verbose = resp.version_verbose
        serializer = ProjectVersionSerializer(version, context={'version_verbose': version_verbose})
        return Response(serializer.data)
    
class UserListAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsUserAllowedToAccessUsers]
    def get(self, request):
        user_count = User.objects.count()
        

        analyst = Analyst(model , assistant)

        query="Write me a short, professional sentence to present number of users | I need you to answear me in the context language"
        context = {"user_count": user_count,
                   "language": "en"}
        user_count_verbose = analyst.ask(query, context)

        # with OpenAIAssistant(UserCountRequette, model) as assistant:
        #     resp = assistant.process(user_count=user_count, lang="fr")
        # user_count_verbose = resp.user_count_verbose

        serializer = UserCountSerializer({
            'userCount': user_count,
            'user_count_verbose': user_count_verbose.content
        })
        return Response(serializer.data)
    

def project_version_view(request):
    api_url = reverse('firstApi:project-version', request=request)
    token = Token.objects.get(user=request.user).key
    headers = {'Authorization': f'Token {token}'}
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        version_data = response.json()
        version = version_data.get('version_verbose', 'Inconnue')
    else:
        version = "You have not access to this data"

    return render(request, 'firstApi/display_version.html', {'version': version})

def project_user_view(request):
    api_url = reverse('firstApi:user-list', request=request)
    token = Token.objects.get(user=request.user).key
    
    headers = {'Authorization': f'Token {token}'}
    response = requests.get(api_url, headers=headers)
    print(response.status_code)
    if response.status_code == 200:
        count_data = response.json()
        count = count_data.get('user_count_verbose', 'Inconnue')
    else:
        count = f"You have not access to this data "

    return render(request, 'firstApi/display_count.html', {'count': count})




def change_version_view(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You have not access to this form")

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



def create_event(request):
        if not request.user.is_superuser:
            return HttpResponseForbidden("You have not access to this form")
        if request.method == 'POST':
            form = EventForm(request.POST)
            if form.is_valid():
                event = form.save(commit=False)
                event.user = request.user
                event.save()
                return redirect('firstApi:dashboard')
        else:
            form = EventForm()
        return render(request, 'firstApi/create_event.html', {'form': form})

       


def dashboard_view(request):
    return render(request, 'firstApi/dashboard.html')

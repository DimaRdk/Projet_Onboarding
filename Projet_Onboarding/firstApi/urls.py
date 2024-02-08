from django.urls import path
from .views import UserListAPIView, ProjectVersionAPIView , dashboard_view , change_version_view , project_version_view , project_user_view
from rest_framework.authtoken import views

app_name = "firstApi"
urlpatterns = [
    
    
    path('', dashboard_view, name='dashboard'),
    path('api-token-auth/', views.obtain_auth_token, name='api_token_auth'),
    path('disp-statistics', project_user_view, name='project-user'),
    path('disp-version/',project_version_view, name='disp-version'),
    path('statistics/', UserListAPIView.as_view(), name='user-list'),
    path('version/', ProjectVersionAPIView.as_view(), name='project-version'),
    path('change-version/', change_version_view, name='change-version'),
]
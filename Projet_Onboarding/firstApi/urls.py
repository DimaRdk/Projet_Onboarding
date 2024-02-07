from django.urls import path
from .views import UserListAPIView, ProjectVersionAPIView , dashboard_view , change_version_view , project_version_view , project_user_view
app_name = "firstApi"
urlpatterns = [
    
    
    path('', dashboard_view, name='dashboard'),
    path('statistics', project_user_view, name='project-user'),
    path('version/',project_version_view, name='disp-version'),
    path('get-users/', UserListAPIView.as_view(), name='user-list'),
    path('get-version/', ProjectVersionAPIView.as_view(), name='project-version'),
    path('change-version/', change_version_view, name='change-version'),
]
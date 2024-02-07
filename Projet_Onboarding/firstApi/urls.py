from django.urls import path
from .views import UserListAPIView, ProjectVersionAPIView , dashboard_view , change_version_view , project_version_view , project_user_view
app_name = "firstApi"
urlpatterns = [
    
    
    path('', dashboard_view, name='dashboard'),
    path('user/', project_user_view, name='project-user'),
    path('dispversion/',project_version_view, name='disp-version'),
    path('users/', UserListAPIView.as_view(), name='user-list'),
    path('version/', ProjectVersionAPIView.as_view(), name='project-version'),
    path('change-version/', change_version_view, name='change-version'),
]
from django.urls import path
from .views import UserListAPIView, ProjectVersionAPIView

urlpatterns = [
    # Ajoutez vos autres URL ici
    path('users/', UserListAPIView.as_view(), name='user-list'),
    path('version/', ProjectVersionAPIView.as_view(), name='project-version'),
]
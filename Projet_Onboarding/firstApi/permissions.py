from rest_framework.permissions import BasePermission


class IsUserAllowedToAccessUsers(BasePermission):
   

    def has_permission(self, request, view):
        
        return request.user.is_superuser or request.user.has_perm('auth.view_user')
    
class IsUserAllowedToAccessVersion(BasePermission):
   

    def has_permission(self, request, view):
        
        return request.user.is_superuser or request.user.has_perm('firstApi.view_projectversion')
    

class IsUserAllowedToPostEvent(BasePermission):

    def has_permission(self, request, view):

        return request.user.is_superuser or request.user.has_perm('firstApi.add_event')


class IsUserAllowedToGetEvents(BasePermission):

    def has_permission(self, request, view):

        return request.user.is_superuser or request.user.has_perm('firstApi.view_event')
from rest_framework import permissions

class AdminOrReadOnly(permissions.IsAdminUser):
    def has_permission(self,request,view):
        if request.method in permissions.SAFE_METHODS:
            return True
        # if request.method is get then true
        else:
            return bool(request.user and request.user.is_staff)
class ReviewUserOrReadOnly(permissions.BasePermission):
    def has_object_permission(self,request,view,obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # if request.method is get then true
        else:
            return obj.review_user  == request.user
        
        # logged in user and review user is same
            
        
        
        
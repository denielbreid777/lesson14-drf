from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAuthor(BasePermission):
    def has_object_permission(self,request,view,obj):
        if request.method in SAFE_METHODS:
            return True
        
        return obj.user == request.user
    
class IsModerated(BasePermission):
    def has_object_permission(self, request, view, obj):
            if obj.is_visible != False:
                return True

class IsCartOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        
        return obj.cart.user == request.user
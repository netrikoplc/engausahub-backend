from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsStudentRetrieve(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        ALLOWED_METHODS = ["GET"]
        if request.user == obj.user and request.method in ALLOWED_METHODS:
            return True
        return False

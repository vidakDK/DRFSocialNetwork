from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # allow logged-in normal user to view own details, allows super-user to view all records
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.creator == request.user

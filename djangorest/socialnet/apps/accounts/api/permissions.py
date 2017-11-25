from rest_framework import permissions


class IsSuperOrNormalUser(permissions.BasePermission):
    def has_permission(self, request, view):
        # allow user to access all users if it's a super-user
        return view.action == 'retrieve' or request.user.is_staff

    def has_object_permission(self, request, view, obj):
        # allow logged-in normal user to view own details, allows super-user to view all records
        return request.user.is_staff or obj == request.user

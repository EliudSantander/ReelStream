from rest_framework import permissions


class IsSelf(permissions.BasePermission):
    """
    Verify self identity of an user
    """

    def has_object_permission(self, request, view, obj):
        return obj == request.user


class IsNotAuthenticated(permissions.BasePermission):
    """
    Allow access only to not authenticated users
    """

    def has_permission(self, request, view):
        return not request.user.is_authenticated

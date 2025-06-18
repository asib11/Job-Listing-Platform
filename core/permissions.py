from rest_framework import permissions
from core.choices import RoleChoices


class IsRecruiter(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and request.user.role == RoleChoices.RECRUITER
        )


class IsCandidate(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and request.user.role == RoleChoices.CANDIDATE
        )


class IsOwnerOrRecruiter(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.role == RoleChoices.RECRUITER:
            return True
        return hasattr(obj, 'user') and obj.user == request.user

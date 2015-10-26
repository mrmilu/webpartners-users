from rest_framework import permissions


class IsAdminOrIsSelf(permissions.BasePermission):
    message = 'Check the authenticated user is admin or self.'

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or request.user.pk == obj.pk

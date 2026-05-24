from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Права на изменения только у администратора, у остальных только чтение.
    """
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated and request.user.is_admin)
        )

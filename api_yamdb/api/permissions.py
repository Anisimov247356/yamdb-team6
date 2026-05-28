"""Permission for app api."""

from rest_framework.permissions import SAFE_METHODS, BasePermission


ADMIN = 'admin'
MODERATOR = 'moderator'
USER = 'user'

def is_admin(user):
    """
    Функция проверки: является ли пользователь суперпользователем или имеет
    права администратора.

    """
    return user.is_authenticated and (
        user.is_superuser or getattr(user, 'role', None) == ADMIN)


def is_moderator(user):
    """
    Функция проверки: является ли пользователь модератором.

    """
    return user.is_authenticated and getattr(user, 'role', None) == MODERATOR


def is_authenticated_user(user):
    """
    Функция проверки: прошел ли пользователь аутентификацию.

    """
    return bool(user and user.is_authenticated)


class BaseReadOnlyPermission(BasePermission):
    """Базовый класс для разрешений с доступом на чтение всем."""

    def has_permission(self, request, view):
        """Разрешение всех безопасныех HTTP-методов (GET, HEAD, OPTIONS)."""
        return request.method in SAFE_METHODS


class IsAdmin(BasePermission):
    """Права администратора. Только пользователи с правами администратора
    (суперпользователь или роль 'admin') могут выполнять любые действия.

    """

    def has_permission(self, request, view):
        """Проверка права администратора у пользователя."""
        return is_admin(request.user)


class IsAdminOrReadOnly(BaseReadOnlyPermission):
    """Чтение всем, а редактирование только администратору.
        - GET, HEAD, OPTIONS — разрешено всем;
        - POST, PUT, PATCH, DELETE — только администраторы.

    """

    def has_permission(self, request, view):
        if super().has_permission(request, view):
            return True
        return is_admin(request.user)


class IsAuthenticatedOrReadOnly(BaseReadOnlyPermission):
    """Чтение всем, а создание/изменение только авторизованным пользователям.
        - GET, HEAD, OPTIONS — разрешено всем;
        - POST, PUT, PATCH, DELETE — только авторизованные пользователи.

    """

    def has_permission(self, request, view):
        if super().has_permission(request, view):
            return True
        return is_authenticated_user(request.user)


class IsAuthorModeratorOrAdmin(BaseReadOnlyPermission):
    """
    Права на редактирование автору, модератору и администратору.
        - Автор: может редактировать и удалять только свои объекты.
        - Модератор: может выполнять любые действия с любым объектом.
        - Администратор: полный доступ.
        - Остальные: только чтение.

    """

    def has_permission(self, request, view):
        """
        Проверяет аутентификацию пользователя и разрешает безопасные методы.

        """
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        """Проверяет права на уровне объекта."""
        # Текущий пользователь:
        user = request.user

        if request.method in SAFE_METHODS:
            return True

        # Проверка, является ли пользователь модератором или администратором:
        if is_admin(user) or is_moderator(user):
            return True

        # Только автор может изменять свой объект:
        author = getattr(obj, 'author', None)
        return author == user

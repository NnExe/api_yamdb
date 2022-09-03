from rest_framework import permissions
from users.models import User


class ReviewCommentPermissions(permissions.BasePermission):
    """
    Админ, суперадмин, модератор или автор могут всё, остальные только чтение.
    """
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.method == 'POST' and request.user.is_authenticated
            or obj.author == request.user
            or request.user.role in [User.ADMIN, User.MODERATOR]
        )


class IsAdminOrSuperadmin(permissions.BasePermission):
    """
    Админ и суперадмин могут всё. Остальные ничего.
    """
    def has_permission(self, request, view):
        return request.user.is_superuser or request.user.role == User.ADMIN


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Проверка доступа пользователю.
    Админ и суперадмин могут изменять данные. Остальные только просматривать.
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (
                request.method in permissions.SAFE_METHODS
                or request.user.is_superuser
                or request.user.role == User.ADMIN
            )
        return request.method in permissions.SAFE_METHODS

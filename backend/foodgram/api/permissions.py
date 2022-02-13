from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    message = 'Изменение чужого контента запрещено!'

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                )


class FoodgramUsersPermission(permissions.BasePermission):
    message = 'Нет прав доступа!'

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated

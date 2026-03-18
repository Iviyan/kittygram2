from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Владелец может редактировать, остальные — только чтение."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        owner = getattr(obj, 'owner', None) or obj.trip.owner
        return owner == request.user

from rest_framework import permissions
from .utils.permissions import is_owner_or_admin


class EstProprietaireOuAdmin(permissions.BasePermission):
 
    def has_object_permission(self, request, view, obj):
        return is_owner_or_admin(request.user, obj)

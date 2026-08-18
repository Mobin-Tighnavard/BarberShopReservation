from rest_framework.permissions import BasePermission

class IsBarberShopManager(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.groups.filter(name="Barbershop manager").exists())
    # and request.user.is_superuser
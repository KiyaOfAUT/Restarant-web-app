from rest_framework.permissions import BasePermission


class MenuItemsAccess(BasePermission):
    message = '403 – Forbidden'

    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.groups.filter(name='Manager').exists()
        else:
            return True


class MenuItemAccess(BasePermission):
    message = '403 – Forbidden'

    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        else:
            return request.user.groups.filter(name='Manager').exists()


class CategoryAccess(BasePermission):
    message = '403 – Forbidden!'

    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        elif request.user.groups.filter(name='Admin').exists():
            return True
        else:
            return False


class CustomerOnly(BasePermission):
    message = '403 – Forbidden'

    def has_permission(self, request, view):
        if request.user.groups.filter(name='Admin').exists() or request.user.groups.filter(name='Manager').exists() or request.user.groups.filter(name='Delivery').exists():
            return False
        else:
            return True


class OrderAccess(BasePermission):
    message = '403 – Forbidden'

    def has_permission(self, request, view):
        if request.method == 'PUT' or request.method == 'DELETE':
            if request.user.groups.filter(name='Manager').exists():
                return True
            else:
                return False
        elif request.method == 'PATCH':
            if request.user.groups.filter(name='Manager').exists() or request.user.groups.filter(name='Delivery').exists():
                return True
            else:
                return False
        elif request.method == 'GET':
            return True
        else:
            return False


class AdminOnly(BasePermission):
    message = "403 - Forbidden"

    def has_permission(self, request, view):
        if request.user.groups.filter(name='Admin').exists():
            return True
        else:
            return False


class ManagerOnly(BasePermission):
    message = "403 - Forbidden"

    def has_permission(self, request, view):
        if request.user.groups.filter(name='Manager').exists():
            return True
        else:
            return False

from rest_framework.permissions import BasePermission


class UserPermission(BasePermission):

    def has_permission(self, request, view):
        """
        Indica si un usuario puede acceder a la vista que quiere
        :param request:
        :param view:
        :return:
        """
        from users.api import UserDetailAPI
        if request.method == "POST":
            return True
        if request.user.is_superuser:
            return True
        if isinstance(view, UserDetailAPI):
            return True
        return False

    def has_object_permission(self, request, view, obj):
        """
        Indica si un usuario puede realizar una operacion sobre un objeto obj
        :param request:
        :param view:
        :param obj:
        :return:
        """
        return request.user.is_superuser or request.user == obj

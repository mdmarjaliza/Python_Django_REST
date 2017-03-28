from django.utils import timezone
from rest_framework.permissions import BasePermission


class PostDetailPermission(BasePermission):
    def has_permission(self, request, view):
        """
        Indica si un usuario puede acceder a la vista que quiere
        :param request:
        :param view:
        :return:
        """
        from post.api import PostDetailAPI
        if request.user.is_superuser:
            return True
        if isinstance(view, PostDetailAPI):
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
        if request.user.is_superuser or request.user.username == obj.owner.username:
            return True
        if request.method == "GET":
            if obj.fec_publicacion <= timezone.now():
                return True
        else:
            return False

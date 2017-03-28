from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework.generics import CreateAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_202_ACCEPTED, \
    HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from users.permissions import UserPermission
from users.serializers import BlogsSerializer, UserSerializer


class BlogsListViewSet(ListModelMixin, GenericViewSet):
    """
    Endpoint que muestra el listado de blogs de la plataforma
    """
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    ordering_fields = ('username',)
    search_fields = ('username',)
    serializer_class = BlogsSerializer
    queryset = User.objects.all()


class SignupAPI(CreateAPIView):
    """
    Endpoint de creación de usuarios
    """
    permission_classes = (UserPermission,)

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailAPI(APIView):
    """
    Endpoint de detalle de un usuario
    """
    permission_classes = (UserPermission,)

    def get(self, request, blogger):
        user = get_object_or_404(User, username=blogger)
        self.check_object_permissions(request, user)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, blogger):
        user = get_object_or_404(User, username=blogger)
        self.check_object_permissions(request, user)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, blogger):
        user = get_object_or_404(User, username=blogger)
        self.check_object_permissions(request, user)
        user.delete()
        return Response(status=HTTP_204_NO_CONTENT)

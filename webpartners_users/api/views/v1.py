# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model

from rest_framework import exceptions
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from ..permissions.v1 import IsAdminOrIsSelf
from ..serializers.v1 import UserSerializer, UserCreateSerializer, UserChangePasswordSerializer


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    serializer_class_create = UserCreateSerializer
    serializer_class_change_password = UserChangePasswordSerializer
    permission_classes = (IsAuthenticated, IsAdminOrIsSelf, )

    def get_serializer_class(self):
        if self.action == 'create':
            return self.serializer_class_create
        elif self.action == 'change_password':
            return self.serializer_class_change_password
        return super(UserViewSet, self).get_serializer_class()

    def get_permissions(self):
        permissions_list = {
            'create': [],
            'destroy': (IsAdminUser, )
        }

        if self.action not in permissions_list.keys():
            permissions = (IsAuthenticated, IsAdminOrIsSelf, )
        else:
            permissions = permissions_list.get(self.action)

        return [permission() for permission in permissions]

    @detail_route(methods=['post'], permission_classes=[IsAdminOrIsSelf], url_path='change-password')
    def change_password(self, request, pk=None):
        serializer = self.get_serializer(instance=self.get_object(), data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response_serializer = self.serializer_class(instance=self.get_object())
        return Response(response_serializer.data, status=status.HTTP_200_OK)

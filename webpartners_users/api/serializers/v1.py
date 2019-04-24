# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name')


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'password')

    def validate_password(self, value):
        instance = User()
        instance.set_password(value)
        instance.clean()
        return instance.password


class UserChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('password', 'old_password')

    def validate_old_password(self, value):
        if self.instance:
            if not self.instance.check_password(value):
                raise ValidationError('Old password missmatch', code='old_password:invalid')
        return value

    def validate_password(self, value):
        instance = User()
        instance.set_password(value)
        instance.clean()
        return instance.password

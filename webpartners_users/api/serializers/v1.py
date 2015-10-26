# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from rest_framework import serializers
from ...models import User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True)
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name')


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

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

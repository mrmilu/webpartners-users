# -*- coding: utf-8 -*-
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from .settings import package_settings


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff,
                          is_active=True,
                          is_superuser=is_superuser,
                          date_joined=now,
                          **extra_fields)
        user.set_password(password)
        user.full_clean()
        user.save(using=self._db)
        return user

    def create_user(self, username=None, email=None, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, username=None, email=None, password=None, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)


@python_2_unicode_compatible
class AbstractUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(_('email address'), blank=True, unique=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        abstract = True
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __init__(self, *args, **kwargs):
        super(AbstractUser, self).__init__(*args, **kwargs)
        self._password = None

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        full_name = full_name.strip()
        if full_name == '':
            return self.email
        return full_name

    def __str__(self):
        return self.get_full_name()

    def get_short_name(self):
        return self.first_name

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password

    def clean(self):
        super(AbstractUser, self).clean()
        if self._password is not None:
            self.validate_password(self._password)

    @classmethod
    def validate_password(cls, raw_password):
        if 'MIN_LENGTH' in package_settings.PASSWORD_VALIDATION:
            validation = package_settings.PASSWORD_VALIDATION['MIN_LENGTH']
            if validation is not None and len(raw_password) < validation:
                raise ValidationError('Password must be at lest {} characters long'.format(validation), code='password:min_length')

        if 'NUMERIC_DISALLOWED' in package_settings.PASSWORD_VALIDATION:
            validation = package_settings.PASSWORD_VALIDATION['NUMERIC_DISALLOWED']
            if validation and raw_password.isdigit():
                raise ValidationError({'password:numeric_disallowed': "This password is entirely numeric."})

        if 'AT_LEAST_ONE_NUMBER' in package_settings.PASSWORD_VALIDATION:
            validation = package_settings.PASSWORD_VALIDATION['AT_LEAST_ONE_NUMBER']
            if validation:
                valid = any(char.isdigit() for char in raw_password)
                if not valid:
                    raise ValidationError({'password:number_not_found': "Password must have at least one number."})


class User(AbstractUser):
    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

# -*- coding: utf-8 -*-
from rest_framework.routers import DefaultRouter

from ..views.v1 import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)

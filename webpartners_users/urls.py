# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url, include
from .api.routers.v1 import router

urlpatterns = [
    url(r'^api-token-auth/', 'rest_framework_jwt.views.obtain_jwt_token', name='jwt_auth'),
    url(r'^api-token-refresh/', 'rest_framework_jwt.views.refresh_jwt_token', name='jwt_refresh'),
    url(r'^api-token-verify/', 'rest_framework_jwt.views.verify_jwt_token', name='jwt_verify'),
    url(r'^api/1.0/', include(router.urls, namespace='api-v1')),
]

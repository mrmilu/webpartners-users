# -*- coding: utf-8 -*-
from django.urls import path, re_path, include

from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from .api.routers.v1 import router

app_name = 'webpartners_users'

urlpatterns = [
    path('api-token-auth/', obtain_jwt_token, name='jwt_auth'),
    path('api-token-refresh/', refresh_jwt_token, name='jwt_refresh'),
    path('api-token-verify/', verify_jwt_token, name='jwt_verify'),
    path('api/1.0/', include((router.urls, 'webpartners_users'), namespace='api-v1')),
]

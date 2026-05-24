"""URL configuration for app api."""

from django.urls import include, path
from rest_framework import routers

from .views import SignUpViewSet, UserViewSet, TokenViewSet, UserMeView

app_name = 'api'

v1_router = routers.DefaultRouter()
v1_router.register(r'auth/signup', SignUpViewSet, basename='signup')
v1_router.register(r'auth/token', TokenViewSet, basename='token')
v1_router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/users/me/', UserMeView.as_view(), name='user_me'),
    path('v1/', include(v1_router.urls)),
]

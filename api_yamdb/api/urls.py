"""URL configuration for app api."""

from django.urls import include, path
from rest_framework import routers

from .views import (SignUpViewSet, UserViewSet, TokenViewSet, UserMeView,
                    CategoryViewSet, GenreViewSet, TitleViewSet,
                    ReviewViewSet, CommentViewSet)

app_name = 'api'

v1_router = routers.DefaultRouter()
v1_router.register(r'auth/signup', SignUpViewSet, basename='signup')
v1_router.register(r'auth/token', TokenViewSet, basename='token')
v1_router.register(r'users', UserViewSet, basename='users')
v1_router.register(r'categories', CategoryViewSet)
v1_router.register(r'genres', GenreViewSet)
v1_router.register(r'titles', TitleViewSet)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment'
)

urlpatterns = [
    path('v1/users/me/', UserMeView.as_view(), name='user_me'),
    path('v1/', include(v1_router.urls)),
]

"""URL configuration for app api."""

from django.urls import include, path
from rest_framework import routers

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, SignUpViewSet, TitleViewSet, TokenViewSet,
                    UserMeView, UserViewSet)


app_name = 'api'

v1_router = routers.DefaultRouter()
v1_router.register(r'users', UserViewSet, basename='users')
v1_router.register(r'categories', CategoryViewSet, basename='categories')
v1_router.register(r'genres', GenreViewSet, basename='genres')
v1_router.register(r'titles', TitleViewSet, basename='titles')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/auth/signup/', SignUpViewSet.as_view({'post': 'create'}), name='signup'),
    path('v1/auth/token/', TokenViewSet.as_view({'post': 'create'}), name='token'),
    path('v1/users/me/', UserMeView.as_view(), name='user_me'),
    path('v1/', include(v1_router.urls)),
]

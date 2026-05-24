"""ViewSet for app api."""

from django.contrib.auth import get_user_model
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.mixins import (CreateModelMixin)
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .permissions import IsAdmin
from .serializers import (SignUpSerializer, TokenSerializer, UserSerializer,
                          UserMeSerializer)

# Получаем кастомную модель пользователя:
User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """Просмотр и создание пользователей администратором."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'patch', 'delete']


class UserMeView(RetrieveUpdateAPIView):
    """Просмотр и редактирование профиля текущего пользователя."""

    serializer_class = UserMeSerializer
    # Только для авторизованных пользователей:
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class SignUpViewSet(CreateModelMixin, viewsets.GenericViewSet):
    """Регистрация нового пользователя."""

    permission_classes = (AllowAny,)
    serializer_class = SignUpSerializer

    def create(self, request, *args, **kwargs):
        """Метод переопределен для возвращения status 200."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {'email': user.email, 'username': user.username},
            status=status.HTTP_200_OK,
        )


class TokenViewSet(CreateModelMixin, viewsets.GenericViewSet):
    """Выдача токена."""

    permission_classes = (AllowAny,)
    serializer_class = TokenSerializer

    def create(self, request, *args, **kwargs):
        """Переопределение метода create для отправки необходимых статусов."""
        # Имя пользователя и код подтверждения из запроса:
        username = request.data.get('username')
        confirmation_code = request.data.get('confirmation_code')

        # Проверка наличия имя пользователя и кода подтверждения в запросе:
        if not username:
            return Response(
                {'username': ['Обязательное поле.']},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not confirmation_code:
            return Response(
                {'confirmation_code': ['Обязательное поле.']},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Поиск пользователя в БД:
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                {'detail': 'Пользователь не найден.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.get_serializer(
            data=request.data,
            context={'user': user},
        )
        serializer.is_valid(raise_exception=True)
        return Response(serializer.save(), status=status.HTTP_200_OK)

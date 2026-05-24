"""Serializers for app api."""

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Genre, Title
from .mixins import (CheckEmailMixin, CheckUsernameMixin,
                     SignUpValidationMixin, TokenValidationMixin)
from .utils import generate_confirmation_code, send_confirmation_email

# Получаем кастомную модель пользователя:
User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Category.
    """

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Genre.
    """

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализотор для чтония произведений."""

    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True, default=None)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating',
            'description', 'genre', 'category'
        )
        read_only_fields = fields


class TitleWriteSerializer(serializers.ModelSerializer):
    """
    Сериализатор для изменения произведений.
    """

    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_fields='slug',
        many=True
    )
    category = serializers.SlugRelatedField(
        quryset=Category.objects.all(),
        slug_field='slug'
    )

    class Meta:
        madel = Title
        fields = (
            'id', 'name', 'year', 'rating',
            'description', 'genre', 'category'
        )


class UserSerializer(CheckEmailMixin, CheckUsernameMixin,
                     serializers.ModelSerializer):
    """Сериализатор просмотра и создания пользователей администратором."""

    # Задаём выбор значений для role согласно модели, используя константу
    # и разрешаем PATCH:
    role = serializers.ChoiceField(
        choices=User.ROLE_CHOICES,
        required=False
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'role',
                  'bio')


class UserMeSerializer(CheckEmailMixin, CheckUsernameMixin,
                       serializers.ModelSerializer):
    """Сериализатор просмотра и редактир-ния профиля текущего пользователя."""

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'role',
                  'bio')
        read_only_fields = ('role',)


class SignUpSerializer(SignUpValidationMixin,
                       serializers.ModelSerializer):
    """Сериализатор регистрации нового пользователя."""

    class Meta:
        model = User
        fields = ('email', 'username')
        extra_kwargs: dict = {'email': {'validators': []},
                              'username': {'validators': []}}

    def create(self, validated_data):
        """Метод создания пользователя."""
        email = validated_data['email']
        username = validated_data['username']
        code = generate_confirmation_code()

        user, created = User.objects.get_or_create(
            username=username,
            defaults={'email': email}
        )
        if not created:
            user.email = email

        user.confirmation_code = code
        user.set_unusable_password()
        user.save()

        send_confirmation_email(email, code)
        return user


class TokenSerializer(TokenValidationMixin, serializers.Serializer):
    """Сериализатор выдачи токена."""

    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField()

    def create(self, validated_data):
        """Переопределяем метод для выдачи токена."""
        user = self.context['user']
        token = AccessToken.for_user(user)
        return {'token': str(token)}

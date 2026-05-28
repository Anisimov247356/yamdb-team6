"""Serializers for app api."""

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Comment, Genre, Review, Title

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
    """Сериализатор для чтения произведений."""

    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True, default=None)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year',
            'description', 'genre', 'category', 'rating'
        )


class TitleWriteSerializer(serializers.ModelSerializer):
    """
    Сериализатор для изменения произведений.
    """

    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year',
            'description', 'genre', 'category'
        )

    def validate_year(self, value):
        """Проверка года выпуска."""
        if not isinstance(value, int):
            raise serializers.ValidationError(
                'Год выпуска должен быть целым числом.'
            )
        return value

    def validate_name(self, value):
        """Проверка длины названия."""
        if len(value) > 256:
            raise serializers.ValidationError(
                'Название произведения не может быть длиннее 256 символов.'
            )
        return value


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


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для отзывов."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        """Запрещаем повторный отзыв при создании."""
        if self.context['request'].method == 'POST':
            title_id = self.context['view'].kwargs.get('title_id')
            author = self.context['request'].user
            if Review.objects.filter(
                title_id=title_id, author=author
            ).exists():
                raise serializers.ValidationError(
                    'Вы уже оставили отзыв на это произведение.'
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')

"""Validators for app api."""

from django.contrib.auth import get_user_model
import re
from rest_framework import serializers

# Получаем кастомную модель пользователя:
User = get_user_model()

# Формат символов для username:
USERNAME_REGEX = re.compile(r'^[\w.@+-]+\Z')


class CheckUsernameMixin:
    """Миксин для проверки имени пользователя."""

    def validate_username(self, username):
        """Проверка имени пользователя."""

        # Проверка значения поля username, 'me' запрещено по ТЗ:
        if username == 'me':
            raise serializers.ValidationError(
                'Имя пользователя "me" запрещено.')

        # Проверка формата username:
        if not USERNAME_REGEX.fullmatch(username):
            raise serializers.ValidationError(
                'Username должен соответствовать формату: ^[\\w.@+-]+\\Z'
            )

        # Проверяка уникальности username:
        if User.objects.filter(username=username).exists():
            if not (self.instance and self.instance.username == username):
                raise serializers.ValidationError(
                    'Пользователь с таким "username" уже существует.')
        return username


class CheckEmailMixin:
    """Миксин для проверки email."""

    def validate_email(self, email):
        """Проверка email."""

        # Проверяка уникальности email:
        if User.objects.filter(email=email).exists():
            if not (self.instance and self.instance.email == email):
                raise serializers.ValidationError(
                    'Пользователь с таким "email" уже существует.')
        return email


class SignUpValidationMixin:
    """Миксин для валидации регистрации."""

    def validate_username(self, username):
        """Проверка имени пользователя (без проверки уникальности)."""
        if username == 'me':
            raise serializers.ValidationError(
                'Имя пользователя "me" запрещено.')
        if not USERNAME_REGEX.fullmatch(username):
            raise serializers.ValidationError(
                'Username должен соответствовать формату: ^[\\w.@+-]+\\Z')
        return username

    def validate(self, data):
        """Сравнение с существующими пользователями перед регистрацией. """

        # Имя пользователя и email из запроса:
        email = data.get('email')
        username = data.get('username')

        # Ищем совпадения в БД:
        username_db = User.objects.filter(username=username).first()
        email_db = User.objects.filter(email=email).first()

        # Используем словарь для накопления совпадений с БД:
        errors = {}

        # username и email схожи с существующими пользователями:
        if username_db and email_db and (username_db.pk != email_db.pk):
            errors['username'] = ['Пользователь с таким username существует.']
            errors['email'] = ['Пользователь с таким email существует.']
            raise serializers.ValidationError(errors)

        # Только username существует:
        if username_db and username_db.email != email:
            errors['username'] = ['Пользователь с таким username существует.']
            raise serializers.ValidationError(errors)

        # Только email существует:
        if email_db and email_db.username != username:
            errors['email'] = ['Пользователь с таким email уже существует.']
            raise serializers.ValidationError(errors)

        return data


class TokenValidationMixin:
    """Миксин для валидации при выдаче токена."""

    def validate(self, data):
        """Валидация данных при выдаче токена."""
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {'username': 'Пользователь с таким username не найден.'}
            )

        if user.confirmation_code != confirmation_code:
            raise serializers.ValidationError(
                {'confirmation_code': 'Неверный код подтверждения.'}
            )

        self.context['user'] = user
        return data

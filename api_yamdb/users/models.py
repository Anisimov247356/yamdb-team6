"""Model for app user."""

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Модель пользователя."""
    # Определим поле email, как уникальное:
    email = models.EmailField('email', max_length=254, unique=True)
    # Поле для определения прав пользователей:
    role = models.CharField(
        max_length=20,
        blank=False,
        choices=(('user', 'Пользователь'),
                 ('moderator', 'Модератор'),
                 ('admin', 'Администратор'),),
        default='user',
        verbose_name='Пользовательская роль')
    # Поле для кода подтверждения:
    confirmation_code = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Код подтверждения')
    # Поле информации о пользователе:
    bio = models.TextField(
        blank=True,
        max_length=256,
        verbose_name='Биография'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

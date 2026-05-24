"""Model for app user."""

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Модель пользователя."""

    # Константа для выбора ролей — используем её в сериализаторе
    ROLE_CHOICES = (
        ('user', 'Пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор')
    )
    # Определим поле email, как уникальное:
    email = models.EmailField(max_length=254, unique=True,
                              verbose_name='email')
    # Поле для определения прав пользователей:
    role = models.CharField(
        max_length=20,
        blank=False,
        choices=ROLE_CHOICES,
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

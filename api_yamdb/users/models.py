"""Model for app user."""

from django.contrib.auth.models import AbstractUser
from django.db import models


USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

EMEIL_MAX_LENGTH = 254
ROLE_MAX_LENGTH = 20
CONFIRMATIN_CODE_MAX_LENGTH = 150
BIO_MAX_LENGTH = 266


class CustomUser(AbstractUser):
    """Модель пользователя."""

    # Константа для выбора ролей — используем её в сериализаторе
    ROLE_CHOICES = (
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор')
    )
    # Определим поле email, как уникальное:
    email = models.EmailField(max_length=EMEIL_MAX_LENGTH,
                              unique=True,
                              verbose_name='email')
    # Поле для определения прав пользователей:
    role = models.CharField(
        max_length=ROLE_MAX_LENGTH,
        blank=False,
        choices=ROLE_CHOICES,
        default=USER,
        verbose_name='Пользовательская роль')
    # Поле для кода подтверждения:
    confirmation_code = models.CharField(
        max_length=CONFIRMATIN_CODE_MAX_LENGTH,
        blank=True,
        verbose_name='Код подтверждения')
    # Поле информации о пользователе:
    bio = models.TextField(
        blank=True,
        max_length=BIO_MAX_LENGTH,
        verbose_name='Биография'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username

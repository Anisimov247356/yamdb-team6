"""Admin file for app users."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser

# Добавляем поля с электронной почтой и правами пользователя
# к стандартному набору полей (fieldsets) пользователя в админке.
UserAdmin.fieldsets += (
    ('Extra Fields', {'fields': ('role', 'confirmation_code',)}),
)
# Регистрируем модель пользователя в админке:
admin.site.register(CustomUser, UserAdmin)

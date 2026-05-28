"""utils for app api."""

import random
import string
from django.conf import settings
from django.core.mail import send_mail


def generate_confirmation_code(length=8):
    """Генерация кода подтверждения."""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))


def send_confirmation_email(email, code):
    """Отправка кода подтверждения на email."""
    send_mail(
        subject='Код подтверждения YaMDb',
        message=f'Ваш код подтверждения: {code}',
        from_email=settings.DEFAULT_FROM_EMAIL,  # 'yamdb_team6@ya.ru'
        recipient_list=[email],
        fail_silently=False,
    )

"""utils for app api."""

from django.core.mail import send_mail
import random
import string


def generate_confirmation_code(length=8):
    """Генерация кода подтверждения."""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))


def send_confirmation_email(email, code):
    """Отправка кода подтверждения на email."""
    send_mail(
        subject='Код подтверждения YaMDb',
        message=f'Ваш код подтверждения: {code}',
        from_email='yamdb_team6@ya.ru',
        recipient_list=[email],
        fail_silently=False,
    )

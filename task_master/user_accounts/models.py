from django.db import models
from encrypted_model_fields.fields import EncryptedCharField, EncryptedEmailField
from django.contrib.auth.models import User


# Create your models here.

class UserProfile(models.Model):
    """Для расширения данных пользователя."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='Пользователь')
    first_name = EncryptedCharField(max_length=50, verbose_name='Имя')
    last_name = EncryptedCharField(max_length=50, verbose_name='Фамилия')
    email = EncryptedEmailField(verbose_name='Электронная почта')


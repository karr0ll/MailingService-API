from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='Email')
    first_name = models.CharField(max_length=250, verbose_name='Имя', **NULLABLE)
    last_name = models.CharField(max_length=250, verbose_name='Фамилия', **NULLABLE)
    verification_code = models.CharField(max_length=256, verbose_name='Код проверки', **NULLABLE)

    # переопределение поля юзернейма
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.email}'
    class Meta:
        verbose_name = ('Пользователь')
        verbose_name_plural = ('Пользователи')



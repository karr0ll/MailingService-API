from django.db import models

# from mailings.models import Mailing
from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Customer(models.Model):
    first_name = models.CharField(max_length=255, verbose_name='Имя', **NULLABLE)
    last_name = models.CharField(max_length=255, verbose_name='Фамилия', **NULLABLE)
    email = models.EmailField(max_length=255, verbose_name='email', unique=False)
    comment = models.TextField(verbose_name='Комментарий', **NULLABLE)
    owner = models.ManyToManyField(User, verbose_name='Пользователь')
    # mailing = models.ManyToManyField(Mailing, verbose_name='Рассылка')

    def __str__(self):
        return f'{self.email} {self.first_name} {self.last_name}'

    class Meta:
        verbose_name = ('Клиент')
        verbose_name_plural = ('Клиенты')


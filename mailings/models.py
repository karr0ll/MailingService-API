from django.db import models

from customers.models import Customer
from users.models import User

NULLABLE = {'blank': True, 'null': True}

MAILING_STATUS_CHOICES = (
    ('created', 'СОЗДАНА'),
    ('enabled', 'АКТИВНА'),
    ('disabled', 'НЕАКТИВНА')
)

MAILING_PERIOD_CHOICES = (
    ('daily', 'Ежедневно'),
    ('weekly', 'Еженедельно'),
    ('monthly', 'Ежемесячно')

)


class Mailing(models.Model):
    subject = models.TextField(verbose_name='Тема рассылки')
    body = models.TextField(verbose_name='Содержание рассылки')
    customers = models.ManyToManyField(Customer, verbose_name='Клиенты')
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.subject}'

    class Meta:
        ordering = ["pk"]
        verbose_name = ('Рассылка')
        verbose_name_plural = ('Рассылки')


class MailingSettings(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    time = models.DateTimeField(verbose_name='Дата рассылки')
    interval = models.CharField(max_length=7, choices=MAILING_PERIOD_CHOICES, default='daily',
                                verbose_name='Периодичность')
    status = models.CharField(max_length=8, choices=MAILING_STATUS_CHOICES, default='active',
                              verbose_name='Статус рассылки')

    def __str__(self):
        return f'{self.time} {self.interval} {self.status}'

    class Meta:
        verbose_name = ('Настройка рассылки')
        verbose_name_plural = ('Настройки рассылки')
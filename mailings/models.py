from django.db import models

from customers.models import Customer
from users.models import User

NULLABLE = {'blank': True, 'null': True}

MAILING_STATUS_CHOICES = (
    ('created', 'Создана'),
    ('enabled', 'Активна'),
    ('disabled', 'Неактивна')
)

MAILING_PERIOD_CHOICES = (
    ('every_minute', 'Каждую минуту'),
    ('daily', 'Ежедневно'),
    ('weekly', 'Еженедельно'),
    ('monthly', 'Ежемесячно')

)


class Mailing(models.Model):
    subject = models.TextField(verbose_name='Тема рассылки')
    body = models.TextField(verbose_name='Содержание рассылки')
    customers = models.ManyToManyField(Customer, verbose_name='Клиенты')
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)

    start_time = models.DateTimeField(verbose_name='Дата начала рассылки', **NULLABLE)
    creation_date = models.DateTimeField(verbose_name='Дата создания', auto_now=True)
    interval = models.CharField(max_length=15, choices=MAILING_PERIOD_CHOICES, default='daily',
                                verbose_name='Периодичность')
    status = models.CharField(max_length=8, choices=MAILING_STATUS_CHOICES, default='enabled',
                              verbose_name='Статус рассылки')
    next_attempt = models.DateTimeField(verbose_name='Дата последней отправки', **NULLABLE)

    def __str__(self):
        return f'{self.subject}'

    class Meta:
        ordering = ["pk"]
        verbose_name = ('Рассылка')
        verbose_name_plural = ('Рассылки')


class Logs(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    last_attempt_time = models.DateTimeField(verbose_name='Последняя отправка рассылки', auto_now=True)
    status = models.CharField(max_length=6, verbose_name='Статус отправки рассылки')
    mailing = models.ForeignKey(Mailing, verbose_name='Рассылка', on_delete=models.CASCADE)
    error_message = models.TextField(verbose_name='Сообщение об ошибке', **NULLABLE)

    def __str__(self):
        return (f'{self.last_attempt_time} '
                f'{self.status} '
                f'{self.mailing} '
                f'{self.error_message}')

    class Meta:
        verbose_name = ('Лог')
        verbose_name_plural = ('Логи')

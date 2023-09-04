import datetime

from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Blog(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок', **NULLABLE)
    slug = models.CharField(max_length=250, verbose_name='Человекопонятный URL', **NULLABLE)
    content = models.TextField(verbose_name='Содержание', **NULLABLE)
    thumbnail = models.ImageField(upload_to='blog_images/', verbose_name='Изображение', **NULLABLE)

    # settings.py -> TIME_ZONE = 'Europe/Moscow'
    creation_date = models.DateTimeField(verbose_name='Дата создания', default=datetime.datetime.now())
    views_count = models.IntegerField(default=0, verbose_name='Количество просмотров')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = ('Запись в блоге')
        verbose_name_plural = ('Записи в блоге')
        ordering = ('-creation_date',)

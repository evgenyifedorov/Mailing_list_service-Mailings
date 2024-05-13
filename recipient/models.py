from django.db import models

NULLABLE = {'null': True, 'blank': True}


class Recipient(models.Model):
    email = models.EmailField(verbose_name='Почта', unique=True)
    name = models.CharField(max_length=100, verbose_name='Имя')
    description = models.TextField(verbose_name='Описание', **NULLABLE)

    def __str__(self):
        return f'{self.email} - {self.name}'

    class Meta:
        verbose_name = 'Получатель'
        verbose_name_plural = 'Получатели'

from django.db import models
from django.contrib.auth.models import User


# Расходы
class Costs(models.Model):
    CHOICES_COSTS = (
    ('Без категории', 'Без категории'),
    ('Комунальные услуги', 'Комунальные услуги'),
    ('Продуктовые покупки', 'Продуктовые покупки'),
    ('Товары для дома', 'Товары для дома'),
    ('Одежда, обувь, аксессуары', 'Одежда, обувь, аксессуары'),
    ('Образование', 'Образование'),
    ('Лекарства и медицина', 'Лекарства и медицина'),
    ('Автомобиль/транспорт', 'Автомобиль/транспорт'),
    ('Развлечения', 'Развлечения'),
    ('Хобби', 'Хобби'),
    ('Личные траты', 'Личные траты'),
        )
    content = models.CharField(max_length=25, choices=CHOICES_COSTS, default='Без категории',
                               verbose_name='Категория')
    title = models.CharField(max_length=40,blank=True, null=True, verbose_name='Комментарий')
    price = models.FloatField(default=0, verbose_name='Сумма')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    created_at = models.DateField(verbose_name='Дата')

    class Meta:
        verbose_name_plural = 'Записи о расходах'
        verbose_name = 'Расход'
        ordering = ['-created_at']


# Доходы
class Income(models.Model):
    CHOICES_INCOME = (
        ('Другое', 'Другое'),
        ('Аванс', 'Аванс'),
        ('Зарплата', 'Зарплата'),
        ('Социальные выплаты', 'Социальные выплаты'),)

    content = models.CharField(max_length=25, choices=CHOICES_INCOME, default='Другое',
                               verbose_name='Категория')
    title = models.CharField(max_length=40, blank=True, null=True, verbose_name='Комментарий')
    price = models.FloatField(default=0, verbose_name='Сумма')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    created_at = models.DateField(verbose_name='Дата')


    class Meta:
        verbose_name_plural = 'Записи о доходах'
        verbose_name = 'Доход'
        ordering = ['-created_at']

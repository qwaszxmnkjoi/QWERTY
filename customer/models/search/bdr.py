__all__ = ['Bdr', 'BdrElement']

from django.db import models

from .base import UserForeignKey


class Bdr(models.Model):
    user = UserForeignKey(related_name='bdr')
    plate = models.CharField(max_length=100, verbose_name='Номер ТЗ')
    document = models.CharField(max_length=100, verbose_name='Документ')
    date_start = models.DateTimeField(verbose_name='дата добавления',
                                      auto_now_add=True)
    status = models.BooleanField(default=False, verbose_name='статус')

    class Meta:
        verbose_name = 'БДР'
        verbose_name_plural = 'БДР'


class BdrElement(models.Model):
    bdr = models.ForeignKey(Bdr, on_delete=models.CASCADE, related_name='bdr_elem', verbose_name='БДР')
    number = models.CharField(max_length=300, verbose_name='номер постановления')
    link = models.URLField(verbose_name='ссылка')
    date = models.DateField(verbose_name='дата нарушения')
    pay = models.BooleanField(verbose_name='оплачен?')
    amount = models.FloatField(verbose_name='сумма штрафа')
    description = models.CharField(max_length=300, verbose_name='описание')
    date_add = models.DateTimeField(verbose_name='дата добавления', auto_now_add=True)

    class Meta:
        ordering = ['date']
        verbose_name = 'штраф'
        verbose_name_plural = 'штрафы'

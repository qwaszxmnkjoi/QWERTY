__all__ = ['Debtors', 'DebtorsElem', 'AsvpElem']

from functools import cached_property
from django.db import models

from .base import SearchForeignKey


class Debtors(models.Model):
    search = SearchForeignKey(related_name='debtors')
    subscribe = models.BooleanField(default=False, verbose_name='подписка?')

    class Meta:
        ordering = ['pk']
        verbose_name = 'должника'
        verbose_name_plural = 'должники'


class DebtorsElem(models.Model):
    debtors = models.ForeignKey(Debtors, on_delete=models.CASCADE, related_name='debtors_elem', verbose_name='должник')
    birth = models.DateField(verbose_name='дата рождения')
    publisher = models.CharField(max_length=300, verbose_name='документ выдан')
    connection = models.TextField(verbose_name='связь')
    number = models.CharField(max_length=100, verbose_name='ВП номер')
    deduction = models.CharField(max_length=300, verbose_name='Категория взысканий')

    class Meta:
        ordering = ['pk']
        verbose_name = 'долг'
        verbose_name_plural = 'долги'


class AsvpElem(models.Model):
    search = SearchForeignKey(related_name='asvp_elem')

    agency_edrpou = models.CharField(blank=True, null=True, max_length=300, verbose_name='ЕДРП исполнителя')
    agency = models.CharField(max_length=300, verbose_name='исполнитель')

    date_open = models.DateField(verbose_name='Дата открытия', blank=True, null=True)
    creditors_name = models.CharField(max_length=300, blank=True, null=True, verbose_name='коллектор')
    number = models.CharField(max_length=100, verbose_name='номер')

    debtors = models.CharField(max_length=300, blank=True, null=True, verbose_name='должник')
    birth = models.DateField(verbose_name='дата рождения', blank=True, null=True)

    status = models.CharField(max_length=100, verbose_name='статус')
    subscribe = models.BooleanField(default=False, verbose_name='подписка?')

    class Meta:
        ordering = ['pk']
        verbose_name = 'АСВП элемент'
        verbose_name_plural = 'АСВП элементы'

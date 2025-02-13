__all__ = ['Departure', 'DepartureElem']

from django.db import models

from .base import UserForeignKey


class Departure(models.Model):
    user = UserForeignKey(related_name='departure')

    days = models.IntegerField(default=0)
    subscribe = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'миграцию'
        verbose_name_plural = 'миграции'


class DepartureElem(models.Model):
    departure = models.ForeignKey(Departure, on_delete=models.CASCADE, related_name='dep_elem', verbose_name='миграция')
    date_of_entry = models.DateField(verbose_name='дата прибытия')
    date_of_departure = models.DateField(blank=True, null=True, verbose_name='дата убытия')

    class Meta:
        verbose_name = 'дату миграции'
        verbose_name_plural = 'даты миграции'
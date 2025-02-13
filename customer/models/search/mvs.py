__all__ = ['Mvs']

from django.db import models

from .base import SearchForeignKey


class Mvs(models.Model):
    search = SearchForeignKey(related_name='mvs')
    photo = models.URLField(verbose_name='фото')
    region = models.CharField(max_length=300, verbose_name='регион')
    category = models.CharField(max_length=300, verbose_name='категория')
    disappearance = models.DateField(verbose_name='дата исчезновения')
    accusations = models.CharField(max_length=300, verbose_name='статья обвинений')
    birth = models.DateField(verbose_name='др')
    precaution = models.CharField(max_length=300, verbose_name='мера пресечения')
    link = models.URLField(verbose_name='ссылка')
    subscribe = models.BooleanField(default=False, verbose_name='подписка?')

    class Meta:
        ordering = ['disappearance']
        verbose_name = 'МВС розыск'
        verbose_name_plural = 'МВС розыски'
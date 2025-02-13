__all__ = ['SavedSearch']

from functools import cached_property

from django.contrib.postgres.fields import ArrayField
from django.db import models

from .base import UserForeignKey
from ...enums import State


class SavedSearch(models.Model):
    user = UserForeignKey(related_name='saved_search')
    state = models.CharField(max_length=16, choices=State.as_model_choices(), default=State.NATIONAL.as_str, verbose_name='реестр')
    saved_data = ArrayField(models.CharField(max_length=250), verbose_name='Сохраненная информация')

    @cached_property
    def data_as_str(self) -> str:
        return ' '.join(self.saved_data)

    class Meta:
        verbose_name = 'Сохраненный поиск'
        verbose_name_plural = 'Сохраненные поиски'

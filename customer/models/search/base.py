__all__ = ['UserForeignKey', 'Search', 'SearchForeignKey']

from django.db import models

from ..user import User


class UserForeignKey(models.ForeignKey):
    def __init__(self, *args, **kwargs):
        kwargs['to'] = 'User'
        kwargs['on_delete'] = models.CASCADE
        kwargs['verbose_name'] = 'пользователь'
        super().__init__(*args, **kwargs)


class SearchForeignKey(models.ForeignKey):
    def __init__(self, *args, **kwargs):
        kwargs['to'] = 'Search'
        kwargs['on_delete'] = models.CASCADE
        kwargs['verbose_name'] = 'поисковый запрос'
        super().__init__(*args, **kwargs)


class Search(models.Model):
    user = UserForeignKey(related_name='search')
    name = models.CharField(max_length=100, verbose_name='имя')
    surname = models.CharField(max_length=100, verbose_name='фамилия')
    patronymic = models.CharField(max_length=100, verbose_name='отчество', blank=True, null=True)
    date_start = models.DateTimeField(verbose_name='дата добавления', auto_now_add=True)
    status = models.BooleanField(default=True, verbose_name='статус')

    @property
    def count_subs(self):
        return sum((
            self.court.filter(subscribe=True).count(), self.mvs.filter(subscribe=True).count(),
            self.asvp_elem.filter(subscribe=True).count()
        ))

    @property
    def get_full_name(self):
        return f'{self.surname} {self.name if self.name else ""} {self.patronymic if self.patronymic else ""}'

    class Meta:
        app_label = 'customer'
        ordering = ['pk']
        verbose_name = 'поиск'
        verbose_name_plural = 'поиски'

    def __str__(self):
        return f'{self.surname} {self.name} {self.patronymic} {self.date_start.date()}'


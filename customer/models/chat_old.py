from django.db import models

from .user import User


class Country(models.Model):
    name = models.CharField(max_length=200, verbose_name='название')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True,
                             null=True, verbose_name='создатель')

    class Meta:
        verbose_name = 'страну'
        verbose_name_plural = 'страны'

    def __str__(self):
        return self.name


class Chat(models.Model):
    country = models.ForeignKey(Country, on_delete=models.SET_NULL,
                                blank=True, null=True, verbose_name='страна')
    title = models.CharField(blank=True, null=True, max_length=100,
                             verbose_name='название')
    chat_id = models.CharField(max_length=300, verbose_name='Chat Id')

    class Meta:
        verbose_name = 'чат'
        verbose_name_plural = 'чаты'

    @property
    def get_country(self):
        return self.country.name if self.country else ''

    def __str__(self):
        return f'{self.get_country} {self.title} {self.chat_id}'


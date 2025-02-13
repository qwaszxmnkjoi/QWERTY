import typing

from functools import cached_property
from django.db import models

from ..enums import State, UserRole

LANGUAGE_OPTIONS = [('en', 'Англ'), ('ua', 'Укр'), ('ru', 'Рус')]


class User(models.Model):
    chat_id = models.CharField(max_length=200, verbose_name='Chat Id')
    username = models.CharField(max_length=100, blank=True, null=True,
                                verbose_name='username')
    language = models.CharField(max_length=10,
                                choices=LANGUAGE_OPTIONS, default='en',
                                verbose_name='Язык пользователя')
    name = models.CharField(blank=True, null=True, max_length=200,
                            verbose_name='имя')
    name_en = models.CharField(blank=True, null=True, max_length=200,
                               verbose_name='имя на англ')
    date_end = models.DateTimeField(blank=True, null=True,
                                    verbose_name='дата окончания подписки')
    date_register = models.DateTimeField(auto_now_add=True,
                                         verbose_name='дата регистрации')
    role = models.CharField(max_length=10, choices=UserRole.as_model_choices(), default='client',
                            verbose_name='тариф')
    subs_id = models.CharField(max_length=200, blank=True, null=True,
                               verbose_name='order_id последней оплаты')
    blocked = models.BooleanField(default=False, verbose_name='статус',
                                  choices=[(False, 'Активный'),
                                           (True, 'Заблокирован')])
    unsubscribe_news = models.BooleanField(default=False,
                                           verbose_name='отписан от новых '
                                                        'новостей?')

    tg_data = models.JSONField(blank=True, null=True)

    class Meta:
        ordering = ['date_register']
        verbose_name = 'пользователя'
        verbose_name_plural = 'пользователей'

    @cached_property
    def tg_lang(self):
        result = None
        if self.tg_data:
            result = self.tg_data.get("language_code")
        return result

    @cached_property
    def tg_name(self):
        result = None
        if self.tg_data:
            result = self.tg_data.get("first_name", '')
            if last_name := self.tg_data.get('last_name'):
                result += f' {last_name}'
        return result

    def build_save_btn(self, state: typing.Union[str, State]):
        from telebot.types import KeyboardButton
        result = None
        if isinstance(state, State):
            state = state.as_str
        if result_objs := list(self.saved_search.filter(state=state)):
            result = [[KeyboardButton(obj.data_as_str).to_dict()] for obj in result_objs]

        return result

    def __str__(self):
        return f'{self.chat_id} {self.name or self.tg_name} {self.language or self.tg_lang}'

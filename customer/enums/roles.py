import typing

from django.utils.translation import gettext_lazy as _

from Emigrant.utils import StrEnumBase


class UserRole(StrEnumBase):
    CLIENT = 'client'
    AGENT = 'agent'
    EXPERT = 'expert'
    SUPPORT = 'support'
    ADMIN = 'admin'

    @classmethod
    def as_choices(cls) -> typing.Tuple[typing.Tuple['StrEnumBase', str], ...]:
        return (
            (cls.CLIENT, _('Обычный')),
            (cls.AGENT, _('Свободный')),
            (cls.EXPERT, _('Полный')),
            (cls.SUPPORT, _('Тех.Поддержка')),
            (cls.ADMIN, _('Администратор')),
        )

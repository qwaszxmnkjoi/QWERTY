import typing

from django.utils.translation import gettext_lazy as _

from Emigrant.utils import StrEnumBase


class State(StrEnumBase):
    ASVP = 'asvp'
    BDR = 'bdr'
    COURT = 'court'
    COURT_ASSIGN = 'assign'
    DEBTORS = 'debtors'
    NATIONAL = 'national'
    WANTED = 'wanted'

    @classmethod
    def as_choices(cls) -> typing.Tuple[typing.Tuple['StrEnumBase', str], ...]:
        return (
            (cls.ASVP, _('Автоматизированая система исполнительного производства')),
            (cls.BDR, _('Штрафы ПДД')),
            (cls.COURT, _('Судебные дела')),
            (cls.COURT_ASSIGN, _('Cудебные рассмотрения')),
            (cls.DEBTORS, _('Должники')),
            (cls.NATIONAL, _('Все')),
            (cls.WANTED, _('Розыск')),
        )

    @classmethod
    def map_as_num(cls) -> typing.Dict['State', int]:
        return {
            cls.ASVP: 1,
            cls.BDR: 2,
            cls.COURT: 3,
            cls.COURT_ASSIGN: 4,
            cls.DEBTORS: 5,
            cls.NATIONAL: 6,
            cls.WANTED: 7
        }

    @property
    def as_num(self) -> int:
        return self.map_as_num()[self]

    @classmethod
    def from_num(cls, num: int) -> typing.Optional['State']:
        return next((a for a, a_num in cls.map_as_num().items() if a_num == num), None)

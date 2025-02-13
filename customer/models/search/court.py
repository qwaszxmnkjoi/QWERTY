__all__ = ['Court', 'CourtElement', 'CourtAssignment', 'AssignmentElem']

from django.db import models

from .base import SearchForeignKey


class Court(models.Model):
    search = SearchForeignKey(related_name='court')
    number = models.CharField(max_length=300, verbose_name='номер дела')
    code = models.CharField(max_length=150, verbose_name='код дела')
    court = models.CharField(max_length=300, verbose_name='Суд')
    claimant = models.TextField(verbose_name='стороны спора')
    date = models.DateField(verbose_name='Дата')
    subscribe = models.BooleanField(default=False, verbose_name='подписка?')

    @property
    def form(self):
        return self.court_elem.last().form if self.court_elem.last() else '-'

    class Meta:
        ordering = ['date']
        verbose_name = 'судебное дело'
        verbose_name_plural = 'судебные дела'

    def __str__(self):
        return f'{self.number} - {self.search.surname}'


class CourtElement(models.Model):
    court = models.ForeignKey(Court, on_delete=models.CASCADE, related_name='court_elem', verbose_name='судебное дело')
    date_approval = models.DateField(verbose_name='дата принятие решение')
    number = models.CharField(max_length=300, verbose_name='номер решения')
    chairmen = models.CharField(max_length=300, verbose_name='судья')
    form = models.CharField(max_length=300, verbose_name='форма судебного решения')
    court_type = models.CharField(max_length=300, verbose_name='форма судопроизводства')
    link = models.URLField(verbose_name='ссылка')

    class Meta:
        ordering = ['date_approval']
        verbose_name = 'судебное решение'
        verbose_name_plural = 'судебные решения'

    def __str__(self):
        return f'{self.form} {self.number} ({self.date_approval})'


class CourtAssignment(models.Model):
    search = SearchForeignKey(related_name='court_assign')
    subscribe = models.BooleanField(default=False, verbose_name='подписка?')

    class Meta:
        ordering = ['pk']
        verbose_name = 'Поиск Судебного рассмотрения'
        verbose_name_plural = 'Поиск Судебных рассмотрений'

    def __str__(self):
        return f'{str(self.search)} [is_subscribe={self.subscribe}]'


class AssignmentElem(models.Model):
    court_assign = models.ForeignKey(CourtAssignment, on_delete=models.CASCADE, related_name='assign_elem', verbose_name='Cудебное рассмотрение')
    court = models.ForeignKey(
        Court,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='assignment',
        verbose_name='Cудебное дело'
    )
    dt_meet = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Назначенная дата'
    )
    judges = models.TextField(verbose_name='Состав судейтсва')
    number = models.CharField(verbose_name='Номер Дела', max_length=300)
    name_court = models.TextField(verbose_name='Название Суда')
    room_court = models.TextField(verbose_name='Зал судебных заседаний')
    involved = models.TextField(verbose_name='Стороны по делу')
    description = models.TextField(verbose_name='Суть Дела')
    address = models.TextField(verbose_name='Адрес')

    class Meta:
        ordering = ['dt_meet']
        verbose_name = 'Cудебное рассмотрение'
        verbose_name_plural = 'Судебные рассмотрения'

    def __str__(self):
        return f'{str(self.court_assign)} [number={self.number} dt={self.dt_meet}]'


from django.db import models

from .user import User


class Departure(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    days = models.IntegerField(default=0)
    subscribe = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'миграцию'
        verbose_name_plural = 'миграции'


class DepartureElem(models.Model):
    departure = models.ForeignKey(Departure, on_delete=models.CASCADE,
                                  related_name='dep_elem',
                                  verbose_name='миграция')
    date_of_entry = models.DateField(verbose_name='дата прибытия')
    date_of_departure = models.DateField(blank=True, null=True,
                                         verbose_name='дата убытия')

    class Meta:
        verbose_name = 'дату миграции'
        verbose_name_plural = 'даты миграции'


class Search(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='пользователь')
    name = models.CharField(max_length=100, verbose_name='имя')
    surname = models.CharField(max_length=100, verbose_name='фамилия')
    patronymic = models.CharField(max_length=100, verbose_name='отчество', blank=True, null=True)
    date_start = models.DateTimeField(verbose_name='дата добавления', auto_now_add=True)
    status = models.BooleanField(default=True, verbose_name='статус')

    @property
    def count_subs(self):
        return self.court.filter(subscribe=True).count() + \
            self.mvs.filter(subscribe=True).count() + sum(
                x.minjust_fop.filter(subscribe=True).count() +
                x.minjust_company.filter(subscribe=True).count() for x in
                self.minjust.all()) + sum(x.count_subs_asvp for x in
                                          self.debtors.all())

    @property
    def get_full_name(self):
        return f'{self.surname} {self.name if self.name else ""} ' \
               f'{self.patronymic if self.patronymic else ""}'

    class Meta:
        ordering = ['pk']
        verbose_name = 'поиск'
        verbose_name_plural = 'поиски'

    def __str__(self):
        return f'{self.surname} {self.name} {self.patronymic} ' \
               f'{self.date_start.date()}'


class Bdr(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='пользователь')
    plate = models.CharField(max_length=100, verbose_name='Номер ТЗ')
    document = models.CharField(max_length=100, verbose_name='Документ')
    date_start = models.DateTimeField(verbose_name='дата добавления',
                                      auto_now_add=True)
    status = models.BooleanField(default=False, verbose_name='статус')

    class Meta:
        verbose_name = 'БДР'
        verbose_name_plural = 'БДР'


class BdrElement(models.Model):
    bdr = models.ForeignKey(Bdr, on_delete=models.CASCADE,
                            related_name='bdr_elem',
                            verbose_name='БДР')
    number = models.CharField(max_length=300,
                              verbose_name='номер постановления')
    link = models.URLField(verbose_name='ссылка')
    date = models.DateField(verbose_name='дата нарушения')
    pay = models.BooleanField(verbose_name='оплачен?')
    amount = models.FloatField(verbose_name='сумма штрафа')
    description = models.CharField(max_length=300, verbose_name='описание')
    date_add = models.DateTimeField(verbose_name='дата добавления',
                                    auto_now_add=True)

    class Meta:
        ordering = ['date']
        verbose_name = 'штраф'
        verbose_name_plural = 'штрафы'


class Court(models.Model):
    search = models.ForeignKey(Search, on_delete=models.CASCADE,
                               related_name='court',
                               verbose_name='поисковый запрос')
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
    court = models.ForeignKey(Court, on_delete=models.CASCADE,
                              related_name='court_elem',
                              verbose_name='судебное дело')
    date_approval = models.DateField(verbose_name='дата принятие решение')
    number = models.CharField(max_length=300, verbose_name='номер решения')
    chairmen = models.CharField(max_length=300, verbose_name='судья')
    form = models.CharField(max_length=300,
                            verbose_name='форма судебного решения')
    court_type = models.CharField(max_length=300,
                                  verbose_name='форма судопроизводства')
    link = models.URLField(verbose_name='ссылка')

    class Meta:
        ordering = ['date_approval']
        verbose_name = 'судебное решение'
        verbose_name_plural = 'судебные решения'

    def __str__(self):
        return f'{self.form} {self.number} ({self.date_approval})'


class Mvs(models.Model):
    search = models.ForeignKey(Search, on_delete=models.CASCADE,
                               related_name='mvs',
                               verbose_name='поисковый запрос')
    photo = models.URLField(verbose_name='фото')
    region = models.CharField(max_length=300, verbose_name='регион')
    category = models.CharField(max_length=300, verbose_name='категория')
    disappearance = models.DateField(verbose_name='дата исчезновения')
    accusations = models.CharField(max_length=300,
                                   verbose_name='статья обвинений')
    birth = models.DateField(verbose_name='др')
    precaution = models.CharField(max_length=300,
                                  verbose_name='мера пресечения')
    link = models.URLField(verbose_name='ссылка')
    subscribe = models.BooleanField(default=False, verbose_name='подписка?')

    class Meta:
        ordering = ['disappearance']
        verbose_name = 'МВС розыск'
        verbose_name_plural = 'МВС розыски'


class InactiveDocument(models.Model):
    DOC_TYPE = (
        ('2', 'ID Паспорт'),
        ('1', 'Паспорт Украины в виде книги'),
        ('3', 'Загран Паспорт'),
        ('5', 'Временное удостоверение гражданина Украины'),
        ('6', 'Удостоверение лица без гражданства для выезда за границу'),
        ('8', 'Удостоверение на временное жительство'),
        ('16', 'Удостоверение на временное жительство (биометрическое)'),
        ('7', 'Удостоверение на постоянное жительство'),
        ('15', 'Удостоверение на постоянное жительство (биометрическое)'),
        ('10', 'Удостоверение беженца'),
        ('11', 'Проездной документ беженца'),
        ('12', 'Удостоверение личности, которая нуждается в дополнительной '
               'защите'),
        ('13', 'Проездной документ лица, которому предоставлена '
               'дополнительная защита'),
        ('14', 'Проездной документ ребенка'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='inactive_doc',
                             verbose_name='пользователь')
    type_doc = models.CharField(max_length=5, verbose_name='тип документа',
                                choices=DOC_TYPE)
    series = models.CharField(max_length=50, blank=True, null=True,
                              verbose_name='серия документа')
    number = models.CharField(max_length=50, verbose_name='номер документа')
    status = models.BooleanField(blank=True, null=True, verbose_name='статус')
    description = models.TextField(verbose_name='текст')
    subscribe = models.BooleanField(default=False, verbose_name='подписка?')

    class Meta:
        verbose_name = 'неактивный документ'
        verbose_name_plural = 'неактивные документы'

    def __str__(self):
        return '{} {}{}'.format(self.get_type_doc_display(), self.series if
        self.series else '', self.number)


class DocState(models.Model):
    DOC_TYPE = (
        ('zp', 'Загран Паспорт'),
        ('id', 'ID Паспорт'),
        ('tt', 'Удостоверение на временное жительство'),
        ('tp', 'Удостоверение на постоянное жительство'),
        ('dd', 'Разрешение на имиграция в Украину'),
        ('pp', 'Продолжения срока нахождения в Украинре'),
    )
    DOC_FOR = (
        ('0', 'Для взрослого'),
        ('1', 'Для ребенка')
    )
    DOC_REGISTER = (
        ('book', 'Паспорт Украины в форме книжечки'),
        ('id', 'Паспорт Украины в форме карточки'),
        ('cert', 'Свидетельства о рождении'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='doc_state',
                             verbose_name='пользователь')
    type_doc = models.CharField(max_length=5, verbose_name='тип документа',
                                choices=DOC_TYPE)
    for_doc = models.CharField(max_length=5,
                               verbose_name='для кого оформлялся',
                               choices=DOC_FOR, default='1')
    register_doc = models.CharField(max_length=5, blank=True, null=True,
                                    verbose_name='оформление на основе',
                                    choices=DOC_REGISTER)
    series = models.CharField(max_length=50, blank=True, null=True,
                              verbose_name='серия документа')
    number = models.CharField(max_length=50, verbose_name='номер документа')
    description = models.TextField(verbose_name='текст')
    subscribe = models.BooleanField(default=False, verbose_name='подписка?')

    @property
    def doc_type_id(self):
        if self.type_doc == 'book':
            return 0
        elif self.type_doc == 'id':
            return 1
        else:
            return 3

    class Meta:
        verbose_name = 'готовность документа'
        verbose_name_plural = 'готовность документов'

    def __str__(self):
        return '{} {}{}'.format(self.get_type_doc_display(), self.series if
        self.series else '', self.number)


class Minjust(models.Model):
    search = models.ForeignKey(Search, on_delete=models.CASCADE,
                               related_name='minjust',
                               verbose_name='поисковый запрос')
    subscribe = models.BooleanField(default=False, verbose_name='подписка?')

    class Meta:
        verbose_name = 'миньюст'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.search.name} {self.search.surname}'


class MinjustFop(models.Model):
    minjust = models.ForeignKey(Minjust, on_delete=models.CASCADE,
                                related_name='minjust_fop',
                                verbose_name='миньюст')
    # name = models.CharField(max_length=150, verbose_name='Название ФОП',
    #                         blank=True, null=True)
    person = models.CharField(max_length=200, verbose_name='ФИО')
    record_number = models.CharField(max_length=500, verbose_name='Номер '
                                                                  'записи')
    address = models.CharField(max_length=300, verbose_name='Адрес')
    action = models.TextField(verbose_name='Деятельность')
    tax = models.CharField(max_length=100, verbose_name='Тип налогов',
                           blank=True, null=True)
    state = models.CharField(max_length=150, verbose_name='Состояние')
    phone = models.TextField(verbose_name='Телефон', blank=True, null=True)
    date = models.DateField(verbose_name='Дата записи', blank=True, null=True)
    subscribe = models.BooleanField(default=False, verbose_name='подписка?')

    class Meta:
        ordering = ['pk']
        verbose_name = 'фоп'
        verbose_name_plural = 'фопы'

    def __str__(self):
        return f'{self.person} {self.state}'


class MinjustCompany(models.Model):
    minjust = models.ForeignKey(Minjust, on_delete=models.CASCADE,
                                related_name='minjust_company',
                                verbose_name='миньюст')
    name = models.CharField(max_length=200, verbose_name='Название Юр.Лица')
    code = models.CharField(max_length=100, verbose_name='Код Юр.Лица')
    address = models.CharField(max_length=500, verbose_name='Адрес')
    managers = models.TextField(verbose_name='Управляющие')
    action = models.TextField(verbose_name='Деятельность')
    capital = models.FloatField(verbose_name='Капитал', default=0)
    phone = models.TextField(verbose_name='Телефон',
                             blank=True, null=True)
    state = models.CharField(max_length=150, verbose_name='Состояние')
    date = models.DateField(verbose_name='Дата записи', blank=True, null=True)
    subscribe = models.BooleanField(default=False, verbose_name='подписка?')

    class Meta:
        ordering = ['pk']
        verbose_name = 'юр.лицо'
        verbose_name_plural = 'юр.лица'

    def __str__(self):
        return f'{self.code} {self.name}'


class Debtors(models.Model):
    search = models.ForeignKey(Search, on_delete=models.CASCADE,
                               related_name='debtors',
                               verbose_name='поисковый запрос')
    subscribe = models.BooleanField(default=False, verbose_name='подписка?')

    @property
    def count_asvp(self):
        i = 0
        if self.debtors_elem.all():
            for obj in self.debtors_elem.all():
                i += obj.asvp_elem.count()

        return i

    @property
    def count_subs_asvp(self):
        i = 0
        if self.debtors_elem.all():
            for obj in self.debtors_elem.all():
                i += obj.asvp_elem.filter(subscribe=True).count()

        return i

    class Meta:
        ordering = ['pk']
        verbose_name = 'должника'
        verbose_name_plural = 'должники'


class DebtorsElem(models.Model):
    debtors = models.ForeignKey(Debtors, on_delete=models.CASCADE,
                                related_name='debtors_elem',
                                verbose_name='должник')
    birth = models.DateField(verbose_name='дата рождения')
    publisher = models.CharField(max_length=300, verbose_name='документ выдан')
    connection = models.TextField(verbose_name='связь')
    number = models.CharField(max_length=100, verbose_name='ВП номер')
    deduction = models.CharField(max_length=300,
                                 verbose_name='Категория взысканий')

    class Meta:
        ordering = ['pk']
        verbose_name = 'долг'
        verbose_name_plural = 'долги'


class AsvpElem(models.Model):
    debtors = models.ForeignKey(DebtorsElem, on_delete=models.CASCADE,
                                related_name='asvp_elem',
                                verbose_name='должник')
    agency = models.CharField(max_length=300, verbose_name='исполнитель')
    date_open = models.DateField(verbose_name='Дата открытия', blank=True,
                                 null=True)
    creditors_name = models.CharField(max_length=300, blank=True, null=True,
                                      verbose_name='коллектор')
    status = models.CharField(max_length=100, verbose_name='статус')
    subscribe = models.BooleanField(default=False, verbose_name='подписка?')

    class Meta:
        ordering = ['pk']
        verbose_name = 'АСВП элемент'
        verbose_name_plural = 'АСВП элементы'

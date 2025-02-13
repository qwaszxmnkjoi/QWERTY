__all__ = ['InactiveDocument', 'DocState']

from django.db import models

from .base import UserForeignKey


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
    user = UserForeignKey(related_name='inactive_doc')
    type_doc = models.CharField(max_length=5, verbose_name='тип документа', choices=DOC_TYPE)
    series = models.CharField(max_length=50, blank=True, null=True, verbose_name='серия документа')
    number = models.CharField(max_length=50, verbose_name='номер документа')
    status = models.BooleanField(blank=True, null=True, verbose_name='статус')
    description = models.TextField(verbose_name='текст')
    subscribe = models.BooleanField(default=False, verbose_name='подписка?')

    class Meta:
        verbose_name = 'неактивный документ'
        verbose_name_plural = 'неактивные документы'

    def __str__(self):
        return '{} {}{}'.format(self.get_type_doc_display(), self.series if self.series else '', self.number)


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
    user = UserForeignKey(related_name='doc_state')
    type_doc = models.CharField(max_length=5, verbose_name='тип документа', choices=DOC_TYPE)
    for_doc = models.CharField(max_length=5, verbose_name='для кого оформлялся', choices=DOC_FOR, default='1')
    register_doc = models.CharField(max_length=5, blank=True, null=True, verbose_name='оформление на основе', choices=DOC_REGISTER)
    series = models.CharField(max_length=50, blank=True, null=True, verbose_name='серия документа')
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

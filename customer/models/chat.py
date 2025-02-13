import os
from functools import cached_property

from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from versatileimagefield.fields import VersatileImageField

from .user import User

CYRILLIC_MAP = {
    'а': 'a',
    'б': 'b',
    'в': 'v',
    'г': 'g',
    'ґ': 'g',
    'д': 'd',
    'е': 'e',
    'є': 'ye',
    'ё': 'e',
    'ж': 'zh',
    'з': 'z',
    'и': 'i',
    'і': 'i',
    'ї': 'i',
    'й': 'y',
    'к': 'k',
    'л': 'l',
    'м': 'm',
    'н': 'n',
    'о': 'o',
    'п': 'p',
    'р': 'r',
    'с': 's',
    'т': 't',
    'у': 'u',
    'ф': 'f',
    'х': 'ch',
    'ц': 'ts',
    'ч': 'ch',
    'ш': 'sh',
    'щ': 'sch',
    'ъ': '_',
    'ы': 'y',
    'ь': '_',
    'э': 'e',
    'ю': 'yu',
    'я': 'ya'
}


def generate_slug(name):
    result = ''
    for x in name:
        x = CYRILLIC_MAP.get(x.lower(), x.lower())
        result += x
    result = slugify(result)

    return result


class Country(models.Model):
    slug = models.SlugField(
        max_length=200,
        null=False,
        blank=False,
        unique=True,
        allow_unicode=True,
        db_index=True,
        verbose_name=_('SLUG')
    )
    name = models.CharField(max_length=200, verbose_name=_('Название'))
    name_uk = models.CharField(max_length=200, verbose_name=_('Название УКР'))
    name_en = models.CharField(max_length=200, verbose_name=_('Название АНГЛ'))

    def save(self, *args, **kwargs):
        self.slug = generate_slug(self.slug)
        return super().save(*args, **kwargs)

    class Meta:
        app_label = 'customer'
        db_table = 'em_customer_country'

        verbose_name = _('Страна')
        verbose_name_plural = _('Страны')

    def __str__(self):
        return f'{self.name} [SLUG={self.slug}]'


class Category(MPTTModel):
    slug = models.SlugField(
        max_length=200,
        null=False,
        blank=False,
        unique=False,
        allow_unicode=True,
        db_index=True,
        verbose_name=_('SLUG')
    )
    parent = TreeForeignKey(
        'self',
        blank=True,
        on_delete=models.CASCADE,
        null=True,
        verbose_name=_('Родитель'),
        related_name='children'
    )
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        verbose_name=_('Страна')
    )
    name = models.CharField(max_length=200, verbose_name=_('Название'))
    name_uk = models.CharField(max_length=200, verbose_name=_('Название УКР'))
    name_en = models.CharField(max_length=200, verbose_name=_('Название АНГЛ'))

    @cached_property
    def ancestors(self):
        return self.get_ancestors(include_self=True)

    @cached_property
    def file_path(self):
        result = ''
        for obj in self.ancestors:
            result += f'{obj.slug}/'
        if result and result[-1] == '/':
            result = result[:-1]
        return result

    @cached_property
    def file_path_with_country(self):
        return f'{self.country.slug}/{self.file_path}'

    class Meta:
        app_label = 'customer'
        db_table = 'em_customer_category'

        verbose_name = _('Категория')
        verbose_name_plural = _('Категории')
        unique_together = ('parent', 'slug')

    def save(self, *args, **kwargs):
        self.slug = generate_slug(self.slug)
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} [SLUG={self.slug}, COUNTRY={self.country.slug}]'


class Message(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        verbose_name=_('Категория'),
        related_name='message'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name=_('Отправитель'))
    text = models.TextField(
        blank=True,
        null=True,
        max_length=1024,
        verbose_name=_('Текст')
    )

    dt_create = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата создания')
    )

    class Meta:
        app_label = 'customer'
        db_table = 'em_customer_message'

        verbose_name = _('Сообщение')
        verbose_name_plural = _('Сообщения')

    def __str__(self):
        return f'{str(self.user)} -> {str(self.category)}'


def document_directory_path(instance: 'MessageDocument', filename):
    # file will be uploaded to MEDIA_ROOT/<country.slug>/<cat_list_slug>/<filename>
    return '{category_path}/{message_id}/{filename}'.format(
        category_path=instance.message.category.file_path_with_country,
        message_id=instance.message_id,
        filename=filename
    )


class MessageDocument(models.Model):
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        verbose_name=_('Сообщение'),
        related_name='document'
    )

    src_file = models.FileField(
        blank=True,
        null=True,
        upload_to=document_directory_path,
        verbose_name=_('Файл'),
    )

    src_image = VersatileImageField(
        blank=True,
        null=True,
        upload_to=document_directory_path,
        verbose_name=_('Изображение'),
        width_field='width',
        height_field='height'
    )

    height = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name=_('Image Height')
    )
    width = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name=_('Image Width')
    )

    class Meta:
        app_label = 'customer'
        db_table = 'em_customer_message_document'

        verbose_name = _('Документ')
        verbose_name_plural = _('Документы')

    @cached_property
    def file_name(self):
        result = None
        if self.src_file:
            result = os.path.basename(self.src_file.path)
        return result

    @cached_property
    def file_ext(self):
        result = None
        if self.file_name:
            result = self.file_name.split('.')[-1]
        return result

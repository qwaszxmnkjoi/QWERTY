from django.core.validators import FileExtensionValidator
from django.db import models


class News(models.Model):
    title = models.CharField(max_length=200, verbose_name='название')
    text = models.TextField(max_length=800, verbose_name='описание')
    image = models.FileField(upload_to='news/', blank=True, null=True,
                             verbose_name='медиа',
                             validators=[FileExtensionValidator(
                                 allowed_extensions=['png', 'jpg', 'jpeg', 'mp4'])])
    language = models.CharField(max_length=100, verbose_name='язык')
    date = models.DateField(auto_now_add=True, verbose_name='дата')
    status = models.CharField(max_length=50,
                              choices=[('save', 'Сохранена'),
                                       ('publish', 'Опубликована'),
                                       ('send', 'Готовится к отправке'),
                                       ('finish', 'Завершена')
                                       ],
                              default='save', verbose_name='статус')

    class Meta:
        verbose_name = 'новость'
        verbose_name_plural = 'новости'

    def __str__(self):
        return f'{self.title} {self.get_status_display()}'


class NewsContent(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE,
                             related_name='content',
                             verbose_name='новость')
    text = models.TextField(max_length=800, verbose_name='текст')
    image = models.FileField(upload_to='news/', blank=True, null=True,
                             verbose_name='медиа',
                             validators=[FileExtensionValidator(
                                 allowed_extensions=['png', 'jpg', 'jpeg', 'mp4'])]
                             )

    class Meta:
        verbose_name = 'контент'
        verbose_name_plural = 'контенты'

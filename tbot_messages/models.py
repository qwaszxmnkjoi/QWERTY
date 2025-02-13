import importlib

from django.core.exceptions import ValidationError
from django.db import models
from loguru import logger
from telebot.apihelper import ApiTelegramException

try:
    m = importlib.import_module('tbot_messages._generated.botmessage')
    BotMessage = m.__getattribute__('TbotMessagesBotmessage')
    BotMessage._meta.verbose_name = 'текст сообщения'
    BotMessage._meta.verbose_name_plural = 'текста сообщений'
except (ModuleNotFoundError, AttributeError) as e:
    class BotMessage(models.Model):
        name = models.CharField(verbose_name='ID',
                                max_length=200, unique=True)
        text = models.TextField(verbose_name='Текст', max_length=4096,
                                null=True, default='', blank=True)
        is_active = models.BooleanField(verbose_name='Активно?',
                                        null=True, default=True)

        def __str__(self):
            return f'{self.id:2d}.{self.name}'

        class Meta:
            verbose_name = 'текст сообщения'
            verbose_name_plural = 'текста сообщений'

try:
    m = importlib.import_module('tbot_messages._generated.button')
    Button = m.__getattribute__('TbotMessagesButton')
    Button._meta.ordering = ('num',)
except (ModuleNotFoundError, AttributeError):
    class Button(models.Model):
        message = models.ForeignKey(BotMessage, on_delete=models.CASCADE, related_name='buttons')
        text = models.CharField(verbose_name='Текст кнопки', max_length=200, default='', null=True)
        num = models.SmallIntegerField(verbose_name='Номер кнопки', default=0)
        is_active = models.BooleanField(verbose_name='Активна?', default=True, null=True)

        # for inline-mode
        is_inline_mode = models.BooleanField(default=False, null=True)

        # for default(inline) buttons
        callback_data = models.CharField(max_length=40, null=True)

        # for default(inline) buttons
        url = models.URLField(blank=True, null=True)

        # for reply buttons
        is_reply = models.BooleanField(default=False, null=True)
        row = models.SmallIntegerField(default=0, null=True)

        def __str__(self):
            return self.text

        class Meta:
            ordering = ('num',)
            verbose_name = 'Кнопка'
            verbose_name_plural = 'Кнопки'


class TBot(models.Model):
    token = models.CharField(verbose_name='токен', max_length=100)
    webhook_url = models.CharField(verbose_name='Webhook URL', max_length=255)
    is_active = models.BooleanField(default=True, verbose_name='активный')

    class Meta:
        verbose_name = 'конфиг'
        verbose_name_plural = 'конфиги'

    def update_bot_config(self):
        from .bot import bot
        bot.config = self
        bot.token = self.token

        return bot

    def set_active_config(self):
        if self.is_active:
            other_active_configs = TBot.objects.filter(is_active=True)
            for config in other_active_configs:
                if config.pk != self.pk:
                    config.is_active = False
                    config.save()

    def set_hook(self, tbot):
        result = tbot.set_webhook(self.webhook_url, drop_pending_updates=True, timeout=10)
        logger.info(f"Webhook: {result}")

    def clean(self):
        tbot = self.update_bot_config()

        try:
            self.set_hook(tbot)
            self.set_active_config()

        except ApiTelegramException as e:
            logger.debug(e)
            raise ValidationError(
                'Неверный указан "Токен Бота" либо "Webhook Url"!'
                'Исправьте ошибку и сохраните конфигурацию ещё раз.'
            )

    @property
    def bot_url(self):
        result = self.webhook_url.replace('/', '')
        if not result.startswith('http'):
            result = f'https://{result}/'
        return result

    def __str__(self):
        return self.token

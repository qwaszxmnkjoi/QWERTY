import loguru
from django.contrib import admin
from django.utils.html import format_html

from .bot import bot
from .models import BotMessage, Button, TBot


class ButtonInline(admin.StackedInline):
    model = Button
    extra = 0
    max_num = 0

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj):
        return False

    def get_fields(self, request, obj=None):
        fields = ['is_active']
        if obj.buttons.first():
            for text_key in filter(lambda key: key.startswith('text'),
                                   Button.__dict__):
                fields.append(text_key)
            if obj.buttons.first().is_reply is not True:
                for text_key in filter(lambda key: key.startswith('url'),
                                       Button.__dict__):
                    fields.append(text_key)

            fields.append('is_inline_mode')
        return fields

    def get_readonly_fields(self, request, obj=None):
        fields = ['is_inline_mode']
        if obj.buttons.first():
            if obj.buttons.first().is_reply:
                for text_key in filter(lambda key: key.startswith('text'),
                                       Button.__dict__):
                    fields.append(text_key)
        return fields


@admin.register(BotMessage)
class MessageAdmin(admin.ModelAdmin):
    ordering = ('id',)
    inlines = [ButtonInline]

    def get_list_display(self, request):
        list_display = ['name', ]
        for text_key in filter(lambda key: key.startswith('text'),
                               BotMessage.__dict__):
            list_display.append(text_key)
        list_display.extend(['buttons', 'status'])
        return list_display

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    @admin.display(description='Кнопки')
    def buttons(self, obj):
        texts = []
        for btn in obj.buttons.all():
            if hasattr(btn, 'text_ru') and btn.text_ru:
                texts.append(btn.text_ru)
            else:
                texts.append(btn.text)

        return texts

    @admin.display(description='Статус')
    def status(self, obj):
        return '🟢' if obj.is_active else '🔴'


@admin.register(TBot)
class TBotAdmin(admin.ModelAdmin):
    list_display = ('name', 'token', 'webhook_url', 'bot_link', 'is_active')

    @admin.display(description='Имя')
    def name(self, obj):
        try:
            return bot.get_me().first_name
        except Exception:
            return '-'

    @admin.display(description='Username')
    def bot_link(self, obj):
        try:
            username = bot.get_me().username
            return format_html(
                f'<a href="https://t.me/{username}">{username}</a>'
            )
        except Exception:
            return '-'

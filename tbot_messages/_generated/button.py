# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class TbotMessagesButton(models.Model):
    id = models.BigAutoField(primary_key=True)
    text = models.CharField(max_length=200, blank=True, null=True)
    num = models.SmallIntegerField()
    is_active = models.BooleanField(blank=True, null=True)
    is_inline_mode = models.BooleanField(blank=True, null=True)
    callback_data = models.CharField(max_length=40, blank=True, null=True)
    url = models.URLField(max_length=200, blank=True, null=True)
    is_reply = models.BooleanField(blank=True, null=True)
    row = models.SmallIntegerField(blank=True, null=True)
    message = models.ForeignKey('TbotMessagesBotmessage', models.CASCADE, related_name="buttons")
    text_en = models.CharField(max_length=256, blank=True, null=True)
    text_ua = models.CharField(max_length=256, blank=True, null=True)
    url_en = models.CharField(max_length=200, blank=True, null=True)
    url_ua = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f'{self.text}'

    class Meta:
        db_table = 'tbot_messages_button'

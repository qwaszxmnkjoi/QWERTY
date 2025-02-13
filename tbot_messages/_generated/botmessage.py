# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class TbotMessagesBotmessage(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=200)
    text = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(blank=True, null=True)
    text_en = models.TextField(blank=True, null=True)
    text_ua = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.id:2d}.{self.name}'

    class Meta:
        db_table = 'tbot_messages_botmessage'
        verbose_name = 'Тексти повідомлень'
        verbose_name_plural = 'Текст повідомлення'

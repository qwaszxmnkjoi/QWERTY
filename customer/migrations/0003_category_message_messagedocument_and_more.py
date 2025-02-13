# Generated by Django 4.0.1 on 2023-06-24 08:08

import customer.models.chat
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_user_tg_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(allow_unicode=True, max_length=200, verbose_name='SLUG')),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'db_table': 'em_customer_category',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, max_length=1024, null=True, verbose_name='Текст')),
                ('dt_create', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message', to='customer.category', verbose_name='Категория')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='customer.user', verbose_name='Отправитель')),
            ],
            options={
                'verbose_name': 'Сообщение',
                'verbose_name_plural': 'Сообщения',
                'db_table': 'em_customer_message',
            },
        ),
        migrations.CreateModel(
            name='MessageDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('src_file', models.FileField(blank=True, null=True, upload_to=customer.models.chat.document_directory_path, verbose_name='Файл')),
                ('src_image', versatileimagefield.fields.VersatileImageField(blank=True, height_field='height', null=True, upload_to=customer.models.chat.document_directory_path, verbose_name='Изображение', width_field='width')),
                ('height', models.PositiveIntegerField(blank=True, null=True, verbose_name='Image Height')),
                ('width', models.PositiveIntegerField(blank=True, null=True, verbose_name='Image Width')),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='document', to='customer.message', verbose_name='Сообщение')),
            ],
            options={
                'verbose_name': 'Документ',
                'verbose_name_plural': 'Документы',
                'db_table': 'em_customer_message_document',
            },
        ),
        migrations.AlterModelOptions(
            name='country',
            options={'verbose_name': 'Страна', 'verbose_name_plural': 'Страны'},
        ),
        migrations.RemoveField(
            model_name='country',
            name='user',
        ),
        migrations.AddField(
            model_name='country',
            name='slug',
            field=models.SlugField(allow_unicode=True, default='sss', max_length=200, unique=True, verbose_name='SLUG'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='country',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Название'),
        ),
        migrations.AlterModelTable(
            name='country',
            table='em_customer_country',
        ),
        migrations.DeleteModel(
            name='Chat',
        ),
        migrations.AddField(
            model_name='category',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.country', verbose_name='Страна'),
        ),
        migrations.AddField(
            model_name='category',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='customer.category', verbose_name='Родитель'),
        ),
        migrations.AlterUniqueTogether(
            name='category',
            unique_together={('parent', 'slug')},
        ),
    ]

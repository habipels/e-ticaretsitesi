# Generated by Django 4.1.2 on 2024-01-08 18:11

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('site_set', '0003_yasal_metinler'),
    ]

    operations = [
        migrations.AlterField(
            model_name='yasal_metinler',
            name='yasalmetin',
            field=ckeditor.fields.RichTextField(verbose_name='Yasal Metin İçeriği'),
        ),
    ]

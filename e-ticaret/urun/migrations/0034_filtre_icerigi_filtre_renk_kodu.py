# Generated by Django 4.1.2 on 2024-02-18 01:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('urun', '0033_urun_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='filtre_icerigi',
            name='filtre_renk_kodu',
            field=models.CharField(default=' ', max_length=200, verbose_name='filtre Renk Kodu'),
        ),
    ]

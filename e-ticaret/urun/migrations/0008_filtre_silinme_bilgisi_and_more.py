# Generated by Django 4.1.2 on 2023-12-08 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('urun', '0007_meslek_silinme_bilgisi'),
    ]

    operations = [
        migrations.AddField(
            model_name='filtre',
            name='silinme_bilgisi',
            field=models.BooleanField(default=False, verbose_name='Silinme Bilgisi'),
        ),
        migrations.AddField(
            model_name='filtre_icerigi',
            name='silinme_bilgisi',
            field=models.BooleanField(default=False, verbose_name='Silinme Bilgisi'),
        ),
        migrations.AddField(
            model_name='urun',
            name='silinme_bilgisi',
            field=models.BooleanField(default=False, verbose_name='Silinme Bilgisi'),
        ),
    ]

# Generated by Django 4.1.2 on 2023-12-10 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('urun', '0010_filtre_icerigi_filtre_renk_kodu'),
    ]

    operations = [
        migrations.AddField(
            model_name='urun',
            name='urun_bakma_saysi',
            field=models.BigIntegerField(default=0, verbose_name='Ürün Bakma Sayısı'),
        ),
    ]
# Generated by Django 4.1.2 on 2023-12-08 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('urun', '0005_urun_resimleri'),
    ]

    operations = [
        migrations.AddField(
            model_name='urun',
            name='urun_stok',
            field=models.FloatField(blank=True, null=True, verbose_name='Stok Bilgisi'),
        ),
    ]

# Generated by Django 4.1.2 on 2023-12-18 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('urun', '0017_sepet_olusturma_ip_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sepet_olusturma_ip',
            name='sepet_sahibi',
            field=models.GenericIPAddressField(default=0),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='ip',
        ),
    ]

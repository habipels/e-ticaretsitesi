# Generated by Django 4.1.2 on 2024-01-11 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_set', '0004_alter_yasal_metinler_yasalmetin'),
    ]

    operations = [
        migrations.CreateModel(
            name='kargo_tutari',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('min_siparis_tutari', models.FloatField(default=0)),
                ('eklenecek_kargo_tutari', models.FloatField(default=0)),
            ],
        ),
    ]
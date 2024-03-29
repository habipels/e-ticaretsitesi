# Generated by Django 4.1.2 on 2024-01-15 19:37

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('urun', '0021_sepet_sahibi_bilgileri_faturatipi'),
    ]

    operations = [
        migrations.CreateModel(
            name='satin_alinanlar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('silinme_bilgisi', models.BooleanField(default=False, verbose_name='Silinme Bilgisi')),
                ('kayit_tarihi', models.DateTimeField(default=datetime.datetime.now, null=True)),
                ('kayitli_kullanici', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='urun.sepet_olusturma')),
                ('kayitli_olmayan_kullanici', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='urun.sepet_olusturma_ip')),
                ('siparis_sahibi_bilgileri', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='urun.sepet_sahibi_bilgileri')),
            ],
        ),
    ]

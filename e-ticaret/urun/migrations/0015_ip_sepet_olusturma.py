# Generated by Django 4.1.2 on 2023-12-18 12:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('urun', '0014_rename_images_urun_resimleri_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='ip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_bilgisi', models.GenericIPAddressField()),
                ('kayit_tarihi', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='sepet_olusturma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sepet_satin_alma_durumu', models.BooleanField(default=False)),
                ('sepet_sahibi', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

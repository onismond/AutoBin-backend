# Generated by Django 5.0.7 on 2025-01-13 12:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0007_bin_color_alter_bin_serial_number'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='bin',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bin',
            name='pickups',
            field=models.ManyToManyField(blank=True, to='apis.pickup'),
        ),
    ]

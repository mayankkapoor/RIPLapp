# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('RIPLapp', '0005_auto_20150405_1934'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bus',
            name='id',
        ),
        migrations.RemoveField(
            model_name='depot',
            name='id',
        ),
        migrations.RemoveField(
            model_name='volunteer',
            name='id',
        ),
        migrations.AlterField(
            model_name='bus',
            name='bus_code_num',
            field=models.CharField(max_length=20, serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='depot',
            name='depot_code',
            field=models.CharField(max_length=32, serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='volunteer',
            name='volunteer_phone_num',
            field=models.BigIntegerField(serialize=False, primary_key=True, validators=[django.core.validators.MaxLengthValidator(10), django.core.validators.MinLengthValidator(10)]),
        ),
    ]

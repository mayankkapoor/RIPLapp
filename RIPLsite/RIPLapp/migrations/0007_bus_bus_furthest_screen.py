# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('RIPLapp', '0006_auto_20150406_0632'),
    ]

    operations = [
        migrations.AddField(
            model_name='bus',
            name='bus_furthest_screen',
            field=models.IntegerField(null=True),
        ),
    ]

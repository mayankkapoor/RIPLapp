# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('RIPLapp', '0009_auto_20150409_0551'),
    ]

    operations = [
        migrations.AddField(
            model_name='bus',
            name='bus_number_tickets_initial',
            field=models.IntegerField(null=True),
        ),
    ]

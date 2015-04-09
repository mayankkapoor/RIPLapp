# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('RIPLapp', '0008_auto_20150409_0543'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bus',
            name='bus_expected_number_of_children',
            field=models.IntegerField(null=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('RIPLapp', '0007_bus_bus_furthest_screen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bus',
            name='bus_expected_number_of_children',
            field=models.IntegerField(default=99, null=True),
        ),
    ]

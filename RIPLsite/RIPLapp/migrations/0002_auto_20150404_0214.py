# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('RIPLapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bus',
            old_name='bus_registration_no',
            new_name='bus_code_no',
        ),
        migrations.RenameField(
            model_name='volunteer',
            old_name='bus',
            new_name='volunteer_bus',
        ),
    ]

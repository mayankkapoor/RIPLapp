# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('RIPLapp', '0002_auto_20150404_0214'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bus',
            old_name='bus_code_no',
            new_name='bus_code_num',
        ),
        migrations.RenameField(
            model_name='volunteer',
            old_name='volunteer_phone_number',
            new_name='volunteer_phone_num',
        ),
    ]

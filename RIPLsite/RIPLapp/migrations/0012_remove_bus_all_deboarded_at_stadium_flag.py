# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('RIPLapp', '0011_auto_20150409_1042'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bus',
            name='all_deboarded_at_stadium_flag',
        ),
    ]

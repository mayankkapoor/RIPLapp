# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('RIPLapp', '0010_bus_bus_number_tickets_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bus',
            name='all_deboarded_at_stadium_flag',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='bus',
            name='bus_first_aid_kit_available_flag',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='bus',
            name='bus_started_from_depot_flag',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='bus',
            name='everyone_dropped_off_flag',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='bus',
            name='feedback_form_taken_from_ngo_flag',
            field=models.IntegerField(null=True),
        ),
    ]

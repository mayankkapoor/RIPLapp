# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('RIPLapp', '0003_auto_20150404_0610'),
    ]

    operations = [
        migrations.AddField(
            model_name='bus',
            name='all_deboarded_at_stadium_flag',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='bus',
            name='all_deboarded_at_stadium_time',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='bus',
            name='bus_first_aid_kit_available_flag',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='bus',
            name='bus_num_adults_female_pickedup',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='bus',
            name='bus_num_adults_female_return_journey',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='bus',
            name='bus_num_adults_male_pickedup',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='bus',
            name='bus_num_adults_male_return_journey',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='bus',
            name='bus_num_children_female_pickedup',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='bus',
            name='bus_num_children_female_return_journey',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='bus',
            name='bus_num_children_male_pickedup',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='bus',
            name='bus_num_children_male_return_journey',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='bus',
            name='everyone_dropped_off_flag',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='bus',
            name='everyone_dropped_off_time',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='bus',
            name='feedback_form_taken_from_ngo_flag',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='bus',
            name='feedback_form_taken_from_ngo_time',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='bus',
            name='num_adults_female_seated',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='bus',
            name='num_adults_male_seated',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='bus',
            name='num_children_female_seated',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='bus',
            name='num_children_male_seated',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='bus',
            name='bus_safe_flag',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='bus',
            name='bus_started_from_depot_flag',
            field=models.NullBooleanField(),
        ),
    ]

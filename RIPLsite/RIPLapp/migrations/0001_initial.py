# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bus_registration_no', models.CharField(max_length=20)),
                ('bus_safe_flag', models.BooleanField(default=False)),
                ('bus_safe_time', models.DateTimeField(null=True, blank=True)),
                ('bus_expected_number_of_children', models.IntegerField(null=True)),
                ('bus_expected_number_of_adults', models.IntegerField(null=True)),
                ('bus_number_water_bottles_initial', models.IntegerField(null=True)),
                ('bus_number_food_packets_initial', models.IntegerField(null=True)),
                ('bus_started_from_depot_flag', models.BooleanField(default=False)),
                ('bus_started_from_depot_time', models.DateTimeField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Volunteer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('volunteer_phone_number', models.BigIntegerField(validators=[django.core.validators.MaxLengthValidator(10), django.core.validators.MinLengthValidator(10)])),
                ('volunteer_full_name', models.CharField(max_length=200, null=True, blank=True)),
                ('bus', models.ForeignKey(to='RIPLapp.Bus')),
            ],
        ),
    ]

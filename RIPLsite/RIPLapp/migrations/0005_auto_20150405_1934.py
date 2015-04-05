# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('RIPLapp', '0004_auto_20150405_1246'),
    ]

    operations = [
        migrations.CreateModel(
            name='Depot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('depot_zone', models.IntegerField()),
                ('depot_code', models.CharField(max_length=32)),
                ('depot_name', models.CharField(max_length=99)),
            ],
        ),
        migrations.CreateModel(
            name='SOS',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sos_raise_time', models.DateTimeField()),
                ('sos_bus', models.ForeignKey(to='RIPLapp.Bus')),
                ('sos_volunteer', models.ForeignKey(to='RIPLapp.Volunteer')),
            ],
        ),
        migrations.AddField(
            model_name='bus',
            name='bus_depot',
            field=models.ForeignKey(to='RIPLapp.Depot', null=True),
        ),
    ]

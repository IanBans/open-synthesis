# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-26 16:56
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('openach', '0004_auto_20160826_1651'),
    ]

    operations = [
        migrations.AddField(
            model_name='evidencesource',
            name='source_date',
            field=models.DateField(default=datetime.datetime(2016, 8, 26, 16, 56, 39, 255717, tzinfo=utc), verbose_name='source date'),
            preserve_default=False,
        ),
    ]

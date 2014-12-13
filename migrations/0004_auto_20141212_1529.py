# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('sigmafuzz', '0003_auto_20141212_1442'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='fileName',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='submission',
            name='submissionDate',
            field=models.DateTimeField(default=datetime.datetime(2034, 1, 18, 23, 40)),
            preserve_default=True,
        ),
    ]

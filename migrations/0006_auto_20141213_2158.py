# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sigmafuzz', '0005_auto_20141212_1530'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='archiveDate',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='submission',
            name='archiveException',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='submission',
            name='archiveStatus',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]

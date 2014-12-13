# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sigmafuzz', '0004_auto_20141212_1529'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='fileName',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
    ]

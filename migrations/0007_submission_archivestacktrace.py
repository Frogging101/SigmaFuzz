# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sigmafuzz', '0006_auto_20141213_2158'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='archiveStackTrace',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]

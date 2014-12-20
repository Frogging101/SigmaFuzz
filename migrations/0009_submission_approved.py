# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sigmafuzz', '0008_submission_thumbnailed'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='approved',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]

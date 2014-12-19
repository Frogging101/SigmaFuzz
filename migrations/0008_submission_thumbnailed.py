# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sigmafuzz', '0007_submission_archivestacktrace'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='thumbnailed',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sigmafuzz', '0002_submission_imgsource'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='submissionDate',
            field=models.DateTimeField(blank=True),
            preserve_default=True,
        ),
    ]

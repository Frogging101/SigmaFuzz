# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sigmafuzz', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='imgSource',
            field=models.URLField(default=''),
            preserve_default=False,
        ),
    ]

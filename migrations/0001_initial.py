# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('submissionDate', models.DateTimeField()),
                ('indexDate', models.DateTimeField(auto_now_add=True)),
                ('artist', models.CharField(max_length=255)),
                ('submitter', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('source', models.URLField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

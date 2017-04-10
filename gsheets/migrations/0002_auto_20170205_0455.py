# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gsheets', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CandidateAlias',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('candidate_alias', models.CharField(max_length=30)),
                ('candidate', models.ForeignKey(to='gsheets.Candidate', related_name='aliases')),
            ],
        ),
        migrations.AlterField(
            model_name='referendum',
            name='short_title',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='referendummapping',
            name='measure_name',
            field=models.CharField(max_length=200),
        ),
    ]

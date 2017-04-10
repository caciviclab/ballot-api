# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gsheets', '0002_auto_20170205_0455'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='candidatealias',
            options={'verbose_name_plural': 'candidate aliases'},
        ),
        migrations.AlterField(
            model_name='candidate',
            name='candidate',
            field=models.CharField(max_length=30, help_text="The candidate's full name."),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='party_affiliation',
            field=models.CharField(max_length=1, choices=[('D', 'Democrat'), ('R', 'Republican'), ('I', 'Independent'), ('O', 'Other')], blank=True),
        ),
    ]

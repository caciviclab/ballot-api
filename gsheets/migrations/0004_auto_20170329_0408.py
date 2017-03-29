# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gsheets', '0003_auto_20170205_0802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='referendummapping',
            name='measure_number',
            field=models.CharField(max_length=10),
        ),
    ]

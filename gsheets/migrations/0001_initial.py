# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('fppc', models.IntegerField(blank=True, unique=True, null=True)),
                ('committee_name', models.CharField(blank=True, max_length=120)),
                ('candidate', models.CharField(max_length=30)),
                ('office', models.CharField(blank=True, help_text='Office the candidate is running for.', max_length=30)),
                ('incumbent', models.BooleanField(default=False)),
                ('accepted_expenditure_ceiling', models.BooleanField(default=False)),
                ('website', models.URLField(blank=True, null=True)),
                ('twitter', models.URLField(blank=True, null=True)),
                ('party_affiliation', models.CharField(blank=True, max_length=15)),
                ('occupation', models.CharField(blank=True, max_length=80)),
                ('bio', models.TextField(blank=True)),
                ('photo', models.URLField(blank=True, null=True)),
                ('votersedge', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Committee',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('filer_id', models.CharField(max_length=15)),
                ('filer_naml', models.CharField(blank=True, max_length=200)),
                ('committee_type', models.CharField(choices=[('RCP', 'RCP'), ('BMC', 'BMC')], blank=True, max_length=3)),
                ('description', models.CharField(blank=True, max_length=40)),
                ('ballot_measure', models.CharField(blank=True, max_length=3)),
                ('support_or_oppose', models.CharField(choices=[('S', 'Support'), ('O', 'Oppose')], blank=True, max_length=1)),
                ('website', models.URLField(blank=True, null=True)),
                ('twitter', models.URLField(blank=True, null=True)),
                ('facebook', models.URLField(blank=True, null=True)),
                ('netfilelocalid', models.CharField(blank=True, max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Referendum',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('measure_number', models.CharField(max_length=5)),
                ('short_title', models.CharField(blank=True, max_length=30)),
                ('full_title', models.TextField(blank=True)),
                ('summary', models.TextField()),
                ('votersedge', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ReferendumMapping',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('measure_name', models.CharField(max_length=30)),
                ('measure_number', models.CharField(max_length=3)),
            ],
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-09 10:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cfp', '0005_proposal_selected'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkshopProposal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('speaker_information', models.TextField(blank=True)),
                ('title', models.TextField()),
                ('description', models.TextField()),
                ('audience', models.TextField()),
                ('props', models.TextField(blank=True)),
                ('skill_level', models.PositiveIntegerField(choices=[(1, 'everyone'), (2, 'novice'), (3, 'intermediate'), (4, 'advanced')], default=1)),
                ('notes', models.TextField(blank=True)),
                ('mentoring', models.BooleanField(default=False)),
                ('selected', models.BooleanField(default=False)),
                ('submitted_on', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
            ],
            options={
                'verbose_name': 'workshop proposal',
                'verbose_name_plural': 'workshop proposals',
            },
        ),
    ]

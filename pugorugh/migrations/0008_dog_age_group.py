# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2018-03-19 18:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pugorugh', '0007_auto_20180316_2140'),
    ]

    operations = [
        migrations.AddField(
            model_name='dog',
            name='age_group',
            field=models.CharField(default='b', max_length=1),
        ),
    ]

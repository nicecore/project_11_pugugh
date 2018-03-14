# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2018-03-13 18:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pugorugh', '0004_auto_20180312_1939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdog',
            name='status',
            field=models.CharField(choices=[('l', 'Like'), ('d', 'Dislike'), ('u', 'Undecided')], default='u', max_length=1),
        ),
    ]

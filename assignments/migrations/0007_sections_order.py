# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-04 13:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0006_voluntarysignuptask'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='section',
            options={'ordering': ['order_number', 'title'], 'verbose_name': 'Section', 'verbose_name_plural': 'Sections'},
        ),
        migrations.AddField(
            model_name='section',
            name='order_number',
            field=models.IntegerField(default=0, help_text='Order in which sections are shown', verbose_name='order number'),
        ),
    ]

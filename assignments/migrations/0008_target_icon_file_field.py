# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-26 06:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0007_sorted_budgeting_targets'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='assignment/image/', verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='budgetingtarget',
            name='icon',
            field=models.FileField(blank=True, null=True, upload_to='target/icons/', verbose_name='icon'),
        ),
    ]

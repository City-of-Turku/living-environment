# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-15 08:16
from __future__ import unicode_literals

import assignments.fields
from django.db import migrations
from sortedm2m.operations import AlterSortedManyToManyField


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0006_assignment_help_text'),
    ]

    operations = [
        AlterSortedManyToManyField(
            model_name='budgetingtask',
            name='targets',
            field=assignments.fields.SortedAsSelectedManyToManyField(help_text=None, related_name='budgeting_tasks',
                                                                     to='assignments.BudgetingTarget',
                                                                     verbose_name='budget targets'),
        ),
    ]

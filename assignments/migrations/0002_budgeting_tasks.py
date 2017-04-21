# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-19 09:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BudgetingTarget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='nimi')),
                ('unit_price', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='price')),
                ('reference_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='reference amount')),
                ('min_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='min amount')),
                ('max_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='max amount')),
                ('icon', models.FileField(blank=True, default='target/icons/default.png', upload_to='target/icons/')),
            ],
            options={
                'verbose_name': 'budget target',
                'verbose_name_plural': 'budget targets',
            },
        ),
        migrations.CreateModel(
            name='BudgetingTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='nimi')),
                ('unit', models.IntegerField(choices=[(0, 'ha'), (1, 'pcs')], default=0)),
                ('amount_of_consumption', models.DecimalField(decimal_places=2, default=0, help_text='Number of units required to be spent on the task', max_digits=10, verbose_name='amount of consumption')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='budgetingtasks', to='assignments.Section')),
                ('targets', models.ManyToManyField(related_name='budgeting_tasks', to='assignments.BudgetingTarget')),
            ],
            options={
                'verbose_name': 'budgeting task',
                'verbose_name_plural': 'budgeting tasks',
            },
        ),
        migrations.AlterField(
            model_name='opentexttask',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='opentexttasks', to='assignments.Section'),
        ),
    ]
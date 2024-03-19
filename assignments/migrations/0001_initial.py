# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-05 08:31
from __future__ import unicode_literals

import django_ckeditor_5.fields
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import djgeojson.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='name')),
                ('header', models.CharField(max_length=255, null=True, verbose_name='header')),
                ('description', django_ckeditor_5.fields.CKEditor5Field(blank=True, verbose_name='description')),
                ('area', djgeojson.fields.GeometryField(verbose_name='area')),
                ('status', models.IntegerField(choices=[(0, 'Open'), (1, 'Closed')], default=0, verbose_name='status')),
                ('budget', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='budget')),
                ('slug', models.SlugField(help_text='The user-friendly URL identifier ex. www.example.com/runosmaen-koulu', max_length=80, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Assignments',
                'verbose_name': 'Assignment',
            },
        ),
        migrations.CreateModel(
            name='BudgetingTarget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('unit_price', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='price')),
                ('reference_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='reference amount')),
                ('min_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='min amount')),
                ('max_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='max amount')),
                ('icon', models.FileField(blank=True, default='target/icons/default.png', upload_to='target/icons/', verbose_name='icon')),
            ],
            options={
                'verbose_name_plural': 'budget targets',
                'verbose_name': 'budget target',
            },
        ),
        migrations.CreateModel(
            name='BudgetingTargetAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('point', djgeojson.fields.PointField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='OpenTextAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schools', to='assignments.Assignment')),
            ],
            options={
                'verbose_name_plural': 'schools',
                'verbose_name': 'school',
            },
        ),
        migrations.CreateModel(
            name='SchoolClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'classes',
                'verbose_name': 'class',
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', django_ckeditor_5.fields.CKEditor5Field(blank=True, verbose_name='description')),
                ('video', models.URLField(blank=True, null=True)),
                ('order_number', models.IntegerField(default=0, help_text='Order in which sections are shown', verbose_name='order number')),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='assignments.Assignment', verbose_name='Assignment')),
            ],
            options={
                'verbose_name_plural': 'Sections',
                'verbose_name': 'Section',
                'ordering': ['order_number', 'title'],
            },
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='assignments.School')),
                ('school_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='assignments.SchoolClass')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.IntegerField(default=0, help_text='Order in which tasks are shown', verbose_name='order number')),
            ],
            options={
                'ordering': ['order_number'],
            },
            managers=[
                ('objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='BudgetingTask',
            fields=[
                ('task_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='assignments.Task')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('unit', models.IntegerField(choices=[(0, 'ha'), (1, 'pcs')], default=0, verbose_name='unit')),
                ('amount_of_consumption', models.DecimalField(decimal_places=2, default=0, help_text='Number of units required to be spent on the task', max_digits=10, verbose_name='amount of consumption')),
                ('targets', models.ManyToManyField(related_name='budgeting_tasks', to='assignments.BudgetingTarget', verbose_name='budget targets')),
            ],
            options={
                'verbose_name_plural': 'budgeting tasks',
                'verbose_name': 'budgeting task',
            },
            bases=('assignments.task',),
            managers=[
                ('objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='OpenTextTask',
            fields=[
                ('task_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='assignments.Task')),
                ('question', models.TextField(verbose_name='question')),
            ],
            options={
                'verbose_name_plural': 'open text tasks',
                'verbose_name': 'open text task',
            },
            bases=('assignments.task',),
            managers=[
                ('objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='VoluntarySignupTask',
            fields=[
                ('task_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='assignments.Task')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
            ],
            options={
                'verbose_name_plural': 'voluntary signup tasks',
                'verbose_name': 'voluntary signup task',
            },
            bases=('assignments.task',),
            managers=[
                ('objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_assignments.task_set+', to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='task',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='assignments.Section'),
        ),
        migrations.AddField(
            model_name='school',
            name='classes',
            field=models.ManyToManyField(related_name='schools', to='assignments.SchoolClass'),
        ),
        migrations.AddField(
            model_name='opentextanswer',
            name='submission',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='open_text_answers', to='assignments.Submission'),
        ),
        migrations.AddField(
            model_name='budgetingtargetanswer',
            name='submission',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='budgeting_answers', to='assignments.Submission'),
        ),
        migrations.AddField(
            model_name='budgetingtargetanswer',
            name='target',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='budgeting_answers', to='assignments.BudgetingTarget'),
        ),
        migrations.AddField(
            model_name='opentextanswer',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='open_text_answers', to='assignments.OpenTextTask'),
        ),
        migrations.AddField(
            model_name='budgetingtargetanswer',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='budgeting_answers', to='assignments.BudgetingTask'),
        ),
    ]

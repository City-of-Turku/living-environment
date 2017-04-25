# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-02 10:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0003_answers'),
    ]

    operations = [
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='assignments.School')),
                ('school_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='assignments.SchoolClass')),
            ],
        ),
        migrations.RemoveField(
            model_name='student',
            name='school',
        ),
        migrations.RemoveField(
            model_name='student',
            name='school_class',
        ),
        migrations.RemoveField(
            model_name='budgetingtargetanswer',
            name='student',
        ),
        migrations.RemoveField(
            model_name='opentextanswer',
            name='student',
        ),
        migrations.DeleteModel(
            name='Student',
        ),
        migrations.AddField(
            model_name='budgetingtargetanswer',
            name='submission',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='budgeting_answers', to='assignments.Submission'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='opentextanswer',
            name='submission',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='open_text_answers', to='assignments.Submission'),
            preserve_default=False,
        ),
    ]
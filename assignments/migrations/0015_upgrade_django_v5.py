# Generated by Django 5.0.2 on 2024-02-23 03:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0014_add_km_unit'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='budgetingtask',
            managers=[
            ],
        ),
        migrations.AlterModelManagers(
            name='opentexttask',
            managers=[
            ],
        ),
        migrations.AlterModelManagers(
            name='task',
            managers=[
            ],
        ),
        migrations.AlterModelManagers(
            name='voluntarysignuptask',
            managers=[
            ],
        ),
        migrations.AlterField(
            model_name='submission',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)ss', to='assignments.school'),
        ),
        migrations.AlterField(
            model_name='submission',
            name='school_class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)ss', to='assignments.schoolclass'),
        ),
        migrations.AlterField(
            model_name='task',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_%(app_label)s.%(class)s_set+', to='contenttypes.contenttype'),
        ),
    ]

# Generated by Django 5.1.1 on 2024-10-07 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmploiApp', '0017_rename_teacher_course_teacher'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profdispoweek',
            options={},
        ),
        migrations.AddField(
            model_name='profdispoweek',
            name='occupied_intervals',
            field=models.JSONField(blank=True, default=list),
        ),
    ]

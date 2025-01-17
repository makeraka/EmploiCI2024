# Generated by Django 5.1.1 on 2024-09-27 16:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmploiApp', '0015_classroom_capacity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='licence',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='groups', to='EmploiApp.licence'),
        ),
        migrations.RemoveField(
            model_name='seance',
            name='group',
        ),
        migrations.AddField(
            model_name='seance',
            name='group',
            field=models.ManyToManyField(to='EmploiApp.group'),
        ),
    ]

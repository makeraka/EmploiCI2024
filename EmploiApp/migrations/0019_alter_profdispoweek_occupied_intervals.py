# Generated by Django 5.1.1 on 2024-10-07 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmploiApp', '0018_alter_profdispoweek_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profdispoweek',
            name='occupied_intervals',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
    ]

# Generated by Django 5.1.1 on 2024-09-21 16:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('EmploiApp', '0003_alter_hourrange_end_time_alter_hourrange_start_time'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='licence',
            options={'verbose_name': 'Licence', 'verbose_name_plural': 'Licences'},
        ),
        migrations.AlterUniqueTogether(
            name='licence',
            unique_together={('number', 'department')},
        ),
    ]

# Generated by Django 5.1.1 on 2024-09-27 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmploiApp', '0012_seance_h_end_seance_h_start'),
    ]

    operations = [
        migrations.AddField(
            model_name='seance',
            name='day_week',
            field=models.IntegerField(choices=[(0, 'Lundi'), (1, 'Mardi'), (2, 'Mercredi'), (3, 'Jeudi'), (4, 'Vendredi'), (5, 'Samedi'), (6, 'Dimanche')], default=1),
            preserve_default=False,
        ),
    ]

# Generated by Django 5.1.1 on 2024-09-27 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmploiApp', '0014_remove_profdispoweek_hourrange_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='classroom',
            name='capacity',
            field=models.IntegerField(default=30),
            preserve_default=False,
        ),
    ]
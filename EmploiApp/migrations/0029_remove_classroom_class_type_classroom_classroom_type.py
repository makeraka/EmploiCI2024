# Generated by Django 5.1.2 on 2024-10-29 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmploiApp', '0028_course_course_type_course_duration_course_syllabus'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classroom',
            name='class_type',
        ),
        migrations.AddField(
            model_name='classroom',
            name='classroom_type',
            field=models.CharField(choices=[('A', 'Amphithéâtre'), ('TP', 'Salle de TP')], default='A', help_text='Type de la salle', max_length=2),
        ),
    ]

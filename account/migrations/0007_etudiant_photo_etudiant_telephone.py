# Generated by Django 5.1.1 on 2024-10-15 01:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_alter_teacher_options_teacher_adresse_teacher_cv_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='etudiant',
            name='photo',
            field=models.ImageField(default='image.jpg', upload_to='student_profils'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='etudiant',
            name='telephone',
            field=models.CharField(default='34456334', max_length=20),
            preserve_default=False,
        ),
    ]
# Generated by Django 5.0.1 on 2024-01-27 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testusers', '0002_student_teachers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='teachers',
            field=models.ManyToManyField(blank='true', related_name='teachers', to='testusers.teacher'),
        ),
    ]

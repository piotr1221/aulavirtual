# Generated by Django 3.2.5 on 2021-07-15 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0003_alter_course_day'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='time_end',
            field=models.TimeField(default='10:00:00'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='course',
            name='time_start',
            field=models.TimeField(default='12:00:00'),
            preserve_default=False,
        ),
    ]

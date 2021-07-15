# Generated by Django 3.2.5 on 2021-07-14 21:16

import ckeditor.fields
import classroom.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('module', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('icon', models.CharField(default='article', max_length=100, verbose_name='Icon')),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('picture', models.ImageField(upload_to=classroom.models.user_directory_path)),
                ('title', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=300)),
                ('syllabus', ckeditor.fields.RichTextField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classroom.category')),
                ('enrolled', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('modules', models.ManyToManyField(to='module.Module')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.PositiveIntegerField(default=0)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classroom.course')),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

# Generated by Django 5.1.1 on 2024-09-11 09:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='ScreenContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('genres', models.ManyToManyField(to='screen_content.genre', verbose_name='content')),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_%(app_label)s.%(class)s_set+', to='contenttypes.contenttype')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('screencontent_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='screen_content.screencontent')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('screen_content.screencontent',),
        ),
        migrations.CreateModel(
            name='TVShow',
            fields=[
                ('screencontent_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='screen_content.screencontent')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('screen_content.screencontent',),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('history', models.ManyToManyField(to='screen_content.screencontent')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

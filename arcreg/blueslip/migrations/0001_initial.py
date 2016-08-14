# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='General',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('semester', models.DecimalField(blank=True, decimal_places=0, max_digits=1, null=True)),
                ('id_no', models.CharField(blank=True, max_length=14, null=True)),
                ('name', models.CharField(blank=True, max_length=80, null=True)),
                ('phone_no', models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True)),
                ('add_course_no', models.CharField(blank=True, max_length=12, null=True)),
                ('add_lecture_no', models.DecimalField(decimal_places=0, max_digits=2)),
                ('add_tutorial_no', models.DecimalField(decimal_places=0, max_digits=2)),
                ('add_practical_no', models.DecimalField(decimal_places=0, max_digits=2)),
                ('rem_course_no', models.CharField(blank=True, max_length=12, null=True)),
                ('rem_lecture_no', models.DecimalField(decimal_places=0, max_digits=2)),
                ('rem_tutorial_no', models.DecimalField(decimal_places=0, max_digits=2)),
                ('rem_practical_no', models.DecimalField(decimal_places=0, max_digits=2)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Capacity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Course_id', models.IntegerField()),
                ('Subject', models.CharField(max_length=10)),
                ('catalog_course_no', models.CharField(max_length=7)),
                ('descr', models.CharField(max_length=70)),
                ('Section', models.CharField(max_length=5)),
                ('Cap_enrl', models.IntegerField()),
                ('Tot_enrl', models.IntegerField()),
                ('class_nbr', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Elective_list',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Campus_ID', models.CharField(blank=True, null=True, max_length=12)),
                ('Catalog', models.CharField(blank=True, null=True, max_length=6)),
                ('Course_Title', models.CharField(blank=True, null=True, max_length=100)),
                ('Class_Pattern', models.CharField(blank=True, null=True, max_length=6)),
                ('Mtg_Start', models.TimeField(blank=True, null=True)),
                ('End_time', models.TimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FD_priority_number',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('erp_id', models.IntegerField(blank=True, null=True)),
                ('campus_id', models.CharField(max_length=5)),
                ('name', models.CharField(max_length=5)),
                ('priority_number', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='HD_priority_number',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('erp_id', models.IntegerField(blank=True, null=True)),
                ('campus_id', models.CharField(max_length=5)),
                ('name', models.CharField(max_length=5)),
                ('priority_number', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Pre_requisite_senate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Cata_log', models.CharField(blank=True, null=True, max_length=7)),
                ('preq1', models.CharField(blank=True, null=True, max_length=7)),
                ('condition1', models.CharField(blank=True, null=True, max_length=5)),
                ('preq2', models.CharField(blank=True, null=True, max_length=7)),
                ('condition2', models.CharField(blank=True, null=True, max_length=5)),
                ('preq3', models.CharField(blank=True, null=True, max_length=7)),
                ('condition3', models.CharField(blank=True, null=True, max_length=5)),
                ('preq4', models.CharField(blank=True, null=True, max_length=7)),
            ],
        ),
        migrations.CreateModel(
            name='Registration_data',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Campus_ID', models.CharField(blank=True, null=True, max_length=12)),
                ('erp_ID', models.IntegerField(blank=True, null=True)),
                ('Name', models.CharField(blank=True, null=True, max_length=70)),
                ('Subject', models.CharField(blank=True, null=True, max_length=12)),
                ('Catalog', models.CharField(blank=True, null=True, max_length=12)),
                ('Course_ID', models.IntegerField(blank=True, null=True)),
                ('Lecture_Section_No', models.CharField(blank=True, null=True, max_length=5)),
                ('Practical_Section_No', models.CharField(blank=True, null=True, max_length=5)),
                ('Tutorial_Section_No', models.CharField(blank=True, null=True, max_length=5)),
                ('Project_Section_No', models.CharField(blank=True, null=True, max_length=5)),
                ('Thesis_section', models.CharField(blank=True, null=True, max_length=5)),
                ('Graded_Component', models.CharField(blank=True, null=True, max_length=5)),
                ('Grade_In', models.CharField(blank=True, null=True, max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Time_Table_Semester_Wise',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Course_id', models.IntegerField(blank=True, null=True)),
                ('Subject', models.CharField(blank=True, null=True, max_length=7)),
                ('catalog_course_no', models.CharField(blank=True, null=True, max_length=7)),
                ('course_title', models.CharField(blank=True, null=True, max_length=50)),
                ('class_nbr', models.IntegerField(blank=True, null=True)),
                ('Section', models.CharField(blank=True, null=True, max_length=5)),
                ('room', models.CharField(blank=True, null=True, max_length=6)),
                ('class_pattern', models.CharField(blank=True, null=True, max_length=6)),
                ('mtg_start_time', models.TimeField(blank=True, null=True)),
                ('end_time', models.TimeField(blank=True, null=True)),
                ('display_name', models.CharField(blank=True, null=True, max_length=70)),
            ],
        ),
        migrations.CreateModel(
            name='Upload_file',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Capacity', models.FileField(upload_to='xls_sheets/Capacity/temporary')),
                ('Elective_list', models.FileField(upload_to='xls_sheets/Elective_list/temporary')),
                ('FD_Priority_number', models.FileField(upload_to='xls_sheets/FD_Priority_number/temporary')),
                ('HD_Priority_number', models.FileField(upload_to='xls_sheets/HD_Priority_number/temporary')),
                ('Pre_requisite_senate', models.FileField(upload_to='xls_sheets/Pre_requisite_senate/temporary')),
                ('Time_Table_Semester_Wise', models.FileField(upload_to='xls_sheets/Time_Table_Semester_Wise/temporary')),
                ('Registration_data', models.FileField(upload_to='xls_sheets/Registration_data/temporary')),
            ],
        ),
    ]

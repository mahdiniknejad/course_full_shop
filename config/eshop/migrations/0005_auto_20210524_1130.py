# Generated by Django 3.2.3 on 2021-05-24 07:00

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('eshop', '0004_alter_course_publish'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='publish',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 24, 7, 0, 24, 468820, tzinfo=utc), verbose_name='زمان انتشار دوره'),
        ),
        migrations.AlterField(
            model_name='course',
            name='slug',
            field=models.SlugField(allow_unicode=True, unique=True, verbose_name='دامنه'),
        ),
    ]

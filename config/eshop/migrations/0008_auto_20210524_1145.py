# Generated by Django 3.2.3 on 2021-05-24 07:15

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('eshop', '0007_auto_20210524_1135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='publish',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 24, 7, 15, 14, 214930, tzinfo=utc), verbose_name='زمان انتشار دوره'),
        ),
        migrations.AlterField(
            model_name='course',
            name='teacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='course', to=settings.AUTH_USER_MODEL, verbose_name='مدرس'),
        ),
    ]
# Generated by Django 2.2.5 on 2019-09-19 00:48

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bysjapp', '0002_auto_20190919_0829'),
    ]

    operations = [
        migrations.AddField(
            model_name='developments',
            name='create_date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='创建日期'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='developments',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='创建时间'),
            preserve_default=False,
        ),
    ]

# Generated by Django 2.2.5 on 2019-10-20 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bysjapp', '0013_orders'),
    ]

    operations = [
        migrations.AddField(
            model_name='likes',
            name='likes',
            field=models.IntegerField(default=0, verbose_name='点赞数'),
        ),
    ]

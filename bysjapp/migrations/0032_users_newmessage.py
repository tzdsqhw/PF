# Generated by Django 2.2.5 on 2020-04-12 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bysjapp', '0031_users_mnum'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='newmessage',
            field=models.TextField(default='{"like":[],"comment":[],"follow":[]}', verbose_name='新信息'),
        ),
    ]

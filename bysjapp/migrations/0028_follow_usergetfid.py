# Generated by Django 2.2.5 on 2020-03-25 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bysjapp', '0027_follow'),
    ]

    operations = [
        migrations.AddField(
            model_name='follow',
            name='usergetfid',
            field=models.CharField(default=1, max_length=20, verbose_name='被关注用户id'),
            preserve_default=False,
        ),
    ]

# Generated by Django 2.2.5 on 2019-10-13 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bysjapp', '0011_developments_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='goods',
            name='goodprice',
            field=models.FloatField(default=0, verbose_name='商品单价'),
        ),
    ]
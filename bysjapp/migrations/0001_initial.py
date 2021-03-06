# Generated by Django 2.2.5 on 2019-09-18 09:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('goodsid', models.AutoField(primary_key=True, serialize=False)),
                ('goodname', models.CharField(max_length=20, verbose_name='商品名')),
                ('goodnum', models.IntegerField(default=0, verbose_name='商品存货数')),
                ('goodtext', models.TextField(verbose_name='商品详情')),
                ('goodtype', models.CharField(max_length=20, verbose_name='商品类型')),
            ],
            options={
                'verbose_name': '商品',
                'verbose_name_plural': '商品',
            },
        ),
        migrations.CreateModel(
            name='Pets',
            fields=[
                ('petid', models.AutoField(primary_key=True, serialize=False)),
                ('petname', models.CharField(max_length=20, verbose_name='宠物名')),
                ('petsex', models.CharField(max_length=20, verbose_name='宠物性别')),
                ('petbirth', models.DateField(verbose_name='宠物生日')),
            ],
            options={
                'verbose_name': '宠物',
                'verbose_name_plural': '宠物',
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('userid', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=20, verbose_name='用户名')),
                ('password', models.CharField(max_length=20, verbose_name='密码')),
                ('birth', models.DateField(verbose_name='生日')),
                ('sex', models.CharField(max_length=6, verbose_name='性别')),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
            },
        ),
        migrations.CreateModel(
            name='WhosCar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('carname', models.CharField(max_length=20, verbose_name='购物车表名')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bysjapp.Users', verbose_name='用户')),
            ],
            options={
                'verbose_name': '谁的车',
                'verbose_name_plural': '谁的车',
            },
        ),
        migrations.CreateModel(
            name='Developments',
            fields=[
                ('dmentid', models.AutoField(primary_key=True, serialize=False)),
                ('dmenttext', models.TextField(verbose_name='动态详情')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bysjapp.Users', verbose_name='用户')),
            ],
            options={
                'verbose_name': '动态',
                'verbose_name_plural': '动态',
            },
        ),
    ]

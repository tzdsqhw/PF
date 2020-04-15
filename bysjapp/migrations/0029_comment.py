# Generated by Django 2.2.5 on 2020-04-11 05:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bysjapp', '0028_follow_usergetfid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('cid', models.AutoField(primary_key=True, serialize=False)),
                ('likenum', models.IntegerField(default=0, verbose_name='点赞数')),
                ('ctext', models.TextField(verbose_name='评论详情')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('dment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bysjapp.Developments', verbose_name='动态')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bysjapp.Users', verbose_name='用户')),
            ],
            options={
                'verbose_name': '评论',
                'verbose_name_plural': '评论',
            },
        ),
    ]

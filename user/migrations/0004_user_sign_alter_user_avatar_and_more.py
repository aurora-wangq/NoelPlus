# Generated by Django 4.2.1 on 2023-07-31 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_user_title_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='sign',
            field=models.CharField(blank=True, default='', max_length=25, null=True, verbose_name='签名'),
        ),
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='/media/user/avatar/txdefault.jpg', upload_to='media/user/avatar', verbose_name='头像'),
        ),
        migrations.AlterField(
            model_name='user',
            name='background_image',
            field=models.ImageField(default='/media/user/userpage_background/backimg.jpg', upload_to='media/user/userpage_background', verbose_name='背景图片'),
        ),
        migrations.AlterField(
            model_name='user',
            name='description',
            field=models.TextField(blank=True, max_length=100, null=True, verbose_name='个人介绍'),
        ),
        migrations.AlterField(
            model_name='user',
            name='nickname',
            field=models.CharField(max_length=10, verbose_name='昵称'),
        ),
        migrations.AlterField(
            model_name='user',
            name='title',
            field=models.CharField(default='普通网友', max_length=50, verbose_name='头衔'),
        ),
    ]

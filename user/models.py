#user-models
from typing import Any
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.deconstruct import deconstructible
import os

@deconstructible
class Rename(object):
    def __init__(self, path):
        self.path = path
    def __call__(self, inst, name):
        ext = name.split('.')[-1]
        filename = f'{inst.username}.{ext}'
        return os.path.join(self.path, filename)

class User(AbstractUser):
    nickname = models.CharField('昵称', max_length=10)
    description = models.TextField('个人介绍', max_length=100, blank=True, null=True)
    sign = models.CharField('签名', max_length=25, blank=True, default='', null=True)
    background_image = models.ImageField('背景图片', upload_to=Rename('media/user/userpage_background'), default='/media/user/userpage_background/backimg.jpg')
    avatar = models.ImageField('头像', upload_to=Rename('media/user/avatar'), default='/media/user/avatar/txdefault.jpg')
    title = models.CharField('头衔', max_length=50, default='普通网友')
    title_level = models.IntegerField('头衔类别,1站主,2管理员,3特殊,4普通', default=4)
class Follow(models.Model):
    up = models.ForeignKey(User, on_delete=models.CASCADE, related_name="博主")
    fan = models.ForeignKey(User, on_delete=models.CASCADE, related_name="粉丝")

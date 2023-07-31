#blog-models
from django.db import models
from NoelPlus.settings import AUTH_USER_MODEL
from mdeditor.fields import MDTextField

class Blog(models.Model):
    title = models.CharField('博客标题', max_length=100, default="原神，启动！")
    content = MDTextField(verbose_name='博文内容')
    aurthor = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='作者')
class Like(models.Model):
    post = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name='所属博客')
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='点赞者')
class Comment(models.Model):
    post = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name='所属博客')
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='评论者')
    content = models.CharField('评论内容', max_length=1000)


#zone-models
from django.db import models
from django.conf import settings

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='作者')
    content = models.TextField('内容')
    images = models.ImageField('配图', upload_to='media/post/post_images')
    pinned = models.BooleanField('是否顶置', default=False)
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='所属文章')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='点赞者', related_name='帖子点赞者')
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='所属文章')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='评论者', related_name='帖子评论者')
    content = models.TextField('评论内容', max_length=1000)
    pub_time = models.DateTimeField('发布时间')
    reply = models.IntegerField('Reply index', default=-1)
class Notice(models.Model):
    creater = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='公告发布者')
    notice = models.TextField('公告内容', max_length=300)
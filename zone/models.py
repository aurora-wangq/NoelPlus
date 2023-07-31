#zone-models
from django.db import models
from NoelPlus.settings import AUTH_USER_MODEL

class Post(models.Model):
    author = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='作者')
    content = models.CharField('内容', max_length=10000)
    images = models.ImageField('配图', upload_to='media/post/post_images')
    pinned = models.BooleanField('是否顶置', default=False)
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='所属文章')
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='点赞者')
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='所属文章')
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='评论者')
    content = models.CharField('评论内容', max_length=1000)
class Notice(models.Model):
    creater = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='公告发布者')
    notice = models.TextField('公告内容', max_length=300)
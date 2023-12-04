# zone-view
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import render, HttpResponse, redirect
from .models import *
import json
import random
from PIL import Image
from user.models import User
from datetime import datetime

thesaurus = []
with open('collection.json', encoding='utf8') as f:
    thesaurus = json.loads(f.read())

class HttpResponseImATeaPot(HttpResponse):
    status_code = 418

#主页
@login_required(login_url='user:login')
def home(request):
    user_ = User.objects.get(username=request.user.username)
    post_list = Post.objects.order_by("-pinned", "-id")
    notice = Notice.objects.all()
    for i in post_list:
        i.likes = Like.objects.filter(post=i).count()
    context = {
        "user": user_,
        "post_list": post_list,
        "thesaurus": random.choice(thesaurus),
        "notice": notice,
    }
    return render(request, 'zone/home.html', context)

#编辑帖子
@login_required(login_url='user:login')
def edit_post(request):
    if request.method == 'POST':
        user_ = User.objects.get(username=request.user.username)
        new_post = Post.objects.create(author=user_, content=request.POST['content'])
        new_post.images = request.FILES.get('post_img')
        new_post.save()
        path = str(new_post.images)
        im = Image.open(path)
        (x, y) = im.size
        x1 = 512
        y1 = int(y * x1 / x)
        path1 = './thumbnail/' + str(new_post.images)
        out = im.resize((x1, y1), Image.Resampling.BICUBIC)
        out.save(path1)
        return redirect('zone:home')

#帖子详情
@login_required(login_url='user:login')
def post(request, post_id):
    user = User.objects.get(username=request.user.username)
    post = Post.objects.get(id=post_id)
    comment_list = Comment.objects.filter(post=post)
    like_list = Like.objects.filter(post=post)
    liked = 0
    for i in like_list:
        if i.user == user:
            liked = 1
            break
    context = {
        "user": user,
        "liked": liked,
        "post": post,
        "comment_list": comment_list,
    }
    return render(request, 'zone/article_detail.html', context)

#帖子评论    
@login_required(login_url='user:login')
def comment(request, post_id):
    if request.method == 'GET':
        return HttpResponseImATeaPot()
    elif request.method == 'POST':
        Comment.objects.create(**{
            'author': request.user,
            'pub_time': datetime.now(),
            'post': Post.objects.get(id=post_id),
            'content': request.POST['content'],
            'reply': request.POST['reply']
        }).save()
        return redirect('zone:post', post_id)

#帖子点赞
@login_required(login_url='user:login')
def post_like(request, post_id):
    user = User.objects.get(username=request.user.username)
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        if Like.objects.filter(post=post, user=user).count() == 0:
            Like.objects.create(user=user, post=post)
            return HttpResponse("点赞成功")
        else:
            Like.objects.filter(user=user, post=post).delete()
            return HttpResponse("取消点赞")
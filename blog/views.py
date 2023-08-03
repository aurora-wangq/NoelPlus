#blog-views
from django import template
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .models import *

class HttpResponseImATeaPot(HttpResponse):
    status_code = 418

#博客选择页面
@login_required(login_url='user:login')
def index(request):
    blogs = Blog.objects.all().order_by('-pinned','-pub_time')
    if len(blogs) > 30:
        blogs = blogs[:30]
    context = {
        "user": request.user,
        "blogs": blogs
    }
    return render(request, 'blog/index.html', context)

#博客详情页
@login_required(login_url='user:login')
def blog(request, blog_id):
    blog = Blog.objects.get(id=blog_id) 
    comments = Comment.objects.filter(blog=blog)
    context = {
        'user': request.user,
        'blog': blog,
        'comments': comments,
    }
    return render(request, 'blog/post.html', context)

#博客评论
@login_required(login_url='user:login')
def comment(request, blog_id):
    print("执行了！！！")
    if request.method == 'GET':
        return HttpResponseImATeaPot()
    elif request.method == 'POST':
        Comment.objects.create(**{
            'author': request.user,
            'pub_time': datetime.now(),
            'blog': Blog.objects.get(id=blog_id),
            'content': request.POST['content'],
            'reply': request.POST['reply']
        }).save()
        return redirect('blog:blog', blog_id)

#写博客
@login_required(login_url='user:login')
def new(request):
    if request.method == 'GET':
        context = {
            "user": request.user,
        }
        return render(request, 'blog/new.html', context)
    elif request.method == 'POST':
        Blog.objects.create(**{
            'author': request.user,
            'pub_time': datetime.now(),
            'title': request.POST['title'],
            'content': request.POST['content']
        }).save()
        return redirect('blog:index')

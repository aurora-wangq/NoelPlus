from django import template
from django.shortcuts import render, redirect
from django.http import *
from django.contrib.auth.decorators import login_required
from datetime import datetime
import markdown

from .models import *


class HttpResponseImATeaPot(HttpResponse):
    status_code = 418


def mdconv(text: str):
    md = markdown.Markdown(
        extensions=[
            'markdown.extensions.codehilite',
            'markdown.extensions.meta',
            'markdown.extensions.extra',
            'pymdownx.arithmatex'
        ],
        extension_configs={
            'pymdownx.arithmatex': {
                'generic': True
            }
        }
    )
    res = md.convert(text)
    meta = md.Meta
    for i in meta:
        if len(meta[i]) == 1:
            meta[i] = meta[i][0]
    return (res, md.Meta)


#博客选择页面
@login_required(login_url='user:login')
def index(request):
    blogs = Blog.objects.all().order_by('-pinned','-pub_time')
    if len(blogs) > 30:
        blogs = blogs[:30]
    
    for blog in blogs:
        blog.comment_count = Comment.objects.filter(blog=blog).count()
        blog.formatted, blog.meta = mdconv(blog.content)
    
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
    blog.formatted, blog.meta = mdconv(blog.content)
    context = {
        'editable': request.user == blog.author,
        'user': request.user,
        'blog': blog,
        'comments': comments,
    }
    return render(request, 'blog/post.html', context)


@login_required(login_url='user:login')
def edit(request: HttpRequest, post_id: int):
    blog = Blog.objects.get(id=post_id)

    if blog.author != request.user:
        return HttpResponseForbidden('You do not own this post')

    if request.method == 'GET':
        context = {
            'user': request.user,
            'blog': blog
        }
        return render(request, 'blog/edit.html', context)
    elif request.method == 'POST':
        blog.content = request.POST['content']
        blog.save()
        return redirect('blog:blog', post_id)


@login_required(login_url='user:login')
def comment(request, blog_id):
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
            'content': request.POST['content']
        }).save()
        return redirect('blog:index')

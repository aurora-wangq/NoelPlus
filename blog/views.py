#novel-view
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import render, HttpResponse, redirect
from user.models import *
from .models import *

#选择小说
@login_required(login_url='user:login')
def select_novel(request):
    user = User.objects.get(username=request.user.username)     
    novel = Novel.objects.order_by("id")
    for i in novel:
        i.likes = Like.objects.filter(novel=i).count()
    context = {
        "user": user,
        "novel_list": novel,
    }
    return render(request, 'novel_fissure_traveler_select.html', context)

#小说详情
@login_required(login_url='user:login')
def novel(request, novel_id):
    user = User.objects.get(username=request.user.username)
    novel = Novel.objects.get(id = novel_id)
    content = novel.content
    comment_list = Comment.objects.filter(novel=novel)
    like_list = Like.objects.filter(novel=novel)
    liked = 0
    for i in like_list:
        if i.user == user:
            liked = 1
            break
    context = {
        "user": user,
        "liked": liked,
        "comment_list": comment_list,
    }
    if request.method == 'POST':
        content = request.POST['comment_text']
        if content:
            new_comment = Comment.objects.create(user=user, novel=novel, content=content)
            new_comment.save()
        return redirect('novel:traveler_content', novel_id = novel_id)
    else:
        return render(request, 'novel_fissure_traveler.html', context)

#小说点赞
@login_required(login_url='user:login')
def novel_like(request, novel_id):
    user = User.objects.get(username=request.user.username)
    novel = Novel.objects.get(id=novel_id)
    if request.method == 'POST':
        if Like.objects.filter(novel=novel, user=user).count() == 0:
            Like.objects.create(user=user, novel=novel)
            return HttpResponse("点赞成功")
        else:
            Like.objects.filter(user=user, novel=novel).delete()
            return HttpResponse("取消点赞")
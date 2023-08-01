#user-view
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import render, HttpResponse, redirect
from .models import *

#注册
def register(request):
    default_avatar = {"avatar": "media/user/avatar/txdefault.jpg",}
    context = {
        "user": default_avatar,
    }
    if request.method == 'GET':
        return render(request, 'user/register.html', context)
    elif request.method == 'POST':
        user = User.objects.create_user(
            username=request.POST['username'], 
            password=request.POST['password'], 
            nickname=request.POST['nickname'],
        )
        user.save()
        return redirect('user:login')

#登陆
def login_(request):
    default_avatar = {"avatar": "media/user/avatar/txdefault.jpg",}
    context = {
        "user": default_avatar,
    }
    if request.method == 'GET':
        return render(request, 'user/login.html', context)
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            
            return redirect('zone:home')
        else:
            return redirect('user:login')

#登出
@login_required(login_url='user:login')
def logout_(request):
    logout(request)
    return redirect('user:login')

#编辑个人信息
@login_required(login_url='user:login')
def edit_profile(request):
    user = User.objects.get(username=request.user.username)
    fans = Follow.objects.filter(up=user)
    context = {
        "user": user,
        "fans_count": fans.count(),
    }
    if request.method == 'POST':
        if request.POST['nickname']:
            user.nickname = request.POST['nickname']
        if request.POST['desc']:
            user.description = request.POST['desc']
        if request.POST['sign']:
            user.sign = request.POST['sign']
        if request.FILES.get('img'):
            user.avatar = request.FILES.get('img')
        if request.FILES.get('backimg'):
            user.background_image = request.FILES.get('backimg')
        user.save()
        return redirect('user:user_page')
    else:
        return render(request, 'user/edit_user.html', context)

#个人主页
@login_required(login_url='user:login')
def user_page(request):
    user = User.objects.get(username=request.user.username)
    fans = Follow.objects.filter(up=user)
    context = {
        "user": user,
        "fans_count": fans.count(),
    }
    return render(request, 'user/user_page.html', context)

#他人主页
@login_required(login_url='user:login')
def others_page(request, target_id):
    user = User.objects.get(username=request.user.username)
    target = User.objects.get(id=target_id)
    fans_list = Follow.objects.filter(up=target_id)
    following = any(x.fan == user  for x in fans_list)
    context = {
        "target": target,
        "user": user,
        "following": following,
        "is_me": target_id == user.id,
        "fans_count": fans_list.count(),
    }
    return render(request, 'user/others_page.html', context)

#关注功能
@login_required(login_url='user:login')
def follow(request, target_id):
    user = User.objects.get(username=request.user.username)
    up = User.objects.get(id=target_id)
    print("我在心里！！！！！！")
    if request.method == 'POST':
        if Follow.objects.filter(up=up, fan=user).count() == 0:
            Follow.objects.create(up=up, fan=user)
            return HttpResponse("关注成功")
        else:
            Follow.objects.filter(up=up, fan=user).delete()
            return HttpResponse("取消关注")
        
#chat-view
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from user.models import *

@login_required(login_url='user:login')
def chat(request):
    user = User.objects.get(username=request.user.username)
    context = {
        "user": user
    }
    return render(request, 'chat/chat.html', context)
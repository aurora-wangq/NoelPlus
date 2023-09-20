#gpt-view
from django.shortcuts import render
import openai
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
import json
from user.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

messages = []

@login_required(login_url='user:login')
def gpt(request):
    user = User.objects.get(username=request.user.username)
    context = {
        "user": user,
    }
    if request.method == 'GET':
        return render(request, 'gpt/gpt.html', context)
    elif request.method == 'POST':
        openai.api_key=""
        openai.api_base = "https://api.ai-yyds.com/v1"
        json_data = json.loads(request.body.decode("utf-8"))
        user_input = json_data.get("user_input")
        user_message_dict = {"role": "user","content": user_input}
        messages.append(user_message_dict)
        response=openai.ChatCompletion.create(model="gpt-3.5-turbo",messages=messages)
        reply = response["choices"][0]["message"]["content"]
        ai_message_dict = {"role": "assistant", "content": reply}
        messages.append(ai_message_dict)
        if len(messages) > 8:
            del(messages[0])
            del(messages[0])
        AGroup_Chat = {
            "user_input": user_input,
            "ai_reply": reply,
        }
        return JsonResponse(AGroup_Chat)
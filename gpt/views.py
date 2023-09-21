#gpt-view
from django.shortcuts import render
import openai
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
import json
from user.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import markdown

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
    return res

log_message = []
#log_message = [{"uid": 1, "message": message[{"role": "user","content": user_input},]},]
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
        have_user_log_message = 0
        response = []
        for i in log_message:
            if i["uid"] == user.id:
                have_user_log_message = 1
                i["message"].append(user_message_dict)
                response = openai.ChatCompletion.create(model="gpt-4",messages=i["message"])
                break
        if have_user_log_message == 0:
            message = []
            message.append(user_message_dict)
            log_message.append({"uid": user.id, "message": message})
            response = openai.ChatCompletion.create(model="gpt-3.5-turbo",messages=message)

        reply = response["choices"][0]["message"]["content"]
        ai_message_dict = {"role": "assistant", "content": reply}

        for i in log_message:
            if i["uid"] == user.id:
                i["message"].append(ai_message_dict)
                break

        for i in log_message:
            if len(i["message"]) > 4:
                del(i["message"][0])
                del(i["message"][0])

        AGroup_Chat = {
            "user_input": user_input,
            "ai_reply": mdconv(reply),
        }
        return JsonResponse(AGroup_Chat)
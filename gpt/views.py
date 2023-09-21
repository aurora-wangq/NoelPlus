from django.shortcuts import render
import openai
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.http import JsonResponse, HttpResponseForbidden, HttpRequest
import json
from user.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import markdown
import collections

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

history = {}

@login_required(login_url='user:login')
def gpt(request: HttpRequest):
    user = request.user
    context = {
        "user": user,
    }
    if request.method == 'GET':
        return render(request, 'gpt/gpt.html', context)
    elif request.method == 'POST':
        openai.api_key = ""
        openai.api_base = "https://api.ai-yyds.com/v1"

        input = request.POST
        if input['model'] == 'gpt-4' and 'gpt4_permitted' not in [ x.name for x in user.groups.all() ]:
            return HttpResponseForbidden('access denied')
        
        msg = {
            "role": "user",
            "content": input['prompt']
        }
        if history.get(user.id):
            history[user.id].append(msg)
        else:
            history[user.id] = collections.deque([msg], maxlen=8)

        response = openai.ChatCompletion.create(model=input['model'],messages=list(history[user.id]))
        reply = response["choices"][0]["message"]["content"]

        history[user.id].append({
            'role': 'assistant',
            'content': reply
        })

        return JsonResponse({
            'model': input['model'],
            'content': mdconv(reply)
        })

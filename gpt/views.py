from django.shortcuts import render
import openai
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.http import JsonResponse, HttpResponseForbidden, HttpRequest, HttpResponseServerError
import json
from user.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import markdown
import time
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
        'messages': [{
            'role': x['role'],
            'content': mdconv(x['content'])
        } for x in history.get(user.id, [])]
    }
    if request.method == 'GET':
        return render(request, 'gpt/gpt.html', context)
    elif request.method == 'POST':
        input = request.POST
        openai.api_key = "sk-U0WLocu4KWrrrh678f6d82F522D34042A6Ce78D6C26eA921"
        openai.api_base = "https://api.ai-yyds.com/v1"

        if input['model'] == 'gpt-4' and 'gpt4_permitted' not in [ x.name for x in user.groups.all() ]:
            return HttpResponseForbidden('您无权访问GPT4')
        
        msg = {
            "role": "user",
            "content": input['prompt']
        }
        if history.get(user.id):
            history[user.id].append(msg)
        else:
            history[user.id] = collections.deque([msg], maxlen=8)

        try:
            response = openai.ChatCompletion.create(model=input['model'],messages=list(history[user.id]))
        except Exception as e:
            return HttpResponseServerError(str(e))
        
        reply = response["choices"][0]["message"]["content"]

        history[user.id].append({
            'role': 'assistant',
            'content': reply
        })

        return JsonResponse({
            'model': input['model'],
            'content': mdconv(reply)
        })

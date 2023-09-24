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

def index(request):
    return render(request, 'index/index.html')

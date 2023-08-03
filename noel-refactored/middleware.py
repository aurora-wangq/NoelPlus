from django.http import HttpRequest
from django.shortcuts import render
import random

probability = 0.2

# Hard-coded blacklist middleware
class BlacklistMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.blacklist = [
            #Emample:
            {
                "uid": 1,
                "banned_from": [
                    '/chat'
                ]
            }
        ]

    def __call__(self, request: HttpRequest):
        id = request.user.id
        a = list(filter(lambda x: x['uid'] == id, self.blacklist))
        if not a:
            return self.get_response(request)
        else:
            if any(request.path.startswith(x) for x in a[0]['banned_from']):
                return render(request, "error.html", {
                    'hit': random.random() < probability
                })
            else:
                return self.get_response(request)
